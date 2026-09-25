<template>
  <div class="bg-surface dark:bg-slate-950 text-on-surface dark:text-slate-100 flex flex-col min-h-screen transition-colors duration-200">
    <AppNavbar />

    <main class="flex-1 flex flex-col relative w-full pt-20 pb-24 md:pb-16 bg-surface dark:bg-slate-950">
      <div class="max-w-6xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6">
        <!-- Client Dashboard Header -->
        <section class="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 class="font-headline-lg text-2xl sm:text-3xl font-bold text-primary-container dark:text-white tracking-tight">
              My Passes &amp; Sessions
            </h1>
            <p class="font-body-md text-sm text-on-surface-variant dark:text-slate-400 mt-0.5">
              Manage your private reservations, schedule history, and studio package credits.
            </p>
          </div>

          <div class="flex items-center gap-3">
            <router-link 
              to="/book" 
              class="inline-flex items-center gap-2 bg-primary-container hover:bg-primary text-on-primary font-label-md text-sm font-semibold px-5 py-2.5 rounded-full shadow-sm active:scale-95 transition-all"
            >
              <span class="material-symbols-outlined text-base">calendar_add_on</span>
              <span>Book New Session</span>
            </router-link>
          </div>
        </section>

        <!-- Top Metrics Ribbon -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          <div class="bg-surface-container-lowest dark:bg-slate-900 p-4 rounded-2xl border border-outline-variant/30 dark:border-slate-800 shadow-xs flex items-center gap-3.5">
            <div class="w-10 h-10 rounded-xl bg-secondary-fixed text-primary flex items-center justify-center font-bold">
              <span class="material-symbols-outlined text-xl">confirmation_number</span>
            </div>
            <div>
              <span class="font-headline-sm text-xl font-bold text-primary-container dark:text-white block">
                {{ totalRemainingCredits }} Left
              </span>
              <span class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400">Pass Credits</span>
            </div>
          </div>

          <div class="bg-surface-container-lowest dark:bg-slate-900 p-4 rounded-2xl border border-outline-variant/30 dark:border-slate-800 shadow-xs flex items-center gap-3.5">
            <div class="w-10 h-10 rounded-xl bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 flex items-center justify-center font-bold">
              <span class="material-symbols-outlined text-xl">event_available</span>
            </div>
            <div>
              <span class="font-headline-sm text-xl font-bold text-primary-container dark:text-white block">{{ upcomingCount }}</span>
              <span class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400">Upcoming</span>
            </div>
          </div>

          <div class="bg-surface-container-lowest dark:bg-slate-900 p-4 rounded-2xl border border-outline-variant/30 dark:border-slate-800 shadow-xs flex items-center gap-3.5">
            <div class="w-10 h-10 rounded-xl bg-surface-container-high dark:bg-slate-800 text-on-surface-variant dark:text-slate-300 flex items-center justify-center font-bold">
              <span class="material-symbols-outlined text-xl">task_alt</span>
            </div>
            <div>
              <span class="font-headline-sm text-xl font-bold text-primary-container dark:text-white block">{{ pastCount }}</span>
              <span class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400">Completed</span>
            </div>
          </div>

          <div class="bg-surface-container-lowest dark:bg-slate-900 p-4 rounded-2xl border border-outline-variant/30 dark:border-slate-800 shadow-xs flex items-center gap-3.5">
            <div class="w-10 h-10 rounded-xl bg-secondary-container/40 dark:bg-sky-950/60 text-secondary dark:text-sky-300 flex items-center justify-center font-bold">
              <span class="material-symbols-outlined text-xl">schedule</span>
            </div>
            <div>
              <span class="font-headline-sm text-sm sm:text-base font-bold text-primary-container dark:text-white block truncate">
                {{ nextSessionDisplay }}
              </span>
              <span class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400">Next Reserved</span>
            </div>
          </div>
        </div>

        <!-- 2-Column Responsive Dashboard Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          <!-- LEFT COLUMN: Bookings List & Tabs (8 Cols) -->
          <div class="lg:col-span-8 flex flex-col gap-6">
            <!-- Filter Tabs -->
            <div class="flex items-center gap-2 p-1 bg-surface-container-low dark:bg-slate-800 rounded-full max-w-md">
              <button 
                @click="activeTab = 'upcoming'" 
                :class="activeTab === 'upcoming' ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-semibold shadow-xs' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
                class="flex-1 py-1.5 px-3 rounded-full font-label-sm text-xs transition-all"
                type="button"
              >
                Upcoming ({{ upcomingCount }})
              </button>
              <button 
                @click="activeTab = 'completed'" 
                :class="activeTab === 'completed' ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-semibold shadow-xs' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
                class="flex-1 py-1.5 px-3 rounded-full font-label-sm text-xs transition-all"
                type="button"
              >
                Past ({{ pastCount }})
              </button>
              <button 
                @click="activeTab = 'cancelled'" 
                :class="activeTab === 'cancelled' ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-semibold shadow-xs' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
                class="flex-1 py-1.5 px-3 rounded-full font-label-sm text-xs transition-all"
                type="button"
              >
                Cancelled ({{ cancelledCount }})
              </button>
            </div>

            <!-- Booking Cards List -->
            <div class="space-y-4">
              <div 
                v-for="booking in displayedBookings" 
                :key="booking.id"
                class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 shadow-sm border border-outline-variant/30 dark:border-slate-800 transition-all hover:shadow-md"
              >
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                  <div class="flex items-center gap-3">
                    <div class="w-12 h-12 rounded-2xl bg-secondary-fixed text-primary flex items-center justify-center font-bold text-lg shrink-0">
                      🧘
                    </div>
                    <div>
                      <div class="flex items-center gap-2 flex-wrap">
                        <h3 class="font-headline-sm text-lg font-bold text-primary-container dark:text-white">
                          {{ booking.service_title }}
                        </h3>
                        <span 
                          v-if="booking.payment_method === 'pass'"
                          class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-secondary-fixed/50 text-primary font-label-sm text-[10px] font-bold"
                        >
                          <span class="material-symbols-outlined text-[12px]">confirmation_number</span> Studio Pass
                        </span>
                      </div>
                      <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 mt-0.5">
                        {{ formatDate(booking.booking_date) }} at {{ booking.time_slot }} • {{ booking.location_name }}
                      </p>
                    </div>
                  </div>

                  <span 
                    :class="{
                      'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300': booking.status === 'confirmed',
                      'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300': booking.status === 'completed',
                      'bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300': booking.status === 'cancelled',
                      'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300': booking.status === 'pending_payment'
                    }"
                    class="px-3 py-1 rounded-full font-label-sm text-xs font-semibold capitalize self-start sm:self-auto"
                  >
                    {{ booking.status === 'pending_payment' ? 'Pending Payment' : booking.status }}
                  </span>
                </div>

                <!-- Session Details / Notes -->
                <p v-if="booking.coach_notes || booking.notes" class="text-xs text-on-surface-variant dark:text-slate-300 bg-surface dark:bg-slate-800/60 p-3 rounded-2xl mb-4 border border-outline-variant/20 dark:border-slate-700">
                  <span class="font-semibold text-primary-container dark:text-white">Note:</span> {{ booking.coach_notes || booking.notes }}
                </p>

                <!-- Actions for Upcoming -->
                <div v-if="booking.status === 'confirmed'" class="flex flex-wrap items-center gap-2.5 pt-3 border-t border-outline-variant/20 dark:border-slate-800">
                  <button 
                    @click="openRescheduleModal(booking)"
                    class="px-4 py-2 rounded-full bg-surface-container-low dark:bg-slate-800 text-on-surface dark:text-slate-200 hover:text-primary-container font-label-sm text-xs font-semibold border border-outline-variant/30 dark:border-slate-700"
                    type="button"
                  >
                    Reschedule
                  </button>
                  <button 
                    @click="handleCancel(booking.id)"
                    class="px-4 py-2 rounded-full text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 font-label-sm text-xs font-semibold"
                    type="button"
                  >
                    Cancel Session
                  </button>
                  <a 
                    href="https://wa.me/254712345678" 
                    target="_blank"
                    class="ml-auto text-xs text-secondary hover:underline flex items-center gap-1 font-semibold"
                  >
                    <span class="material-symbols-outlined text-sm">chat</span>
                    <span>Chat on WhatsApp</span>
                  </a>
                </div>
              </div>

              <!-- Empty state -->
              <div v-if="displayedBookings.length === 0" class="text-center py-12 bg-surface-container-lowest dark:bg-slate-900 rounded-3xl border border-outline-variant/30 dark:border-slate-800">
                <span class="material-symbols-outlined text-4xl text-on-surface-variant mb-2">event_busy</span>
                <p class="font-body-md text-sm text-on-surface-variant dark:text-slate-400">
                  No {{ activeTab }} sessions found.
                </p>
                <router-link to="/book" class="inline-block mt-4 text-xs font-semibold text-secondary hover:underline">
                  Browse schedule &amp; reserve a slot →
                </router-link>
              </div>
            </div>
          </div>

          <!-- RIGHT COLUMN: Real User Passes & Studio Guidelines (4 Cols) -->
          <div class="lg:col-span-4 flex flex-col gap-6 sticky top-28">
            <!-- Studio Passes Container -->
            <div class="space-y-4">
              <div class="flex items-center justify-between px-1">
                <h2 class="font-headline-sm text-base font-bold text-primary-container dark:text-white flex items-center gap-2">
                  <span class="material-symbols-outlined text-secondary text-lg">confirmation_number</span>
                  <span>My Studio Passes</span>
                </h2>
                <router-link 
                  to="/services" 
                  class="font-label-sm text-xs font-semibold text-secondary hover:underline"
                >
                  + Add Pass
                </router-link>
              </div>

              <!-- Render Live User Packages -->
              <div 
                v-for="pkg in packages" 
                :key="pkg.id"
                class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 shadow-sm border border-outline-variant/30 dark:border-slate-800"
              >
                <div class="flex items-center justify-between gap-2 mb-1.5">
                  <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-wider block">Pass Status</span>
                  <span 
                    :class="{
                      'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800': pkg.status === 'active',
                      'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border-slate-200 dark:border-slate-700': pkg.status === 'fully_used',
                      'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border-amber-200 dark:border-amber-800': pkg.status === 'expired'
                    }"
                    class="px-2.5 py-0.5 rounded-full font-label-sm text-[11px] font-bold border capitalize"
                  >
                    {{ pkg.status === 'fully_used' ? 'Fully Used' : pkg.status }}
                  </span>
                </div>

                <h3 class="font-headline-sm text-base font-bold text-primary-container dark:text-white mb-1">
                  {{ pkg.package_name }}
                </h3>
                <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 mb-4">
                  {{ pkg.remaining_sessions }} of {{ pkg.total_sessions }} sessions remaining
                </p>

                <!-- Interactive Session Tokens Progress Grid -->
                <div 
                  class="grid gap-1.5 mb-4" 
                  :style="{ gridTemplateColumns: `repeat(${Math.min(pkg.total_sessions, 6)}, minmax(0, 1fr))` }"
                >
                  <div 
                    v-for="i in Math.min(pkg.total_sessions, 12)" 
                    :key="i"
                    :class="[
                      i <= pkg.used_sessions 
                        ? 'bg-primary-container text-white' 
                        : (i === pkg.used_sessions + 1 && pkg.remaining_sessions > 0)
                          ? 'bg-secondary text-white ring-2 ring-secondary/40' 
                          : 'bg-surface-container dark:bg-slate-800 text-on-surface-variant dark:text-slate-400'
                    ]"
                    class="h-8 rounded-lg flex items-center justify-center font-bold text-xs transition-all shadow-2xs"
                    :title="i <= pkg.used_sessions ? `Session ${i} (Used)` : `Session ${i} (Available)`"
                  >
                    {{ i <= pkg.used_sessions ? '✓' : i }}
                  </div>
                </div>

                <!-- Session Stats & Validity Date -->
                <div class="flex items-center justify-between text-xs text-on-surface-variant dark:text-slate-400 mb-4 pt-2 border-t border-outline-variant/10 dark:border-slate-800">
                  <span class="flex items-center gap-1">
                    <span class="material-symbols-outlined text-xs text-secondary">verified</span>
                    <span>Used: {{ pkg.used_sessions }} / {{ pkg.total_sessions }}</span>
                  </span>
                  <span class="font-medium">
                    {{ pkg.valid_until ? `Valid until ${formatDate(pkg.valid_until)}` : 'No Expiry' }}
                  </span>
                </div>

                <!-- Action Button -->
                <router-link 
                  v-if="pkg.remaining_sessions > 0"
                  to="/book" 
                  class="w-full py-2.5 rounded-full bg-primary-container hover:bg-primary text-on-primary font-label-md text-xs font-semibold shadow-xs transition-all flex items-center justify-center gap-1.5"
                >
                  <span class="material-symbols-outlined text-sm">event</span>
                  <span>Book with Pass</span>
                </router-link>
                <router-link 
                  v-else
                  to="/services" 
                  class="w-full py-2.5 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container text-primary-container dark:text-white font-label-md text-xs font-semibold shadow-xs transition-all flex items-center justify-center gap-1.5 border border-outline-variant/30 dark:border-slate-700"
                >
                  <span class="material-symbols-outlined text-sm">refresh</span>
                  <span>Renew / Purchase Pass</span>
                </router-link>
              </div>

              <!-- Fallback if no packages exist -->
              <div 
                v-if="packages.length === 0" 
                class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 shadow-sm border border-outline-variant/30 dark:border-slate-800 text-center"
              >
                <div class="w-12 h-12 rounded-full bg-secondary-fixed text-primary flex items-center justify-center mx-auto mb-3">
                  <span class="material-symbols-outlined text-2xl">confirmation_number</span>
                </div>
                <h3 class="font-headline-sm text-sm font-bold text-primary-container dark:text-white mb-1">
                  No Active Studio Passes
                </h3>
                <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 mb-4">
                  Purchase a session bundle for preferential rates and priority booking at our Karen sanctuary.
                </p>
                <router-link 
                  to="/services" 
                  class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-semibold transition-all"
                >
                  <span>Explore Passes</span>
                  <span class="material-symbols-outlined text-xs">arrow_forward</span>
                </router-link>
              </div>
            </div>

            <!-- Studio Sanctuary Quick Info -->
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 shadow-sm border border-outline-variant/30 dark:border-slate-800 text-xs text-on-surface-variant dark:text-slate-400 space-y-3">
              <h4 class="font-label-md text-sm font-semibold text-primary-container dark:text-white flex items-center gap-2">
                <span class="material-symbols-outlined text-secondary text-base">info</span>
                <span>Studio Guidelines</span>
              </h4>
              <p>• <strong>Arrival:</strong> Please arrive 5–10 minutes before your slot to settle in calmly.</p>
              <p>• <strong>Attire:</strong> Form-fitting movement wear and grip socks are recommended for Reformer stability.</p>
              <p>• <strong>Cancellation:</strong> 24h notice required for complimentary rescheduling. Your pass session will be instantly restored.</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Reschedule Modal (Teleported to body for guaranteed viewport centering) -->
    <Teleport to="body">
      <div v-if="rescheduleModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-3.5 sm:p-4 bg-black/60 backdrop-blur-sm overflow-y-auto animate-fadeIn">
        <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-7 max-w-md w-full shadow-2xl border border-outline-variant/30 dark:border-slate-800 flex flex-col my-auto">
          <!-- Header -->
          <div class="flex items-center justify-between pb-3 mb-4 border-b border-outline-variant/20 dark:border-slate-800">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-full bg-secondary-container/40 dark:bg-sky-950 text-secondary dark:text-sky-300 flex items-center justify-center">
                <span class="material-symbols-outlined text-lg">schedule</span>
              </div>
              <h3 class="font-headline-sm text-base sm:text-lg font-bold text-primary-container dark:text-white">
                Reschedule Session
              </h3>
            </div>
            <button @click="rescheduleModalOpen = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-on-surface dark:text-slate-300 font-bold transition-colors">
              &times;
            </button>
          </div>

          <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 mb-4">
            Select a new date and time for <strong class="text-primary-container dark:text-white font-semibold">{{ activeBooking?.service_title }}</strong>.
          </p>

          <form @submit.prevent="submitReschedule" class="space-y-4">
            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">New Date *</label>
              <input 
                v-model="newDate" 
                type="date" 
                required
                class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs text-on-surface dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-container/20"
              />
            </div>
            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">New Time Slot *</label>
              <select 
                v-model="newSlot" 
                required
                class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs text-on-surface dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-container/20"
              >
                <option value="08:00 AM">08:00 AM (Morning Calm)</option>
                <option value="09:30 AM">09:30 AM (Morning Prime)</option>
                <option value="11:00 AM">11:00 AM (Midday Focus)</option>
                <option value="02:00 PM">02:00 PM (Afternoon Alignment)</option>
                <option value="04:30 PM">04:30 PM (Evening Sunset)</option>
              </select>
            </div>

            <div class="pt-3 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-end gap-2.5">
              <button 
                @click="rescheduleModalOpen = false" 
                type="button"
                class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low transition-colors"
              >
                Cancel
              </button>
              <button 
                type="submit"
                class="px-5 py-2.5 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all"
              >
                Confirm Reschedule
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <AppBottomNav />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import AppNavbar from '@/components/AppNavbar.vue';
import AppBottomNav from '@/components/AppBottomNav.vue';
import { useBookingStore } from '@/stores/bookingStore';
import { useAuthStore } from '@/stores/authStore';
import { getBookings, getUserPackages, cancelBooking, rescheduleBooking } from '@/services/api';

