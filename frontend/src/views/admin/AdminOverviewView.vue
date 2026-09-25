<template>
  <div class="space-y-8 animate-fadeIn">
    <!-- Top KPI Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
      <div class="bg-surface-container-lowest dark:bg-slate-900 p-5 rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-xs flex items-center justify-between">
        <div>
          <p class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400 font-medium uppercase tracking-wider">Confirmed Revenue</p>
          <h3 class="font-headline-md text-2xl font-bold text-primary-container dark:text-white mt-1">
            KES {{ (metrics.revenue_kes || 0).toLocaleString() }}
          </h3>
          <p class="font-label-sm text-[11px] text-emerald-600 dark:text-emerald-400 mt-1 flex items-center gap-1 font-semibold">
            <span class="material-symbols-outlined text-xs">trending_up</span> M-Pesa + Studio Verified
          </p>
        </div>
        <div class="w-12 h-12 rounded-2xl bg-secondary-container/40 dark:bg-sky-950 text-primary-container dark:text-sky-300 flex items-center justify-center">
          <span class="material-symbols-outlined text-2xl">payments</span>
        </div>
      </div>

      <div class="bg-surface-container-lowest dark:bg-slate-900 p-5 rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-xs flex items-center justify-between">
        <div>
          <p class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400 font-medium uppercase tracking-wider">Active Services</p>
          <h3 class="font-headline-md text-2xl font-bold text-primary-container dark:text-white mt-1">
            {{ metrics.total_services || 10 }} Offerings
          </h3>
          <p class="font-label-sm text-[11px] text-on-surface-variant dark:text-slate-400 mt-1">
            Pilates, Yoga, Sound, Therapy
          </p>
        </div>
        <div class="w-12 h-12 rounded-2xl bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 flex items-center justify-center">
          <span class="material-symbols-outlined text-2xl">spa</span>
        </div>
      </div>

      <div class="bg-surface-container-lowest dark:bg-slate-900 p-5 rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-xs flex items-center justify-between">
        <div>
          <p class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400 font-medium uppercase tracking-wider">Scheduled Slots</p>
          <h3 class="font-headline-md text-2xl font-bold text-primary-container dark:text-white mt-1">
            {{ metrics.total_slots || 0 }} Sessions
          </h3>
          <p class="font-label-sm text-[11px] text-secondary dark:text-sky-400 mt-1">
            Available across 14 days
          </p>
        </div>
        <div class="w-12 h-12 rounded-2xl bg-indigo-50 dark:bg-indigo-950/50 text-indigo-700 dark:text-indigo-300 flex items-center justify-center">
          <span class="material-symbols-outlined text-2xl">event_available</span>
        </div>
      </div>

      <div class="bg-surface-container-lowest dark:bg-slate-900 p-5 rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-xs flex items-center justify-between">
        <div>
          <p class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400 font-medium uppercase tracking-wider">Total Bookings</p>
          <h3 class="font-headline-md text-2xl font-bold text-primary-container dark:text-white mt-1">
            {{ metrics.total_bookings || 0 }} Clients
          </h3>
          <p class="font-label-sm text-[11px] text-on-surface-variant dark:text-slate-400 mt-1">
            {{ metrics.confirmed_bookings || 0 }} Confirmed &bull; {{ metrics.completed_bookings || 0 }} Completed
          </p>
        </div>
        <div class="w-12 h-12 rounded-2xl bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 flex items-center justify-center">
          <span class="material-symbols-outlined text-2xl">groups</span>
        </div>
      </div>
    </div>

    <!-- Quick Operations Launchpad -->
    <div class="bg-surface-container-low dark:bg-slate-900/60 p-6 rounded-3xl border border-outline-variant/30 dark:border-slate-800">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="font-headline-sm text-lg font-bold text-primary-container dark:text-white">
            Operations Launchpad
          </h3>
          <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
            Rapid access shortcuts for studio managers
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
        <router-link
          to="/admin/services"
          class="flex items-center gap-3 p-4 rounded-2xl bg-surface-container-lowest dark:bg-slate-800 border border-outline-variant/20 dark:border-slate-700 hover:border-primary-container/40 dark:hover:border-sky-500 shadow-xs transition-all text-left group"
        >
          <div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 flex items-center justify-center group-hover:scale-105 transition-transform">
            <span class="material-symbols-outlined">add_circle</span>
          </div>
          <div>
            <p class="font-label-md text-xs font-bold text-primary-container dark:text-white">Manage Services</p>
            <p class="font-body-sm text-[11px] text-on-surface-variant dark:text-slate-400">Add or edit offerings</p>
          </div>
        </router-link>

        <router-link
          to="/admin/sessions"
          class="flex items-center gap-3 p-4 rounded-2xl bg-surface-container-lowest dark:bg-slate-800 border border-outline-variant/20 dark:border-slate-700 hover:border-primary-container/40 dark:hover:border-sky-500 shadow-xs transition-all text-left group"
        >
          <div class="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950 text-amber-600 dark:text-amber-400 flex items-center justify-center group-hover:scale-105 transition-transform">
            <span class="material-symbols-outlined">bolt</span>
          </div>
          <div>
            <p class="font-label-md text-xs font-bold text-primary-container dark:text-white">Bulk Schedule</p>
            <p class="font-body-sm text-[11px] text-on-surface-variant dark:text-slate-400">Generate recurring slots</p>
          </div>
        </router-link>

        <router-link
          to="/admin/bookings"
          class="flex items-center gap-3 p-4 rounded-2xl bg-surface-container-lowest dark:bg-slate-800 border border-outline-variant/20 dark:border-slate-700 hover:border-primary-container/40 dark:hover:border-sky-500 shadow-xs transition-all text-left group"
        >
          <div class="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 flex items-center justify-center group-hover:scale-105 transition-transform">
            <span class="material-symbols-outlined">event_available</span>
          </div>
          <div>
            <p class="font-label-md text-xs font-bold text-primary-container dark:text-white">Live Roster</p>
            <p class="font-body-sm text-[11px] text-on-surface-variant dark:text-slate-400">Manage attendee sessions</p>
          </div>
        </router-link>

        <router-link
          to="/admin/customers"
          class="flex items-center gap-3 p-4 rounded-2xl bg-surface-container-lowest dark:bg-slate-800 border border-outline-variant/20 dark:border-slate-700 hover:border-primary-container/40 dark:hover:border-sky-500 shadow-xs transition-all text-left group"
        >
          <div class="w-10 h-10 rounded-xl bg-sky-50 dark:bg-sky-950 text-sky-600 dark:text-sky-400 flex items-center justify-center group-hover:scale-105 transition-transform">
            <span class="material-symbols-outlined">person_add</span>
          </div>
          <div>
            <p class="font-label-md text-xs font-bold text-primary-container dark:text-white">Customer CRM</p>
            <p class="font-body-sm text-[11px] text-on-surface-variant dark:text-slate-400">View client passes &amp; data</p>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Recent Reservations Stream -->
    <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl border border-outline-variant/30 dark:border-slate-800 p-6 shadow-xs">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-headline-sm text-lg font-bold text-primary-container dark:text-white">
          Recent Studio Bookings
        </h3>
        <router-link
          to="/admin/bookings"
          class="font-label-sm text-xs font-semibold text-secondary hover:text-primary-container dark:hover:text-white transition-colors"
        >
          View Full Attendee Roster &rarr;
        </router-link>
      </div>

      <div v-if="recentBookings.length === 0" class="text-center py-8 text-on-surface-variant dark:text-slate-400 text-sm">
        No recent bookings recorded yet.
      </div>

      <div v-else class="divide-y divide-outline-variant/20 dark:divide-slate-800">
        <div
          v-for="b in recentBookings"
          :key="b.id"
          class="py-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
        >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-secondary-container/30 dark:bg-slate-800 text-secondary dark:text-sky-300 font-bold flex items-center justify-center text-sm">
              {{ (b.user_name || 'U').charAt(0).toUpperCase() }}
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span class="font-label-md text-sm font-bold text-primary-container dark:text-white">{{ b.user_name }}</span>
                <span
                  class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider"
                  :class="statusBadgeClass(b.status)"
                >
                  {{ b.status }}
                </span>
              </div>
              <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
                {{ b.service_title }} &bull; {{ b.booking_date }} at {{ b.time_slot }}
              </p>
            </div>
          </div>

          <div class="flex items-center gap-3 justify-between sm:justify-end">
            <div class="text-right">
              <span class="font-label-sm text-xs font-bold text-primary-container dark:text-white">
                {{ b.currency }} {{ (b.total_amount || 0).toLocaleString() }}
              </span>
              <span class="block text-[11px] text-on-surface-variant dark:text-slate-400 uppercase font-mono">
                {{ b.payment_reference || 'REF' }}
              </span>
            </div>
            <router-link
              to="/admin/bookings"
              class="px-3 py-1 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container font-label-sm text-xs font-medium border border-outline-variant/30 dark:border-slate-700"
            >
              Manage
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getAdminOverview } from '@/services/api';

const metrics = ref({
  total_services: 0,
  total_slots: 0,
  total_bookings: 0,
  confirmed_bookings: 0,
  completed_bookings: 0,
  revenue_kes: 0,
  revenue_eur: 0
});

const recentBookings = ref([]);

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

onMounted(async () => {
  try {
    const res = await getAdminOverview();
    metrics.value = res.metrics || {};
    recentBookings.value = res.recent_bookings || [];
  } catch (e) {
    console.error('Failed to load admin overview:', e);
  }
});
</script>
