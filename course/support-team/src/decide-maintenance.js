// Maintenance desk. Troubleshooting is open to anyone (it's how-to, not account
// data); tickets touch the account, so they need a verified caller on this call.
const TIMEZONE = 'America/Denver';
const guide = $('Get Troubleshooting').all().map(i => i.json).filter(r => r.guide_id);
const rentals = $('Get Rentals').all().map(i => i.json).filter(r => r.rental_id);
const tickets = $('Get Service').all().map(i => i.json).filter(r => r.ticket_id);
const SAFETY = 'Before anyone checks anything: machine parked on level ground, bucket, blade or body down, parking brake set, engine off, and locked out before anyone climbs on.';

if (topic === 'troubleshoot') {
  const mw = words(args.machine), sw = words(args.symptom);
  const scored = guide.map(g => {
    const mh = words(g.category + ' ' + g.machine).join(' ');
    const sh = words(g.symptom + ' ' + g.likely_cause).join(' ');
    const m = mw.filter(w => mh.includes(w.replace(/s$/, ''))).length;
    const s = sw.filter(w => w.length > 2 && sh.includes(w.replace(/s$/, ''))).length;
    return { g, score: (m ? 2 : g.category === 'Any' ? 1 : 0) + s * 3 };
  }).filter(x => x.score >= 3).sort((a, b) => b.score - a.score).slice(0, 2);
  const matches = scored.map(({ g }) => ({ machine: g.machine, symptom: g.symptom, likely_cause: g.likely_cause,
    what_to_check: g.what_to_check, call_tech_when: g.call_tech_when }));
  return out({ safety_first: SAFETY, matches,
    if_no_match: matches.length ? undefined : 'No guide entry fits. Get the machine safe and open a service ticket.' });
}

if (!me) return out(VERIFY_FIRST);
const myUnits = rentals.filter(r => r.customer_id === me.customer_id && r.status !== 'Off-rent requested');
const pubTicket = t => ({ ticket_id: t.ticket_id, unit_id: t.unit_id, issue: t.issue, status: t.status, tech_eta: t.tech_eta });

if (topic === 'create_ticket') {
  const unitId = String(args.unit_id || '').toUpperCase();
  const r = unitId ? myUnits.find(x => x.unit_id.toUpperCase() === unitId) : myUnits.length === 1 ? myUnits[0] : null;
  if (!r) return out({ error: 'which_unit', your_units: myUnits.map(x => ({ unit_id: x.unit_id, model: x.model, site: x.site })) });
  const issue = String(args.issue || '').trim();
  if (issue.length < 3) return out({ error: 'describe_the_issue' });
  const down = args.machine_down === true || String(args.machine_down).toLowerCase() === 'true';
  const local = DateTime.fromMillis(now).setZone(TIMEZONE);
  const eta = down ? local.plus({ hours: 4 }).startOf('hour') : local.plus({ days: 1 }).set({ hour: 8, minute: 0, second: 0 });
  const next = Math.max(9000, ...tickets.map(t => parseInt(String(t.ticket_id).replace(/\D/g, ''), 10) || 0)) + 1;
  const row = { ticket_id: 'S-' + next, customer_id: me.customer_id, unit_id: r.unit_id, issue: issue.slice(0, 300),
    status: down ? 'Tech dispatched' : 'Open', tech_eta: eta.toFormat('yyyy-MM-dd HH:mm'),
    created_at: local.toFormat('yyyy-MM-dd HH:mm') };
  return [{ json: { action: 'write', write: row, response: { ...pubTicket(row), model: r.model, site: r.site,
    tech_eta_spoken: eta.toFormat("cccc 'at' h:mm a") + ' Mountain time' } } }];
}

if (topic === 'ticket_status') {
  const mine = tickets.filter(t => t.customer_id === me.customer_id);
  const id = String(args.ticket_id || '').toUpperCase();
  const list = id ? mine.filter(t => t.ticket_id.toUpperCase() === id) : mine;
  return out({ first_name: me.first_name, tickets: list.map(pubTicket) });
}

return out({ error: 'unknown_topic' });