const bookingStore = useBookingStore();
const authStore = useAuthStore();

const activeTab = ref('upcoming');
const bookings = ref([]);
const packages = ref([]);
const loading = ref(false);

const rescheduleModalOpen = ref(false);
const activeBooking = ref(null);
const newDate = ref(new Date().toISOString().split('T')[0]);
const newSlot = ref('09:30 AM');

onMounted(async () => {
  await loadData();
});

async function loadData() {
  loading.value = true;
  try {
    const userName = authStore.user.value?.name || authStore.user.value?.username || '';
    const [bookingList, packageList] = await Promise.all([
      getBookings(userName, 'all', true),
      getUserPackages(userName)
    ]);
    bookings.value = Array.isArray(bookingList) ? bookingList : [];
    packages.value = Array.isArray(packageList) ? packageList : [];
  } catch (e) {
    console.warn('Could not load bookings and passes:', e);
  } finally {
    loading.value = false;
  }
}

// Pass Credits Calculation
const totalRemainingCredits = computed(() => {
  return packages.value.reduce((sum, p) => sum + (p.remaining_sessions || 0), 0);
});

// Counts
const upcomingCount = computed(() => bookings.value.filter(b => b.status === 'confirmed').length);
const pastCount = computed(() => bookings.value.filter(b => b.status === 'completed').length);
const cancelledCount = computed(() => bookings.value.filter(b => b.status === 'cancelled').length);

