const API_BASE = '/api';

function getHeaders(custom = {}) {
  const token = localStorage.getItem('karina_access_token') || localStorage.getItem('karina_auth_token');
  const headers = { 'Content-Type': 'application/json', ...custom };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
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

export async function getBookings(userName = '', status = 'all', personal = false) {
  const params = new URLSearchParams();
  if (userName) params.append('user_name', userName);
  if (status && status !== 'all') params.append('status', status);
  if (personal) params.append('personal', '1');
  
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

// ==========================================
// ADMIN DASHBOARD CLIENT SERVICES
// ==========================================

export async function getAdminOverview() {
  const res = await fetch(`${API_BASE}/admin/overview/`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch admin overview metrics');
  return res.json();
}

export async function getAdminServices() {
  const res = await fetch(`${API_BASE}/admin/services/`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch services for admin');
  return res.json();
}

export async function createAdminService(serviceData) {
  const res = await fetch(`${API_BASE}/admin/services/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(serviceData)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || Object.values(err)[0]?.[0] || 'Failed to create service');
  }
  return res.json();
}

export async function updateAdminService(serviceId, serviceData) {
  const res = await fetch(`${API_BASE}/admin/services/${serviceId}/`, {
    method: 'PATCH',
    headers: getHeaders(),
    body: JSON.stringify(serviceData)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || 'Failed to update service');
  }
  return res.json();
}

export async function deleteAdminService(serviceId) {
  const res = await fetch(`${API_BASE}/admin/services/${serviceId}/`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to delete service');
  return res.json();
}

export async function getAdminSlots(paramsObj = {}) {
  const params = new URLSearchParams();
  if (paramsObj.serviceId && paramsObj.serviceId !== 'all') params.append('service_id', paramsObj.serviceId);
  if (paramsObj.date) params.append('date', paramsObj.date);
  if (paramsObj.dateFrom) params.append('date_from', paramsObj.dateFrom);
  if (paramsObj.dateTo) params.append('date_to', paramsObj.dateTo);

  const res = await fetch(`${API_BASE}/admin/slots/?${params.toString()}`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch session slots');
  return res.json();
}

export async function createAdminSlot(slotData) {
  const res = await fetch(`${API_BASE}/admin/slots/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(slotData)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || Object.values(err)[0]?.[0] || 'Failed to create session slot');
  }
  return res.json();
}

export async function bulkGenerateAdminSlots(bulkPayload) {
  const res = await fetch(`${API_BASE}/admin/slots/bulk-generate/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(bulkPayload)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || 'Failed to bulk generate slots');
  }
  return res.json();
}

export async function updateAdminSlot(slotId, updateData) {
  const res = await fetch(`${API_BASE}/admin/slots/${slotId}/`, {
    method: 'PATCH',
    headers: getHeaders(),
    body: JSON.stringify(updateData)
  });
  if (!res.ok) throw new Error('Failed to update slot');
  return res.json();
}

export async function deleteAdminSlot(slotId) {
  const res = await fetch(`${API_BASE}/admin/slots/${slotId}/`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to delete slot');
  return res.json();
}

export async function getAdminBookings(filters = {}) {
  const params = new URLSearchParams();
  if (filters.status && filters.status !== 'all') params.append('status', filters.status);
  if (filters.date) params.append('date', filters.date);
  if (filters.serviceId && filters.serviceId !== 'all') params.append('service_id', filters.serviceId);
  if (filters.search) params.append('search', filters.search);

  const res = await fetch(`${API_BASE}/admin/bookings/?${params.toString()}`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch bookings');
  return res.json();
}

export async function updateAdminBooking(bookingId, updateData) {
  const res = await fetch(`${API_BASE}/admin/bookings/${bookingId}/`, {
    method: 'PATCH',
    headers: getHeaders(),
    body: JSON.stringify(updateData)
  });
  if (!res.ok) throw new Error('Failed to update booking');
  return res.json();
}

export async function deleteAdminBooking(bookingId) {
  const res = await fetch(`${API_BASE}/admin/bookings/${bookingId}/`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to delete booking');
  return res.json();
}

export async function getAdminCustomers(filters = {}) {
  const params = new URLSearchParams();
  if (filters.search) params.append('search', filters.search);
  if (filters.status && filters.status !== 'all') params.append('status', filters.status);

  const res = await fetch(`${API_BASE}/admin/customers/?${params.toString()}`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch customers');
  return res.json();
}

export async function getAdminCustomerDetail(customerId) {
  const res = await fetch(`${API_BASE}/admin/customers/${customerId}/`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to fetch customer details');
  return res.json();
}

export async function updateAdminCustomer(customerId, updateData) {
  const res = await fetch(`${API_BASE}/admin/customers/${customerId}/`, {
    method: 'PATCH',
    headers: getHeaders(),
    body: JSON.stringify(updateData)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || 'Failed to update customer');
  }
  return res.json();
}

export async function createAdminCustomer(customerData) {
  const res = await fetch(`${API_BASE}/admin/customers/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(customerData)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.username?.[0] || err.email?.[0] || err.error || 'Failed to create customer');
  }
  return res.json();
}

export async function issueCustomerPass(customerId, passData) {
  const res = await fetch(`${API_BASE}/admin/customers/${customerId}/passes/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(passData)
  });
  if (!res.ok) throw new Error('Failed to issue pass');
  return res.json();
}

// Media Upload APIs (Phase 2)
export async function uploadServiceImage(serviceId, file) {
  const token = localStorage.getItem('karina_access_token') || localStorage.getItem('karina_auth_token');
  const formData = new FormData();
  formData.append('image', file);
  const headers = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}/admin/services/${serviceId}/image/`, {
    method: 'POST',
    headers,
    body: formData
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || 'Failed to upload service photo');
  }
  return res.json();
}

export async function deleteServiceImage(serviceId) {
  const res = await fetch(`${API_BASE}/admin/services/${serviceId}/image/`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to remove service photo');
  return res.json();
}

export async function uploadSessionBanner(slotId, file) {
  const token = localStorage.getItem('karina_access_token') || localStorage.getItem('karina_auth_token');
  const formData = new FormData();
  formData.append('banner_image', file);
  const headers = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}/admin/slots/${slotId}/banner/`, {
    method: 'POST',
    headers,
    body: formData
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || 'Failed to upload session banner');
  }
  return res.json();
}

export async function deleteSessionBanner(slotId) {
  const res = await fetch(`${API_BASE}/admin/slots/${slotId}/banner/`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to remove session banner');
  return res.json();
}

export async function uploadProfileAvatar(file) {
  const token = localStorage.getItem('karina_access_token') || localStorage.getItem('karina_auth_token');
  const formData = new FormData();
  formData.append('avatar', file);
  const headers = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}/auth/profile/avatar/`, {
    method: 'POST',
    headers,
    body: formData
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || 'Failed to upload avatar');
  }
  return res.json();
}

export async function deleteProfileAvatar() {
  const res = await fetch(`${API_BASE}/auth/profile/avatar/`, {
    method: 'DELETE',
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to remove profile picture');
  return res.json();
}

export async function getUserProfile() {
  const res = await fetch(`${API_BASE}/auth/profile/`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Failed to load user profile');
  return res.json();
}

export async function updateUserProfile(payload) {
  const res = await fetch(`${API_BASE}/auth/profile/`, {
    method: 'PATCH',
    headers: getHeaders(),
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const message = Object.values(err).flat().join(' ') || 'Failed to update profile';
    throw new Error(message);
  }
  return res.json();
}


