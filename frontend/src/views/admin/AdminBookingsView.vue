<template>
  <div class="space-y-6 animate-fadeIn">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">
          Client Reservations &amp; Attendee Roster
        </h3>
        <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
          Track studio attendees, record session completion, reschedule dates, and log practitioner notes
        </p>
      </div>

      <button
        @click="loadBookings"
        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container text-xs font-semibold self-start sm:self-auto"
        type="button"
      >
        <span class="material-symbols-outlined text-sm">refresh</span>
        <span>Refresh Roster</span>
      </button>
    </div>

    <!-- Notice -->
    <div v-if="notice" class="p-3.5 rounded-2xl flex items-center justify-between gap-2 text-xs font-medium" :class="noticeType === 'error' ? 'bg-red-50 text-red-800 dark:bg-red-950/50 dark:text-red-300' : 'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300'">
      <span>{{ notice }}</span>
      <button @click="notice = ''" class="font-bold">&times;</button>
    </div>

    <!-- Filter Bar -->
    <div class="flex flex-col sm:flex-row items-center gap-3">
      <div class="relative w-full sm:w-80">
        <span class="material-symbols-outlined absolute left-3 top-2.5 text-on-surface-variant text-base">search</span>
        <input
          v-model="search"
          type="text"
          placeholder="Search by client, email, phone, ref..."
          class="w-full pl-9 pr-4 py-2 rounded-2xl bg-surface-container-lowest dark:bg-slate-900 border border-outline-variant/30 dark:border-slate-800 text-xs font-body-sm focus:outline-none focus:ring-2 focus:ring-primary-container/30"
        />
      </div>

      <div class="flex items-center gap-2 overflow-x-auto w-full pb-1 no-scrollbar">
        <button
          v-for="st in ['all', 'confirmed', 'completed', 'cancelled']"
          :key="st"
          @click="statusFilter = st"
          :class="statusFilter === st ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-bold' : 'bg-surface-container-low dark:bg-slate-800 text-on-surface-variant dark:text-slate-300'"
          class="px-3.5 py-1.5 rounded-full font-label-sm text-xs capitalize whitespace-nowrap transition-all"
          type="button"
        >
          {{ st }}
        </button>
      </div>
    </div>

    <!-- Bookings Table -->
    <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-xs overflow-hidden">
      <div v-if="filteredBookings.length === 0" class="text-center py-12 text-on-surface-variant dark:text-slate-400 text-sm">
        <span class="material-symbols-outlined text-4xl block mb-2 opacity-50">inbox</span>
        No reservations match your search or filter.
      </div>

      <!-- Mobile Bookings Cards (< 768px) -->
      <div v-else class="md:hidden divide-y divide-outline-variant/20 dark:divide-slate-800">
        <div
          v-for="b in filteredBookings"
          :key="'mb-' + b.id"
          class="p-4 space-y-2.5 hover:bg-surface-container-low/40 dark:hover:bg-slate-800/40 transition-colors"
        >
          <div class="flex items-center justify-between gap-2">
            <div>
              <h4 class="font-headline-sm text-sm font-bold text-primary-container dark:text-white">
                {{ b.user_name }}
              </h4>
              <p class="font-body-sm text-[11px] text-on-surface-variant dark:text-slate-400">
                {{ b.user_email }} &bull; {{ b.user_phone }}
              </p>
            </div>
            <span
              class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider shrink-0"
              :class="statusBadgeClass(b.status)"
            >
              {{ b.status }}
            </span>
          </div>

          <div class="bg-surface-container-low dark:bg-slate-800/60 p-2.5 rounded-xl border border-outline-variant/20 dark:border-slate-800 flex items-center justify-between text-xs">
            <div>
              <span class="font-semibold text-primary-container dark:text-white block">{{ b.service_title }}</span>
              <span class="text-[11px] text-on-surface-variant dark:text-slate-400 font-mono">{{ b.booking_date }} at {{ b.time_slot }}</span>
            </div>
            <div class="text-right">
              <span class="font-bold text-primary-container dark:text-white block">{{ b.currency }} {{ (b.total_amount || 0).toLocaleString() }}</span>
              <span class="text-[10px] uppercase font-mono text-on-surface-variant dark:text-slate-400">{{ b.payment_method }}</span>
            </div>
          </div>

          <div v-if="b.coach_notes" class="text-[11px] text-on-surface-variant dark:text-slate-400 bg-surface-container-lowest dark:bg-slate-900 p-2 rounded-lg border border-outline-variant/20 dark:border-slate-800 italic">
            Coach Notes: {{ b.coach_notes }}
          </div>

          <div class="flex items-center justify-end gap-1.5 pt-1">
            <button
              v-if="b.status !== 'completed'"
              @click="updateStatus(b, 'completed')"
              class="px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 font-label-sm text-[11px] font-semibold hover:bg-emerald-100 transition-colors"
              type="button"
            >
              Complete
            </button>
            <button
              @click="openManageModal(b)"
              class="px-3 py-1 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container font-label-sm text-xs font-semibold border border-outline-variant/30 dark:border-slate-700 text-on-surface dark:text-slate-200 transition-colors"
              type="button"
            >
              Manage
            </button>
            <button
              @click="removeBooking(b)"
              class="w-7 h-7 rounded-full bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 hover:bg-red-100 flex items-center justify-center transition-colors"
              title="Delete Record"
              type="button"
            >
              <span class="material-symbols-outlined text-xs">delete</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Desktop Bookings Table (>= 768px) -->
      <div v-if="filteredBookings.length > 0" class="hidden md:block overflow-x-auto">
        <table class="w-full text-left text-xs font-body-sm">
          <thead class="bg-surface-container-low dark:bg-slate-800/60 text-on-surface-variant dark:text-slate-400 font-label-sm text-[11px] uppercase tracking-wider border-b border-outline-variant/20 dark:border-slate-800">
            <tr>
              <th class="px-5 py-3.5">Client &amp; Contact</th>
              <th class="px-5 py-3.5">Service Offering</th>
              <th class="px-5 py-3.5">Date &amp; Time</th>
              <th class="px-5 py-3.5">Amount &amp; Ref</th>
              <th class="px-5 py-3.5">Status</th>
              <th class="px-5 py-3.5">Notes</th>
              <th class="px-5 py-3.5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-outline-variant/20 dark:divide-slate-800">
            <tr
              v-for="b in filteredBookings"
              :key="b.id"
              class="hover:bg-surface-container-low/40 dark:hover:bg-slate-800/40 transition-colors"
            >
              <td class="px-5 py-3.5 whitespace-nowrap">
                <div class="font-bold text-primary-container dark:text-white">{{ b.user_name }}</div>
                <div class="text-[11px] text-on-surface-variant dark:text-slate-400">{{ b.user_email }}</div>
                <div class="text-[11px] text-secondary font-mono">{{ b.user_phone }}</div>
              </td>
              <td class="px-5 py-3.5 font-semibold text-primary-container dark:text-white max-w-xs truncate">
                {{ b.service_title }}
              </td>
              <td class="px-5 py-3.5 whitespace-nowrap">
                <div class="font-medium text-on-surface dark:text-slate-200">{{ b.booking_date }}</div>
                <div class="text-[11px] text-secondary font-mono">{{ b.time_slot }}</div>
              </td>
              <td class="px-5 py-3.5 whitespace-nowrap">
                <div class="font-bold text-primary-container dark:text-white">
                  {{ b.currency }} {{ (b.total_amount || 0).toLocaleString() }}
                </div>
                <div class="text-[10px] text-on-surface-variant dark:text-slate-400 uppercase font-mono truncate max-w-[120px]">
                  {{ b.payment_method }} &bull; {{ b.payment_reference }}
                </div>
              </td>
              <td class="px-5 py-3.5 whitespace-nowrap">
                <span
                  class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider"
                  :class="statusBadgeClass(b.status)"
                >
                  {{ b.status }}
                </span>
              </td>
              <td class="px-5 py-3.5 text-on-surface-variant dark:text-slate-400 max-w-xs truncate text-[11px]">
                {{ b.coach_notes || b.notes || '—' }}
              </td>
              <td class="px-5 py-3.5 text-right whitespace-nowrap">
                <div class="flex items-center justify-end gap-1.5">
                  <button
                    v-if="b.status !== 'completed'"
                    @click="updateStatus(b, 'completed')"
                    class="px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 font-label-sm text-[11px] font-semibold hover:bg-emerald-100 transition-colors"
                    type="button"
                  >
                    Complete
                  </button>
                  <button
                    @click="openManageModal(b)"
                    class="px-3 py-1 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container font-label-sm text-xs font-semibold border border-outline-variant/30 dark:border-slate-700 transition-colors"
                    type="button"
                  >
                    Manage
                  </button>
                  <button
                    @click="removeBooking(b)"
                    class="w-7 h-7 rounded-full bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 hover:bg-red-100 flex items-center justify-center transition-colors"
                    title="Delete Record"
                    type="button"
                  >
                    <span class="material-symbols-outlined text-xs">delete</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Booking Edit Modal (Teleported to body) -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center p-3.5 sm:p-4 bg-black/60 backdrop-blur-sm overflow-y-auto animate-fadeIn">
        <div class="bg-surface-container-lowest dark:bg-slate-900 w-full max-w-lg rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-2xl flex flex-col max-h-[85vh] sm:max-h-[88vh] overflow-hidden my-auto">
          
          <!-- Sticky Header -->
          <div class="shrink-0 px-5 sm:px-7 py-4 border-b border-outline-variant/20 dark:border-slate-800 flex items-center justify-between bg-surface-container-lowest dark:bg-slate-900">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-secondary text-2xl">event_available</span>
              <h3 class="font-headline-sm text-base sm:text-lg font-bold text-primary-container dark:text-white">
                Manage Client Reservation
              </h3>
            </div>
            <button @click="showModal = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-on-surface dark:text-slate-300 font-bold transition-colors">
              &times;
            </button>
          </div>

          <!-- Scrollable Body with form -->
          <form id="bookingEditForm" @submit.prevent="saveBooking" class="flex-1 min-h-0 overflow-y-auto p-5 sm:p-7 space-y-4">
            <div class="bg-surface-container-low dark:bg-slate-800/80 p-3.5 rounded-2xl border border-outline-variant/20 dark:border-slate-700">
              <p class="font-label-md text-sm font-bold text-primary-container dark:text-white">{{ activeBooking.user_name }}</p>
              <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">{{ activeBooking.user_email }} &bull; {{ activeBooking.user_phone }}</p>
              <p class="font-body-sm text-xs text-secondary dark:text-sky-300 font-medium mt-1">{{ activeBooking.service_title }} &bull; Ref: {{ activeBooking.payment_reference }}</p>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Status</label>
                <select v-model="editForm.status" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white">
                  <option value="confirmed">Confirmed</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>

              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Time Slot</label>
                <input v-model="editForm.time_slot" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div class="col-span-2">
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Reschedule Session Date</label>
                <input v-model="editForm.booking_date" type="date" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Internal Coach / Practitioner Notes</label>
              <textarea v-model="editForm.coach_notes" rows="3" placeholder="Record posture alignment, reformer spring tensions, injury notes..." class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white"></textarea>
            </div>
          </form>

          <!-- Sticky Action Footer -->
          <div class="shrink-0 px-5 sm:px-7 py-3.5 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-end gap-3 bg-surface-container-lowest dark:bg-slate-900 pb-safe">
            <button @click="showModal = false" type="button" class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low transition-colors">
              Cancel
            </button>
            <button form="bookingEditForm" :disabled="submitting" type="submit" class="px-5 py-2.5 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all disabled:opacity-50">
              {{ submitting ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { getAdminBookings, updateAdminBooking, deleteAdminBooking } from '@/services/api';

const bookings = ref([]);
const search = ref('');
const statusFilter = ref('all');
const notice = ref('');
const noticeType = ref('success');
const submitting = ref(false);

const showModal = ref(false);
const activeBooking = ref({});
const editForm = reactive({
  status: 'confirmed',
  booking_date: '',
  time_slot: '',
  coach_notes: ''
});

const filteredBookings = computed(() => {
  return bookings.value.filter(b => {
    const matchStatus = statusFilter.value === 'all' || b.status === statusFilter.value;
    const q = search.value.toLowerCase().trim();
    const matchSearch = !q ||
      (b.user_name || '').toLowerCase().includes(q) ||
      (b.user_email || '').toLowerCase().includes(q) ||
      (b.user_phone || '').toLowerCase().includes(q) ||
      (b.payment_reference || '').toLowerCase().includes(q) ||
      (b.service_title || '').toLowerCase().includes(q);
    return matchStatus && matchSearch;
  });
});

function statusBadgeClass(st) {
  switch (st) {
    case 'confirmed':
      return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300';
    case 'completed':
      return 'bg-sky-100 text-sky-800 dark:bg-sky-950 dark:text-sky-300';
    case 'cancelled':
      return 'bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300';
    default:
      return 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300';
  }
}

async function loadBookings() {
  try {
    bookings.value = await getAdminBookings();
  } catch (e) {
    console.error(e);
  }
}

function openManageModal(b) {
  activeBooking.value = b;
  editForm.status = b.status || 'confirmed';
  editForm.booking_date = b.booking_date || '';
  editForm.time_slot = b.time_slot || '';
  editForm.coach_notes = b.coach_notes || '';
  showModal.value = true;
}

async function saveBooking() {
  submitting.value = true;
  try {
    await updateAdminBooking(activeBooking.value.id, editForm);
    notice.value = `Updated reservation for ${activeBooking.value.user_name}.`;
    noticeType.value = 'success';
    showModal.value = false;
    await loadBookings();
  } catch (err) {
    notice.value = err.message;
    noticeType.value = 'error';
  } finally {
    submitting.value = false;
  }
}

async function updateStatus(b, newStatus) {
  try {
    await updateAdminBooking(b.id, { status: newStatus });
    b.status = newStatus;
    notice.value = `Marked booking as ${newStatus}.`;
    noticeType.value = 'success';
  } catch (err) {
    notice.value = err.message;
    noticeType.value = 'error';
  }
}

async function removeBooking(b) {
  if (!confirm(`Permanently remove reservation record for ${b.user_name}?`)) return;
  try {
    await deleteAdminBooking(b.id);
    notice.value = 'Booking record removed.';
    noticeType.value = 'success';
    await loadBookings();
  } catch (err) {
    notice.value = err.message;
    noticeType.value = 'error';
  }
}

onMounted(() => {
  loadBookings();
});
</script>
