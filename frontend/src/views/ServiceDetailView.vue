<template>
  <div class="min-h-screen bg-surface dark:bg-slate-950 font-body-md text-body-md text-on-surface dark:text-slate-100 antialiased transition-colors duration-200">
    <AppNavbar />

    <!-- MAIN BODY -->
    <main class="w-full pt-20">
      <!-- Top Banner / Breadcrumb & Header -->
      <section class="relative w-full overflow-hidden bg-surface-container-lowest dark:bg-slate-900 shadow-sm border-b border-outline-variant/20 dark:border-slate-800">
        <div class="max-w-7xl mx-auto px-margin py-8 md:py-12">
          <!-- Breadcrumb & Badge -->
          <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
            <nav class="flex items-center gap-2 font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">
              <router-link to="/" class="hover:text-primary-container dark:hover:text-sky-300 transition-colors">Home</router-link>
              <span class="material-symbols-outlined text-xs">chevron_right</span>
              <router-link to="/services" class="hover:text-primary-container dark:hover:text-sky-300 transition-colors">Services</router-link>
              <span class="material-symbols-outlined text-xs">chevron_right</span>
              <span class="text-primary-container dark:text-white font-semibold">{{ service.title }}</span>
            </nav>
            <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-secondary-container/40 dark:bg-sky-950/60 text-primary-container dark:text-sky-300 font-label-sm text-label-sm font-semibold">
              <span class="material-symbols-outlined text-base text-secondary" style="font-variation-settings: 'FILL' 1;">star</span>
              <span>Most Popular Private Session</span>
            </div>
          </div>

          <!-- Main Title & Subtitle -->
          <div class="max-w-4xl">
            <h1 class="font-display text-4xl sm:text-5xl font-semibold text-primary-container dark:text-white tracking-tight leading-tight mb-4">
              {{ service.title }}
            </h1>
            <p class="font-body-lg text-body-lg text-on-surface-variant dark:text-slate-300 leading-relaxed mb-8 max-w-3xl">
              {{ service.description }}
            </p>

            <!-- Metadata Ribbon Grid -->
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
              <div class="flex items-center gap-3 p-3 rounded-xl bg-surface dark:bg-slate-800 shadow-sm border border-outline-variant/20 dark:border-slate-700">
                <span class="material-symbols-outlined text-secondary text-2xl">schedule</span>
                <div>
                  <p class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Duration</p>
                  <p class="font-label-md text-label-md text-on-surface dark:text-white font-semibold">{{ service.duration_minutes || 60 }} Minutes</p>
                </div>
              </div>
              <div class="flex items-center gap-3 p-3 rounded-xl bg-surface dark:bg-slate-800 shadow-sm border border-outline-variant/20 dark:border-slate-700">
                <span class="material-symbols-outlined text-secondary text-2xl">pin_drop</span>
                <div>
                  <p class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Location</p>
                  <p class="font-label-md text-label-md text-on-surface dark:text-white font-semibold">Karen Studio</p>
                </div>
              </div>
              <div class="flex items-center gap-3 p-3 rounded-xl bg-surface dark:bg-slate-800 shadow-sm border border-outline-variant/20 dark:border-slate-700">
                <span class="material-symbols-outlined text-secondary text-2xl">person</span>
                <div>
                  <p class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Format</p>
                  <p class="font-label-md text-label-md text-on-surface dark:text-white font-semibold">1:1 Dedicated</p>
                </div>
              </div>
              <div class="flex items-center gap-3 p-3 rounded-xl bg-surface dark:bg-slate-800 shadow-sm border border-outline-variant/20 dark:border-slate-700">
                <span class="material-symbols-outlined text-secondary text-2xl">savings</span>
                <div>
                  <p class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Pricing</p>
                  <p class="font-label-md text-label-md text-on-surface dark:text-white font-semibold">
                    {{ bookingStore.currency.value === 'KES' ? `KES ${(service.price_kes || 6500).toLocaleString()}` : `€${service.price_eur || 75}` }}
                  </p>
                </div>
              </div>
              <div class="flex items-center gap-3 p-3 rounded-xl bg-surface dark:bg-slate-800 shadow-sm border border-outline-variant/20 dark:border-slate-700 col-span-2 sm:col-span-1">
                <span class="material-symbols-outlined text-secondary text-2xl">verified_user</span>
                <div>
                  <p class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Policy</p>
                  <p class="font-label-md text-label-md text-on-surface dark:text-white font-semibold">24h Free Reschedule</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Dual Column Layout -->
      <div class="max-w-7xl mx-auto px-margin py-10 lg:py-16 w-full">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          <!-- LEFT COLUMN: In-depth Session Content (7 Cols) -->
          <div class="lg:col-span-7 flex flex-col gap-10">
            <!-- Studio Sanctuary Feature Card -->
            <div class="rounded-3xl overflow-hidden bg-surface-container-lowest dark:bg-slate-900 shadow-md border border-outline-variant/30 dark:border-slate-800">
              <div class="relative h-80 sm:h-96 w-full">
                <img 
                  class="w-full h-full object-cover" 
                  alt="Karen Studio" 
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuCIbQnXjnlDtQMmLQ1SS2pYB9QhB3BbMG5AERAj7d3BLRxymzGLhNWDjicBtVQjnLhBGwtkEZn9OYGGDAmKPJWgxHe7d0K_I3N7xq3aOHXJzef9uoZs9WQ5ALuZ-rlgtb0_yPrXcsv9hoq98c2M_KRPtx4PnrdJNMI0OJ3a40KNv0ELt21Hf7yyA9xNKNagAIjW6tv58ZitcSq2jU__9C9Re7zcWg_FDgLwN5aCXqovuB5PnfjV5w42"
                />
                <div class="absolute bottom-4 left-4 right-4 bg-surface-container-lowest/90 dark:bg-slate-900/90 backdrop-blur-md p-4 rounded-2xl flex items-center justify-between shadow-sm">
                  <div class="flex items-center gap-3">
                    <span class="material-symbols-outlined text-secondary">spa</span>
                    <span class="font-label-md text-label-md text-primary-container dark:text-white font-semibold">Tree Lane Studio Sanctuary, Karen</span>
                  </div>
                  <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-wider">Private Garden Setting</span>
                </div>
              </div>
            </div>

            <!-- What to Expect Progression -->
            <div class="rounded-3xl p-6 sm:p-8 bg-surface-container-lowest dark:bg-slate-900 shadow-sm border border-outline-variant/30 dark:border-slate-800">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-10 h-10 rounded-full bg-secondary-fixed dark:bg-slate-800 flex items-center justify-center text-primary dark:text-sky-300">
                  <span class="material-symbols-outlined">psychology_alt</span>
                </div>
                <div>
                  <h2 class="font-headline-md text-2xl font-bold text-primary-container dark:text-white">What to Expect in Your Session</h2>
                  <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400">A deliberate 4-stage progression crafted for maximum somatic restoration</p>
                </div>
              </div>

              <div class="space-y-4">
                <div class="p-4 rounded-2xl bg-surface dark:bg-slate-800/50 flex items-start gap-4">
                  <span class="w-7 h-7 rounded-full bg-primary-container text-on-primary font-label-md text-label-md flex items-center justify-center shrink-0 mt-0.5 font-bold">1</span>
                  <div>
                    <h3 class="font-label-lg text-label-lg font-semibold text-primary-container dark:text-white mb-1">Dynamic Postural &amp; Breathwork Calibration</h3>
                    <p class="font-body-md text-body-md text-on-surface-variant dark:text-slate-300">
                      We begin with a 10-minute kinetic scan assessing pelvo-lumbar rhythm, thoracic rotation restrictions, and diaphragmatic breathing patterns before touching the apparatus.
                    </p>
                  </div>
                </div>

                <div class="p-4 rounded-2xl bg-surface dark:bg-slate-800/50 flex items-start gap-4">
                  <span class="w-7 h-7 rounded-full bg-primary-container text-on-primary font-label-md text-label-md flex items-center justify-center shrink-0 mt-0.5 font-bold">2</span>
                  <div>
                    <h3 class="font-label-lg text-label-lg font-semibold text-primary-container dark:text-white mb-1">Tailored Spring Tension Calibration</h3>
                    <p class="font-body-md text-body-md text-on-surface-variant dark:text-slate-300">
                      Customized spring combinations calibrated specifically to offload strained joints, activate deep transverse abdominis fibers, and gently open tight hip flexors.
                    </p>
                  </div>
                </div>

                <div class="p-4 rounded-2xl bg-surface dark:bg-slate-800/50 flex items-start gap-4">
                  <span class="w-7 h-7 rounded-full bg-primary-container text-on-primary font-label-md text-label-md flex items-center justify-center shrink-0 mt-0.5 font-bold">3</span>
                  <div>
                    <h3 class="font-label-lg text-label-lg font-semibold text-primary-container dark:text-white mb-1">Somatic Reformer Flow &amp; Articulation</h3>
                    <p class="font-body-md text-body-md text-on-surface-variant dark:text-slate-300">
                      Slow, mindful eccentric contractions emphasizing continuous axial elongation, scapular stabilization, and rhythmic lymphatic circulation.
                    </p>
                  </div>
                </div>

                <div class="p-4 rounded-2xl bg-surface dark:bg-slate-800/50 flex items-start gap-4">
                  <span class="w-7 h-7 rounded-full bg-primary-container text-on-primary font-label-md text-label-md flex items-center justify-center shrink-0 mt-0.5 font-bold">4</span>
                  <div>
                    <h3 class="font-label-lg text-label-lg font-semibold text-primary-container dark:text-white mb-1">Down-Regulation &amp; Nervous System Reset</h3>
                    <p class="font-body-md text-body-md text-on-surface-variant dark:text-slate-300">
                      Concluding with assisted spinal traction, myofascial releases, and soothing parasympathetic breathwork leaving you feeling light, centered, and energized.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- RIGHT COLUMN: Direct Scheduling Panel (5 Cols) -->
          <div class="lg:col-span-5 sticky top-28">
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-xl border border-outline-variant/30 dark:border-slate-800">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-widest block">Direct Reservation</span>
                  <h3 class="font-headline-sm text-headline-sm font-bold text-primary-container dark:text-white">Select Date &amp; Time</h3>
                </div>
                <div class="text-right">
                  <span class="font-headline-sm text-2xl font-bold text-primary-container dark:text-white">
                    {{ bookingStore.currency.value === 'KES' ? `KES ${(service.price_kes || 6500).toLocaleString()}` : `€${service.price_eur || 75}` }}
                  </span>
                  <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400 block">per session</span>
                </div>
              </div>

              <!-- Multi-Session Pack Notice -->
              <div class="p-3.5 rounded-2xl bg-secondary-container/20 dark:bg-sky-950/40 border border-secondary-container/40 dark:border-sky-800 mb-6 flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-secondary text-lg">local_activity</span>
                  <span class="font-label-sm text-label-sm text-primary-container dark:text-sky-200">5-Session Wellness Pack</span>
                </div>
                <span class="font-label-sm text-label-sm font-bold text-secondary dark:text-sky-300">Save 15%</span>
              </div>

              <!-- Date Picker -->
              <div class="mb-5">
                <label class="block font-label-sm text-label-sm text-on-surface-variant dark:text-slate-300 mb-2">Select Date</label>
                <input 
                  v-model="bookingDate" 
                  type="date" 
                  class="w-full px-4 py-3 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/40 dark:border-slate-700 text-on-surface dark:text-white font-medium focus:outline-none focus:border-secondary"
                />
              </div>

              <!-- Available Time Slots -->
              <div class="mb-6">
                <label class="block font-label-sm text-label-sm text-on-surface-variant dark:text-slate-300 mb-2">Available Time Slots</label>
                <div class="grid grid-cols-2 gap-2.5">
                  <button 
                    v-for="slot in sampleSlots" 
                    :key="slot"
                    type="button"
                    @click="selectedSlot = slot"
                    :class="selectedSlot === slot ? 'bg-primary-container text-white border-primary-container dark:bg-sky-500 dark:text-slate-950 font-semibold' : 'bg-surface dark:bg-slate-800 border-outline-variant/30 dark:border-slate-700 text-on-surface dark:text-slate-200 hover:border-secondary'"
                    class="py-2.5 px-3 rounded-xl border text-center font-label-sm text-label-sm transition-all"
                  >
                    {{ slot }}
                  </button>
                </div>
              </div>

              <!-- CTA Button -->
              <button 
                @click="proceedToCheckout"
                type="button" 
                class="w-full py-4 rounded-full bg-primary-container hover:bg-primary text-on-primary font-label-md text-label-md font-semibold shadow-md active:scale-[0.98] transition-all flex items-center justify-center gap-2"
              >
                <span>Continue to Checkout</span>
                <span class="material-symbols-outlined text-lg">arrow_forward</span>
              </button>

              <!-- Trainer guarantee -->
              <div class="mt-6 pt-4 border-t border-outline-variant/20 dark:border-slate-800 flex items-center gap-3">
                <img 
                  alt="Karina" 
                  class="w-10 h-10 rounded-full object-cover shadow-sm shrink-0" 
                  src="https://lh3.googleusercontent.com/aida/AEtjO1UwxvO7_3GTbgWd4EMPt4rt_w381oAezID3bV9-NdwIdn55FZ_9EuUxkek0b1g_CCD7OREkS7yHj5Cgb747yd7hji3o7wMsF5yMWX7Y-9WXeuNJSV87pRW9T6yotkdPzul6-kYjIysNWHJ6rcSRnoCnngzil7rsid2c6iewLxqYX2u5vPcQFLY7r3ZEkPxwmhnE8RfShmfVHjQTEbYJSi9MwKlsQzRFBydQI4ftgATXc7O0xLaTmJmS44Z2gA8121FAes4FrKhN"
                />
                <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
                  Personally led by Karina. Sanitized apparatus &amp; private garden view guaranteed.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AppNavbar from '@/components/AppNavbar.vue';
