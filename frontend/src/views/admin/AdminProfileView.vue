<template>
  <div class="space-y-6 animate-fadeIn pb-12">
    <!-- Top Header Banner -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-outline-variant/20 dark:border-slate-800">
      <div>
        <div class="flex items-center gap-2 text-xs text-on-surface-variant dark:text-slate-400 mb-1">
          <router-link to="/admin/overview" class="hover:underline text-secondary">Admin Portal</router-link>
          <span>/</span>
          <span class="text-primary-container dark:text-white font-medium">Administrator Profile</span>
        </div>
        <h1 class="font-headline-lg text-2xl sm:text-3xl font-bold text-primary-container dark:text-white tracking-tight">
          Admin Profile &amp; Settings
        </h1>
        <p class="font-body-md text-sm text-on-surface-variant dark:text-slate-400 mt-0.5">
          Manage your administrator identity, bio, avatar framing, and platform security credentials.
        </p>
      </div>

      <div class="flex items-center gap-2.5">
        <router-link 
          to="/profile" 
          class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container text-xs font-semibold text-primary-container dark:text-white border border-outline-variant/30 dark:border-slate-700 transition-all shadow-2xs"
          title="Open in Consumer View"
        >
          <span class="material-symbols-outlined text-sm text-secondary">visibility</span>
          <span>Consumer View</span>
        </router-link>

        <router-link 
          to="/admin/overview" 
          class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-primary-container hover:bg-primary text-white text-xs font-semibold shadow-xs transition-all"
        >
          <span class="material-symbols-outlined text-sm">dashboard</span>
          <span>Overview</span>
        </router-link>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="pageLoading" class="py-20 flex flex-col items-center justify-center text-center">
      <div class="w-10 h-10 border-3 border-secondary border-t-transparent rounded-full animate-spin mb-3"></div>
      <p class="text-xs text-on-surface-variant dark:text-slate-400">Loading administrator profile...</p>
    </div>

    <div v-else class="space-y-6">
      <!-- Admin Hero Identity Card -->
      <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-sm border border-outline-variant/30 dark:border-slate-800">
        <div class="flex flex-col sm:flex-row items-center sm:items-start gap-6">
          
          <!-- Avatar Display with Dynamic Initial Fallback -->
          <div class="relative group shrink-0 flex flex-col items-center">
            <div 
              class="w-28 h-28 sm:w-32 sm:h-32 rounded-full overflow-hidden ring-4 ring-primary-container/20 dark:ring-sky-500/30 shadow-md bg-surface-container-low dark:bg-slate-800 flex items-center justify-center relative transition-all duration-300"
            >
              <img 
                v-if="form.avatar_url && !previewAvatarFailed" 
                :src="form.avatar_url" 
                alt="Admin Avatar" 
                class="w-full h-full object-cover transition-all duration-300"
                @error="previewAvatarFailed = true"
              />
              <div 
                v-else 
                class="w-full h-full bg-primary-container text-white font-bold text-4xl flex items-center justify-center select-none shadow-inner"
              >
                {{ userInitial }}
              </div>

              <!-- Uploading Spinner Overlay -->
              <div 
                v-if="avatarUploading" 
                class="absolute inset-0 bg-black/60 backdrop-blur-xs flex items-center justify-center text-white"
              >
                <span class="material-symbols-outlined animate-spin text-2xl">sync</span>
              </div>
            </div>

            <!-- Avatar Action Buttons -->
            <div class="mt-3.5 flex items-center justify-center gap-2 flex-wrap">
              <label 
                class="cursor-pointer inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-primary-container hover:bg-primary text-white text-[11px] font-semibold shadow-xs transition-all active:scale-95"
                title="Upload new photo"
              >
                <span class="material-symbols-outlined text-sm">photo_camera</span>
                <span>{{ form.avatar_url ? 'Change Photo' : 'Upload Photo' }}</span>
                <input 
                  type="file" 
                  accept="image/jpeg,image/png,image/webp" 
                  class="hidden" 
                  @change="handleFileSelected" 
                  :disabled="avatarUploading"
                />
              </label>

              <!-- Reframe button -->
              <button 
                v-if="form.avatar_url && !previewAvatarFailed"
                @click="openCropWithCurrentAvatar"
                type="button"
                :disabled="avatarUploading"
                class="inline-flex items-center gap-1 px-3 py-1.5 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container text-primary-container dark:text-white text-[11px] font-semibold border border-outline-variant/30 dark:border-slate-700 transition-colors"
                title="Adjust crop framing & position"
              >
                <span class="material-symbols-outlined text-sm text-secondary">crop</span>
                <span>Reframe</span>
              </button>

              <!-- Delete Avatar -->
              <button 
                v-if="form.avatar_url"
                @click="handleAvatarDelete"
                type="button"
                :disabled="avatarUploading"
                class="w-8 h-8 rounded-full bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 hover:bg-red-100 flex items-center justify-center border border-red-200 dark:border-red-900 transition-colors"
                title="Remove profile photo"
              >
                <span class="material-symbols-outlined text-sm">delete</span>
              </button>
            </div>

            <span v-if="previewAvatarFailed" class="text-[10px] text-amber-600 dark:text-amber-400 mt-1">
              Using letter initial fallback
            </span>
          </div>

          <!-- Admin Header Info -->
          <div class="flex-1 text-center sm:text-left">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
              <div>
                <h2 class="font-headline-sm text-xl sm:text-2xl font-bold text-primary-container dark:text-white">
                  {{ displayName }}
                </h2>
                <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
                  @{{ form.username }} &bull; {{ form.email }}
                </p>
              </div>

              <!-- Admin Verification Badges -->
              <div class="flex items-center gap-2">
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/80 text-emerald-700 dark:text-emerald-300 font-label-sm text-xs font-bold border border-emerald-300 dark:border-emerald-800 shadow-2xs">
                  <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  <span>{{ isSuperuser ? 'Platform Superuser' : 'Studio Administrator' }}</span>
                </span>
              </div>
            </div>

            <p v-if="form.bio" class="font-body-sm text-xs text-on-surface-variant dark:text-slate-300 bg-surface dark:bg-slate-800/60 p-3 rounded-2xl border border-outline-variant/20 dark:border-slate-800 mt-2">
              "{{ form.bio }}"
            </p>

            <!-- Quick Metadata Pills -->
            <div class="flex flex-wrap items-center justify-center sm:justify-start gap-3 mt-4 text-[11px] text-on-surface-variant dark:text-slate-400">
              <span class="flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium">
                <span class="material-symbols-outlined text-xs">verified_user</span>
                <span>Role: Full Studio RBAC</span>
              </span>
              <span>&bull;</span>
              <span class="flex items-center gap-1">
                <span class="material-symbols-outlined text-xs text-secondary">calendar_today</span>
                <span>Admin since {{ memberSinceDisplay }}</span>
              </span>
              <span>&bull;</span>
              <span class="flex items-center gap-1">
                <span class="material-symbols-outlined text-xs text-secondary">security</span>
                <span>Simple JWT Authenticated</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Edit Form & System Privileges Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        <!-- Left: Editable Personal & Contact Details (8 Cols) -->
        <div class="lg:col-span-8 space-y-6">
          <form @submit.prevent="submitProfileUpdate" class="space-y-6">
            
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-7 shadow-sm border border-outline-variant/30 dark:border-slate-800">
              <h3 class="font-headline-sm text-base font-bold text-primary-container dark:text-white flex items-center gap-2 mb-4 pb-3 border-b border-outline-variant/20 dark:border-slate-800">
                <span class="material-symbols-outlined text-secondary text-lg">badge</span>
                <span>Personal &amp; Contact Credentials</span>
              </h3>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block font-label-sm text-xs font-semibold text-on-surface dark:text-slate-300 mb-1.5">
                    First Name
                  </label>
                  <input 
                    v-model="form.first_name" 
                    type="text" 
                    placeholder="Enter first name"
                    class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs text-on-surface dark:text-white focus:outline-none focus:ring-2 focus:ring-secondary/40 transition-all"
                  />
                </div>

                <div>
                  <label class="block font-label-sm text-xs font-semibold text-on-surface dark:text-slate-300 mb-1.5">
                    Last Name
                  </label>
                  <input 
                    v-model="form.last_name" 
                    type="text" 
                    placeholder="Enter last name"
                    class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs text-on-surface dark:text-white focus:outline-none focus:ring-2 focus:ring-secondary/40 transition-all"
                  />
                </div>

                <div>
                  <label class="block font-label-sm text-xs font-semibold text-on-surface dark:text-slate-300 mb-1.5">
                    Admin Email Address
                  </label>
                  <input 
                    :value="form.email" 
                    type="email" 
                    disabled
                    class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-high/40 dark:bg-slate-800/40 border border-outline-variant/20 dark:border-slate-800 text-xs text-on-surface-variant dark:text-slate-500 cursor-not-allowed"
                  />
                  <p class="text-[10px] text-on-surface-variant dark:text-slate-500 mt-1">
                    Primary administrative credentials. Protected by Django grade RBAC.
                  </p>
                </div>

                <div>
                  <label class="block font-label-sm text-xs font-semibold text-on-surface dark:text-slate-300 mb-1.5">
                    Direct Phone Number
                  </label>
                  <input 
                    v-model="form.phone" 
                    type="text" 
                    placeholder="+254 700 000 000"
                    class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs text-on-surface dark:text-white focus:outline-none focus:ring-2 focus:ring-secondary/40 transition-all"
                  />
                  <p class="text-[10px] text-on-surface-variant dark:text-slate-500 mt-1">
                    Used for studio alert notifications and administrative dispatch.
                  </p>
                </div>
              </div>

              <div class="mt-4">
                <label class="block font-label-sm text-xs font-semibold text-on-surface dark:text-slate-300 mb-1.5">
                  Admin Bio &amp; Studio Philosophy
                </label>
                <textarea 
                  v-model="form.bio" 
                  rows="2" 
                  placeholder="Founder & Master Movement Practitioner at Karina Wellness Sanctuary..."
                  class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs text-on-surface dark:text-white focus:outline-none focus:ring-2 focus:ring-secondary/40 transition-all"
                ></textarea>
              </div>
            </div>

            <!-- Emergency & Additional Notes -->
            <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-7 shadow-sm border border-outline-variant/30 dark:border-slate-800">
              <h3 class="font-headline-sm text-base font-bold text-primary-container dark:text-white flex items-center gap-2 mb-4 pb-3 border-b border-outline-variant/20 dark:border-slate-800">
                <span class="material-symbols-outlined text-secondary text-lg">contact_emergency</span>
                <span>Emergency Contact &amp; Studio Notes</span>
              </h3>

              <div class="space-y-4">
                <div>
                  <label class="block font-label-sm text-xs font-semibold text-on-surface dark:text-slate-300 mb-1.5">
                    Emergency Contact Information
                  </label>
                  <input 
                    v-model="form.emergency_contact" 
                    type="text" 
                    placeholder="e.g. Studio Security / Senior Co-Founder - +254 700 999 888"
                    class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs text-on-surface dark:text-white focus:outline-none focus:ring-2 focus:ring-secondary/40 transition-all"
                  />
                </div>

                <div>
                  <label class="block font-label-sm text-xs font-semibold text-on-surface dark:text-slate-300 mb-1.5">
                    Administrative &amp; Movement Notes
                  </label>
                  <textarea 
                    v-model="form.somatic_notes" 
                    rows="2" 
                    placeholder="Internal instructor notes, teaching schedules, or somatic instructions..."
                    class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs text-on-surface dark:text-white focus:outline-none focus:ring-2 focus:ring-secondary/40 transition-all"
                  ></textarea>
                </div>
              </div>
            </div>

            <!-- Save Action Button -->
            <div class="flex items-center justify-end pt-2">
              <button 
                type="submit" 
                :disabled="saving"
                class="inline-flex items-center gap-2 px-8 py-3 rounded-full bg-primary-container hover:bg-primary text-white font-label-md text-xs font-bold shadow-md hover:shadow-lg active:scale-95 transition-all disabled:opacity-50"
              >
                <span v-if="saving" class="material-symbols-outlined animate-spin text-sm">sync</span>
                <span v-else class="material-symbols-outlined text-sm">check_circle</span>
                <span>{{ saving ? 'Saving Changes...' : 'Save Admin Profile' }}</span>
              </button>
            </div>
          </form>
        </div>

        <!-- Right: Privileges & Quick Links (4 Cols) -->
        <div class="lg:col-span-4 space-y-6">
          <!-- Administrator Permissions Checklist -->
          <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 shadow-sm border border-outline-variant/30 dark:border-slate-800">
            <h4 class="font-label-md text-sm font-bold text-primary-container dark:text-white flex items-center gap-2 mb-4">
              <span class="material-symbols-outlined text-secondary text-base">security</span>
              <span>Administrative Privileges</span>
            </h4>

            <div class="space-y-3 text-xs">
              <div class="flex items-center gap-2.5 text-on-surface dark:text-slate-300">
                <span class="material-symbols-outlined text-emerald-500 text-base">check_circle</span>
                <span>Full Service Catalog (Create/Edit/Delete)</span>
              </div>
              <div class="flex items-center gap-2.5 text-on-surface dark:text-slate-300">
                <span class="material-symbols-outlined text-emerald-500 text-base">check_circle</span>
                <span>Bulk Slot &amp; Scheduling Engine</span>
              </div>
              <div class="flex items-center gap-2.5 text-on-surface dark:text-slate-300">
                <span class="material-symbols-outlined text-emerald-500 text-base">check_circle</span>
                <span>Client Pass Issuing &amp; Balance Overrides</span>
              </div>
              <div class="flex items-center gap-2.5 text-on-surface dark:text-slate-300">
                <span class="material-symbols-outlined text-emerald-500 text-base">check_circle</span>
                <span>M-Pesa STK &amp; Transaction Verification</span>
              </div>
              <div class="flex items-center gap-2.5 text-on-surface dark:text-slate-300">
                <span class="material-symbols-outlined text-emerald-500 text-base">check_circle</span>
                <span>Supabase S3 Cloud Media Storage</span>
              </div>
            </div>
          </div>

          <!-- Quick Navigation Shortcuts -->
          <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 shadow-sm border border-outline-variant/30 dark:border-slate-800 space-y-3">
            <h4 class="font-label-md text-sm font-bold text-primary-container dark:text-white flex items-center gap-2">
              <span class="material-symbols-outlined text-secondary text-base">link</span>
              <span>Quick Navigation</span>
            </h4>

            <div class="space-y-2 text-xs">
              <router-link 
                to="/admin/services" 
                class="flex items-center justify-between p-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container text-on-surface dark:text-slate-200 transition-colors"
              >
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-sm text-secondary">spa</span>
                  <span>Manage Offerings</span>
                </span>
                <span class="material-symbols-outlined text-xs text-on-surface-variant">arrow_forward</span>
              </router-link>

              <router-link 
                to="/admin/sessions" 
                class="flex items-center justify-between p-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container text-on-surface dark:text-slate-200 transition-colors"
              >
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-sm text-secondary">calendar_today</span>
                  <span>Scheduling Engine</span>
                </span>
                <span class="material-symbols-outlined text-xs text-on-surface-variant">arrow_forward</span>
              </router-link>

              <router-link 
                to="/admin/customers" 
                class="flex items-center justify-between p-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container text-on-surface dark:text-slate-200 transition-colors"
              >
                <span class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-sm text-secondary">groups</span>
                  <span>Customers CRM</span>
                </span>
                <span class="material-symbols-outlined text-xs text-on-surface-variant">arrow_forward</span>
              </router-link>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- INTERACTIVE AVATAR CROP & REPOSITION MODAL -->
    <Teleport to="body">
      <div 
        v-if="showCropModal" 
        class="fixed inset-0 z-[110] flex items-center justify-center p-3 sm:p-4 bg-black/75 backdrop-blur-md overflow-y-auto animate-fadeIn"
      >
        <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-6 sm:p-7 max-w-lg w-full shadow-2xl border border-outline-variant/30 dark:border-slate-800 flex flex-col my-auto">
          
          <!-- Modal Header -->
          <div class="flex items-center justify-between pb-3 mb-4 border-b border-outline-variant/20 dark:border-slate-800">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-full bg-secondary-container/50 dark:bg-sky-950 text-secondary dark:text-sky-300 flex items-center justify-center">
                <span class="material-symbols-outlined text-lg">crop</span>
              </div>
              <div>
                <h3 class="font-headline-sm text-base sm:text-lg font-bold text-primary-container dark:text-white leading-tight">
                  Frame &amp; Reposition Photo
                </h3>
                <p class="text-[11px] text-on-surface-variant dark:text-slate-400">
                  Drag the photo to reposition and use the zoom slider to scale
                </p>
              </div>
            </div>
            <button 
              @click="closeCropModal" 
              class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-on-surface dark:text-slate-300 font-bold transition-colors"
            >
              &times;
            </button>
          </div>

          <!-- Interactive Viewport Container -->
          <div class="flex flex-col items-center">
            <div 
              ref="cropViewport"
              @mousedown="startDrag"
              @touchstart.passive="startTouchDrag"
              @touchmove.passive="onTouchDrag"
              @touchend.passive="endTouchDrag"
              @wheel="onWheel"
              :class="[
                isDragging ? 'cursor-grabbing' : 'cursor-grab',
                'relative w-[280px] h-[280px] sm:w-[320px] sm:h-[320px] bg-slate-950 rounded-2xl overflow-hidden shadow-inner select-none touch-none'
              ]"
            >
              <!-- Transformed Image -->
              <img 
                ref="cropImgRef"
                :src="cropImageSrc" 
                alt="Crop preview" 
                @load="onImageLoaded"
                class="absolute pointer-events-none select-none max-w-none transition-transform duration-75 ease-out"
                :style="imageTransformStyle"
              />

              <!-- Circular Mask Overlay with Rule-of-Thirds Grid -->
              <div class="absolute inset-0 pointer-events-none flex items-center justify-center">
                <div class="rounded-full w-[240px] h-[240px] sm:w-[270px] sm:h-[270px] border-2 border-white/90 shadow-[0_0_0_9999px_rgba(0,0,0,0.55)] relative overflow-hidden transition-all duration-300">
                  <!-- Rule-of-Thirds Grid Lines -->
                  <div 
                    :class="isDragging ? 'opacity-50' : 'opacity-20'" 
                    class="absolute inset-0 grid grid-cols-3 grid-rows-3 pointer-events-none transition-opacity duration-200"
                  >
                    <div class="border-r border-b border-white/60"></div>
                    <div class="border-r border-b border-white/60"></div>
                    <div class="border-b border-white/60"></div>
                    <div class="border-r border-b border-white/60"></div>
                    <div class="border-r border-b border-white/60"></div>
                    <div class="border-b border-white/60"></div>
                    <div class="border-r border-white/60"></div>
                    <div class="border-r border-white/60"></div>
                    <div></div>
                  </div>
                </div>
              </div>

              <!-- Tooltip Hint -->
              <div class="absolute bottom-2.5 left-1/2 -translate-x-1/2 px-2.5 py-1 rounded-full bg-black/65 backdrop-blur-xs text-[10px] text-white/90 font-medium flex items-center gap-1 pointer-events-none shadow-xs">
                <span class="material-symbols-outlined text-[13px]">pan_tool</span>
                <span>Drag to pan</span>
              </div>
            </div>
          </div>

          <!-- Zoom Slider Control -->
          <div class="mt-4 bg-surface-container-low dark:bg-slate-800/80 p-3.5 rounded-2xl border border-outline-variant/20 dark:border-slate-800 space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="font-label-sm font-semibold text-on-surface dark:text-slate-300 flex items-center gap-1.5">
                <span class="material-symbols-outlined text-sm text-secondary">zoom_in</span>
                <span>Zoom Scale</span>
              </span>
              <div class="flex items-center gap-2">
                <span class="font-mono text-[11px] text-secondary font-bold">
                  {{ Math.round(zoomScale * 100) }}%
                </span>
                <button 
                  type="button" 
                  @click="resetPanZoom" 
                  class="text-[10px] text-on-surface-variant hover:text-primary-container dark:hover:text-white underline"
                >
                  Reset
                </button>
              </div>
            </div>

            <div class="flex items-center gap-3">
              <button 
                type="button" 
                @click="stepZoom(-0.15)"
                class="w-7 h-7 rounded-lg bg-surface-container dark:bg-slate-700 hover:bg-surface-container-high flex items-center justify-center text-on-surface dark:text-slate-200 transition-colors"
                title="Zoom Out"
              >
                <span class="material-symbols-outlined text-base">remove</span>
              </button>

              <input 
                type="range" 
                min="1" 
                max="3" 
                step="0.01" 
                v-model.number="zoomScale"
                class="flex-1 accent-secondary h-1.5 bg-surface-container-high dark:bg-slate-700 rounded-lg cursor-pointer"
              />

              <button 
                type="button" 
                @click="stepZoom(0.15)"
                class="w-7 h-7 rounded-lg bg-surface-container dark:bg-slate-700 hover:bg-surface-container-high flex items-center justify-center text-on-surface dark:text-slate-200 transition-colors"
                title="Zoom In"
              >
                <span class="material-symbols-outlined text-base">add</span>
              </button>
            </div>
          </div>

          <!-- Modal Action Buttons -->
          <div class="mt-5 pt-3 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-between gap-3">
            <button 
              type="button" 
              @click="closeCropModal" 
              class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low transition-colors"
            >
              Cancel
            </button>

            <button 
              type="button" 
              @click="applyCropAndUpload" 
              :disabled="savingCroppedPhoto"
              class="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-primary-container hover:bg-primary text-white font-label-md text-xs font-bold shadow-md hover:shadow-lg active:scale-95 transition-all disabled:opacity-50"
            >
              <span v-if="savingCroppedPhoto" class="material-symbols-outlined animate-spin text-sm">sync</span>
              <span v-else class="material-symbols-outlined text-sm">check</span>
              <span>{{ savingCroppedPhoto ? 'Processing & Saving...' : 'Save & Set Picture' }}</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useBookingStore } from '@/stores/bookingStore';
