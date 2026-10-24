// Shared by the Rentals, Maintenance and Billing workflows: who is verified on this call.
const inp = $('Unwrap').first().json;
const { topic, args, ctx, call_sid } = inp;
const now = Date.now();
const customers = $('Get Customers').all().map(i => i.json).filter(r => r.customer_id);
const ver = $('Get Verification').all().map(i => i.json).find(r => call_sid && r.call_sid === call_sid);
const verified = !!(ver && ver.verified && ver.expires_at && Date.parse(ver.expires_at) > now);
const me = verified ? customers.find(c => c.customer_id === ver.customer_id) || null : null;
const out = (response, extra = {}) => [{ json: { action: 'respond', response, write: null, ...extra } }];
const VERIFY_FIRST = { error: 'verify_first', say: 'Verify the caller first: send them a code, then check it.' };
const words = s => String(s || '').toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter(w => w.length > 1);
const money = n => '$' + Number(n || 0).toLocaleString('en-US', { minimumFractionDigits: 0 });