import { useBookingStore } from '@/stores/bookingStore';
import { useThemeStore } from '@/stores/themeStore';
import { useAuthStore } from '@/stores/authStore';
import { getServices } from '@/services/api';

const route = useRoute();
const router = useRouter();
const bookingStore = useBookingStore();
const themeStore = useThemeStore();
const authStore = useAuthStore();

const service = ref({
  title: '1:1 Pilates Reformer & Alignment',
  slug: 'reformer',
  duration_minutes: 60,
  price_kes: 6500,
  price_eur: 45,
  description: 'A personalized reformer session engineered around your spine, core posture, and bio-individual movement mechanics with Pilates Master Karina. Experience targeted spring decompression, restorative length, and lasting structural vitality.'
});

const bookingDate = ref(new Date().toISOString().split('T')[0]);
const selectedSlot = ref('09:30 AM');
const sampleSlots = ['08:00 AM', '09:30 AM', '11:00 AM', '02:00 PM', '04:30 PM', '06:00 PM'];

onMounted(async () => {
  try {
    const list = await getServices();
    if (list && list.length > 0) {
      const paramId = route.params.id;
      const matched = list.find(s => s.id === paramId || s.slug === paramId);
      if (matched) {
        service.value = matched;
      }
    }
  } catch (e) {
    console.warn('Using default service details:', e);
  }
});

function proceedToCheckout() {
  bookingStore.setDraftService(service.value);
  bookingStore.setDraftSchedule(bookingDate.value, bookingDate.value, selectedSlot.value);
  router.push('/checkout');
}
</script>