import { getUserProfile, updateUserProfile, uploadProfileAvatar, deleteProfileAvatar } from '@/services/api';

const authStore = useAuthStore();
const bookingStore = useBookingStore();

const pageLoading = ref(true);
const saving = ref(false);
const avatarUploading = ref(false);
const previewAvatarFailed = ref(false);

const form = reactive({
  id: '',
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  bio: '',
  emergency_contact: '',
  somatic_notes: '',
  avatar_url: null,
  role: 'studio_admin',
  is_superuser: false,
  date_joined: ''
});

// ========================================================
// INTERACTIVE AVATAR CROP & REPOSITION STATE & CONTROLS
// ========================================================
const showCropModal = ref(false);
const cropImageSrc = ref('');
const zoomScale = ref(1);
const panX = ref(0);
const panY = ref(0);
const isDragging = ref(false);
const savingCroppedPhoto = ref(false);

const cropViewport = ref(null);
const cropImgRef = ref(null);

let naturalWidth = 0;
let naturalHeight = 0;
let baseScale = 1;
let dragStartX = 0;
let dragStartY = 0;

const VIEWPORT_SIZE = 320;

watch(() => form.avatar_url, () => {
  previewAvatarFailed.value = false;
});

onMounted(async () => {
  await fetchProfile();
  window.addEventListener('mousemove', onDrag);
  window.addEventListener('mouseup', endDrag);
});

