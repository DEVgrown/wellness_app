<template>
  <div class="bg-surface dark:bg-slate-950 text-on-surface dark:text-slate-100 flex flex-col min-h-screen transition-colors duration-200">
    <AppNavbar />

    <main class="flex-1 flex flex-col relative w-full pt-20 pb-24 md:pb-16 bg-surface dark:bg-slate-950">
      <div class="max-w-6xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6">
        <!-- Breadcrumb & Header -->
        <div class="mb-6 flex items-center justify-between">
          <div>
            <router-link to="/book" class="inline-flex items-center gap-1.5 text-secondary hover:underline font-label-sm text-sm mb-1">
              <span class="material-symbols-outlined text-sm">arrow_back</span>
              <span>Back to Schedule</span>
            </router-link>
            <h1 class="font-headline-lg text-2xl sm:text-3xl font-bold text-primary-container dark:text-white tracking-tight">
              Session Reservation &amp; Checkout
            </h1>
          </div>
          <div class="hidden sm:flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-secondary-container/30 dark:bg-sky-950/60 text-secondary font-label-sm text-sm font-semibold">
            <span class="material-symbols-outlined text-base">lock</span>
            <span>256-bit Encrypted</span>
          </div>
        </div>

        <!-- 2-Column Split Checkout Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          <!-- LEFT COLUMN: Contact & Payment Info (7 Cols) -->
          <div class="lg:col-span-7 flex flex-col gap-6">
            <!-- Attendee Details Card -->
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-sm border border-outline-variant/30 dark:border-slate-800">
              <h3 class="font-headline-sm text-lg font-bold text-primary-container dark:text-white mb-4 flex items-center gap-2">
                <span class="w-7 h-7 rounded-full bg-secondary-fixed text-primary flex items-center justify-center text-xs font-bold">1</span>
                <span>Attendee Information</span>
              </h3>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block font-label-sm text-xs text-on-surface-variant dark:text-slate-400 mb-1.5 font-semibold">Full Name</label>
                  <input 
                    v-model="attendee.name" 
                    type="text" 
                    required
                    class="w-full px-4 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white font-medium focus:outline-none focus:border-secondary"
                  />
                </div>
                <div>
                  <label class="block font-label-sm text-xs text-on-surface-variant dark:text-slate-400 mb-1.5 font-semibold">Email Address</label>
                  <input 
                    v-model="attendee.email" 
                    type="email" 
                    required
                    class="w-full px-4 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white font-medium focus:outline-none focus:border-secondary"
                  />
                </div>
              </div>

              <div class="mt-4">
                <label class="block font-label-sm text-xs text-on-surface-variant dark:text-slate-400 mb-1.5 font-semibold">Phone Number (M-Pesa prompts)</label>
                <input 
                  v-model="attendee.phone" 
                  type="tel" 
                  required
                  placeholder="+254 712 345 678"
                  class="w-full px-4 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white font-medium focus:outline-none focus:border-secondary"
                />
              </div>

              <div class="mt-4">
                <label class="block font-label-sm text-xs text-on-surface-variant dark:text-slate-400 mb-1.5 font-semibold">Personal Notes for Karina (Injuries, pregnancy, or goals)</label>
                <textarea 
                  v-model="attendee.notes" 
                  rows="2"
                  placeholder="e.g. Mild lower lumbar tension or recovering from postpartum..."
                  class="w-full px-4 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white font-medium focus:outline-none focus:border-secondary"
                ></textarea>
              </div>
            </div>

            <!-- Payment Method Selection Card -->
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-sm border border-outline-variant/30 dark:border-slate-800">
              <h3 class="font-headline-sm text-lg font-bold text-primary-container dark:text-white mb-4 flex items-center gap-2">
                <span class="w-7 h-7 rounded-full bg-secondary-fixed text-primary flex items-center justify-center text-xs font-bold">2</span>
                <span>Select Payment Method</span>
              </h3>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
                <!-- M-Pesa Option -->
                <div 
                  @click="selectedPaymentMethod = 'mpesa'"
                  class="p-4 rounded-2xl border transition-all cursor-pointer flex items-center gap-3.5"
                  :class="selectedPaymentMethod === 'mpesa' ? 'bg-secondary-container/20 dark:bg-sky-950/40 border-secondary' : 'bg-surface dark:bg-slate-800 border-outline-variant/30 dark:border-slate-700'"
                >
                  <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center"
                    :class="selectedPaymentMethod === 'mpesa' ? 'border-secondary bg-secondary text-white' : 'border-outline-variant'"
                  >
                    <span v-if="selectedPaymentMethod === 'mpesa'" class="w-2 h-2 rounded-full bg-white"></span>
                  </div>
                  <div>
                    <span class="font-label-md text-sm font-bold text-primary-container dark:text-white block">Safaricom M-Pesa</span>
                    <span class="text-xs text-on-surface-variant dark:text-slate-400">Instant STK Push on phone</span>
                  </div>
                </div>

                <!-- Card Option -->
                <div 
                  @click="selectedPaymentMethod = 'card'"
                  class="p-4 rounded-2xl border transition-all cursor-pointer flex items-center gap-3.5"
                  :class="selectedPaymentMethod === 'card' ? 'bg-secondary-container/20 dark:bg-sky-950/40 border-secondary' : 'bg-surface dark:bg-slate-800 border-outline-variant/30 dark:border-slate-700'"
                >
                  <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center"
                    :class="selectedPaymentMethod === 'card' ? 'border-secondary bg-secondary text-white' : 'border-outline-variant'"
                  >
                    <span v-if="selectedPaymentMethod === 'card'" class="w-2 h-2 rounded-full bg-white"></span>
                  </div>
                  <div>
                    <span class="font-label-md text-sm font-bold text-primary-container dark:text-white block">Credit / Debit Card</span>
                    <span class="text-xs text-on-surface-variant dark:text-slate-400">Visa, Mastercard</span>
                  </div>
                </div>

                <!-- Digital Pay Option -->
                <div 
                  @click="selectedPaymentMethod = 'digital'"
                  class="p-4 rounded-2xl border transition-all cursor-pointer flex items-center gap-3.5"
                  :class="selectedPaymentMethod === 'digital' ? 'bg-secondary-container/20 dark:bg-sky-950/40 border-secondary' : 'bg-surface dark:bg-slate-800 border-outline-variant/30 dark:border-slate-700'"
                >
                  <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center"
                    :class="selectedPaymentMethod === 'digital' ? 'border-secondary bg-secondary text-white' : 'border-outline-variant'"
                  >
                    <span v-if="selectedPaymentMethod === 'digital'" class="w-2 h-2 rounded-full bg-white"></span>
                  </div>
                  <div>
                    <span class="font-label-md text-sm font-bold text-primary-container dark:text-white block">Apple Pay / Google Pay</span>
                    <span class="text-xs text-on-surface-variant dark:text-slate-400">One-tap mobile checkout</span>
                  </div>
                </div>

                <!-- Studio Desk Option -->
                <div 
                  @click="selectedPaymentMethod = 'studio'"
                  class="p-4 rounded-2xl border transition-all cursor-pointer flex items-center gap-3.5"
                  :class="selectedPaymentMethod === 'studio' ? 'bg-secondary-container/20 dark:bg-sky-950/40 border-secondary' : 'bg-surface dark:bg-slate-800 border-outline-variant/30 dark:border-slate-700'"
                >
                  <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center"
                    :class="selectedPaymentMethod === 'studio' ? 'border-secondary bg-secondary text-white' : 'border-outline-variant'"
                  >
                    <span v-if="selectedPaymentMethod === 'studio'" class="w-2 h-2 rounded-full bg-white"></span>
                  </div>
                  <div>
                    <span class="font-label-md text-sm font-bold text-primary-container dark:text-white block">Pay at Studio</span>
                    <span class="text-xs text-on-surface-variant dark:text-slate-400">Cash or card upon arrival</span>
                  </div>
                </div>
              </div>

              <!-- M-Pesa STK Prompt Notice -->
              <div v-if="selectedPaymentMethod === 'mpesa'" class="p-4 rounded-2xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/50 flex items-start gap-3">
                <span class="material-symbols-outlined text-emerald-600 dark:text-emerald-400 text-xl mt-0.5">phone_iphone</span>
                <p class="font-body-sm text-xs text-emerald-800 dark:text-emerald-200 leading-relaxed">
                  Upon clicking <strong>Complete Reservation</strong>, an M-Pesa STK push prompt will appear on <strong>{{ attendee.phone }}</strong>. Enter your PIN to verify your reservation instantly.
                </p>
              </div>
            </div>
          </div>

          <!-- RIGHT COLUMN: Order Summary (5 Cols) -->
          <div class="lg:col-span-5 sticky top-28">
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-xl border border-outline-variant/30 dark:border-slate-800">
              <h3 class="font-headline-sm text-lg font-bold text-primary-container dark:text-white mb-4">
                Order Summary
              </h3>

              <div class="flex items-center gap-3.5 mb-6 pb-6 border-b border-outline-variant/20 dark:border-slate-800">
                <div class="w-14 h-14 rounded-2xl bg-secondary-fixed flex items-center justify-center text-primary shrink-0 shadow-xs font-bold text-xl">
                  🧘
                </div>
                <div>
                  <h4 class="font-headline-sm text-base font-bold text-primary-container dark:text-white">
                    {{ draft.serviceTitle || '1:1 Pilates Reformer & Alignment' }}
                  </h4>
                  <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 mt-0.5">
                    {{ draft.dateDisplay || draft.date }} • {{ draft.timeSlot }}
                  </p>
                  <p class="font-body-sm text-xs text-secondary font-medium">
                    Karen Studio Sanctuary, Nairobi
                  </p>
                </div>
              </div>

              <!-- Itemized pricing -->
              <div class="space-y-3 mb-6 text-sm">
                <div class="flex items-center justify-between text-on-surface-variant dark:text-slate-400">
                  <span>Session Fee</span>
                  <span class="font-semibold text-on-surface dark:text-white">{{ formattedBasePrice }}</span>
                </div>
                <div v-if="draft.isPackApplied" class="flex items-center justify-between text-emerald-600 dark:text-emerald-400 font-medium">
                  <span>5-Session Pack Discount (15%)</span>
                  <span>-15% Applied</span>
                </div>
                <div class="flex items-center justify-between text-on-surface-variant dark:text-slate-400">
                  <span>Studio Amenities &amp; Mat</span>
                  <span class="font-semibold text-emerald-600 dark:text-emerald-400">FREE</span>
                </div>
                <div class="pt-3 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-between font-bold text-lg text-primary-container dark:text-white">
                  <span>Total Amount</span>
                  <span class="text-2xl">{{ formattedTotal }}</span>
                </div>
              </div>

              <!-- Complete Payment Button -->
              <button 
                @click="handlePaymentSubmit" 
                :disabled="isProcessing"
                class="w-full py-4 rounded-full bg-primary-container hover:bg-primary text-on-primary font-label-md text-label-md font-semibold shadow-md active:scale-[0.98] transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                type="button"
              >
                <span v-if="isProcessing" class="material-symbols-outlined animate-spin text-lg">progress_activity</span>
                <span>{{ isProcessing ? 'Processing M-Pesa STK...' : 'Complete Reservation' }}</span>
              </button>

              <div class="mt-4 pt-4 border-t border-outline-variant/20 dark:border-slate-800 text-center">
                <span class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400 flex items-center justify-center gap-1">
                  <span class="material-symbols-outlined text-sm text-secondary">verified_user</span>
                  <span>24-Hour Free Cancellation &amp; Rescheduling</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Payment Success / STK Push Simulation Modal -->
    <div v-if="showSuccessModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fadeIn">
      <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl border border-outline-variant/30 dark:border-slate-800 text-center">
        <div class="w-16 h-16 rounded-full bg-emerald-100 dark:bg-emerald-950 flex items-center justify-center text-emerald-600 dark:text-emerald-400 mx-auto mb-4">
          <span class="material-symbols-outlined text-3xl">celebration</span>
        </div>
        <h3 class="font-headline-lg text-2xl font-bold text-primary-container dark:text-white mb-2">
          Reservation Confirmed!
        </h3>
        <p class="font-body-md text-sm text-on-surface-variant dark:text-slate-300 mb-6 leading-relaxed">
          Your session with Karina has been reserved for <strong class="text-primary-container dark:text-white">{{ draft.dateDisplay || draft.date }} at {{ draft.timeSlot }}</strong>. A confirmation SMS &amp; email have been dispatched.
        </p>
        <button 
          @click="finishCheckout"
          class="w-full py-3.5 rounded-full bg-primary-container text-on-primary font-label-md text-sm font-semibold shadow-md active:scale-95 transition-all"
        >
          View My Bookings &amp; Passes
        </button>
      </div>
    </div>

    <AppBottomNav />
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import AppNavbar from '@/components/AppNavbar.vue';
import AppBottomNav from '@/components/AppBottomNav.vue';
import { useBookingStore } from '@/stores/bookingStore';
import { useAuthStore } from '@/stores/authStore';
import { createBooking, initiateMpesaStkPush } from '@/services/api';

