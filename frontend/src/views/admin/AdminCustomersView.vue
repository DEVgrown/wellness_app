<template>
  <div class="space-y-6 animate-fadeIn">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">
          Customer Directory &amp; CRM
        </h3>
        <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
          Manage registered clients, review personal booking histories, track lifetime spend, and issue class packages
        </p>
      </div>

      <div class="flex items-center gap-2 self-start sm:self-auto">
        <button
          @click="openCreateModal"
          class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all"
          type="button"
        >
          <span class="material-symbols-outlined text-sm">person_add</span>
          <span>Onboard New Client</span>
        </button>

        <button
          @click="loadCustomers"
          class="w-9 h-9 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-on-surface transition-colors"
          title="Refresh"
          type="button"
        >
          <span class="material-symbols-outlined text-sm">refresh</span>
        </button>
      </div>
    </div>

    <!-- Notice Banner -->
    <div v-if="notice" class="p-3.5 rounded-2xl flex items-center justify-between gap-2 text-xs font-medium" :class="noticeType === 'error' ? 'bg-red-50 text-red-800 dark:bg-red-950/50 dark:text-red-300' : 'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300'">
      <span>{{ notice }}</span>
      <button @click="notice = ''" class="font-bold">&times;</button>
    </div>

    <!-- Metrics Summary Bar -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div class="bg-surface-container-lowest dark:bg-slate-900 p-4 rounded-2xl border border-outline-variant/30 dark:border-slate-800">
        <p class="font-label-sm text-[11px] text-on-surface-variant dark:text-slate-400 uppercase tracking-wider">Total Clients</p>
        <h4 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white mt-0.5">
          {{ customers.length }}
        </h4>
      </div>

      <div class="bg-surface-container-lowest dark:bg-slate-900 p-4 rounded-2xl border border-outline-variant/30 dark:border-slate-800">
        <p class="font-label-sm text-[11px] text-on-surface-variant dark:text-slate-400 uppercase tracking-wider">Active Bookers</p>
        <h4 class="font-headline-sm text-xl font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">
          {{ activeBookersCount }}
        </h4>
      </div>

      <div class="bg-surface-container-lowest dark:bg-slate-900 p-4 rounded-2xl border border-outline-variant/30 dark:border-slate-800">
        <p class="font-label-sm text-[11px] text-on-surface-variant dark:text-slate-400 uppercase tracking-wider">Pass Holders</p>
        <h4 class="font-headline-sm text-xl font-bold text-secondary dark:text-sky-300 mt-0.5">
          {{ passHoldersCount }}
        </h4>
      </div>

      <div class="bg-surface-container-lowest dark:bg-slate-900 p-4 rounded-2xl border border-outline-variant/30 dark:border-slate-800">
        <p class="font-label-sm text-[11px] text-on-surface-variant dark:text-slate-400 uppercase tracking-wider">Total Client Spend</p>
        <h4 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white mt-0.5">
          KES {{ totalClientSpend.toLocaleString() }}
        </h4>
      </div>
    </div>

    <!-- Filter & Search Bar -->
    <div class="flex flex-col sm:flex-row items-center gap-3">
      <div class="relative w-full sm:w-80">
        <span class="material-symbols-outlined absolute left-3 top-2.5 text-on-surface-variant text-base">search</span>
        <input
          v-model="search"
          type="text"
          placeholder="Search by client name, email, or phone..."
          class="w-full pl-9 pr-4 py-2 rounded-2xl bg-surface-container-lowest dark:bg-slate-900 border border-outline-variant/30 dark:border-slate-800 text-xs font-body-sm focus:outline-none focus:ring-2 focus:ring-primary-container/30"
        />
      </div>

      <div class="flex items-center gap-2 overflow-x-auto w-full pb-1 no-scrollbar">
        <button
          v-for="st in filterTabs"
          :key="st.id"
          @click="selectedTab = st.id"
          :class="selectedTab === st.id ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-bold' : 'bg-surface-container-low dark:bg-slate-800 text-on-surface-variant dark:text-slate-300'"
          class="px-3.5 py-1.5 rounded-full font-label-sm text-xs whitespace-nowrap transition-all"
          type="button"
        >
          {{ st.label }}
        </button>
      </div>
    </div>

    <!-- Customers Table -->
    <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-xs overflow-hidden">
      <div v-if="filteredCustomers.length === 0" class="text-center py-12 text-on-surface-variant dark:text-slate-400 text-sm">
        <span class="material-symbols-outlined text-4xl block mb-2 opacity-50">person_search</span>
        No customer accounts match your search or filter.
      </div>

      <!-- Mobile Customers Cards (< 768px) -->
      <div v-else class="md:hidden divide-y divide-outline-variant/20 dark:divide-slate-800">
        <div
          v-for="c in filteredCustomers"
          :key="'mc-' + c.id"
          class="p-4 space-y-2.5 hover:bg-surface-container-low/40 dark:hover:bg-slate-800/40 transition-colors"
        >
          <div class="flex items-center justify-between gap-2">
            <div class="flex items-center gap-2.5">
              <div class="w-9 h-9 rounded-full bg-secondary-container/40 dark:bg-slate-800 text-secondary dark:text-sky-300 font-bold flex items-center justify-center text-xs shrink-0">
                {{ (c.name || c.username || 'C').charAt(0).toUpperCase() }}
              </div>
              <div>
                <h4 class="font-headline-sm text-sm font-bold text-primary-container dark:text-white">
                  {{ c.name }}
                </h4>
                <p class="font-body-sm text-[11px] text-on-surface-variant dark:text-slate-400 font-mono">
                  @{{ c.username }}
                </p>
              </div>
            </div>

            <div class="flex items-center gap-1.5">
              <span
                class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase"
                :class="c.is_staff ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300' : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300'"
              >
                {{ c.is_staff ? 'Admin' : 'Client' }}
              </span>
              <span
                class="w-2 h-2 rounded-full"
                :class="c.is_active ? 'bg-emerald-500' : 'bg-red-400'"
                :title="c.is_active ? 'Active' : 'Disabled'"
              ></span>
            </div>
          </div>

          <div class="text-xs text-on-surface-variant dark:text-slate-400">
            <div>{{ c.email }}</div>
            <div v-if="c.phone" class="font-mono text-[11px] text-secondary">{{ c.phone }}</div>
          </div>

          <div class="grid grid-cols-3 gap-2 bg-surface-container-low dark:bg-slate-800/60 p-2.5 rounded-xl border border-outline-variant/20 dark:border-slate-800 text-center">
            <div>
              <span class="block font-bold text-primary-container dark:text-white text-xs">{{ c.total_bookings }}</span>
              <span class="text-[10px] text-on-surface-variant dark:text-slate-400">Bookings</span>
            </div>
            <div>
              <span class="block font-bold text-primary-container dark:text-white text-xs">KES {{ (c.total_spend_kes || 0).toLocaleString() }}</span>
              <span class="text-[10px] text-on-surface-variant dark:text-slate-400">Total Spend</span>
            </div>
            <div>
              <span class="block font-bold text-xs" :class="c.active_passes > 0 ? 'text-sky-600 dark:text-sky-400' : 'text-slate-500'">
                {{ c.active_passes > 0 ? `${c.active_passes} left` : 'None' }}
              </span>
              <span class="text-[10px] text-on-surface-variant dark:text-slate-400">Pass Balance</span>
            </div>
          </div>

          <div class="flex items-center justify-end pt-1">
            <button
              @click="openCustomerDetail(c)"
              class="w-full sm:w-auto px-4 py-2 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-semibold shadow-xs transition-all text-center"
              type="button"
            >
              Manage Client Profile &amp; Passes
            </button>
          </div>
        </div>
      </div>

      <!-- Desktop Customers Table (>= 768px) -->
      <div v-if="filteredCustomers.length > 0" class="hidden md:block overflow-x-auto">
        <table class="w-full text-left text-xs font-body-sm">
          <thead class="bg-surface-container-low dark:bg-slate-800/60 text-on-surface-variant dark:text-slate-400 font-label-sm text-[11px] uppercase tracking-wider border-b border-outline-variant/20 dark:border-slate-800">
            <tr>
              <th class="px-5 py-3.5">Customer &amp; Profile</th>
              <th class="px-5 py-3.5">Contact Details</th>
              <th class="px-5 py-3.5">Bookings History</th>
              <th class="px-5 py-3.5">Total Spend</th>
              <th class="px-5 py-3.5">Pass Balance</th>
              <th class="px-5 py-3.5">Role &amp; Status</th>
              <th class="px-5 py-3.5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-outline-variant/20 dark:divide-slate-800">
            <tr
              v-for="c in filteredCustomers"
              :key="c.id"
              class="hover:bg-surface-container-low/40 dark:hover:bg-slate-800/40 transition-colors"
            >
              <td class="px-5 py-3.5">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-secondary-container/40 dark:bg-slate-800 text-secondary dark:text-sky-300 font-bold flex items-center justify-center text-xs shrink-0">
                    {{ (c.name || c.username || 'C').charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <div class="font-bold text-primary-container dark:text-white">{{ c.name }}</div>
                    <div class="text-[11px] text-on-surface-variant dark:text-slate-400 font-mono">@{{ c.username }}</div>
                  </div>
                </div>
              </td>

              <td class="px-5 py-3.5">
                <div class="text-on-surface dark:text-slate-200">{{ c.email }}</div>
                <div class="text-[11px] text-secondary font-mono">{{ c.phone || 'No phone recorded' }}</div>
              </td>

              <td class="px-5 py-3.5 whitespace-nowrap">
                <div class="font-semibold text-primary-container dark:text-white">
                  {{ c.total_bookings }} total
                </div>
                <div class="text-[10px] text-on-surface-variant dark:text-slate-400">
                  {{ c.completed_bookings }} completed &bull; {{ c.confirmed_bookings }} confirmed
                </div>
              </td>

              <td class="px-5 py-3.5 whitespace-nowrap font-bold text-primary-container dark:text-white">
                KES {{ (c.total_spend_kes || 0).toLocaleString() }}
              </td>

              <td class="px-5 py-3.5 whitespace-nowrap">
                <span
                  class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider"
                  :class="c.active_passes > 0 ? 'bg-sky-100 text-sky-800 dark:bg-sky-950 dark:text-sky-300' : 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'"
                >
                  {{ c.active_passes > 0 ? `${c.active_passes} sessions` : 'No pass' }}
                </span>
              </td>

              <td class="px-5 py-3.5 whitespace-nowrap">
                <div class="flex items-center gap-1.5">
                  <span
                    class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase"
                    :class="c.is_staff ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300' : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300'"
                  >
                    {{ c.is_staff ? 'Admin' : 'Client' }}
                  </span>
                  <span
                    class="w-2 h-2 rounded-full"
                    :class="c.is_active ? 'bg-emerald-500' : 'bg-red-400'"
                    :title="c.is_active ? 'Active Account' : 'Disabled Account'"
                  ></span>
                </div>
              </td>

              <td class="px-5 py-3.5 text-right whitespace-nowrap">
                <div class="flex items-center justify-end gap-1.5">
                  <button
                    @click="openCustomerDetail(c)"
                    class="px-3 py-1 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-semibold shadow-xs transition-all"
                    type="button"
                  >
                    Manage Client
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ============================================== -->
    <!-- MODAL 1: CUSTOMER DEEP DIVE & BOOKINGS DRAWER  -->
    <!-- ============================================== -->
    <Teleport to="body">
      <div v-if="showDetailModal" class="fixed inset-0 z-[100] flex items-center justify-center p-3.5 sm:p-4 bg-black/60 backdrop-blur-sm overflow-y-auto animate-fadeIn">
        <div class="bg-surface-container-lowest dark:bg-slate-900 w-full max-w-3xl rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-2xl flex flex-col max-h-[85vh] sm:max-h-[88vh] overflow-hidden my-auto">
          
          <!-- Sticky Header -->
          <div class="shrink-0 px-5 sm:px-7 py-4 border-b border-outline-variant/20 dark:border-slate-800 flex items-center justify-between bg-surface-container-lowest dark:bg-slate-900">
            <div class="flex items-center gap-3 min-w-0">
              <div class="w-10 h-10 rounded-2xl bg-secondary-container/40 dark:bg-slate-800 text-secondary dark:text-sky-300 font-bold flex items-center justify-center text-base shrink-0">
                {{ (detailCustomer.user?.name || 'C').charAt(0).toUpperCase() }}
              </div>
              <div class="min-w-0">
                <h3 class="font-headline-sm text-base sm:text-lg font-bold text-primary-container dark:text-white truncate">
                  {{ detailCustomer.user?.name || detailCustomer.user?.username }}
                </h3>
                <p class="font-body-sm text-[11px] text-on-surface-variant dark:text-slate-400 truncate">
                  {{ detailCustomer.user?.email }} &bull; Member since {{ detailCustomer.user?.date_joined?.slice(0, 10) }}
                </p>
              </div>
            </div>
            <button @click="showDetailModal = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-on-surface dark:text-slate-300 font-bold transition-colors">
              &times;
            </button>
          </div>

          <!-- Sticky Navigation Tabs -->
          <div class="shrink-0 px-5 sm:px-7 pt-4 pb-2 bg-surface-container-lowest dark:bg-slate-900 border-b border-outline-variant/20 dark:border-slate-800">
            <div class="flex p-1 bg-surface-container-low dark:bg-slate-800/80 rounded-full">
              <button
                v-for="t in ['profile', 'bookings', 'passes']"
                :key="t"
                @click="activeDetailTab = t"
                :class="activeDetailTab === t ? 'bg-surface-container-lowest dark:bg-slate-700 text-primary-container dark:text-white font-bold shadow-xs' : 'text-on-surface-variant dark:text-slate-400'"
                class="flex-1 py-1.5 rounded-full font-label-sm text-xs capitalize transition-all"
                type="button"
              >
                {{ t === 'passes' ? 'Session Passes' : (t === 'bookings' ? `Bookings (${detailCustomer.bookings?.length || 0})` : 'Profile & Data') }}
              </button>
            </div>
          </div>

          <!-- Scrollable Body with Sub-Tabs -->
          <div class="flex-1 min-h-0 overflow-y-auto p-5 sm:p-7 space-y-4">
            <!-- SUB-TAB 1: Profile Edit -->
            <div v-if="activeDetailTab === 'profile'" class="space-y-4">
              <form id="customerProfileForm" @submit.prevent="saveCustomerProfile" class="space-y-4">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">First Name</label>
                    <input v-model="editProfileForm.first_name" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none text-on-surface dark:text-white" />
                  </div>

                  <div>
                    <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Last Name</label>
                    <input v-model="editProfileForm.last_name" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none text-on-surface dark:text-white" />
                  </div>

                  <div class="sm:col-span-2">
                    <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Email Address</label>
                    <input v-model="editProfileForm.email" type="email" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none text-on-surface dark:text-white" />
                  </div>

                  <div>
                    <label class="flex items-center gap-2 text-xs font-semibold cursor-pointer pt-2">
                      <input v-model="editProfileForm.is_active" type="checkbox" class="rounded text-primary-container" />
                      <span>Account Active</span>
                    </label>
                  </div>

                  <div>
                    <label class="flex items-center gap-2 text-xs font-semibold cursor-pointer pt-2">
                      <input v-model="editProfileForm.is_staff" type="checkbox" class="rounded text-primary-container" />
                      <span>Grant Admin / Staff Access</span>
                    </label>
                  </div>
                </div>
              </form>
            </div>

            <!-- SUB-TAB 2: User's Bookings List -->
            <div v-if="activeDetailTab === 'bookings'" class="space-y-3">
              <div v-if="!detailCustomer.bookings || detailCustomer.bookings.length === 0" class="text-center py-8 text-on-surface-variant dark:text-slate-400 text-xs">
                This customer has no recorded bookings yet.
              </div>

              <div v-else class="space-y-2.5">
                <div
                  v-for="b in detailCustomer.bookings"
                  :key="b.id"
                  class="p-3.5 rounded-2xl bg-surface-container-low dark:bg-slate-800/80 border border-outline-variant/20 dark:border-slate-700 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
                >
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="font-bold text-primary-container dark:text-white">{{ b.service_title }}</span>
                      <span
                        class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider"
                        :class="b.status === 'confirmed' ? 'bg-emerald-100 text-emerald-800' : (b.status === 'completed' ? 'bg-sky-100 text-sky-800' : 'bg-red-100 text-red-800')"
                      >
                        {{ b.status }}
                      </span>
                    </div>
                    <p class="text-on-surface-variant dark:text-slate-400 mt-0.5">
                      {{ b.booking_date }} at {{ b.time_slot }} &bull; {{ b.location_name }}
                    </p>
                    <p v-if="b.coach_notes" class="text-secondary dark:text-sky-300 font-medium mt-1">
                      Practitioner note: {{ b.coach_notes }}
                    </p>
                  </div>

                  <div class="text-right shrink-0">
                    <span class="font-bold text-primary-container dark:text-white block">
                      {{ b.currency }} {{ (b.total_amount || 0).toLocaleString() }}
                    </span>
                    <span class="text-[10px] text-on-surface-variant dark:text-slate-400 font-mono">
                      {{ b.payment_reference }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- SUB-TAB 3: Session Passes & Grant Pass -->
            <div v-if="activeDetailTab === 'passes'" class="space-y-6">
              <!-- Existing Passes List -->
              <div>
                <h4 class="font-headline-sm text-sm font-bold text-primary-container dark:text-white mb-2">Active Packages &amp; Passes</h4>
                <div v-if="!detailCustomer.packages || detailCustomer.packages.length === 0" class="p-4 rounded-2xl bg-surface-container-low dark:bg-slate-800 text-center text-xs text-on-surface-variant dark:text-slate-400">
                  No active session passes for this customer.
                </div>
                <div v-else class="space-y-2">
                  <div
                    v-for="p in detailCustomer.packages"
                    :key="p.id"
                    class="p-3.5 rounded-2xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/20 dark:border-slate-700 flex items-center justify-between text-xs"
                  >
                    <div>
                      <p class="font-bold text-primary-container dark:text-white">{{ p.package_name }}</p>
                      <p class="text-[11px] text-on-surface-variant dark:text-slate-400">Valid until: {{ p.valid_until }}</p>
                    </div>
                    <div class="text-right">
                      <span class="font-bold text-secondary dark:text-sky-300 text-sm">
                        {{ p.remaining_sessions }} / {{ p.total_sessions }}
                      </span>
                      <span class="block text-[10px] text-on-surface-variant dark:text-slate-400">sessions remaining</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Issue New Pass Form -->
              <div class="p-4 rounded-2xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700">
                <h4 class="font-headline-sm text-sm font-bold text-primary-container dark:text-white mb-2">Issue / Credit Session Pass</h4>
                <form @submit.prevent="submitIssuePass" class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div>
                    <label class="block font-label-sm text-[11px] font-semibold mb-1 text-on-surface dark:text-slate-300">Package Name</label>
                    <input v-model="passForm.package_name" type="text" required placeholder="e.g. 5x Reformer Pass" class="w-full px-3 py-2 rounded-xl bg-surface-container-lowest dark:bg-slate-900 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none text-on-surface dark:text-white" />
                  </div>
                  <div>
                    <label class="block font-label-sm text-[11px] font-semibold mb-1 text-on-surface dark:text-slate-300">Sessions Count</label>
                    <input v-model.number="passForm.total_sessions" type="number" min="1" required class="w-full px-3 py-2 rounded-xl bg-surface-container-lowest dark:bg-slate-900 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none text-on-surface dark:text-white" />
                  </div>
                  <div>
                    <label class="block font-label-sm text-[11px] font-semibold mb-1 text-on-surface dark:text-slate-300">Valid Until</label>
                    <input v-model="passForm.valid_until" type="text" placeholder="31 Dec 2026" class="w-full px-3 py-2 rounded-xl bg-surface-container-lowest dark:bg-slate-900 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none text-on-surface dark:text-white" />
                  </div>
                  <div class="sm:col-span-3 flex justify-end">
                    <button :disabled="submitting" type="submit" class="px-5 py-2 rounded-full bg-secondary hover:bg-secondary/90 text-white font-label-sm text-xs font-semibold shadow-xs active:scale-95 transition-all">
                      Grant Pass
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>

          <!-- Sticky Action Footer -->
          <div class="shrink-0 px-5 sm:px-7 py-3.5 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-between bg-surface-container-lowest dark:bg-slate-900 pb-safe">
            <span class="text-xs text-on-surface-variant dark:text-slate-400">
              Viewing Client: <strong class="text-primary-container dark:text-white">{{ detailCustomer.user?.name || detailCustomer.user?.username }}</strong>
            </span>
            <div class="flex items-center gap-3">
              <button @click="showDetailModal = false" type="button" class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low transition-colors">
                Close
              </button>
              <button v-if="activeDetailTab === 'profile'" form="customerProfileForm" :disabled="submitting" type="submit" class="px-5 py-2.5 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all disabled:opacity-50">
                {{ submitting ? 'Updating...' : 'Save Profile Changes' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ============================================== -->
    <!-- MODAL 2: ONBOARD NEW CLIENT MODAL              -->
    <!-- ============================================== -->
    <Teleport to="body">
      <div v-if="showCreateModal" class="fixed inset-0 z-[100] flex items-center justify-center p-3.5 sm:p-4 bg-black/60 backdrop-blur-sm overflow-y-auto animate-fadeIn">
        <div class="bg-surface-container-lowest dark:bg-slate-900 w-full max-w-lg rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-2xl flex flex-col max-h-[85vh] sm:max-h-[88vh] overflow-hidden my-auto">
          
          <!-- Sticky Header -->
          <div class="shrink-0 px-5 sm:px-7 py-4 border-b border-outline-variant/20 dark:border-slate-800 flex items-center justify-between bg-surface-container-lowest dark:bg-slate-900">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-secondary text-2xl">person_add</span>
              <h3 class="font-headline-sm text-base sm:text-lg font-bold text-primary-container dark:text-white">
                Onboard New Client
              </h3>
            </div>
            <button @click="showCreateModal = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-on-surface dark:text-slate-300 font-bold transition-colors">
              &times;
            </button>
          </div>

          <!-- Scrollable Body with form -->
          <form id="createCustomerForm" @submit.prevent="submitCreateCustomer" class="flex-1 min-h-0 overflow-y-auto p-5 sm:p-7 space-y-4">
            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Full Name *</label>
              <input v-model="createForm.name" type="text" required placeholder="e.g. Amara Mwangi" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Username *</label>
                <input v-model="createForm.username" type="text" required placeholder="amara_m" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Phone (M-Pesa)</label>
                <input v-model="createForm.phone" type="tel" placeholder="+254 712 000 000" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Email Address *</label>
              <input v-model="createForm.email" type="email" required placeholder="amara@example.com" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Initial Password</label>
              <input v-model="createForm.password" type="text" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none font-mono text-on-surface dark:text-white" />
            </div>

            <div>
              <label class="flex items-center gap-2 text-xs font-medium cursor-pointer pt-2">
                <input v-model="createForm.is_staff" type="checkbox" class="rounded text-primary-container" />
                <span>Grant Studio Administrator Privileges</span>
              </label>
            </div>
          </form>

          <!-- Sticky Action Footer -->
          <div class="shrink-0 px-5 sm:px-7 py-3.5 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-end gap-3 bg-surface-container-lowest dark:bg-slate-900 pb-safe">
            <button @click="showCreateModal = false" type="button" class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low transition-colors">
              Cancel
            </button>
            <button form="createCustomerForm" :disabled="submitting" type="submit" class="px-5 py-2.5 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all disabled:opacity-50">
              {{ submitting ? 'Creating...' : 'Register Client' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { getAdminCustomers, getAdminCustomerDetail, updateAdminCustomer, createAdminCustomer, issueCustomerPass } from '@/services/api';

const customers = ref([]);
const search = ref('');
const selectedTab = ref('all');
const notice = ref('');
const noticeType = ref('success');
const submitting = ref(false);

const filterTabs = [
  { id: 'all', label: 'All Clients' },
  { id: 'active_bookers', label: 'Active Bookers' },
  { id: 'pass_holders', label: 'Pass Holders' },
  { id: 'staff', label: 'Admin Staff' }
];

const showDetailModal = ref(false);
const activeDetailTab = ref('profile');
const detailCustomer = ref({});
const editProfileForm = reactive({
  first_name: '',
  last_name: '',
  email: '',
  is_active: true,
  is_staff: false
});

const passForm = reactive({
  package_name: 'Complimentary Studio Pass',
  total_sessions: 1,
  valid_until: '31 Dec 2026'
});

const showCreateModal = ref(false);
const createForm = reactive({
  name: '',
  username: '',
  email: '',
  phone: '+254 ',
  password: 'Welcome123!',
  is_staff: false
});

const filteredCustomers = computed(() => {
  return customers.value.filter(c => {
    if (selectedTab.value === 'staff' && !c.is_staff) return false;
    if (selectedTab.value === 'active_bookers' && c.total_bookings === 0) return false;
    if (selectedTab.value === 'pass_holders' && c.active_passes === 0) return false;

    const q = search.value.toLowerCase().trim();
    if (!q) return true;
    return (c.name || '').toLowerCase().includes(q) ||
           (c.username || '').toLowerCase().includes(q) ||
           (c.email || '').toLowerCase().includes(q) ||
           (c.phone || '').toLowerCase().includes(q);
  });
});

const activeBookersCount = computed(() => customers.value.filter(c => c.total_bookings > 0).length);
const passHoldersCount = computed(() => customers.value.filter(c => c.active_passes > 0).length);
const totalClientSpend = computed(() => customers.value.reduce((acc, c) => acc + (c.total_spend_kes || 0), 0));

async function loadCustomers() {
  try {
    customers.value = await getAdminCustomers();
  } catch (e) {
    console.error(e);
  }
}

async function openCustomerDetail(c) {
  try {
    const detail = await getAdminCustomerDetail(c.id);
    detailCustomer.value = detail;
    editProfileForm.first_name = detail.user.first_name || '';
    editProfileForm.last_name = detail.user.last_name || '';
    editProfileForm.email = detail.user.email || '';
    editProfileForm.is_active = !!detail.user.is_active;
    editProfileForm.is_staff = !!detail.user.is_staff;
    activeDetailTab.value = 'profile';
    showDetailModal.value = true;
  } catch (err) {
    notice.value = err.message;
    noticeType.value = 'error';
  }
}

async function saveCustomerProfile() {
  submitting.value = true;
  try {
    await updateAdminCustomer(detailCustomer.value.user.id, editProfileForm);
    notice.value = 'Client profile updated.';
    noticeType.value = 'success';
    await loadCustomers();
    showDetailModal.value = false;
  } catch (err) {
    notice.value = err.message;
    noticeType.value = 'error';
  } finally {
    submitting.value = false;
  }
}

async function submitIssuePass() {
  submitting.value = true;
  try {
    await issueCustomerPass(detailCustomer.value.user.id, passForm);
    notice.value = `Issued ${passForm.total_sessions} sessions to client.`;
    noticeType.value = 'success';
    // Refresh detail
    const updated = await getAdminCustomerDetail(detailCustomer.value.user.id);
    detailCustomer.value = updated;
    await loadCustomers();
  } catch (err) {
    notice.value = err.message;
    noticeType.value = 'error';
  } finally {
    submitting.value = false;
  }
}

function openCreateModal() {
  createForm.name = '';
  createForm.username = '';
  createForm.email = '';
  createForm.phone = '+254 ';
  createForm.password = 'Welcome123!';
  createForm.is_staff = false;
  showCreateModal.value = true;
}

async function submitCreateCustomer() {
  submitting.value = true;
  try {
    await createAdminCustomer(createForm);
    notice.value = `Client "${createForm.username}" registered successfully with starter pass.`;
    noticeType.value = 'success';
    showCreateModal.value = false;
    await loadCustomers();
  } catch (err) {
    notice.value = err.message;
    noticeType.value = 'error';
  } finally {
    submitting.value = false;
  }
}

onMounted(() => {
  loadCustomers();
});
</script>