const displayedBookings = computed(() => {
  if (activeTab.value === 'upcoming') {
    return bookings.value.filter(b => b.status === 'confirmed' || b.status === 'pending_payment');
  }
  return bookings.value.filter(b => b.status === activeTab.value);
});

// Next Reserved Session Display
const nextSessionDisplay = computed(() => {
  const confirmed = bookings.value
    .filter(b => b.status === 'confirmed')
    .sort((a, b) => new Date(`${a.booking_date}T${a.time_slot}`) - new Date(`${b.booking_date}T${b.time_slot}`));
  
  if (confirmed.length === 0) return 'None';
  const b = confirmed[0];
  return `${b.time_slot}`;
});

function formatDate(dateString) {
  if (!dateString) return '';
  try {
    const d = new Date(dateString);
    return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
  } catch {
    return dateString;
  }
}

function openRescheduleModal(booking) {
  activeBooking.value = booking;
  newDate.value = booking.booking_date;
  newSlot.value = booking.time_slot;
  rescheduleModalOpen.value = true;
}

async function submitReschedule() {
  if (!activeBooking.value) return;
  try {
    await rescheduleBooking(activeBooking.value.id, newDate.value, newSlot.value);
    rescheduleModalOpen.value = false;
    bookingStore.showToast('Session rescheduled successfully! 🌿', 'success');
    await loadData();
  } catch (e) {
    bookingStore.showToast(e.message || 'Reschedule failed', 'error');
  }
}

async function handleCancel(bookingId) {
  if (!confirm('Are you sure you want to cancel this session? Any pass session used will be restored.')) return;
  try {
    await cancelBooking(bookingId);
    bookingStore.showToast('Session cancelled. Pass credit restored.', 'info');
    await loadData();
  } catch (e) {
    bookingStore.showToast(e.message || 'Cancellation failed', 'error');
  }
}
</script>