const router = useRouter();
const bookingStore = useBookingStore();
const authStore = useAuthStore();

const draft = computed(() => bookingStore.draft.value);
const currency = computed(() => bookingStore.currency.value);

const selectedPaymentMethod = ref('mpesa');
const isProcessing = ref(false);
const showSuccessModal = ref(false);

const attendee = reactive({
  name: authStore.user.value.name || 'Sarah W.',
  email: authStore.user.value.email || 'sarah@example.com',
  phone: authStore.user.value.phone || '+254 712 345 678',
  notes: ''
});

const formattedBasePrice = computed(() => {
  const price = currency.value === 'KES' ? draft.value.basePriceKes : draft.value.basePriceEur;
  return currency.value === 'KES' ? `KES ${(price || 6500).toLocaleString()}` : `€${price || 75}`;
});

const formattedTotal = computed(() => {
  const total = bookingStore.currentPrice.value;
  return currency.value === 'KES' ? `KES ${(total || 6500).toLocaleString()}` : `€${total || 75}`;
});

async function handlePaymentSubmit() {
  isProcessing.value = true;
  try {
    const bookingPayload = {
      service_id: draft.value.serviceId,
      service_title: draft.value.serviceTitle || '1:1 Pilates Reformer',
      user_name: attendee.name,
      user_email: attendee.email,
      user_phone: attendee.phone,
      booking_date: draft.value.date || new Date().toISOString().split('T')[0],
      time_slot: draft.value.timeSlot || '09:30 AM',
      location_name: 'Karen Studio, Nairobi',
      payment_method: selectedPaymentMethod.value,
      currency: currency.value,
      total_amount: bookingStore.currentPrice.value,
      notes: attendee.notes
    };

    const bookingRes = await createBooking(bookingPayload);

    if (selectedPaymentMethod.value === 'mpesa') {
      await initiateMpesaStkPush(attendee.phone, bookingStore.currentPrice.value, bookingRes.id);
    }

    showSuccessModal.value = true;
    bookingStore.showToast('Session reserved successfully! 🌿', 'success');
  } catch (err) {
    bookingStore.showToast(err.message || 'Payment initiation failed', 'error');
  } finally {
    isProcessing.value = false;
  }
}

function finishCheckout() {
  showSuccessModal.value = false;
  router.push('/bookings');
}
</script>
