const API_BASE = '/api';

function getHeaders(custom = {}) {
  const token = localStorage.getItem('karina_auth_token');
  const headers = { 'Content-Type': 'application/json', ...custom };
  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }
  return headers;
}

export async function getServices(category = 'all', location = 'all') {
  const params = new URLSearchParams();
  if (category && category !== 'all') params.append('category', category);
  if (location && location !== 'all') params.append('location', location);
  
  const res = await fetch(`${API_BASE}/services/?${params.toString()}`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch services');
  return res.json();
}

export async function getServiceById(id) {
  const res = await fetch(`${API_BASE}/services/${id}/`);
  if (!res.ok) throw new Error('Failed to fetch service');
  return res.json();
}

export async function getTimeSlots(serviceId, date) {
  const params = new URLSearchParams();
  if (serviceId) params.append('service_id', serviceId);
  if (date) params.append('date', date);
  
  const res = await fetch(`${API_BASE}/slots/?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch slots');
  return res.json();
}

export async function getBookings(userName = 'Sarah', status = 'all') {
  const params = new URLSearchParams();
  if (userName) params.append('user_name', userName);
  if (status && status !== 'all') params.append('status', status);
  
  const res = await fetch(`${API_BASE}/bookings/?${params.toString()}`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch bookings');
  return res.json();
}

export async function createBooking(payload) {
  const res = await fetch(`${API_BASE}/bookings/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || 'Failed to create booking');
  }
  return res.json();
}

export async function cancelBooking(bookingId) {
  const res = await fetch(`${API_BASE}/bookings/${bookingId}/cancel/`, {
    method: 'POST',
    headers: getHeaders(),
  });
  if (!res.ok) throw new Error('Failed to cancel booking');
  return res.json();
}

export async function rescheduleBooking(bookingId, booking_date, time_slot) {
  const res = await fetch(`${API_BASE}/bookings/${bookingId}/reschedule/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ booking_date, time_slot }),
  });
  if (!res.ok) throw new Error('Failed to reschedule booking');
  return res.json();
}

export async function initiateMpesaStkPush(phone_number, amount, booking_id = '') {
  const res = await fetch(`${API_BASE}/payments/mpesa-stk/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ phone_number, amount, booking_id }),
  });
  if (!res.ok) throw new Error('Failed to initiate M-Pesa STK push');
  return res.json();
}

export async function getUserPackages(userName = 'Sarah') {
  const res = await fetch(`${API_BASE}/user-packages/?user_name=${encodeURIComponent(userName)}`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch packages');
  return res.json();
}