onUnmounted(() => {
  window.removeEventListener('mousemove', onDrag);
  window.removeEventListener('mouseup', endDrag);
});

async function fetchProfile() {
  pageLoading.value = true;
  try {
    const data = await getUserProfile();
    if (data) {
      form.id = data.id || '';
      form.username = data.username || '';
      form.email = data.email || '';
      form.first_name = data.first_name || '';
      form.last_name = data.last_name || '';
      form.phone = data.phone || '';
      form.bio = data.bio || '';
      form.emergency_contact = data.emergency_contact || '';
      form.somatic_notes = data.somatic_notes || '';
      form.avatar_url = data.avatar_url || null;
      form.role = data.role || 'studio_admin';
      form.is_superuser = !!data.is_superuser;
      form.date_joined = data.date_joined || '';

      authStore.updateUser({
        name: `${data.first_name} ${data.last_name}`.trim() || data.username,
        email: data.email,
        phone: data.phone,
        avatar: data.avatar_url,
        role: data.role
      });
    }
  } catch (err) {
    console.error('Failed to load admin profile:', err);
    const cur = authStore.user.value;
    if (cur) {
      form.username = cur.username || '';
      form.email = cur.email || '';
      form.first_name = cur.first_name || (cur.name ? cur.name.split(' ')[0] : '');
      form.last_name = cur.last_name || (cur.name ? cur.name.split(' ').slice(1).join(' ') : '');
      form.phone = cur.phone || '';
      form.avatar_url = cur.avatar || null;
      form.role = cur.role || 'studio_admin';
    }
  } finally {
    pageLoading.value = false;
  }
}

