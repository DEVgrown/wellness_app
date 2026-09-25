<template>
  <div class="bg-surface dark:bg-slate-950 text-on-surface dark:text-slate-100 flex flex-col min-h-screen transition-colors duration-200">
    <AppNavbar />

    <main class="flex-1 flex flex-col relative w-full pt-20 pb-24 md:pb-16 bg-surface dark:bg-slate-950">
      <div class="max-w-6xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6">
        <!-- Progress Stepper -->
        <div class="mb-8">
          <div class="flex items-center justify-between max-w-xl mx-auto gap-4">
            <div class="flex items-center gap-2">
              <span class="w-8 h-8 rounded-full bg-primary-container text-white flex items-center justify-center font-bold text-sm shadow-xs">1</span>
              <span class="font-label-md text-sm font-semibold text-primary-container dark:text-white">Select Service</span>
            </div>
            <div class="h-0.5 flex-1 bg-primary-container"></div>
            <div class="flex items-center gap-2">
              <span class="w-8 h-8 rounded-full bg-primary-container text-white flex items-center justify-center font-bold text-sm shadow-xs">2</span>
              <span class="font-label-md text-sm font-semibold text-primary-container dark:text-white">Choose Slot</span>
            </div>
            <div class="h-0.5 flex-1 bg-outline-variant/40 dark:bg-slate-700"></div>
            <div class="flex items-center gap-2">
              <span class="w-8 h-8 rounded-full bg-surface-container-high dark:bg-slate-800 text-on-surface-variant dark:text-slate-400 flex items-center justify-center font-bold text-sm">3</span>
              <span class="font-label-md text-sm text-on-surface-variant dark:text-slate-400">Checkout</span>
            </div>
          </div>
        </div>

        <!-- 2-Column Split Desktop Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          <!-- LEFT COLUMN: Date & Time Picker (7 Cols) -->
          <div class="lg:col-span-7 flex flex-col gap-6">
            <!-- Calendar Date Picker Card -->
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-sm border border-outline-variant/30 dark:border-slate-800">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-wider block">Step 1</span>
                  <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">Select Date</h3>
                </div>
                <div class="flex items-center gap-1.5 text-secondary font-label-sm text-sm">
                  <span class="material-symbols-outlined text-base">calendar_month</span>
                  <span>Upcoming 14 Days</span>
                </div>
              </div>

              <!-- Date Picker Input -->
              <input 
                v-model="selectedDate" 
                type="date" 
                class="w-full px-4 py-3 rounded-2xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white font-medium focus:outline-none focus:border-secondary transition-colors mb-4"
              />

              <!-- Quick Next Days Pill Scroller -->
              <div class="grid grid-cols-4 sm:grid-cols-7 gap-2">
                <button 
                  v-for="day in quickDays" 
                  :key="day.dateStr"
                  @click="selectedDate = day.dateStr"
                  type="button"
                  :class="selectedDate === day.dateStr ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-bold shadow-sm' : 'bg-surface dark:bg-slate-800 text-on-surface dark:text-slate-300 hover:border-secondary border border-outline-variant/20 dark:border-slate-700'"
                  class="p-2.5 rounded-2xl flex flex-col items-center justify-center transition-all"
                >
                  <span class="font-eyebrow text-[10px] uppercase">{{ day.dayName }}</span>
                  <span class="font-headline-sm text-base mt-0.5">{{ day.dayNum }}</span>
                </button>
              </div>
            </div>

            <!-- Time Slots Matrix Card -->
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-sm border border-outline-variant/30 dark:border-slate-800">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-wider block">Step 2</span>
                  <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">Choose Time Slot</h3>
                </div>
                <span class="font-label-sm text-xs text-secondary font-semibold">East Africa Time (EAT)</span>
              </div>

              <!-- Time Slot Categories -->
              <div class="space-y-6">
                <!-- Morning Slots -->
                <div>
                  <h4 class="font-label-sm text-xs uppercase tracking-wider text-on-surface-variant dark:text-slate-400 font-bold mb-3 flex items-center gap-1.5">
                    <span class="material-symbols-outlined text-sm text-secondary">wb_sunny</span>
                    Morning Calm (07:30 – 11:30 AM)
                  </h4>
                  <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
                    <button 
                      v-for="slot in morningSlots" 
                      :key="slot.time"
                      @click="selectedTimeSlot = slot.time"
                      type="button"
                      :class="selectedTimeSlot === slot.time ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-bold shadow-sm' : 'bg-surface dark:bg-slate-800 text-on-surface dark:text-slate-200 border border-outline-variant/30 dark:border-slate-700 hover:border-secondary'"
                      class="py-3 px-3.5 rounded-2xl flex flex-col items-center justify-center transition-all"
                    >
                      <span class="font-label-md text-sm font-semibold">{{ slot.time }}</span>
                      <span class="text-[10px] opacity-80 mt-0.5">{{ slot.spots }} spots left</span>
                    </button>
                  </div>
                </div>

                <!-- Afternoon Slots -->
                <div>
                  <h4 class="font-label-sm text-xs uppercase tracking-wider text-on-surface-variant dark:text-slate-400 font-bold mb-3 flex items-center gap-1.5">
                    <span class="material-symbols-outlined text-sm text-secondary">wb_twilight</span>
                    Afternoon Focus (01:00 – 05:00 PM)
                  </h4>
                  <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
                    <button 
                      v-for="slot in afternoonSlots" 
                      :key="slot.time"
                      @click="selectedTimeSlot = slot.time"
                      type="button"
                      :class="selectedTimeSlot === slot.time ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-bold shadow-sm' : 'bg-surface dark:bg-slate-800 text-on-surface dark:text-slate-200 border border-outline-variant/30 dark:border-slate-700 hover:border-secondary'"
                      class="py-3 px-3.5 rounded-2xl flex flex-col items-center justify-center transition-all"
                    >
                      <span class="font-label-md text-sm font-semibold">{{ slot.time }}</span>
                      <span class="text-[10px] opacity-80 mt-0.5">{{ slot.spots }} spots left</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- RIGHT COLUMN: Sticky Session Summary & Checkout CTA (5 Cols) -->
          <div class="lg:col-span-5 sticky top-28">
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-xl border border-outline-variant/30 dark:border-slate-800">
              <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-widest block mb-2">Reservation Summary</span>
              
              <div class="flex items-center gap-3.5 mb-6 pb-6 border-b border-outline-variant/20 dark:border-slate-800">
                <img 
                  :src="activeService.image_url" 
                  alt="Service" 
                  class="w-16 h-16 rounded-2xl object-cover shadow-sm shrink-0" 
                />
                <div>
                  <h3 class="font-headline-sm text-lg font-bold text-primary-container dark:text-white leading-tight">
                    {{ activeService.title }}
                  </h3>
                  <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 mt-0.5">
                    Lead Coach Karina • 60 mins • Karen Studio
                  </p>
                </div>
              </div>

              <!-- Selected Time pill -->
              <div class="bg-surface-container-low dark:bg-slate-800 p-4 rounded-2xl mb-6">
                <div class="flex items-center gap-2.5 text-primary-container dark:text-white font-semibold text-sm">
                  <span class="material-symbols-outlined text-secondary text-lg">event</span>
                  <span>{{ formatSelectedDate(selectedDate) }}</span>
                </div>
                <div class="flex items-center gap-2.5 text-on-surface-variant dark:text-slate-300 text-xs mt-1.5 pl-6">
                  <span class="material-symbols-outlined text-secondary text-sm">schedule</span>
                  <span>{{ selectedTimeSlot }} (East Africa Time)</span>
                </div>
              </div>

              <!-- 5-Session Pack Discount Toggle -->
              <div 
                @click="isPackApplied = !isPackApplied"
                class="p-4 rounded-2xl mb-6 border transition-all cursor-pointer flex items-center justify-between"
                :class="isPackApplied ? 'bg-secondary-container/20 dark:bg-sky-950/40 border-secondary' : 'bg-surface dark:bg-slate-800 border-outline-variant/30 dark:border-slate-700'"
              >
                <div class="flex items-center gap-2.5">
                  <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all"
                    :class="isPackApplied ? 'border-secondary bg-secondary text-white' : 'border-outline-variant'"
                  >
                    <span v-if="isPackApplied" class="material-symbols-outlined text-xs">check</span>
                  </div>
                  <div>
                    <span class="font-label-sm text-sm font-semibold text-primary-container dark:text-white block">
                      5-Session Pass
                    </span>
                    <span class="text-xs text-on-surface-variant dark:text-slate-400">Save 15% on each session</span>
                  </div>
                </div>
                <span class="font-label-sm text-xs font-bold text-secondary dark:text-sky-300 bg-secondary-container/40 dark:bg-sky-900/60 px-2.5 py-1 rounded-full">
                  15% OFF
                </span>
              </div>

              <!-- Price Breakdown -->
              <div class="space-y-2 mb-6 text-sm">
                <div class="flex items-center justify-between text-on-surface-variant dark:text-slate-400">
                  <span>{{ isPackApplied ? '5-Session Pass Rate' : 'Single Session Rate' }}</span>
                  <span class="font-medium text-on-surface dark:text-white">{{ displayPrice }}</span>
                </div>
                <div class="flex items-center justify-between text-on-surface-variant dark:text-slate-400">
                  <span>Studio Amenities &amp; Mat</span>
                  <span class="font-medium text-emerald-600 dark:text-emerald-400">Complimentary</span>
                </div>
                <div class="pt-3 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-between font-bold text-base text-primary-container dark:text-white">
                  <span>Total Due</span>
                  <span class="text-xl">{{ displayPrice }}</span>
                </div>
              </div>

              <!-- Continue CTA -->
              <button 
                @click="proceedToCheckout"
                class="w-full py-4 rounded-full bg-primary-container hover:bg-primary text-on-primary font-label-md text-label-md font-semibold shadow-md active:scale-[0.98] transition-all flex items-center justify-center gap-2"
                type="button"
              >
                <span>Proceed to Checkout</span>
                <span class="material-symbols-outlined text-lg">arrow_forward</span>
              </button>

              <p class="text-center font-body-sm text-xs text-on-surface-variant dark:text-slate-400 mt-4">
                Free reschedule up to 24h before session time.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <AppBottomNav />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AppNavbar from '@/components/AppNavbar.vue';
