/*
 * Leadlock Talking-Website voice engine — drop-in, framework-agnostic.
 *
 * Usage (no build step, works on WordPress / GHL / plain HTML / any site):
 *   <script src="/voice-agent.js"
 *           data-leadlock-ws="wss://leadlock-app.onrender.com"
 *           data-leadlock-slug="YOUR_DEMO_SLUG"></script>
 *
 * It renders a small restyleable "Talk to us" button (bottom-right), captures the
 * mic, plays the agent's audio, and executes the page-control tools the agent calls
 * (navigate, scroll, scroll-to-section, spotlight, fill, click, remember). The call
 * routes through Leadlock, so minutes bill to the account that owns the slug.
 *
 * Options (data-* on the script tag):
 *   data-leadlock-ws       (required) wss origin of the Leadlock backend
 *   data-leadlock-slug     (required) the web demo slug
 *   data-leadlock-label    button text (default "Talk to us")
 *   data-leadlock-headless "true" → render NO UI; drive it yourself via window.LeadlockVoice
 *
 * Custom UI / SPA:
 *   window.LeadlockVoice.start() / .stop() / .isActive()
 *   window.LeadlockVoice.registerTool(name, fn)  // override or add a page-control handler
 *   window.LeadlockVoice.on(event, fn)           // 'connected' | 'ended' | 'error' | 'tool'
 *   window.__llNavigate = (path) => router.push(path)  // SPA hook: keeps the call alive
 *       across page changes. If absent, web_navigate does a full-page load (which ends the
 *       call on a classic multi-page site — that's the documented multi-page limitation).
 *
 * Style the button by overriding #ll-voice-btn in your own CSS.
 */