const displayName = computed(() => {
  const full = `${form.first_name} ${form.last_name}`.trim();
  return full || form.username || 'Administrator';
});

const userInitial = computed(() => {
  const name = form.first_name || form.username || 'A';
  return name.charAt(0).toUpperCase();
});

const isSuperuser = computed(() => {
  return form.is_superuser || form.username === 'karina' || form.username === 'admin';
});

const memberSinceDisplay = computed(() => {
  if (!form.date_joined) return '2026';
  try {
    const d = new Date(form.date_joined);
    return d.toLocaleDateString('en-GB', { month: 'short', year: 'numeric' });
  } catch {
    return '2026';
  }
});

// ========================================================
// FILE SELECTION & INTERACTIVE CROPPER PIPELINE
// ========================================================

function handleFileSelected(event) {
  const file = event.target.files?.[0];
  if (!file) return;

  if (file.size > 10 * 1024 * 1024) {
    bookingStore.showToast('Image size exceeds 10 MB limit.', 'error');
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    cropImageSrc.value = e.target.result;
    resetPanZoom();
    showCropModal.value = true;
  };
  reader.readAsDataURL(file);
  event.target.value = '';
}

function openCropWithCurrentAvatar() {
  if (!form.avatar_url) return;
  cropImageSrc.value = form.avatar_url;
  resetPanZoom();
  showCropModal.value = true;
}

