<template>
  <div class="bg-surface dark:bg-slate-950 text-on-surface dark:text-slate-100 flex flex-col min-h-screen transition-colors duration-200">
    <AppNavbar />

    <main class="flex-1 flex flex-col relative w-full pt-20 pb-24 md:pb-16 bg-surface dark:bg-slate-950">
      <div class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6">
        <!-- Catalog Header Banner -->
        <section class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary-container/30 dark:bg-sky-950/60 text-primary-container dark:text-sky-300 font-label-sm text-label-sm font-semibold mb-2">
              <span class="material-symbols-outlined text-sm text-secondary">spa</span>
              <span>Movement &amp; Longevity</span>
            </div>
            <h1 class="font-headline-lg text-3xl sm:text-4xl font-bold text-primary-container dark:text-white tracking-tight">
              Services &amp; Offerings
            </h1>
            <p class="font-body-md text-body-md text-on-surface-variant dark:text-slate-400 mt-1 max-w-2xl leading-relaxed">
              Private Pilates Reformer, functional biomechanics, and personalized endocrine coaching designed for your season of life.
            </p>
          </div>

          <!-- Currency & Filter indicator -->
          <div class="flex items-center gap-3 shrink-0">
            <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">
              Showing prices in <strong>{{ currency }}</strong>
            </span>
          </div>
        </section>

        <!-- Category Filter Pills Bar -->
        <div class="flex items-center gap-2 overflow-x-auto pb-4 mb-6 no-scrollbar">
          <button 
            v-for="cat in categories" 
            :key="cat.id"
            @click="activeCategory = cat.id"
            type="button"
            :class="activeCategory === cat.id ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-semibold shadow-sm' : 'bg-surface-container-low dark:bg-slate-800 text-on-surface dark:text-slate-300 hover:bg-surface-container border border-outline-variant/30 dark:border-slate-700'"
            class="px-4 py-2 rounded-full font-label-sm text-label-sm whitespace-nowrap transition-all"
          >
            {{ cat.label }}
          </button>
        </div>

        <!-- 3-Column Responsive Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="service in filteredServices" 
            :key="service.id"
            class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-5 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between group border border-outline-variant/30 dark:border-slate-800"
          >
            <div>
              <!-- Service Image -->
              <div class="rounded-2xl overflow-hidden aspect-[16/10] mb-4 bg-surface-container-low relative">
                <img 
                  :src="service.image_url" 
                  :alt="service.title"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                />
                <span 
                  v-if="service.badge"
                  class="absolute top-3 left-3 bg-surface-container-lowest/90 dark:bg-slate-900/90 backdrop-blur-sm px-3 py-1 rounded-full font-label-sm text-xs text-primary-container dark:text-white font-semibold shadow-xs"
                >
                  {{ service.badge }}
                </span>
              </div>

              <!-- Metadata ribbon -->
              <div class="flex items-center justify-between text-secondary font-label-sm text-xs mb-1.5">
                <span class="flex items-center gap-1 font-medium">
                  <span class="material-symbols-outlined text-sm">schedule</span> 
                  {{ service.duration_minutes }} mins
                </span>
                <span class="flex items-center gap-1 font-medium">
                  <span class="material-symbols-outlined text-sm">location_on</span> 
                  {{ service.location_display || 'Karen Studio' }}
                </span>
              </div>

              <!-- Service Title -->
              <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white mb-2 group-hover:text-secondary transition-colors">
                {{ service.title }}
              </h3>

              <!-- Description -->
              <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400 leading-relaxed mb-4 line-clamp-3">
                {{ service.description }}
              </p>
            </div>

            <!-- Footer: Price & Action Buttons -->
            <div class="pt-4 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-between gap-3">
              <div>
                <span class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400 block">Single Session</span>
                <div class="font-headline-sm text-lg font-bold text-primary-container dark:text-white">
                  {{ formatPrice(service) }}
                </div>
              </div>

              <div class="flex items-center gap-2">
                <router-link 
                  :to="`/services/${service.slug || service.id}`"
                  class="px-3.5 py-2 rounded-full bg-surface-container-low dark:bg-slate-800 text-on-surface dark:text-slate-200 hover:bg-surface-container font-label-sm text-xs font-semibold border border-outline-variant/30 dark:border-slate-700 transition-all"
                >
                  Details
                </router-link>
                <button 
                  @click="bookNow(service)"
                  class="px-4 py-2 rounded-full bg-primary-container hover:bg-primary text-on-primary font-label-sm text-xs font-semibold shadow-xs active:scale-95 transition-all"
                  type="button"
                >
                  Book Slot
                </button>
              </div>
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
import { useRouter } from 'vue-router';
import AppNavbar from '@/components/AppNavbar.vue';
import AppBottomNav from '@/components/AppBottomNav.vue';
import { useBookingStore } from '@/stores/bookingStore';
import { getServices } from '@/services/api';

const router = useRouter();
const bookingStore = useBookingStore();
const currency = computed(() => bookingStore.currency.value);

const activeCategory = ref('all');
const services = ref([]);

const categories = [
  { id: 'all', label: 'All Offerings' },
  { id: 'reformer', label: 'Pilates Reformer' },
  { id: 'strength', label: 'Functional Strength' },
  { id: 'hormone', label: 'Hormone Coaching' },
  { id: 'outdoor', label: 'Outdoor MenoMove' }
];

onMounted(async () => {
  try {
    const list = await getServices();
    services.value = list;
  } catch (e) {
    console.error('Error fetching services:', e);
  }
});

const filteredServices = computed(() => {
  if (activeCategory.value === 'all') return services.value;
  return services.value.filter(s => {
    const cat = (s.category || '').toLowerCase();
    const slug = (s.slug || '').toLowerCase();
    return cat.includes(activeCategory.value) || slug.includes(activeCategory.value);
  });
});

function formatPrice(service) {
  if (currency.value === 'KES') {
    return `KES ${(service.price_kes || 6500).toLocaleString()}`;
  }
  return `€${service.price_eur || 75}`;
}

function bookNow(service) {
  bookingStore.setDraftService(service);
  router.push(`/book/${service.slug || service.id}`);
}
</script>
