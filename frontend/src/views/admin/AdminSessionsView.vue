<template>
  <div class="space-y-6 animate-fadeIn">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">
          Session Scheduling &amp; Slot Engine
        </h3>
        <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
          Manage individual session times, capacity constraints, or automate weekly recurring schedules
        </p>
      </div>

      <div class="flex items-center gap-2 self-start sm:self-auto">
        <button
          @click="openSingleModal()"
          class="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container text-primary-container dark:text-white font-label-sm text-xs font-bold border border-outline-variant/30 dark:border-slate-700 transition-all"
          type="button"
        >
          <span class="material-symbols-outlined text-sm">add</span>
          <span>Add Single Slot</span>
        </button>

        <button
          @click="openBulkModal()"
          class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all"
          type="button"
        >
          <span class="material-symbols-outlined text-sm">bolt</span>
          <span>⚡ Bulk Generate Slots</span>
        </button>
      </div>
    </div>

    <!-- Notice -->
    <div v-if="notice" class="p-3.5 rounded-2xl flex items-center justify-between gap-2 text-xs font-medium" :class="noticeType === 'error' ? 'bg-red-50 text-red-800 dark:bg-red-950/50 dark:text-red-300' : 'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300'">
      <span>{{ notice }}</span>
      <button @click="notice = ''" class="font-bold">&times;</button>
    </div>

    <!-- Filters Bar -->
    <div class="bg-surface-container-lowest dark:bg-slate-900 p-4 rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-xs flex flex-wrap items-center gap-3">
      <div class="flex items-center gap-2">
        <label class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400">Date:</label>
        <input
          v-model="filterDate"
          type="date"
          @change="loadSlots"
          class="px-3 py-1.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs font-body-sm focus:outline-none"
        />
        <button
          v-if="filterDate"
          @click="filterDate = ''; loadSlots()"
          class="text-xs text-secondary underline"
          type="button"
        >
          All Dates
        </button>
      </div>

      <div class="flex items-center gap-2">
        <label class="font-label-sm text-xs text-on-surface-variant dark:text-slate-400">Offering:</label>
        <select
          v-model="filterService"
          @change="loadSlots"
          class="px-3 py-1.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs font-body-sm focus:outline-none max-w-xs"
        >
          <option value="all">All Services</option>
          <option v-for="s in services" :key="s.id" :value="s.id">{{ s.title }}</option>
        </select>
      </div>

      <div class="ml-auto flex items-center gap-2">
        <span class="font-label-sm text-xs font-semibold text-primary-container dark:text-white">
          {{ slots.length }} slots shown
        </span>
      </div>
    </div>

    <!-- Slots Table -->
    <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-xs overflow-hidden">
      <div v-if="slots.length === 0" class="text-center py-12 text-on-surface-variant dark:text-slate-400 text-sm">
        <span class="material-symbols-outlined text-4xl block mb-2 opacity-50">event_busy</span>
        No scheduled slots found for the selected filter.
        <div class="mt-3">
          <button @click="openBulkModal" class="text-secondary font-semibold hover:underline">
            Generate bulk slots now
          </button>
        </div>
      </div>

      <!-- Mobile Session Cards (< 768px) -->
      <div v-else class="md:hidden divide-y divide-outline-variant/20 dark:divide-slate-800">
        <div
          v-for="sl in slots"
          :key="'m-' + sl.id"
          class="p-4 space-y-2.5 hover:bg-surface-container-low/40 dark:hover:bg-slate-800/40 transition-colors"
        >
          <div class="flex items-center justify-between gap-2">
            <div class="flex items-center gap-2">
              <span class="font-headline-sm text-sm font-bold text-primary-container dark:text-white">
                {{ sl.start_time }}
              </span>
              <span class="text-xs text-on-surface-variant dark:text-slate-400 font-mono">
                {{ sl.slot_date }}
              </span>
            </div>
            <span
              class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider"
              :class="sl.is_full ? 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300' : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300'"
            >
              {{ sl.is_full ? 'Full' : 'Open' }}
            </span>
          </div>

          <div>
            <h4 class="font-label-md text-xs font-bold text-primary-container dark:text-white">
              {{ getServiceName(sl.service_id) }}
            </h4>
            <p class="font-body-sm text-[11px] text-on-surface-variant dark:text-slate-400 truncate">
              {{ sl.location_name }}
            </p>
          </div>

          <div class="flex items-center justify-between pt-1">
            <span class="inline-flex items-center gap-1 font-semibold text-xs" :class="sl.spots_left === 0 ? 'text-red-500' : 'text-emerald-600 dark:text-emerald-400'">
              <span class="material-symbols-outlined text-xs">person</span>
              {{ sl.spots_left }} spots left
            </span>

            <div class="flex items-center gap-1.5">
              <button
                @click="toggleFull(sl)"
                class="px-2.5 py-1 rounded-full text-[11px] font-medium border border-outline-variant/30 dark:border-slate-700 hover:bg-surface-container-low transition-all"
                type="button"
              >
                {{ sl.is_full ? 'Mark Open' : 'Mark Full' }}
              </button>
              <button
                @click="openSingleModal(sl)"
                class="w-7 h-7 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-primary-container dark:text-white"
                title="Edit Slot"
                type="button"
              >
                <span class="material-symbols-outlined text-xs">edit</span>
              </button>
              <button
                @click="removeSlot(sl)"
                class="w-7 h-7 rounded-full bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 hover:bg-red-100 flex items-center justify-center"
                title="Delete Slot"
                type="button"
              >
                <span class="material-symbols-outlined text-xs">delete</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Desktop Session Table (>= 768px) -->
      <div v-if="slots.length > 0" class="hidden md:block overflow-x-auto">
        <table class="w-full text-left text-xs font-body-sm">
          <thead class="bg-surface-container-low dark:bg-slate-800/60 text-on-surface-variant dark:text-slate-400 font-label-sm text-[11px] uppercase tracking-wider border-b border-outline-variant/20 dark:border-slate-800">
            <tr>
              <th class="px-5 py-3.5">Date</th>
              <th class="px-5 py-3.5">Time</th>
              <th class="px-5 py-3.5">Period</th>
              <th class="px-5 py-3.5">Service</th>
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
                    @click="toggleFull(sl)"
                    class="px-2.5 py-1 rounded-full text-[11px] font-medium border border-outline-variant/30 dark:border-slate-700 hover:bg-surface-container-low transition-all"
                    type="button"
                  >
                    {{ sl.is_full ? 'Mark Open' : 'Mark Full' }}
                  </button>
                  <button
                    @click="openSingleModal(sl)"
                    class="w-7 h-7 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-primary-container dark:text-white"
                    title="Edit Slot"
                    type="button"
                  >
                    <span class="material-symbols-outlined text-xs">edit</span>
                  </button>
                  <button
                    @click="removeSlot(sl)"
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

    <!-- Modal 1: Single Slot (Teleported) -->
    <Teleport to="body">
      <div v-if="showSingleModal" class="fixed inset-0 z-[100] flex items-center justify-center p-3.5 sm:p-4 bg-black/60 backdrop-blur-sm overflow-y-auto animate-fadeIn">
        <div class="bg-surface-container-lowest dark:bg-slate-900 w-full max-w-lg rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-2xl flex flex-col max-h-[85vh] sm:max-h-[88vh] overflow-hidden my-auto">
          
          <!-- Sticky Header -->
          <div class="shrink-0 px-5 sm:px-7 py-4 border-b border-outline-variant/20 dark:border-slate-800 flex items-center justify-between bg-surface-container-lowest dark:bg-slate-900">
            <h3 class="font-headline-sm text-base sm:text-lg font-bold text-primary-container dark:text-white">
              {{ isEditing ? 'Edit Session Slot' : 'Add Single Session Slot' }}
            </h3>
            <button @click="showSingleModal = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-on-surface dark:text-slate-300 font-bold transition-colors">
              &times;
            </button>
          </div>

          <!-- Scrollable Body with form -->
          <form id="singleSlotForm" @submit.prevent="submitSingleSlot" class="flex-1 min-h-0 overflow-y-auto p-5 sm:p-7 space-y-4">
            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Service Offering *</label>
              <select v-model="singleForm.service_id" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white">
                <option value="">Select Service...</option>
                <option v-for="s in services" :key="s.id" :value="s.id">{{ s.title }}</option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Date *</label>
                <input v-model="singleForm.slot_date" type="date" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Start Time *</label>
                <input v-model="singleForm.start_time" type="text" required placeholder="09:30 AM" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Period *</label>
                <select v-model="singleForm.period" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white">
                  <option value="morning">Morning</option>
                  <option value="afternoon">Afternoon</option>
                  <option value="evening">Evening</option>
                </select>
              </div>

              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Spots Left *</label>
                <input v-model.number="singleForm.spots_left" type="number" min="0" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Session Theme / Workshop Title (Optional)</label>
              <input v-model="singleForm.session_theme" type="text" placeholder="e.g. Full Moon Sound Immersion or Pelvic Floor Reset" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
            </div>

            <!-- Workshop / Masterclass Banner Upload -->
            <div class="space-y-2">
              <label class="block font-label-sm text-xs font-semibold text-on-surface dark:text-slate-300">
                Special Workshop / Session Promotional Banner (Optional, up to 10MB)
              </label>
              
              <div class="flex items-start gap-4">
                <div class="relative w-20 h-20 rounded-2xl overflow-hidden border border-outline-variant/30 dark:border-slate-700 bg-surface-container-low dark:bg-slate-800 shrink-0 flex items-center justify-center">
                  <img 
                    v-if="bannerPreviewUrl || singleForm.banner_url" 
                    :src="bannerPreviewUrl || singleForm.banner_url" 
                    alt="Banner Preview" 
                    class="w-full h-full object-cover"
                  />
                  <div v-else class="text-center p-1 text-on-surface-variant dark:text-slate-500">
                    <span class="material-symbols-outlined text-xl">wallpaper</span>
                    <p class="text-[8px]">No Banner</p>
                  </div>
                </div>

                <div class="flex-1 space-y-1.5">
                  <div 
                    @click="$refs.bannerFileInput.click()"
                    class="border-2 border-dashed border-outline-variant/40 dark:border-slate-700 hover:border-secondary rounded-2xl p-2.5 text-center cursor-pointer transition-colors bg-surface-container-low/40 dark:bg-slate-800/40"
                  >
                    <input 
                      ref="bannerFileInput" 
                      type="file" 
                      accept=".jpg,.jpeg,.png,.webp" 
                      @change="handleBannerSelect" 
                      class="hidden" 
                    />
                    <span class="material-symbols-outlined text-lg text-secondary">add_photo_alternate</span>
                    <p class="text-xs font-medium text-on-surface dark:text-slate-200">
                      {{ selectedBannerFile ? selectedBannerFile.name : 'Upload custom session poster' }}
                    </p>
                  </div>
                  <button 
                    v-if="selectedBannerFile || bannerPreviewUrl" 
                    @click="clearBannerFile" 
                    type="button" 
                    class="text-[10px] text-error font-semibold hover:underline"
                  >
                    Clear selected banner
                  </button>
                </div>
              </div>
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Location</label>
              <input v-model="singleForm.location_name" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
            </div>

            <div class="flex items-center gap-3 pt-2">
              <label class="flex items-center gap-2 text-xs font-medium cursor-pointer">
                <input v-model="singleForm.is_full" type="checkbox" class="rounded text-primary-container focus:ring-0" />
                <span>Mark as Fully Booked</span>
              </label>
            </div>
          </form>

          <!-- Sticky Action Footer -->
          <div class="shrink-0 px-5 sm:px-7 py-3.5 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-end gap-3 bg-surface-container-lowest dark:bg-slate-900 pb-safe">
            <button @click="showSingleModal = false" type="button" class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low transition-colors">
              Cancel
            </button>
            <button form="singleSlotForm" :disabled="submitting" type="submit" class="px-5 py-2.5 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all disabled:opacity-50">
              {{ submitting ? 'Saving...' : (isEditing ? 'Save Changes' : 'Create Slot') }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Modal 2: Bulk Slot Generator (Teleported) -->
    <Teleport to="body">
      <div v-if="showBulkModal" class="fixed inset-0 z-[100] flex items-center justify-center p-3.5 sm:p-4 bg-black/60 backdrop-blur-sm overflow-y-auto animate-fadeIn">
        <div class="bg-surface-container-lowest dark:bg-slate-900 w-full max-w-xl rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-2xl flex flex-col max-h-[85vh] sm:max-h-[88vh] overflow-hidden my-auto">
          
          <!-- Sticky Header -->
          <div class="shrink-0 px-5 sm:px-7 py-4 border-b border-outline-variant/20 dark:border-slate-800 flex items-center justify-between bg-surface-container-lowest dark:bg-slate-900">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-amber-500 text-2xl">bolt</span>
              <div>
                <h3 class="font-headline-sm text-base sm:text-lg font-bold text-primary-container dark:text-white">
                  Bulk Recurring Slot Generator
                </h3>
                <p class="font-body-sm text-[11px] text-on-surface-variant dark:text-slate-400">
                  Generate weekly schedule across date spans with one click
                </p>
              </div>
            </div>
            <button @click="showBulkModal = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-on-surface dark:text-slate-300 font-bold transition-colors">
              &times;
            </button>
          </div>

          <!-- Scrollable Body with form -->
          <form id="bulkSlotForm" @submit.prevent="submitBulk" class="flex-1 min-h-0 overflow-y-auto p-5 sm:p-7 space-y-4">
            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Target Offering *</label>
              <select v-model="bulkForm.service_id" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white">
                <option value="">Select Service...</option>
                <option v-for="s in services" :key="s.id" :value="s.id">{{ s.title }}</option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Start Date *</label>
                <input v-model="bulkForm.start_date" type="date" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">End Date *</label>
                <input v-model="bulkForm.end_date" type="date" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>
            </div>

            <div>
              <label class="block font-label-sm text-xs font-semibold mb-1.5 text-on-surface dark:text-slate-300">Days of the Week *</label>
              <div class="grid grid-cols-7 gap-1.5">
                <button
                  v-for="day in weekDays"
                  :key="day.val"
                  @click="toggleDay(day.val)"
                  :class="bulkForm.days_of_week.includes(day.val) ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-bold' : 'bg-surface-container-low dark:bg-slate-800 text-on-surface-variant dark:text-slate-400'"
                  class="py-2 rounded-xl font-label-sm text-xs text-center transition-all"
                  type="button"
                >
                  {{ day.label }}
                </button>
              </div>
            </div>

            <div>
              <div class="flex items-center justify-between mb-1.5">
                <label class="font-label-sm text-xs font-semibold text-on-surface dark:text-slate-300">Daily Session Times *</label>
                <button @click="addTime" type="button" class="text-xs text-secondary dark:text-sky-300 font-semibold hover:underline flex items-center gap-1">
                  <span class="material-symbols-outlined text-xs">add</span> Add Time
                </button>
              </div>
              <div class="space-y-2">
                <div v-for="(t, idx) in bulkForm.times" :key="idx" class="flex items-center gap-2">
                  <input v-model="t.start_time" type="text" placeholder="09:30 AM" class="flex-1 px-3 py-1.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none text-on-surface dark:text-white" />
                  <select v-model="t.period" class="w-28 px-2 py-1.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none text-on-surface dark:text-white">
                    <option value="morning">Morning</option>
                    <option value="afternoon">Afternoon</option>
                    <option value="evening">Evening</option>
                  </select>
                  <button v-if="bulkForm.times.length > 1" @click="bulkForm.times.splice(idx, 1)" type="button" class="w-7 h-7 text-red-500 hover:bg-red-50 rounded-full flex items-center justify-center">
                    &times;
                  </button>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Spots Per Slot *</label>
                <input v-model.number="bulkForm.spots_left" type="number" min="1" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none text-on-surface dark:text-white" />
              </div>
              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Location</label>
                <input v-model="bulkForm.location_name" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none text-on-surface dark:text-white" />
              </div>
            </div>
          </form>

          <!-- Sticky Action Footer -->
          <div class="shrink-0 px-5 sm:px-7 py-3.5 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-end gap-3 bg-surface-container-lowest dark:bg-slate-900 pb-safe">
            <button @click="showBulkModal = false" type="button" class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low transition-colors">
              Cancel
            </button>
            <button form="bulkSlotForm" :disabled="submitting" type="submit" class="px-5 py-2.5 rounded-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all disabled:opacity-50">
              {{ submitting ? 'Generating...' : '⚡ Generate Slots' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { 
  getAdminServices, 
  getAdminSlots, 
  createAdminSlot, 
  updateAdminSlot, 
  deleteAdminSlot, 
  bulkGenerateAdminSlots,
  uploadSessionBanner,
  deleteSessionBanner 
} from '@/services/api';

const services = ref([]);
const slots = ref([]);
const filterDate = ref('');
const filterService = ref('all');
const notice = ref('');
const noticeType = ref('success');
const submitting = ref(false);

const selectedBannerFile = ref(null);
const bannerPreviewUrl = ref(null);

const showSingleModal = ref(false);
const isEditing = ref(false);
const editingId = ref(null);
const singleForm = reactive({
  service_id: '',
  slot_date: '',
  start_time: '09:30 AM',
  period: 'morning',
  location_name: 'Karen Studio, Nairobi',
  spots_left: 4,
  is_full: false,
  session_theme: '',
  banner_url: ''
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
  days_of_week: [0, 2, 4],
  times: [
    { start_time: '08:00 AM', period: 'morning' },
    { start_time: '10:30 AM', period: 'morning' },
    { start_time: '05:30 PM', period: 'evening' }
  ],
  spots_left: 4,
  location_name: 'Karen Studio, Nairobi'
});

function getServiceName(sId) {
  if (!sId) return 'General Studio Session';
  const found = services.value.find(s => s.id === sId);
  return found ? found.title : 'Selected Offering';
}

async function loadServices() {
  try {
    services.value = await getAdminServices();
  } catch (e) {
    console.error(e);
  }
}

async function loadSlots() {
  try {
    slots.value = await getAdminSlots({
      date: filterDate.value || undefined,
      serviceId: filterService.value || undefined
    });
  } catch (e) {
    console.error(e);
  }
}

function handleBannerSelect(e) {
  const file = e.target.files?.[0];
  if (!file) return;

  if (file.size > 10 * 1024 * 1024) {
    alert('Banner file size exceeds 10 MB limit.');
    return;
  }

  selectedBannerFile.value = file;
  bannerPreviewUrl.value = URL.createObjectURL(file);
}

function clearBannerFile() {
  selectedBannerFile.value = null;
  if (bannerPreviewUrl.value) {
    URL.revokeObjectURL(bannerPreviewUrl.value);
    bannerPreviewUrl.value = null;
  }
}

function openSingleModal(item = null) {
  clearBannerFile();
  if (item) {
    isEditing.value = true;
    editingId.value = item.id;
    singleForm.service_id = item.service_id || item.service || '';
    singleForm.slot_date = item.slot_date;
    singleForm.start_time = item.start_time;
    singleForm.period = item.period;
    singleForm.location_name = item.location_name;
    singleForm.spots_left = item.spots_left;
    singleForm.is_full = !!item.is_full;
    singleForm.session_theme = item.session_theme || '';
    singleForm.banner_url = item.banner_url || item.banner_image_url || '';
  } else {
    isEditing.value = false;
    editingId.value = null;
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    singleForm.service_id = services.value[0]?.id || '';
    singleForm.slot_date = tomorrow.toISOString().split('T')[0];
    singleForm.start_time = '09:30 AM';
    singleForm.period = 'morning';
    singleForm.location_name = 'Karen Studio, Nairobi';
    singleForm.spots_left = 4;
    singleForm.is_full = false;
    singleForm.session_theme = '';
    singleForm.banner_url = '';
  }
  showSingleModal.value = true;
}

async function submitSingleSlot() {
  submitting.value = true;
  try {
    let savedSlot = null;
    if (isEditing.value) {
      savedSlot = await updateAdminSlot(editingId.value, singleForm);
      notice.value = 'Session slot updated successfully.';
    } else {
      savedSlot = await createAdminSlot(singleForm);
      notice.value = 'New session slot created.';
    }

    // Upload banner image file if one was selected
    if (selectedBannerFile.value && savedSlot?.id) {
      await uploadSessionBanner(savedSlot.id, selectedBannerFile.value);
    }

    noticeType.value = 'success';
    showSingleModal.value = false;
    clearBannerFile();
    await loadSlots();
  } catch (err) {
    notice.value = err.message;
    noticeType.value = 'error';
  } finally {
    submitting.value = false;
  }
}

async function toggleFull(sl) {
  try {
    const updated = await updateAdminSlot(sl.id, { is_full: !sl.is_full });
    sl.is_full = updated.is_full;
    notice.value = `Slot marked as ${sl.is_full ? 'Full' : 'Open'}.`;
    noticeType.value = 'success';
  } catch (e) {
    notice.value = e.message;
    noticeType.value = 'error';
  }
}

async function removeSlot(sl) {
  if (!confirm(`Delete slot for ${sl.slot_date} at ${sl.start_time}?`)) return;
  try {
    await deleteAdminSlot(sl.id);
    notice.value = 'Slot removed.';
    noticeType.value = 'success';
    await loadSlots();
  } catch (e) {
    notice.value = e.message;
    noticeType.value = 'error';
  }
}

function openBulkModal() {
  const today = new Date();
  const nextMonth = new Date();
  nextMonth.setDate(today.getDate() + 28);
  bulkForm.service_id = services.value[0]?.id || '';
  bulkForm.start_date = today.toISOString().split('T')[0];
  bulkForm.end_date = nextMonth.toISOString().split('T')[0];
  showBulkModal.value = true;
}

function toggleDay(val) {
  const idx = bulkForm.days_of_week.indexOf(val);
  if (idx > -1) bulkForm.days_of_week.splice(idx, 1);
  else bulkForm.days_of_week.push(val);
}

function addTime() {
  bulkForm.times.push({ start_time: '02:00 PM', period: 'afternoon' });
}

async function submitBulk() {
  if (bulkForm.days_of_week.length === 0) {
    notice.value = 'Please select at least one day of the week.';
    noticeType.value = 'error';
    return;
  }
  submitting.value = true;
  try {
    const res = await bulkGenerateAdminSlots(bulkForm);
    notice.value = res.message || `Successfully generated ${res.count} slots.`;
    noticeType.value = 'success';
    showBulkModal.value = false;
    await loadSlots();
  } catch (e) {
    notice.value = e.message;
    noticeType.value = 'error';
  } finally {
    submitting.value = false;
  }
}

onMounted(async () => {
  await loadServices();
  await loadSlots();
});
</script>
