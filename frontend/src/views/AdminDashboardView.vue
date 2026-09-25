<template>
  <div class="bg-surface dark:bg-slate-950 text-on-surface dark:text-slate-100 flex flex-col min-h-screen transition-colors duration-200">
    <!-- Top Admin Header -->
    <header class="sticky top-0 z-40 bg-surface-container-lowest/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-outline-variant/30 dark:border-slate-800 shadow-xs">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between gap-4">
        <!-- Brand & Context -->
        <div class="flex items-center gap-3.5">
          <div class="w-10 h-10 rounded-2xl bg-primary-container dark:bg-sky-500 text-white dark:text-slate-950 flex items-center justify-center shadow-sm">
            <span class="material-symbols-outlined text-xl">admin_panel_settings</span>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h1 class="font-headline-sm text-lg sm:text-xl font-bold text-primary-container dark:text-white tracking-tight">
                Studio Operations
              </h1>
              <span class="px-2 py-0.5 rounded-full bg-secondary-container/40 dark:bg-sky-950 text-primary-container dark:text-sky-300 font-label-sm text-[11px] font-bold uppercase tracking-wider">
                Admin
              </span>
            </div>
            <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 hidden sm:block">
              Karina Wellness &bull; Service Catalog, Session Scheduling &amp; Bookings
            </p>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <nav class="hidden lg:flex items-center gap-1 bg-surface-container-low dark:bg-slate-800/80 p-1.5 rounded-2xl border border-outline-variant/30 dark:border-slate-700">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="activeTab === tab.id ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white shadow-xs font-semibold' : 'text-on-surface-variant dark:text-slate-400 hover:text-on-surface'"
            class="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl font-label-sm text-xs transition-all"
            type="button"
          >
            <span class="material-symbols-outlined text-base">{{ tab.icon }}</span>
            <span>{{ tab.label }}</span>
          </button>
        </nav>

        <!-- Right: Actions & Switch to Storefront -->
        <div class="flex items-center gap-2.5">
          <router-link
            to="/services"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container text-on-surface dark:text-slate-200 font-label-sm text-xs font-medium border border-outline-variant/30 dark:border-slate-700 transition-all"
          >
            <span class="material-symbols-outlined text-sm">storefront</span>
            <span class="hidden sm:inline">Client Storefront</span>
          </router-link>

          <button
            @click="refreshCurrentTab"
            :disabled="loading"
            class="w-9 h-9 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-on-surface-variant dark:text-slate-300 transition-colors"
            title="Refresh Data"
            type="button"
          >
            <span class="material-symbols-outlined text-base" :class="{'animate-spin': loading}">sync</span>
          </button>
        </div>
      </div>

      <!-- Mobile Tab Bar (<1024px) -->
      <div class="lg:hidden flex items-center gap-1 px-4 py-2 overflow-x-auto border-t border-outline-variant/20 dark:border-slate-800 no-scrollbar bg-surface dark:bg-slate-950">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="activeTab === tab.id ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-semibold' : 'bg-surface-container-low dark:bg-slate-800 text-on-surface-variant dark:text-slate-400'"
          class="flex items-center gap-1.5 px-3 py-1.5 rounded-full font-label-sm text-xs whitespace-nowrap transition-all"
          type="button"
        >
          <span class="material-symbols-outlined text-sm">{{ tab.icon }}</span>
          <span>{{ tab.label }}</span>
        </button>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6">
      <!-- Notification Banner -->
      <div v-if="bannerMessage" class="mb-6 p-4 rounded-2xl flex items-center justify-between gap-3 shadow-xs animate-fadeIn" :class="bannerType === 'error' ? 'bg-red-50 text-red-800 border border-red-200 dark:bg-red-950/40 dark:text-red-300 dark:border-red-900' : 'bg-emerald-50 text-emerald-800 border border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-900'">
        <div class="flex items-center gap-2">
          <span class="material-symbols-outlined text-xl">{{ bannerType === 'error' ? 'error' : 'check_circle' }}</span>
          <span class="font-body-md text-sm font-medium">{{ bannerMessage }}</span>
        </div>
        <button @click="bannerMessage = ''" class="text-xs opacity-70 hover:opacity-100 font-bold p-1">&times;</button>
      </div>

      <!-- TAB 1: OVERVIEW -->
      <section v-if="activeTab === 'overview'" class="space-y-8 animate-fadeIn">
        <!-- KPI Cards Grid -->
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
                {{ metrics.total_services || services.length }} Offerings
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
                Available &amp; Upcoming
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

        <!-- Quick Operations Launcher -->
        <div class="bg-surface-container-low dark:bg-slate-900/60 p-6 rounded-3xl border border-outline-variant/30 dark:border-slate-800">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
            <div>
              <h2 class="font-headline-sm text-lg font-bold text-primary-container dark:text-white">
                Quick Actions
              </h2>
              <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
                Instantly create services, add session slots, or generate recurring schedules
              </p>
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <button
              @click="openServiceModal()"
              class="flex items-center gap-3 p-4 rounded-2xl bg-surface-container-lowest dark:bg-slate-800 border border-outline-variant/20 dark:border-slate-700 hover:border-primary-container/40 dark:hover:border-sky-500 shadow-xs transition-all text-left group"
              type="button"
            >
              <div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 flex items-center justify-center group-hover:scale-105 transition-transform">
                <span class="material-symbols-outlined">add_circle</span>
              </div>
              <div>
                <p class="font-label-md text-sm font-bold text-primary-container dark:text-white">Add New Service</p>
                <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">Create offering with price &amp; description</p>
              </div>
            </button>

            <button
              @click="openSingleSlotModal()"
              class="flex items-center gap-3 p-4 rounded-2xl bg-surface-container-lowest dark:bg-slate-800 border border-outline-variant/20 dark:border-slate-700 hover:border-primary-container/40 dark:hover:border-sky-500 shadow-xs transition-all text-left group"
              type="button"
            >
              <div class="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 flex items-center justify-center group-hover:scale-105 transition-transform">
                <span class="material-symbols-outlined">calendar_add_on</span>
              </div>
              <div>
                <p class="font-label-md text-sm font-bold text-primary-container dark:text-white">Add Single Slot</p>
                <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">Schedule one session on a specific date</p>
              </div>
            </button>

            <button
              @click="openBulkModal()"
              class="flex items-center gap-3 p-4 rounded-2xl bg-surface-container-lowest dark:bg-slate-800 border border-outline-variant/20 dark:border-slate-700 hover:border-primary-container/40 dark:hover:border-sky-500 shadow-xs transition-all text-left group"
              type="button"
            >
              <div class="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950 text-amber-600 dark:text-amber-400 flex items-center justify-center group-hover:scale-105 transition-transform">
                <span class="material-symbols-outlined">bolt</span>
              </div>
              <div>
                <p class="font-label-md text-sm font-bold text-primary-container dark:text-white">Bulk Generate Slots</p>
                <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">Automate weekly recurring time slots</p>
              </div>
            </button>
          </div>
        </div>

        <!-- Recent Reservations Stream -->
        <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl border border-outline-variant/30 dark:border-slate-800 p-6 shadow-xs">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-headline-sm text-lg font-bold text-primary-container dark:text-white">
              Recent Bookings
            </h2>
            <button
              @click="activeTab = 'bookings'"
              class="font-label-sm text-xs font-semibold text-secondary hover:text-primary-container dark:hover:text-white transition-colors"
              type="button"
            >
              View All Attendees &rarr;
            </button>
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
                <button
                  @click="openEditBookingModal(b)"
                  class="px-3 py-1 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container font-label-sm text-xs font-medium border border-outline-variant/30 dark:border-slate-700"
                  type="button"
                >
                  Manage
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- TAB 2: SERVICES MANAGEMENT -->
      <section v-if="activeTab === 'services'" class="space-y-6 animate-fadeIn">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 class="font-headline-sm text-2xl font-bold text-primary-container dark:text-white">
              Service Offerings Catalog
            </h2>
            <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
              Manage offerings, pricing, durations, categories, and studio details
            </p>
          </div>
          <button
            @click="openServiceModal()"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all self-start sm:self-auto"
            type="button"
          >
            <span class="material-symbols-outlined text-sm">add</span>
            <span>Add New Service</span>
          </button>
        </div>

        <!-- Filter bar -->
        <div class="flex flex-col sm:flex-row items-center gap-3">
          <div class="relative w-full sm:w-80">
            <span class="material-symbols-outlined absolute left-3 top-2.5 text-on-surface-variant text-base">search</span>
            <input
              v-model="serviceSearch"
              type="text"
              placeholder="Search services by title..."
              class="w-full pl-9 pr-4 py-2 rounded-2xl bg-surface-container-lowest dark:bg-slate-900 border border-outline-variant/30 dark:border-slate-800 text-xs font-body-sm focus:outline-none focus:ring-2 focus:ring-primary-container/30"
            />
          </div>
          <div class="flex items-center gap-2 overflow-x-auto w-full pb-1 no-scrollbar">
            <button
              v-for="cat in serviceCategories"
              :key="cat.id"
              @click="serviceCategoryFilter = cat.id"
              :class="serviceCategoryFilter === cat.id ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-bold' : 'bg-surface-container-low dark:bg-slate-800 text-on-surface-variant dark:text-slate-300'"
              class="px-3 py-1.5 rounded-full font-label-sm text-xs whitespace-nowrap transition-all"
              type="button"
            >
              {{ cat.label }}
            </button>
          </div>
        </div>

        <!-- Services Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="srv in filteredServices"
            :key="srv.id"
            class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-5 border border-outline-variant/30 dark:border-slate-800 shadow-xs flex flex-col justify-between group hover:shadow-md transition-all"
          >
            <div>
              <div class="aspect-[16/9] rounded-2xl overflow-hidden mb-3 bg-surface-container-low relative">
                <img :src="srv.image_url" :alt="srv.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                <span v-if="srv.badge" class="absolute top-2.5 left-2.5 bg-surface-container-lowest/90 dark:bg-slate-900/90 backdrop-blur-xs px-2.5 py-0.5 rounded-full font-label-sm text-[10px] font-bold text-primary-container dark:text-white shadow-xs">
                  {{ srv.badge }}
                </span>
                <span class="absolute top-2.5 right-2.5 bg-primary-container/85 text-white px-2 py-0.5 rounded-full font-label-sm text-[10px] font-semibold uppercase tracking-wider">
                  {{ srv.category }}
                </span>
              </div>

              <div class="flex items-center justify-between text-secondary font-label-sm text-xs mb-1">
                <span class="flex items-center gap-1">
                  <span class="material-symbols-outlined text-xs">schedule</span> {{ srv.duration_minutes }} mins
                </span>
                <span class="flex items-center gap-1">
                  <span class="material-symbols-outlined text-xs">groups</span> {{ srv.capacity || '1:1 / Group' }}
                </span>
              </div>

              <h3 class="font-headline-sm text-lg font-bold text-primary-container dark:text-white mb-1.5">
                {{ srv.title }}
              </h3>

              <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400 line-clamp-3 mb-3 leading-relaxed">
                {{ srv.description }}
              </p>
            </div>

            <div class="pt-3 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-between gap-2">
              <div>
                <span class="font-headline-sm text-sm font-bold text-primary-container dark:text-white block">
                  KES {{ (srv.price_kes || 0).toLocaleString() }}
                </span>
                <span class="text-[11px] text-on-surface-variant dark:text-slate-400 block font-medium">
                  &euro;{{ srv.price_eur || 0 }} EUR
                </span>
              </div>

              <div class="flex items-center gap-1.5">
                <button
                  @click="openServiceModal(srv)"
                  class="px-3 py-1.5 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container font-label-sm text-xs font-semibold text-primary-container dark:text-white border border-outline-variant/30 dark:border-slate-700 transition-all flex items-center gap-1"
                  type="button"
                >
                  <span class="material-symbols-outlined text-xs">edit</span>
                  <span>Edit</span>
                </button>
                <button
                  @click="confirmDeleteService(srv)"
                  class="w-8 h-8 rounded-full bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 hover:bg-red-100 flex items-center justify-center transition-colors"
                  title="Delete Service"
                  type="button"
                >
                  <span class="material-symbols-outlined text-sm">delete</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- TAB 3: SESSIONS & SLOTS -->
      <section v-if="activeTab === 'slots'" class="space-y-6 animate-fadeIn">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 class="font-headline-sm text-2xl font-bold text-primary-container dark:text-white">
              Session Slots &amp; Availability
            </h2>
            <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
              Manage individual time slots, set capacities, or schedule bulk recurring weekly sessions
            </p>
          </div>

          <div class="flex items-center gap-2 self-start sm:self-auto">
            <button
              @click="openSingleSlotModal()"
              class="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container text-primary-container dark:text-white font-label-sm text-xs font-bold border border-outline-variant/30 dark:border-slate-700 transition-all"
              type="button"
            >
              <span class="material-symbols-outlined text-sm">add</span>
              <span>Single Slot</span>
            </button>

            <button
              @click="openBulkModal()"
              class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all"
              type="button"
            >
              <span class="material-symbols-outlined text-sm">bolt</span>
              <span>Bulk Generate Slots</span>
            </button>
          </div>
        </div>

        <!-- Filter Controls Bar -->
        <div class="bg-surface-container-lowest dark:bg-slate-900 p-4 rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-xs flex flex-wrap items-center gap-3">
          <div class="flex items-center gap-2">
            <label class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400">Date:</label>
            <input
              v-model="slotFilterDate"
              type="date"
              class="px-3 py-1.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs font-body-sm focus:outline-none"
            />
            <button
              v-if="slotFilterDate"
              @click="slotFilterDate = ''"
              class="text-xs text-secondary underline"
              type="button"
            >
              Clear
            </button>
          </div>

          <div class="flex items-center gap-2">
            <label class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400">Service:</label>
            <select
              v-model="slotFilterService"
              class="px-3 py-1.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs font-body-sm focus:outline-none max-w-xs"
            >
              <option value="all">All Services</option>
              <option v-for="s in services" :key="s.id" :value="s.id">{{ s.title }}</option>
            </select>
          </div>

          <div class="flex items-center gap-2 ml-auto">
            <span class="font-label-sm text-xs font-semibold text-primary-container dark:text-white">
              {{ slots.length }} slots found
            </span>
          </div>
        </div>

        <!-- Slots List / Table -->
        <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-xs overflow-hidden">
          <div v-if="slots.length === 0" class="text-center py-12 text-on-surface-variant dark:text-slate-400 text-sm">
            <span class="material-symbols-outlined text-4xl block mb-2 opacity-50">event_busy</span>
            No session slots found for the selected filters.
            <div class="mt-3">
              <button @click="openBulkModal()" class="text-secondary font-semibold hover:underline">
                Generate bulk slots now
              </button>
            </div>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full text-left text-xs font-body-sm">
              <thead class="bg-surface-container-low dark:bg-slate-800/60 text-on-surface-variant dark:text-slate-400 font-label-sm text-[11px] uppercase tracking-wider border-b border-outline-variant/20 dark:border-slate-800">
                <tr>
                  <th class="px-5 py-3.5">Slot Date</th>
                  <th class="px-5 py-3.5">Start Time</th>
                  <th class="px-5 py-3.5">Period</th>
                  <th class="px-5 py-3.5">Service Offering</th>
                  <th class="px-5 py-3.5">Location</th>
                  <th class="px-5 py-3.5">Capacity</th>
                  <th class="px-5 py-3.5">Status</th>
                  <th class="px-5 py-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-outline-variant/20 dark:divide-slate-800">
                <tr
                  v-for="sl in slots"
                  :key="sl.id"
                  class="hover:bg-surface-container-low/40 dark:hover:bg-slate-800/40 transition-colors"
                >
                  <td class="px-5 py-3.5 font-semibold text-primary-container dark:text-white whitespace-nowrap">
                    {{ sl.slot_date }}
                  </td>
                  <td class="px-5 py-3.5 font-bold whitespace-nowrap">
                    {{ sl.start_time }}
                  </td>
                  <td class="px-5 py-3.5 capitalize text-secondary font-medium">
                    {{ sl.period }}
                  </td>
                  <td class="px-5 py-3.5 text-on-surface dark:text-slate-200 max-w-xs truncate font-medium">
                    {{ getServiceName(sl.service_id) }}
                  </td>
                  <td class="px-5 py-3.5 text-on-surface-variant dark:text-slate-400 truncate max-w-xs">
                    {{ sl.location_name }}
                  </td>
                  <td class="px-5 py-3.5 whitespace-nowrap">
                    <span class="inline-flex items-center gap-1 font-semibold" :class="sl.spots_left === 0 ? 'text-red-500' : 'text-emerald-600 dark:text-emerald-400'">
                      <span class="material-symbols-outlined text-xs">person</span>
                      {{ sl.spots_left }} left
                    </span>
                  </td>
                  <td class="px-5 py-3.5 whitespace-nowrap">
                    <span
                      class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider"
                      :class="sl.is_full ? 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300' : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300'"
                    >
                      {{ sl.is_full ? 'Full' : 'Open' }}
                    </span>
                  </td>
                  <td class="px-5 py-3.5 text-right whitespace-nowrap">
                    <div class="flex items-center justify-end gap-1.5">
                      <button
                        @click="toggleSlotFullStatus(sl)"
                        class="px-2.5 py-1 rounded-full text-[11px] font-medium border border-outline-variant/30 dark:border-slate-700 hover:bg-surface-container-low transition-all"
                        type="button"
                      >
                        {{ sl.is_full ? 'Mark Open' : 'Mark Full' }}
                      </button>
                      <button
                        @click="openEditSlotModal(sl)"
                        class="w-7 h-7 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-primary-container dark:text-white"
                        title="Edit Slot"
                        type="button"
                      >
                        <span class="material-symbols-outlined text-xs">edit</span>
                      </button>
                      <button
                        @click="confirmDeleteSlot(sl)"
                        class="w-7 h-7 rounded-full bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 hover:bg-red-100 flex items-center justify-center"
                        title="Delete Slot"
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
      </section>

      <!-- TAB 4: BOOKINGS & ATTENDEES -->
      <section v-if="activeTab === 'bookings'" class="space-y-6 animate-fadeIn">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 class="font-headline-sm text-2xl font-bold text-primary-container dark:text-white">
              Client Reservations &amp; Roster
            </h2>
            <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
              Manage client attendance, reschedule sessions, update payment statuses, and notes
            </p>
          </div>
        </div>

        <!-- Filter bar -->
        <div class="flex flex-col sm:flex-row items-center gap-3">
          <div class="relative w-full sm:w-80">
            <span class="material-symbols-outlined absolute left-3 top-2.5 text-on-surface-variant text-base">search</span>
            <input
              v-model="bookingSearch"
              type="text"
              placeholder="Search by client, email, ref code..."
              class="w-full pl-9 pr-4 py-2 rounded-2xl bg-surface-container-lowest dark:bg-slate-900 border border-outline-variant/30 dark:border-slate-800 text-xs font-body-sm focus:outline-none focus:ring-2 focus:ring-primary-container/30"
            />
          </div>

          <div class="flex items-center gap-2 overflow-x-auto w-full pb-1 no-scrollbar">
            <button
              v-for="st in ['all', 'confirmed', 'completed', 'cancelled']"
              :key="st"
              @click="bookingStatusFilter = st"
              :class="bookingStatusFilter === st ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-bold' : 'bg-surface-container-low dark:bg-slate-800 text-on-surface-variant dark:text-slate-300'"
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
            No bookings found matching current filters.
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full text-left text-xs font-body-sm">
              <thead class="bg-surface-container-low dark:bg-slate-800/60 text-on-surface-variant dark:text-slate-400 font-label-sm text-[11px] uppercase tracking-wider border-b border-outline-variant/20 dark:border-slate-800">
                <tr>
                  <th class="px-5 py-3.5">Client &amp; Contact</th>
                  <th class="px-5 py-3.5">Service Offering</th>
                  <th class="px-5 py-3.5">Date &amp; Time</th>
                  <th class="px-5 py-3.5">Payment</th>
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
                  <td class="px-5 py-3.5">
                    <div class="font-bold text-primary-container dark:text-white">{{ b.user_name }}</div>
                    <div class="text-[11px] text-on-surface-variant dark:text-slate-400">{{ b.user_email }}</div>
                    <div class="text-[11px] text-secondary font-mono">{{ b.user_phone }}</div>
                  </td>
                  <td class="px-5 py-3.5 font-medium text-on-surface dark:text-slate-200 max-w-xs">
                    <div>{{ b.service_title }}</div>
                    <div class="text-[11px] text-on-surface-variant dark:text-slate-400 truncate">{{ b.location_name }}</div>
                  </td>
                  <td class="px-5 py-3.5 whitespace-nowrap">
                    <div class="font-semibold text-primary-container dark:text-white">{{ b.booking_date }}</div>
                    <div class="text-[11px] text-secondary font-medium">{{ b.time_slot }}</div>
                  </td>
                  <td class="px-5 py-3.5 whitespace-nowrap">
                    <div class="font-bold text-primary-container dark:text-white">
                      {{ b.currency }} {{ (b.total_amount || 0).toLocaleString() }}
                    </div>
                    <div class="text-[10px] text-on-surface-variant dark:text-slate-400 uppercase font-mono">
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
                        @click="setBookingStatus(b, 'completed')"
                        class="px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 font-label-sm text-[11px] font-semibold hover:bg-emerald-100"
                        title="Mark Session Completed"
                        type="button"
                      >
                        Complete
                      </button>
                      <button
                        @click="openEditBookingModal(b)"
                        class="px-3 py-1 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container font-label-sm text-xs font-semibold border border-outline-variant/30 dark:border-slate-700"
                        type="button"
                      >
                        Manage
                      </button>
                      <button
                        @click="confirmDeleteBooking(b)"
                        class="w-7 h-7 rounded-full bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 hover:bg-red-100 flex items-center justify-center"
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
      </section>
    </main>

    <!-- ============================================== -->
    <!-- MODAL 1: ADD / EDIT SERVICE MODAL              -->
    <!-- ============================================== -->
    <div v-if="showServiceModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-fadeIn">
      <div class="bg-surface-container-lowest dark:bg-slate-900 w-full max-w-2xl rounded-3xl p-6 sm:p-8 border border-outline-variant/30 dark:border-slate-800 shadow-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between pb-4 border-b border-outline-variant/20 dark:border-slate-800 mb-6">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-secondary text-2xl">spa</span>
            <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">
              {{ isEditingService ? 'Edit Wellness Service' : 'Add New Wellness Offering' }}
            </h3>
          </div>
          <button @click="showServiceModal = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 flex items-center justify-center text-on-surface-variant font-bold hover:bg-surface-container">
            &times;
          </button>
        </div>

        <form @submit.prevent="saveService" class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="sm:col-span-2">
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Service Title *</label>
              <input v-model="serviceForm.title" type="text" required placeholder="e.g. Restorative Sound Bath" class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:ring-2 focus:ring-primary-container/30 focus:outline-none" />
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Category *</label>
              <select v-model="serviceForm.category" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none">
                <option value="1-1">1:1 Private Session</option>
                <option value="pilates">Pilates Reformer</option>
                <option value="yoga">Holistic Yoga</option>
                <option value="sound">Sound Bath &amp; Vibration</option>
                <option value="therapy">Therapy &amp; Lymphatic</option>
                <option value="mindfulness">Mindfulness &amp; Meditation</option>
                <option value="hormone">Hormone Coaching</option>
                <option value="retreats">Workshops &amp; Retreats</option>
              </select>
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Duration (Minutes) *</label>
              <input v-model.number="serviceForm.duration_minutes" type="number" min="15" step="5" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Price (KES) *</label>
              <input v-model.number="serviceForm.price_kes" type="number" min="0" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Price (EUR) *</label>
              <input v-model.number="serviceForm.price_eur" type="number" min="0" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Capacity Label</label>
              <input v-model="serviceForm.capacity" type="text" placeholder="e.g. Small Group (4–8) or Private 1:1" class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Highlight Badge</label>
              <input v-model="serviceForm.badge" type="text" placeholder="e.g. Popular, Deep Rest, Masterclass" class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>

            <div class="sm:col-span-2">
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Location Display Name</label>
              <input v-model="serviceForm.location_display" type="text" placeholder="e.g. Karen Studio Sanctuary, Nairobi" class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>

            <div class="sm:col-span-2">
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Image URL</label>
              <input v-model="serviceForm.image_url" type="url" placeholder="https://images.unsplash.com/..." class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>

            <div class="sm:col-span-2">
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Description *</label>
              <textarea v-model="serviceForm.description" rows="3" required placeholder="Describe the therapeutic benefits, techniques, and client outcomes..." class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none"></textarea>
            </div>
          </div>

          <div class="pt-4 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-end gap-3">
            <button @click="showServiceModal = false" type="button" class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low">
              Cancel
            </button>
            <button :disabled="submitting" type="submit" class="px-5 py-2 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all">
              {{ submitting ? 'Saving...' : (isEditingService ? 'Update Service' : 'Create Offering') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ============================================== -->
    <!-- MODAL 2: ADD / EDIT SINGLE SLOT MODAL          -->
    <!-- ============================================== -->
    <div v-if="showSlotModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-fadeIn">
      <div class="bg-surface-container-lowest dark:bg-slate-900 w-full max-w-lg rounded-3xl p-6 sm:p-8 border border-outline-variant/30 dark:border-slate-800 shadow-2xl">
        <div class="flex items-center justify-between pb-4 border-b border-outline-variant/20 dark:border-slate-800 mb-6">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-secondary text-2xl">schedule</span>
            <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">
              {{ isEditingSlot ? 'Edit Session Slot' : 'Add Single Session Slot' }}
            </h3>
          </div>
          <button @click="showSlotModal = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 flex items-center justify-center font-bold">
            &times;
          </button>
        </div>

        <form @submit.prevent="saveSlot" class="space-y-4">
          <div>
            <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Service Offering *</label>
            <select v-model="slotForm.service_id" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none">
              <option value="">Select Service...</option>
              <option v-for="s in services" :key="s.id" :value="s.id">{{ s.title }}</option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Session Date *</label>
              <input v-model="slotForm.slot_date" type="date" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Start Time *</label>
              <input v-model="slotForm.start_time" type="text" required placeholder="09:30 AM" class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Period *</label>
              <select v-model="slotForm.period" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none">
                <option value="morning">Morning</option>
                <option value="afternoon">Afternoon</option>
                <option value="evening">Evening</option>
              </select>
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Spots Left / Capacity *</label>
              <input v-model.number="slotForm.spots_left" type="number" min="0" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>
          </div>

          <div>
            <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Location Name</label>
            <input v-model="slotForm.location_name" type="text" placeholder="Karen Studio, Nairobi" class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
          </div>

          <div class="flex items-center gap-3 pt-2">
            <label class="flex items-center gap-2 text-xs font-medium cursor-pointer">
              <input v-model="slotForm.is_full" type="checkbox" class="rounded text-primary-container" />
              <span>Mark as Fully Booked</span>
            </label>
          </div>

          <div class="pt-4 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-end gap-3">
            <button @click="showSlotModal = false" type="button" class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low">
              Cancel
            </button>
            <button :disabled="submitting" type="submit" class="px-5 py-2 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all">
              {{ submitting ? 'Saving...' : (isEditingSlot ? 'Update Slot' : 'Add Slot') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ============================================== -->
    <!-- MODAL 3: BULK GENERATE RECURRING SLOTS MODAL   -->
    <!-- ============================================== -->
    <div v-if="showBulkModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-fadeIn">
      <div class="bg-surface-container-lowest dark:bg-slate-900 w-full max-w-xl rounded-3xl p-6 sm:p-8 border border-outline-variant/30 dark:border-slate-800 shadow-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between pb-4 border-b border-outline-variant/20 dark:border-slate-800 mb-6">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-amber-500 text-2xl">bolt</span>
            <div>
              <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">
                Bulk Generate Recurring Slots
              </h3>
              <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
                Generate recurring weekly timetable across a custom date span
              </p>
            </div>
          </div>
          <button @click="showBulkModal = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 flex items-center justify-center font-bold">
            &times;
          </button>
        </div>

        <form @submit.prevent="generateBulkSlots" class="space-y-4">
          <div>
            <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Target Offering *</label>
            <select v-model="bulkForm.service_id" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none">
              <option value="">Select Service...</option>
              <option v-for="s in services" :key="s.id" :value="s.id">{{ s.title }}</option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Start Date *</label>
              <input v-model="bulkForm.start_date" type="date" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">End Date *</label>
              <input v-model="bulkForm.end_date" type="date" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>
          </div>

          <!-- Days of Week Selector -->
          <div>
            <label class="block font-label-sm text-xs font-semibold mb-1.5 text-on-surface dark:text-slate-300">Days of the Week *</label>
            <div class="grid grid-cols-7 gap-1.5">
              <button
                v-for="day in weekDays"
                :key="day.val"
                @click="toggleDay(day.val)"
                :class="bulkForm.days_of_week.includes(day.val) ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-bold shadow-xs' : 'bg-surface-container-low dark:bg-slate-800 text-on-surface-variant dark:text-slate-400'"
                class="py-2 rounded-xl font-label-sm text-xs text-center transition-all"
                type="button"
              >
                {{ day.label }}
              </button>
            </div>
          </div>

          <!-- Times list -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="font-label-sm text-xs font-semibold text-on-surface dark:text-slate-300">Daily Session Times *</label>
              <button @click="addTimeRow" type="button" class="text-xs text-secondary font-semibold hover:underline flex items-center gap-1">
                <span class="material-symbols-outlined text-xs">add</span> Add Time
              </button>
            </div>
            <div class="space-y-2">
              <div v-for="(t, idx) in bulkForm.times" :key="idx" class="flex items-center gap-2">
                <input v-model="t.start_time" type="text" placeholder="09:30 AM" class="flex-1 px-3 py-1.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
                <select v-model="t.period" class="w-28 px-2 py-1.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none">
                  <option value="morning">Morning</option>
                  <option value="afternoon">Afternoon</option>
                  <option value="evening">Evening</option>
                </select>
                <button v-if="bulkForm.times.length > 1" @click="bulkForm.times.splice(idx, 1)" type="button" class="w-7 h-7 rounded-full text-red-500 hover:bg-red-50 dark:hover:bg-red-950 flex items-center justify-center">
                  &times;
                </button>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Spots Per Slot *</label>
              <input v-model.number="bulkForm.spots_left" type="number" min="1" required class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>
            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Location</label>
              <input v-model="bulkForm.location_name" type="text" class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>
          </div>

          <div class="pt-4 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-end gap-3">
            <button @click="showBulkModal = false" type="button" class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low">
              Cancel
            </button>
            <button :disabled="submitting" type="submit" class="px-5 py-2 rounded-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all">
              {{ submitting ? 'Generating...' : '⚡ Generate Slots' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ============================================== -->
    <!-- MODAL 4: MANAGE CLIENT BOOKING MODAL           -->
    <!-- ============================================== -->
    <div v-if="showBookingModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-fadeIn">
      <div class="bg-surface-container-lowest dark:bg-slate-900 w-full max-w-lg rounded-3xl p-6 sm:p-8 border border-outline-variant/30 dark:border-slate-800 shadow-2xl">
        <div class="flex items-center justify-between pb-4 border-b border-outline-variant/20 dark:border-slate-800 mb-6">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-secondary text-2xl">person_check</span>
            <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">
              Manage Client Reservation
            </h3>
          </div>
          <button @click="showBookingModal = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 flex items-center justify-center font-bold">
            &times;
          </button>
        </div>

        <form @submit.prevent="saveBookingEdit" class="space-y-4">
          <div class="bg-surface-container-low dark:bg-slate-800/80 p-3.5 rounded-2xl border border-outline-variant/20 dark:border-slate-700">
            <p class="font-label-md text-sm font-bold text-primary-container dark:text-white">{{ activeBooking.user_name }}</p>
            <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">{{ activeBooking.user_email }} &bull; {{ activeBooking.user_phone }}</p>
            <p class="font-body-sm text-xs text-secondary font-medium mt-1">{{ activeBooking.service_title }} ({{ activeBooking.currency }} {{ activeBooking.total_amount }})</p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Status</label>
              <select v-model="bookingEditForm.status" class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none">
                <option value="confirmed">Confirmed</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Time Slot</label>
              <input v-model="bookingEditForm.time_slot" type="text" class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>

            <div class="col-span-2">
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Reschedule Date</label>
              <input v-model="bookingEditForm.booking_date" type="date" class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none" />
            </div>
          </div>

          <div>
            <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Internal Coach / Studio Notes</label>
            <textarea v-model="bookingEditForm.coach_notes" rows="3" placeholder="e.g. Focus on shoulder stabilization; client prefer Reformer 02..." class="w-full px-3.5 py-2 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none"></textarea>
          </div>

          <div class="pt-4 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-end gap-3">
            <button @click="showBookingModal = false" type="button" class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low">
              Cancel
            </button>
            <button :disabled="submitting" type="submit" class="px-5 py-2 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all">
              {{ submitting ? 'Updating...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import {
  getAdminOverview,
  getAdminServices,
  createAdminService,
  updateAdminService,
  deleteAdminService,
  getAdminSlots,
  createAdminSlot,
  bulkGenerateAdminSlots,
  updateAdminSlot,
  deleteAdminSlot,
  getAdminBookings,
  updateAdminBooking,
  deleteAdminBooking
} from '@/services/api';

const activeTab = ref('overview');
const loading = ref(false);
const submitting = ref(false);
const bannerMessage = ref('');
const bannerType = ref('success');

const tabs = [
  { id: 'overview', label: 'Overview', icon: 'dashboard' },
  { id: 'services', label: 'Services', icon: 'spa' },
  { id: 'slots', label: 'Sessions & Slots', icon: 'calendar_month' },
  { id: 'bookings', label: 'Bookings & Attendees', icon: 'group' }
];

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
const services = ref([]);
const slots = ref([]);
const bookings = ref([]);

// Filter states
const serviceSearch = ref('');
const serviceCategoryFilter = ref('all');
const serviceCategories = [
  { id: 'all', label: 'All Offerings' },
  { id: '1-1', label: '1:1 Private' },
  { id: 'pilates', label: 'Pilates Reformer' },
  { id: 'yoga', label: 'Holistic Yoga' },
  { id: 'sound', label: 'Sound Bath' },
  { id: 'therapy', label: 'Therapy & Lymphatic' },
  { id: 'mindfulness', label: 'Mindfulness' },
  { id: 'hormone', label: 'Hormone Coaching' },
  { id: 'retreats', label: 'Retreats & Workshops' }
];

const slotFilterDate = ref('');
const slotFilterService = ref('all');

const bookingSearch = ref('');
const bookingStatusFilter = ref('all');

// Modals State
const showServiceModal = ref(false);
const isEditingService = ref(false);
const editingServiceId = ref(null);
const serviceForm = reactive({
  title: '',
  slug: '',
  category: 'pilates',
  duration_minutes: 60,
  price_kes: 3500,
  price_eur: 40,
  capacity: 'Small Group (4–8)',
  badge: '',
  location_display: 'Karen Studio Sanctuary, Nairobi',
  location_type: 'all nairobi',
  image_url: '',
  description: ''
});

const showSlotModal = ref(false);
const isEditingSlot = ref(false);
const editingSlotId = ref(null);
const slotForm = reactive({
  service_id: '',
  slot_date: '',
  start_time: '09:30 AM',
  period: 'morning',
  location_name: 'Karen Studio, Nairobi',
  spots_left: 4,
  is_full: false
});

const showBulkModal = ref(false);
const weekDays = [
  { val: 0, label: 'Mon' },
  { val: 1, label: 'Tue' },
  { val: 2, label: 'Wed' },
  { val: 3, label: 'Thu' },
  { val: 4, label: 'Fri' },
  { val: 5, label: 'Sat' },
  { val: 6, label: 'Sun' }
];
const bulkForm = reactive({
  service_id: '',
  start_date: '',
  end_date: '',
  days_of_week: [0, 2, 4], // Mon, Wed, Fri
  times: [
    { start_time: '08:00 AM', period: 'morning' },
    { start_time: '10:30 AM', period: 'morning' },
    { start_time: '05:30 PM', period: 'evening' }
  ],
  spots_left: 4,
  location_name: 'Karen Studio, Nairobi'
});

const showBookingModal = ref(false);
const activeBooking = ref({});
const bookingEditForm = reactive({
  status: 'confirmed',
  booking_date: '',
  time_slot: '',
  coach_notes: ''
});

// Computed Filters
const filteredServices = computed(() => {
  return services.value.filter(s => {
    const matchCat = serviceCategoryFilter.value === 'all' || s.category === serviceCategoryFilter.value;
    const matchSearch = !serviceSearch.value || s.title.toLowerCase().includes(serviceSearch.value.toLowerCase()) || (s.description || '').toLowerCase().includes(serviceSearch.value.toLowerCase());
    return matchCat && matchSearch;
  });
});

const filteredBookings = computed(() => {
  return bookings.value.filter(b => {
    const matchStatus = bookingStatusFilter.value === 'all' || b.status === bookingStatusFilter.value;
    const q = bookingSearch.value.toLowerCase().trim();
    const matchSearch = !q ||
      (b.user_name || '').toLowerCase().includes(q) ||
      (b.user_email || '').toLowerCase().includes(q) ||
      (b.user_phone || '').toLowerCase().includes(q) ||
      (b.payment_reference || '').toLowerCase().includes(q) ||
      (b.service_title || '').toLowerCase().includes(q);
    return matchStatus && matchSearch;
  });
});

function getServiceName(serviceId) {
  if (!serviceId) return 'General Studio Session';
  const found = services.value.find(s => s.id === serviceId);
  return found ? found.title : 'Selected Offering';
}

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

function notify(msg, type = 'success') {
  bannerMessage.value = msg;
  bannerType.value = type;
  setTimeout(() => {
    if (bannerMessage.value === msg) bannerMessage.value = '';
  }, 5000);
}

// Data Fetchers
async function fetchOverview() {
  try {
    const res = await getAdminOverview();
    metrics.value = res.metrics || {};
    recentBookings.value = res.recent_bookings || [];
  } catch (e) {
    console.error('fetchOverview error:', e);
  }
}

async function fetchServices() {
  try {
    services.value = await getAdminServices();
  } catch (e) {
    console.error('fetchServices error:', e);
  }
}

async function fetchSlots() {
  try {
    slots.value = await getAdminSlots({
      date: slotFilterDate.value || undefined,
      serviceId: slotFilterService.value || undefined
    });
  } catch (e) {
    console.error('fetchSlots error:', e);
  }
}

async function fetchBookings() {
  try {
    bookings.value = await getAdminBookings();
  } catch (e) {
    console.error('fetchBookings error:', e);
  }
}

async function refreshCurrentTab() {
  loading.value = true;
  await Promise.allSettled([
    fetchOverview(),
    fetchServices(),
    fetchSlots(),
    fetchBookings()
  ]);
  loading.value = false;
  notify('Studio operations synchronized with database.');
}

// Service Actions
function openServiceModal(existing = null) {
  if (existing) {
    isEditingService.value = true;
    editingServiceId.value = existing.id;
    serviceForm.title = existing.title || '';
    serviceForm.slug = existing.slug || '';
    serviceForm.category = existing.category || 'pilates';
    serviceForm.duration_minutes = existing.duration_minutes || 60;
    serviceForm.price_kes = existing.price_kes || 3500;
    serviceForm.price_eur = existing.price_eur || 40;
    serviceForm.capacity = existing.capacity || 'Small Group (4–8)';
    serviceForm.badge = existing.badge || '';
    serviceForm.location_display = existing.location_display || 'Karen Studio Sanctuary, Nairobi';
    serviceForm.location_type = existing.location_type || 'all nairobi';
    serviceForm.image_url = existing.image_url || '';
    serviceForm.description = existing.description || '';
  } else {
    isEditingService.value = false;
    editingServiceId.value = null;
    serviceForm.title = '';
    serviceForm.slug = '';
    serviceForm.category = 'pilates';
    serviceForm.duration_minutes = 60;
    serviceForm.price_kes = 3500;
    serviceForm.price_eur = 40;
    serviceForm.capacity = 'Small Group (4–8)';
    serviceForm.badge = '';
    serviceForm.location_display = 'Karen Studio Sanctuary, Nairobi';
    serviceForm.location_type = 'all nairobi';
    serviceForm.image_url = 'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80';
    serviceForm.description = '';
  }
  showServiceModal.value = true;
}

async function saveService() {
  submitting.value = true;
  try {
    if (isEditingService.value) {
      await updateAdminService(editingServiceId.value, serviceForm);
      notify(`Service "${serviceForm.title}" updated successfully.`);
    } else {
      await createAdminService(serviceForm);
      notify(`Service "${serviceForm.title}" created successfully.`);
    }
    showServiceModal.value = false;
    await fetchServices();
    await fetchOverview();
  } catch (err) {
    notify(err.message, 'error');
  } finally {
    submitting.value = false;
  }
}

async function confirmDeleteService(service) {
  if (!confirm(`Are you sure you want to delete "${service.title}"? Associated time slots will also be removed.`)) {
    return;
  }
  try {
    await deleteAdminService(service.id);
    notify(`Service "${service.title}" deleted.`);
    await fetchServices();
    await fetchOverview();
  } catch (err) {
    notify(err.message, 'error');
  }
}

// Single Slot Actions
function openSingleSlotModal(existing = null) {
  if (existing) {
    isEditingSlot.value = true;
    editingSlotId.value = existing.id;
    slotForm.service_id = existing.service_id || '';
    slotForm.slot_date = existing.slot_date || '';
    slotForm.start_time = existing.start_time || '09:30 AM';
    slotForm.period = existing.period || 'morning';
    slotForm.location_name = existing.location_name || 'Karen Studio, Nairobi';
    slotForm.spots_left = existing.spots_left || 4;
    slotForm.is_full = !!existing.is_full;
  } else {
    isEditingSlot.value = false;
    editingSlotId.value = null;
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    slotForm.service_id = services.value[0]?.id || '';
    slotForm.slot_date = tomorrow.toISOString().split('T')[0];
    slotForm.start_time = '09:30 AM';
    slotForm.period = 'morning';
    slotForm.location_name = 'Karen Studio, Nairobi';
    slotForm.spots_left = 4;
    slotForm.is_full = false;
  }
  showSlotModal.value = true;
}

function openEditSlotModal(slot) {
  openSingleSlotModal(slot);
}

async function saveSlot() {
  submitting.value = true;
  try {
    if (isEditingSlot.value) {
      await updateAdminSlot(editingSlotId.value, slotForm);
      notify('Session slot updated successfully.');
    } else {
      await createAdminSlot(slotForm);
      notify('New session slot created.');
    }
    showSlotModal.value = false;
    await fetchSlots();
    await fetchOverview();
  } catch (err) {
    notify(err.message, 'error');
  } finally {
    submitting.value = false;
  }
}

async function toggleSlotFullStatus(slot) {
  try {
    const updated = await updateAdminSlot(slot.id, { is_full: !slot.is_full });
    slot.is_full = updated.is_full;
    notify(`Slot marked as ${slot.is_full ? 'Full' : 'Open'}.`);
  } catch (err) {
    notify(err.message, 'error');
  }
}

async function confirmDeleteSlot(slot) {
  if (!confirm(`Delete slot for ${slot.slot_date} at ${slot.start_time}?`)) return;
  try {
    await deleteAdminSlot(slot.id);
    notify('Slot removed.');
    await fetchSlots();
    await fetchOverview();
  } catch (err) {
    notify(err.message, 'error');
  }
}

// Bulk Generator Actions
function openBulkModal() {
  const today = new Date();
  const nextMonth = new Date();
  nextMonth.setDate(today.getDate() + 28);
  bulkForm.service_id = services.value[0]?.id || '';
  bulkForm.start_date = today.toISOString().split('T')[0];
  bulkForm.end_date = nextMonth.toISOString().split('T')[0];
  bulkForm.days_of_week = [0, 2, 4];
  bulkForm.spots_left = 4;
  bulkForm.location_name = 'Karen Studio, Nairobi';
  showBulkModal.value = true;
}

function toggleDay(val) {
  const idx = bulkForm.days_of_week.indexOf(val);
  if (idx > -1) {
    bulkForm.days_of_week.splice(idx, 1);
  } else {
    bulkForm.days_of_week.push(val);
  }
}

function addTimeRow() {
  bulkForm.times.push({ start_time: '02:00 PM', period: 'afternoon' });
}

async function generateBulkSlots() {
  if (bulkForm.days_of_week.length === 0) {
    notify('Please select at least one day of the week.', 'error');
    return;
  }
  submitting.value = true;
  try {
    const res = await bulkGenerateAdminSlots(bulkForm);
    notify(res.message || `Successfully generated ${res.count} session slots.`);
    showBulkModal.value = false;
    await fetchSlots();
    await fetchOverview();
  } catch (err) {
    notify(err.message, 'error');
  } finally {
    submitting.value = false;
  }
}

// Booking Actions
function openEditBookingModal(booking) {
  activeBooking.value = booking;
  bookingEditForm.status = booking.status || 'confirmed';
  bookingEditForm.booking_date = booking.booking_date || '';
  bookingEditForm.time_slot = booking.time_slot || '';
  bookingEditForm.coach_notes = booking.coach_notes || '';
  showBookingModal.value = true;
}

async function saveBookingEdit() {
  submitting.value = true;
  try {
    await updateAdminBooking(activeBooking.value.id, bookingEditForm);
    notify(`Booking for ${activeBooking.value.user_name} updated.`);
    showBookingModal.value = false;
    await fetchBookings();
    await fetchOverview();
  } catch (err) {
    notify(err.message, 'error');
  } finally {
    submitting.value = false;
  }
}

async function setBookingStatus(booking, newStatus) {
  try {
    await updateAdminBooking(booking.id, { status: newStatus });
    booking.status = newStatus;
    notify(`Booking status changed to ${newStatus}.`);
    await fetchOverview();
  } catch (err) {
    notify(err.message, 'error');
  }
}

async function confirmDeleteBooking(booking) {
  if (!confirm(`Delete reservation record for ${booking.user_name}?`)) return;
  try {
    await deleteAdminBooking(booking.id);
    notify('Booking record removed.');
    await fetchBookings();
    await fetchOverview();
  } catch (err) {
    notify(err.message, 'error');
  }
}

onMounted(async () => {
  await refreshCurrentTab();
});
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.25s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