function closeCropModal() {
  showCropModal.value = false;
  isDragging.value = false;
}

function onImageLoaded(e) {
  const img = e.target;
  naturalWidth = img.naturalWidth;
  naturalHeight = img.naturalHeight;
  baseScale = Math.max(VIEWPORT_SIZE / naturalWidth, VIEWPORT_SIZE / naturalHeight);
  resetPanZoom();
}

function resetPanZoom() {
  zoomScale.value = 1;
  panX.value = 0;
  panY.value = 0;
}

function stepZoom(delta) {
  const next = +(zoomScale.value + delta).toFixed(2);
  zoomScale.value = Math.min(3, Math.max(1, next));
  clampCurrentPan();
}

function onWheel(e) {
  e.preventDefault();
  const delta = e.deltaY < 0 ? 0.08 : -0.08;
  stepZoom(delta);
}

const maxPanX = computed(() => {
  const dispW = naturalWidth * baseScale * zoomScale.value;
  return Math.max(0, (dispW - VIEWPORT_SIZE) / 2);
});

const maxPanY = computed(() => {
  const dispH = naturalHeight * baseScale * zoomScale.value;
  return Math.max(0, (dispH - VIEWPORT_SIZE) / 2);
});

function clampCurrentPan() {
  panX.value = Math.min(maxPanX.value, Math.max(-maxPanX.value, panX.value));
  panY.value = Math.min(maxPanY.value, Math.max(-maxPanY.value, panY.value));
}

