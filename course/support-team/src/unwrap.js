// Leadlock posts {function, arguments, call_context}. n8n expressions can't read a
// field named "arguments", so this node pulls it out once and passes plain fields on.
// Function names may carry an install prefix (gp_test_rental_status), so match the end.
const body = $input.first().json.body || {};
const args = body['arguments'] || {};
const ctx = body.call_context || {};
const TOPICS = {
  send_verification_code: 'send_code', verify_code: 'check_code',
  fleet_availability: 'availability', rental_quote: 'quote', rental_status: 'rental_status',
  extend_rental: 'extend_rental', call_off_rent: 'call_off_rent',
  troubleshoot_machine: 'troubleshoot', create_service_ticket: 'create_ticket',
  service_ticket_status: 'ticket_status',
  account_balance: 'balance', send_payment_link: 'send_payment_link',
};
const fn = String(body.function || '');
let topic = String(args.topic || '');
if (!topic) {
  const name = Object.keys(TOPICS).sort((a, b) => b.length - a.length)
    .find(k => fn === k || fn.endsWith('_' + k));
  topic = name ? TOPICS[name] : '';
}
return [{ json: { topic, args, ctx, call_sid: String(ctx.call_sid || '') } }];
