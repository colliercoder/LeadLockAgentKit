// Billing desk. Everything here is account data, so every topic needs a verified
// caller. The payment link goes ONLY to the email or phone on file, and no card
// number is ever taken or stored.
const COMPANY = 'Granite Peak';
const PAY_LINK_BASE = 'https://example.com/pay/';
const EMAIL_ENABLED = true;
const SMS_ENABLED = false;
const rentals = $('Get Rentals').all().map(i => i.json).filter(r => r.rental_id);
const digits = s => String(s || '').replace(/\D/g, '');
const maskEmail = e => { const [u, d] = String(e).split('@'); return u.charAt(0) + '***@' + d; };
const maskPhone = p => '***-***-' + digits(p).slice(-4);

if (!me) return out(VERIFY_FIRST);
const invoices = rentals.filter(r => r.customer_id === me.customer_id && r.invoice_id).map(r => ({
  invoice_id: r.invoice_id, rental_id: r.rental_id, model: r.model, total: Number(r.invoice_total || 0),
  total_spoken: money(r.invoice_total), status: r.invoice_status, due: r.invoice_due,
}));
const open = invoices.filter(i => i.status === 'Open' || i.status === 'Overdue');
const balance = open.reduce((s, i) => s + i.total, 0);

if (topic === 'balance') {
  return out({ first_name: me.first_name, company: me.company, balance_due: balance,
    balance_spoken: money(balance), open_invoices: open, all_invoices: invoices });
}

if (topic === 'send_payment_link') {
  if (!open.length) return out({ sent: false, reason: 'nothing_due' });
  const id = String(args.invoice_id || '').toUpperCase();
  const inv = id ? open.find(i => i.invoice_id === id) : null;
  if (id && !inv) return out({ sent: false, reason: 'invoice_not_open', open_invoices: open });
  const amount = inv ? inv.total : balance;
  const ref = inv ? inv.invoice_id : 'balance-' + me.customer_id;
  let channel = String(args.channel || '').toLowerCase() === 'email' ? 'email' : 'sms';
  if (channel === 'sms' && !SMS_ENABLED) channel = 'email';
  if (channel === 'email' && !EMAIL_ENABLED) channel = 'sms';
  if (channel === 'sms' && !SMS_ENABLED) return out({ sent: false, reason: 'no_delivery_channel' });
  const message = `${COMPANY}: ${inv ? 'invoice ' + inv.invoice_id : 'your balance'} for ${money(amount)}. Pay securely here: ${PAY_LINK_BASE}${ref}`;
  return [{ json: { action: channel, message, subject: `${COMPANY} payment link`,
    send_to: channel === 'sms' ? me.phone : me.email,
    response: { sent: true, channel, to: channel === 'sms' ? maskPhone(me.phone) : maskEmail(me.email),
      for: inv ? inv.invoice_id : 'full balance', amount, amount_spoken: money(amount) } } }];
}

return out({ error: 'unknown_topic' });