watch(zoomScale, () => {
  clampCurrentPan();
});

const imageTransformStyle = computed(() => {
  const s = baseScale * zoomScale.value;
  return {
    left: '50%',
    top: '50%',
    transform: `translate(-50%, -50%) translate(${panX.value}px, ${panY.value}px) scale(${s})`,
    transformOrigin: 'center'
  };
});

// Dragging Handlers
function startDrag(e) {
  isDragging.value = true;
  dragStartX = e.clientX - panX.value;
  dragStartY = e.clientY - panY.value;
}

function onDrag(e) {
  if (!isDragging.value) return;
  const rawX = e.clientX - dragStartX;
  const rawY = e.clientY - dragStartY;
  panX.value = Math.min(maxPanX.value, Math.max(-maxPanX.value, rawX));
  panY.value = Math.min(maxPanY.value, Math.max(-maxPanY.value, rawY));
}

function endDrag() {
  isDragging.value = false;
}

function startTouchDrag(e) {
  if (e.touches.length !== 1) return;
  isDragging.value = true;
  dragStartX = e.touches[0].clientX - panX.value;
  dragStartY = e.touches[0].clientY - panY.value;
}

function onTouchDrag(e) {
  if (!isDragging.value || e.touches.length !== 1) return;
  const rawX = e.touches[0].clientX - dragStartX;
  const rawY = e.touches[0].clientY - dragStartY;
  panX.value = Math.min(maxPanX.value, Math.max(-maxPanX.value, rawX));
  panY.value = Math.min(maxPanY.value, Math.max(-maxPanY.value, rawY));
}

