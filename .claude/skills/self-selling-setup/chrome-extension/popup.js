// Leadlock GHL Token Grabber - reads the Firebase refresh token from GHL's
// IndexedDB (firebaseLocalStorageDb), the standard Firebase auth storage.
let refreshToken = null;
const grabBtn = document.getElementById("grabBtn");
const copyBtn = document.getElementById("copyBtn");
const statusEl = document.getElementById("status");
const preview = document.getElementById("preview");

function setStatus(msg, type) {
  statusEl.textContent = msg;
  statusEl.className = type || "info";
}

grabBtn.addEventListener("click", async () => {
  grabBtn.disabled = true;
  setStatus("Reading IndexedDB...", "info");
  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });
    if (!tab?.url?.match(/gohighlevel\.com|leadconnectorhq\.com/)) {
      setStatus("Open an app.gohighlevel.com tab first.", "error");
      grabBtn.disabled = false;
      return;
    }
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: extractToken,
      world: "MAIN",
    });
    const result = results?.[0]?.result;
    if (result?.refreshToken) {
      refreshToken = result.refreshToken;
      setStatus("Token grabbed.", "success");
      preview.textContent =
        refreshToken.slice(0, 36) + "..." + refreshToken.slice(-16);
      preview.style.display = "block";
      copyBtn.disabled = false;
    } else {
      setStatus("No token found. Make sure you're logged into GHL.", "error");
    }
  } catch (err) {
    setStatus("Error: " + err.message, "error");
  }
  grabBtn.disabled = false;
});

copyBtn.addEventListener("click", async () => {
  if (!refreshToken) return;
  try {
    await navigator.clipboard.writeText(refreshToken);
  } catch {
    const ta = document.createElement("textarea");
    ta.value = refreshToken;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    ta.remove();
  }
  setStatus(
    "Copied. Paste it where the setup asks for the refresh token.",
    "success",
  );
});

// Runs in the PAGE context: pull stsTokenManager.refreshToken from Firebase IndexedDB.
function extractToken() {
  return new Promise((resolve) => {
    try {
      const req = indexedDB.open("firebaseLocalStorageDb");
      req.onerror = () => resolve({ error: "Cannot open IndexedDB" });
      req.onsuccess = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains("firebaseLocalStorage")) {
          resolve({ error: "firebaseLocalStorage store not found" });
          return;
        }
        const getAll = db
          .transaction("firebaseLocalStorage", "readonly")
          .objectStore("firebaseLocalStorage")
          .getAll();
        getAll.onsuccess = () => {
          for (const entry of getAll.result) {
            const val = entry?.value || entry;
            const stm = val?.stsTokenManager;
            if (stm?.refreshToken) {
              resolve({ refreshToken: stm.refreshToken, uid: val.uid });
              return;
            }
          }
          resolve({ error: "No refresh token in IndexedDB entries" });
        };
        getAll.onerror = () => resolve({ error: "Failed to read store" });
      };
    } catch (err) {
      resolve({ error: err.message });
    }
  });
}