import AppBottomNav from '@/components/AppBottomNav.vue';
import { useBookingStore } from '@/stores/bookingStore';
import { getServices } from '@/services/api';

const route = useRoute();
const router = useRouter();
const bookingStore = useBookingStore();

const selectedDate = ref(new Date().toISOString().split('T')[0]);
const selectedTimeSlot = ref('09:30 AM');
const isPackApplied = ref(false);

const activeService = ref({
  title: '1:1 Pilates Reformer & Alignment',
  slug: 'reformer',
  price_kes: 6500,
  price_eur: 75,
  image_url: 'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80'
});

const morningSlots = [
  { time: '08:00 AM', spots: 2 },
  { time: '09:30 AM', spots: 1 },
  { time: '11:00 AM', spots: 3 }
];

const afternoonSlots = [
  { time: '01:30 PM', spots: 2 },
  { time: '03:00 PM', spots: 2 },
  { time: '04:30 PM', spots: 1 }
];

const quickDays = computed(() => {
  const days = [];
  const now = new Date();
  for (let i = 0; i < 7; i++) {
    const d = new Date(now);
    d.setDate(now.getDate() + i);
    days.push({
      dateStr: d.toISOString().split('T')[0],
      dayName: d.toLocaleDateString('en-US', { weekday: 'short' }),
      dayNum: d.getDate()
    });
  }
  return days;
});

const displayPrice = computed(() => {
  const base = bookingStore.currency.value === 'KES' ? (activeService.value.price_kes || 6500) : (activeService.value.price_eur || 75);
  if (isPackApplied.value) {
    const total = Math.round(base * 5 * 0.85);
    return bookingStore.currency.value === 'KES' ? `KES ${total.toLocaleString()}` : `€${total}`;
  }
  return bookingStore.currency.value === 'KES' ? `KES ${base.toLocaleString()}` : `€${base}`;
});

onMounted(async () => {
  try {
    const list = await getServices();
    if (list && list.length > 0) {
      const paramId = route.params.serviceId;
      if (paramId) {
        const found = list.find(s => s.id === paramId || s.slug === paramId);
        if (found) activeService.value = found;
      }
    }
  } catch (e) {
    console.warn('Using default service:', e);
  }
});

function formatSelectedDate(dStr) {
  if (!dStr) return '';
  const d = new Date(dStr);
  return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
}

function proceedToCheckout() {
  bookingStore.setDraftService(activeService.value);
  bookingStore.setDraftSchedule(selectedDate.value, formatSelectedDate(selectedDate.value), selectedTimeSlot.value);
  router.push('/checkout');
}
</script>