function endTouchDrag() {
  isDragging.value = false;
}

// Canvas Coordinate Calculation & High-Res Crop Upload
async function applyCropAndUpload() {
  if (!cropImageSrc.value) return;
  savingCroppedPhoto.value = true;

  try {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    await new Promise((resolve, reject) => {
      img.onload = resolve;
      img.onerror = reject;
      img.src = cropImageSrc.value;
    });

    const OUTPUT_SIZE = 512;
    const canvas = document.createElement('canvas');
    canvas.width = OUTPUT_SIZE;
    canvas.height = OUTPUT_SIZE;
    const ctx = canvas.getContext('2d');
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';

    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, OUTPUT_SIZE, OUTPUT_SIZE);

    ctx.translate(OUTPUT_SIZE / 2, OUTPUT_SIZE / 2);
    const ratio = OUTPUT_SIZE / VIEWPORT_SIZE;
    ctx.translate(panX.value * ratio, panY.value * ratio);
    const drawScale = baseScale * zoomScale.value * ratio;
    ctx.scale(drawScale, drawScale);

    ctx.drawImage(img, -img.naturalWidth / 2, -img.naturalHeight / 2, img.naturalWidth, img.naturalHeight);

    const blob = await new Promise((resolve) => {
      canvas.toBlob(resolve, 'image/jpeg', 0.92);
    });

    if (!blob) throw new Error('Failed to render cropped image');

    const croppedFile = new File([blob], 'admin_avatar.jpg', { type: 'image/jpeg' });

    const res = await uploadProfileAvatar(croppedFile);
    if (res.avatar_url) {
      form.avatar_url = res.avatar_url;
      authStore.updateUser({ avatar: res.avatar_url });
      previewAvatarFailed.value = false;
    }

    bookingStore.showToast('Admin photo framed and updated! 🌿', 'success');
    closeCropModal();
  } catch (err) {
    console.error('Failed to crop and save avatar:', err);
    bookingStore.showToast(err.message || 'Failed to process cropped photo', 'error');
  } finally {
    savingCroppedPhoto.value = false;
  }
}