(function () {
  var script = document.currentScript;
  var WS_BASE = (script && script.dataset.leadlockWs) || "";
  var SLUG = (script && script.dataset.leadlockSlug) || "";
  var LABEL = (script && script.dataset.leadlockLabel) || "Talk to us";
  var HEADLESS = script && script.dataset.leadlockHeadless === "true";
  if (!WS_BASE || !SLUG) {
    console.error(
      "[LeadlockVoice] missing data-leadlock-ws or data-leadlock-slug on the script tag",
    );
    return;
  }

  // ── state ──────────────────────────────────────────────────────────
  var ws = null,
    audioCtx = null,
    stream = null,
    processor = null;
  var queue = [],
    playing = false,
    curSource = null,
    sampleRate = 24000;
  var state = "idle";
  var listeners = {};
  var customTools = {};

  function emit(ev, data) {
    (listeners[ev] || []).forEach(function (fn) {
      try {
        fn(data);
      } catch (e) {}
    });
  }
  function setState(s, label) {
    state = s;
    var root = document.getElementById("ll-voice-root");
    if (root) root.dataset.state = s;
    var lbl = document.getElementById("ll-voice-label");
    if (lbl && label) lbl.textContent = label;
  }

  // ── audio playback (24kHz PCM16) ────────────────────────────────────
  function playNext() {
    if (!audioCtx || queue.length === 0) {
      playing = false;
      return;
    }
    playing = true;
    var data = queue.shift();
    var buf = audioCtx.createBuffer(1, data.length, sampleRate);
    buf.getChannelData(0).set(data);
    var src = audioCtx.createBufferSource();
    src.buffer = buf;
    src.connect(audioCtx.destination);
    curSource = src;
    src.onended = function () {
      curSource = null;
      playNext();
    };
    src.start();
  }

  // ── page-control helpers ────────────────────────────────────────────
  function findByText(q) {
    q = (q || "").trim().toLowerCase();
    if (!q) return null;
    var els = document.querySelectorAll(
      "h1,h2,h3,h4,h5,h6,a,button,section,article,li,p,span,div,[id]",
    );
    var best = null,
      bestLen = Infinity;
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.closest("#ll-voice-root")) continue;
      var t = (el.textContent || "").trim().toLowerCase();
      if (t && t.indexOf(q) !== -1 && t.length < bestLen) {
        best = el;
        bestLen = t.length;
      }
    }
    if (!best) best = document.getElementById(q.replace(/\s+/g, "-"));
    return best;
  }
  function findField(q) {
    q = (q || "").trim().toLowerCase();
    if (!q) return null;
    var fields = document.querySelectorAll("input, textarea, select");
    for (var i = 0; i < fields.length; i++) {
      var f = fields[i];
      var hay = [
        f.getAttribute("placeholder"),
        f.getAttribute("name"),
        f.id,
        f.getAttribute("aria-label"),
      ];
      if (f.id) {
        var lbl = document.querySelector('label[for="' + f.id + '"]');
        if (lbl) hay.push(lbl.textContent);
      }
      for (var j = 0; j < hay.length; j++) {
        if (hay[j] && hay[j].toLowerCase().indexOf(q) !== -1) return f;
      }
    }
    return null;
  }
  function doScroll(dir) {
    var step = window.innerHeight * 0.85;
    if (dir === "top") window.scrollTo({ top: 0, behavior: "smooth" });
    else if (dir === "bottom")
      window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    else if (dir === "up") window.scrollBy({ top: -step, behavior: "smooth" });
    else window.scrollBy({ top: step, behavior: "smooth" });
  }
  // cinematic spotlight (box-shadow cutout, no library)
  var spot = null,
    spotTarget = null,
    reposition = null;
  function clearHighlight() {
    if (spot) {
      spot.remove();
      spot = null;
    }
    if (reposition) {
      window.removeEventListener("scroll", reposition, true);
      window.removeEventListener("resize", reposition);
      reposition = null;
    }
    spotTarget = null;
  }
  function highlight(el) {
    clearHighlight();
    spotTarget = el;
    var cut = document.createElement("div");
    cut.style.cssText =
      "position:fixed;z-index:2147482000;pointer-events:none;border-radius:10px;box-shadow:0 0 0 9999px rgba(2,6,23,0.72);outline:3px solid #0b5cff;outline-offset:2px;transition:all .25s ease;";
    document.body.appendChild(cut);
    spot = cut;
    var place = function () {
      if (!spotTarget) return;
      var r = spotTarget.getBoundingClientRect(),
        p = 8;
      cut.style.left = r.left - p + "px";
      cut.style.top = r.top - p + "px";
      cut.style.width = r.width + p * 2 + "px";
      cut.style.height = r.height + p * 2 + "px";
    };
    el.scrollIntoView({ behavior: "smooth", block: "center" });
    place();
    setTimeout(place, 350);
    reposition = place;
    window.addEventListener("scroll", place, true);
    window.addEventListener("resize", place);
  }
  function loadVisitor() {
    try {
      return JSON.parse(localStorage.getItem("ll_visitor") || "{}");
    } catch (e) {
      return {};
    }
  }
  function saveVisitor(patch) {
    try {
      var cur = loadVisitor();
      for (var k in patch) cur[k] = patch[k];
      cur.lastVisit = new Date().toISOString();
      localStorage.setItem("ll_visitor", JSON.stringify(cur));
    } catch (e) {}
  }

  function handleTool(fn, args) {
    args = args || {};
    emit("tool", { fn: fn, args: args });
    if (customTools[fn]) {
      try {
        customTools[fn](args);
      } catch (e) {
        console.error(e);
      }
      return;
    }
    switch (fn) {
      case "web_navigate":
        if (typeof args.path !== "string") return;
        clearHighlight();
        var path = args.path.trim();
        if (path[0] !== "/") path = "/" + path;
        if (typeof window.__llNavigate === "function")
          window.__llNavigate(path); // SPA: keeps call alive
        else window.location.href = path; // multi-page: ends call
        break;
      case "web_scroll":
        clearHighlight();
        doScroll(String(args.direction || "down"));
        break;
      case "web_scroll_to":
        clearHighlight();
        var e1 = findByText(args.text);
        if (e1) e1.scrollIntoView({ behavior: "smooth", block: "center" });
        break;
      case "web_highlight":
        var e2 = findByText(args.text);
        if (e2) highlight(e2);
        break;
      case "web_clear_highlight":
        clearHighlight();
        break;
      case "web_fill":
        if (typeof args.field === "string" && typeof args.value === "string") {
          var f = findField(args.field);
          if (f) {
            f.focus();
            f.value = args.value;
            f.dispatchEvent(new Event("input", { bubbles: true }));
            f.dispatchEvent(new Event("change", { bubbles: true }));
          }
        }
        break;
      case "web_click":
        if (typeof args.text === "string") {
          var q = args.text.trim().toLowerCase();
          var cands = document.querySelectorAll(
            'button, a, [role="button"], input[type="submit"]',
          );
          for (var i = 0; i < cands.length; i++) {
            var c = cands[i];
            if (c.closest("#ll-voice-root")) continue;
            var t = (c.textContent || c.value || "").trim().toLowerCase();
            if (t.indexOf(q) !== -1) {
              c.click();
              break;
            }
          }
        }
        break;
      case "web_remember":
        var patch = {};
        if (typeof args.name === "string") patch.name = args.name;
        if (typeof args.interest === "string") patch.interest = args.interest;
        if (Object.keys(patch).length) saveVisitor(patch);
        break;
    }
  }

  function release() {
    clearHighlight();
    if (ws) {
      try {
        ws.send(JSON.stringify({ type: "stop" }));
        ws.close();
      } catch (e) {}
      ws = null;
    }
    if (stream) {
      stream.getTracks().forEach(function (t) {
        t.stop();
      });
      stream = null;
    }
    if (processor) {
      processor.disconnect();
      processor = null;
    }
    if (audioCtx) {
      audioCtx.close();
      audioCtx = null;
    }
    queue = [];
    playing = false;
    curSource = null;
  }

  function start() {
    if (state === "connected" || state === "connecting") return;
    setState("connecting", "Connecting…");
    navigator.mediaDevices
      .getUserMedia({
        audio: {
          sampleRate: 24000,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      })
      .then(function (s) {
        stream = s;
        audioCtx = new (window.AudioContext || window.webkitAudioContext)({
          sampleRate: 24000,
        });
        var socket = new WebSocket(
          WS_BASE.replace(/\/$/, "") + "/d/" + SLUG + "/voice",
        );
        ws = socket;
        socket.onopen = function () {
          var src = audioCtx.createMediaStreamSource(stream);
          processor = audioCtx.createScriptProcessor(4096, 1, 1);
          processor.onaudioprocess = function (e) {
            if (socket.readyState !== WebSocket.OPEN) return;
            var input = e.inputBuffer.getChannelData(0);
            var pcm = new Int16Array(input.length);
            for (var i = 0; i < input.length; i++) {
              var v = Math.max(-1, Math.min(1, input[i]));
              pcm[i] = v < 0 ? v * 0x8000 : v * 0x7fff;
            }
            socket.send(
              JSON.stringify({
                type: "audio",
                audio: btoa(
                  String.fromCharCode.apply(null, new Uint8Array(pcm.buffer)),
                ),
              }),
            );
          };
          src.connect(processor);
          processor.connect(audioCtx.destination);
          // returning-visitor recognition + current page → lands in the agent's prompt
          var mem = loadVisitor();
          var ctx = { current_page: location.pathname };
          if (mem.name) {
            ctx.visitor_name = mem.name;
            ctx.returning_visitor = "true";
          }
          if (mem.interest) ctx.last_interest = mem.interest;
          socket.send(JSON.stringify({ type: "context", variables: ctx }));
          socket.send(JSON.stringify({ type: "talk_start" }));
          setState("connected", "End call");
          emit("connected");
        };
        socket.onmessage = function (event) {
          var data;
          try {
            data = JSON.parse(event.data);
          } catch (e) {
            return;
          }
          if (data.type === "session.ready") {
            if (data.sampleRate) sampleRate = data.sampleRate;
          } else if (data.type === "audio") {
            var bin = atob(data.audio),
              bytes = new Uint8Array(bin.length);
            for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
            var pcm = new Int16Array(bytes.buffer),
              f32 = new Float32Array(pcm.length);
            for (var k = 0; k < pcm.length; k++)
              f32[k] = pcm[k] / (pcm[k] < 0 ? 0x8000 : 0x7fff);
            queue.push(f32);
            if (!playing) playNext();
          } else if (data.type === "function_call") {
            handleTool(data.function, data.arguments || {});
          } else if (data.type === "interrupt") {
            queue = [];
            playing = false;
            if (curSource) {
              try {
                curSource.stop();
              } catch (e) {}
              curSource = null;
            }
          } else if (data.type === "session_end") {
            setState("idle", LABEL);
            release();
            emit("ended");
          } else if (data.type === "error") {
            setState("error", "Try again");
            release();
            emit("error", data.message || data.error);
          }
        };
        socket.onerror = function () {
          setState("error", "Try again");
          release();
          emit("error", "connect failed");
        };
        socket.onclose = function () {
          if (state === "connected" || state === "connecting")
            setState("idle", LABEL);
          release();
        };
      })
      .catch(function (err) {
        setState("error", "Try again");
        release();
        emit("error", String(err));
      });
  }

  function stop() {
    setState("idle", LABEL);
    release();
    emit("ended");
  }

  // ── public API ──────────────────────────────────────────────────────
  window.LeadlockVoice = {
    start: start,
    stop: stop,
    isActive: function () {
      return state === "connected" || state === "connecting";
    },
    registerTool: function (name, fn) {
      customTools[name] = fn;
    },
    on: function (ev, fn) {
      (listeners[ev] = listeners[ev] || []).push(fn);
    },
  };

  window.addEventListener("beforeunload", function () {
    if (ws && ws.readyState === WebSocket.OPEN) {
      try {
        ws.send(JSON.stringify({ type: "stop" }));
        ws.close();
      } catch (e) {}
    }
  });

  // ── default UI (skip if headless) ───────────────────────────────────
  if (!HEADLESS) {
    var mount = function () {
      if (document.getElementById("ll-voice-root")) return;
      var root = document.createElement("div");
      root.id = "ll-voice-root";
      root.dataset.state = "idle";
      root.innerHTML =
        '<button id="ll-voice-btn" type="button" aria-label="' +
        LABEL +
        '">' +
        '<span id="ll-voice-icon">🎙️</span><span id="ll-voice-label">' +
        LABEL +
        "</span></button>";
      var style = document.createElement("style");
      style.textContent =
        "#ll-voice-root{position:fixed;right:20px;bottom:20px;z-index:2147483000;font-family:system-ui,-apple-system,sans-serif}" +
        "#ll-voice-btn{display:inline-flex;align-items:center;gap:10px;padding:14px 20px;border:none;border-radius:999px;background:#0b5cff;color:#fff;font-size:16px;font-weight:600;cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.25)}" +
        '#ll-voice-root[data-state="connecting"] #ll-voice-btn{background:#5b6470}' +
        '#ll-voice-root[data-state="connected"] #ll-voice-btn{background:#16a34a}' +
        '#ll-voice-root[data-state="error"] #ll-voice-btn{background:#dc2626}';
      document.head.appendChild(style);
      document.body.appendChild(root);
      document
        .getElementById("ll-voice-btn")
        .addEventListener("click", function () {
          if (state === "connected" || state === "connecting") stop();
          else start();
        });
    };
    if (document.readyState === "loading")
      document.addEventListener("DOMContentLoaded", mount);
    else mount();
  }
})();
