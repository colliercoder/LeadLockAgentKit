// Rentals desk. availability and quote are open to anyone; anything about a
// customer's own rentals needs a verified caller on this call (gate.js above).
const fleet = $('Get Fleet').all().map(i => i.json).filter(r => r.unit_id);
const rentals = $('Get Rentals').all().map(i => i.json).filter(r => r.rental_id);
const today = new Date(now).toISOString().slice(0, 10);

function matchUnits(q) {
  const qw = words(q);
  if (!qw.length) return fleet;
  return fleet.filter(u => {
    const hay = words(u.category + ' ' + u.model + ' ' + u.unit_id).join(' ');
    return qw.some(w => hay.includes(w.replace(/s$/, '')));
  });
}

function quote(u, days) {
  const months = Math.floor(days / 28);
  const rem = days - months * 28;
  const weeks = Math.floor(rem / 7);
  const d = rem - weeks * 7;
  let total = months * u.monthly_rate + weeks * u.weekly_rate + Math.min(d * u.daily_rate, u.weekly_rate);
  total = Math.min(total, (months + 1) * u.monthly_rate);
  return total;
}

const pub = u => ({ unit_id: u.unit_id, model: u.model, category: u.category, yard: u.yard, status: u.status,
  available_from: u.available_from, daily_rate: u.daily_rate, weekly_rate: u.weekly_rate, monthly_rate: u.monthly_rate });

if (topic === 'availability') {
  const start = String(args.start_date || today);
  const units = matchUnits(args.category || args.machine);
  if (!units.length) return out({ available: [], categories: [...new Set(fleet.map(u => u.category))] });
  const free = units.filter(u => u.available_from <= start);
  const soon = units.filter(u => !free.includes(u)).map(u => ({ unit_id: u.unit_id, model: u.model, yard: u.yard, available_from: u.available_from }));
  return out({ start_date: start, available: free.slice(0, 5).map(pub), not_free_until_later: soon.slice(0, 3) });
}

if (topic === 'quote') {
  const days = Math.max(1, parseInt(args.days, 10) || 1);
  const units = args.unit_id ? fleet.filter(u => u.unit_id.toLowerCase() === String(args.unit_id).toLowerCase())
                             : matchUnits(args.category || args.machine);
  if (!units.length) return out({ error: 'no_matching_machine', categories: [...new Set(fleet.map(u => u.category))] });
  const seen = new Set();
  const quotes = units.filter(u => !seen.has(u.model) && seen.add(u.model)).slice(0, 3).map(u => ({
    model: u.model, days, total: quote(u, days), total_spoken: money(quote(u, days)),
    daily_rate: u.daily_rate, weekly_rate: u.weekly_rate, monthly_rate: u.monthly_rate,
  }));
  return out({ quotes, note: 'Rental only. Delivery, pickup, fuel and tax are quoted by the yard.' });
}

if (!me) return out(VERIFY_FIRST);
const mine = rentals.filter(r => r.customer_id === me.customer_id);
const pubRental = r => ({ rental_id: r.rental_id, unit_id: r.unit_id, model: r.model, start_date: r.start_date,
  end_date: r.end_date, status: r.status, site: r.site });

if (topic === 'rental_status') {
  return out({ first_name: me.first_name, company: me.company, rentals: mine.map(pubRental) });
}

function findMine() {
  const id = String(args.rental_id || '').toUpperCase();
  if (id) return mine.find(r => r.rental_id.toUpperCase() === id) || null;
  const active = mine.filter(r => r.status !== 'Off-rent requested');
  return active.length === 1 ? active[0] : null;
}

if (topic === 'extend_rental') {
  const r = findMine();
  if (!r) return out({ error: 'which_rental', rentals: mine.map(pubRental) });
  const newEnd = String(args.new_end_date || '');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(newEnd) || newEnd <= r.end_date)
    return out({ error: 'new_end_date_must_be_after', current_end_date: r.end_date });
  const clash = rentals.find(o => o.unit_id === r.unit_id && o.rental_id !== r.rental_id && o.start_date <= newEnd && o.start_date >= r.end_date);
  if (clash) return out({ extended: false, reason: 'unit_booked_next', booked_from: clash.start_date });
  return [{ json: { action: 'write', write: { ...r, end_date: newEnd },
    response: { extended: true, rental_id: r.rental_id, model: r.model, old_end_date: r.end_date, new_end_date: newEnd } } }];
}

if (topic === 'call_off_rent') {
  const r = findMine();
  if (!r) return out({ error: 'which_rental', rentals: mine.map(pubRental) });
  const pickup = /^\d{4}-\d{2}-\d{2}$/.test(String(args.pickup_date || '')) ? String(args.pickup_date) : today;
  return [{ json: { action: 'write', write: { ...r, status: 'Off-rent requested', end_date: pickup },
    response: { called_off: true, rental_id: r.rental_id, model: r.model, pickup_date: pickup,
      note: 'The yard confirms the pickup window.' } } }];
}

return out({ error: 'unknown_topic' });
