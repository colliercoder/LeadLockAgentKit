// All verification logic. The plain code exists only in this run's memory and the
// outgoing message: the table stores sha256(pepper + code + call_sid) and the webhook
// reply never carries it. The pepper lives only in this node, so a copy of the
// Verifications table alone can't be used to brute-force a code.
// The n8n Code sandbox blocks the crypto module, so random bytes come from the
// Crypto node ("Random") and SHA-256 is plain JS below.
const PEPPER = 'set-by-installer';
const COMPANY = 'Granite Peak';
const EMAIL_ENABLED = true;
const SMS_ENABLED = false;
const MAX_ATTEMPTS = 3;
const CODE_TTL_MS = 10 * 60 * 1000;
const SESSION_TTL_MS = 60 * 60 * 1000;

const inp = $('Unwrap').first().json;
const { topic, args, ctx, call_sid } = inp;
const customers = $('Get Customers').all().map(i => i.json).filter(r => r.customer_id);
const existing = $('Get Verification').all().map(i => i.json).find(r => r.call_sid === call_sid) || null;
const now = Date.now();

const digits = s => String(s || '').replace(/\D/g, '');
const last10 = s => digits(s).slice(-10);
const hash = code => sha256(PEPPER + code + call_sid);
const expired = row => !row || !row.expires_at || Date.parse(row.expires_at) <= now;
const maskEmail = e => { const [u, d] = String(e).split('@'); return u.charAt(0) + '***@' + d; };
const maskPhone = p => '***-***-' + digits(p).slice(-4);
const out = (action, response, extra = {}) => [{ json: { action, response, write: null, ...extra } }];

if (!call_sid) return out('respond', { error: 'missing_call_sid' });

function findCustomer() {
  if (ctx.contact_phone) {
    const hit = customers.filter(c => last10(c.phone) === last10(ctx.contact_phone));
    if (hit.length === 1) return hit[0];
  }
  const l4 = digits(args.phone_last4);
  const first = String(args.first_name || '').trim().toLowerCase();
  if (l4.length === 4 && first) {
    const hit = customers.filter(c => digits(c.phone).endsWith(l4) && String(c.first_name).toLowerCase() === first);
    if (hit.length === 1) return hit[0];
  }
  return null;
}

if (topic === 'send_code') {
  if (existing && existing.verified && !expired(existing)) return out('respond', { sent: false, already_verified: true });
  if (existing && !existing.verified && existing.attempts >= MAX_ATTEMPTS && !expired(existing))
    return out('respond', { sent: false, locked: true, reason: 'too_many_attempts' });
  const cust = findCustomer();
  if (!cust) return out('respond', { sent: false, reason: 'no_customer_match' });
  let channel = String(args.channel || 'email').toLowerCase() === 'sms' ? 'sms' : 'email';
  if (channel === 'sms' && !SMS_ENABLED) channel = 'email';
  if (channel === 'email' && !EMAIL_ENABLED) channel = 'sms';
  if (channel === 'sms' && !SMS_ENABLED) return out('respond', { sent: false, reason: 'no_delivery_channel' });
  const code = String(BigInt('0x' + $('Random').first().json.rand) % 1000000n).padStart(6, '0');
  // A resend inside the window keeps the attempt count, so resending never buys more guesses.
  const attempts = existing && !expired(existing) && !existing.verified ? Number(existing.attempts || 0) : 0;
  const write = {
    call_sid, customer_id: cust.customer_id, code_hash: hash(code),
    expires_at: new Date(now + CODE_TTL_MS).toISOString(), attempts, verified: false,
  };
  const message = `Your ${COMPANY} verification code is ${code}. It expires in 10 minutes.`;
  // Send ONLY to what is on file, never to anything the caller says.
  return [{ json: {
    action: channel, write, message, subject: `Your ${COMPANY} verification code`,
    send_to: channel === 'sms' ? cust.phone : cust.email,
    response: { sent: true, channel, to: channel === 'sms' ? maskPhone(cust.phone) : maskEmail(cust.email) },
  } }];
}

if (topic === 'check_code') {
  if (!existing || !existing.code_hash) return out('respond', { verified: false, error: 'no_code_sent' });
  const cust = customers.find(c => c.customer_id === existing.customer_id) || {};
  const ok = { verified: true, first_name: cust.first_name, company: cust.company };
  if (existing.verified && !expired(existing)) return out('respond', ok);
  if (expired(existing)) return out('respond', { verified: false, error: 'code_expired' });
  const attempts = Number(existing.attempts || 0);
  if (attempts >= MAX_ATTEMPTS) return out('respond', { verified: false, locked: true, attempts_left: 0 });
  const match = digits(args.code).length === 6 && sameHex(hash(digits(args.code)), String(existing.code_hash));
  const write = { ...pick(existing), attempts: attempts + 1 };
  if (match) {
    write.verified = true;
    write.expires_at = new Date(now + SESSION_TTL_MS).toISOString();
    return [{ json: { action: 'write', write, response: ok } }];
  }
  const left = MAX_ATTEMPTS - (attempts + 1);
  return [{ json: { action: 'write', write, response: left > 0 ? { verified: false, attempts_left: left } : { verified: false, locked: true, attempts_left: 0 } } }];
}

return out('respond', { error: 'unknown_topic' });

function pick(r) {
  return { call_sid: r.call_sid, customer_id: r.customer_id, code_hash: r.code_hash,
           expires_at: r.expires_at, attempts: Number(r.attempts || 0), verified: !!r.verified };
}

function sameHex(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}
function sha256(msg) {
  const K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  const H = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
  const bytes = Array.from(Buffer.from(String(msg), 'utf8'));
  const bitLen = bytes.length * 8;
  bytes.push(0x80);
  while (bytes.length % 64 !== 56) bytes.push(0);
  for (let i = 7; i >= 0; i--) bytes.push(Math.floor(bitLen / 2 ** (8 * i)) & 0xff);
  const rotr = (x, n) => (x >>> n) | (x << (32 - n));
  const W = new Array(64);
  for (let off = 0; off < bytes.length; off += 64) {
    for (let i = 0; i < 16; i++)
      W[i] = (bytes[off + 4 * i] << 24) | (bytes[off + 4 * i + 1] << 16) | (bytes[off + 4 * i + 2] << 8) | bytes[off + 4 * i + 3];
    for (let i = 16; i < 64; i++) {
      const s0 = rotr(W[i - 15], 7) ^ rotr(W[i - 15], 18) ^ (W[i - 15] >>> 3);
      const s1 = rotr(W[i - 2], 17) ^ rotr(W[i - 2], 19) ^ (W[i - 2] >>> 10);
      W[i] = (W[i - 16] + s0 + W[i - 7] + s1) | 0;
    }
    let [a, b, c, d, e, f, g, h] = H;
    for (let i = 0; i < 64; i++) {
      const t1 = (h + (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + W[i]) | 0;
      const t2 = ((rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) | 0;
      h = g; g = f; f = e; e = (d + t1) | 0; d = c; c = b; b = a; a = (t1 + t2) | 0;
    }
    H[0] = (H[0] + a) | 0; H[1] = (H[1] + b) | 0; H[2] = (H[2] + c) | 0; H[3] = (H[3] + d) | 0;
    H[4] = (H[4] + e) | 0; H[5] = (H[5] + f) | 0; H[6] = (H[6] + g) | 0; H[7] = (H[7] + h) | 0;
  }
  return H.map(x => (x >>> 0).toString(16).padStart(8, '0')).join('');
}