async function handleAvatarDelete() {
  if (!confirm('Are you sure you want to remove your admin profile photo?')) return;

  avatarUploading.value = true;
  try {
    await deleteProfileAvatar();
    form.avatar_url = null;
    previewAvatarFailed.value = false;
    authStore.updateUser({ avatar: null });
    bookingStore.showToast('Profile photo removed.', 'info');
  } catch (err) {
    bookingStore.showToast(err.message || 'Failed to remove photo', 'error');
  } finally {
    avatarUploading.value = false;
  }
}

async function submitProfileUpdate() {
  saving.value = true;
  try {
    const payload = {
      first_name: form.first_name,
      last_name: form.last_name,
      phone: form.phone,
      bio: form.bio,
      emergency_contact: form.emergency_contact,
      somatic_notes: form.somatic_notes
    };

    const res = await updateUserProfile(payload);
    bookingStore.showToast('Admin profile details updated successfully! 🌿', 'success');

    if (res) {
      form.first_name = res.first_name;
      form.last_name = res.last_name;
      form.phone = res.phone;
      form.bio = res.bio;
      form.emergency_contact = res.emergency_contact;
      form.somatic_notes = res.somatic_notes;

      authStore.updateUser({
        name: `${res.first_name} ${res.last_name}`.trim() || res.username,
        phone: res.phone,
        bio: res.bio,
        avatar: res.avatar_url || form.avatar_url
      });
    }
  } catch (err) {
    bookingStore.showToast(err.message || 'Failed to update admin profile', 'error');
  } finally {
    saving.value = false;
  }
}
</script>
