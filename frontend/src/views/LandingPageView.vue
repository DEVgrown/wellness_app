<template>
  <div class="min-h-screen bg-surface dark:bg-slate-950 font-body-md text-body-md text-on-surface dark:text-slate-100 antialiased transition-colors duration-200">
    <AppNavbar />

    <!-- MAIN BODY -->
    <main class="w-full pt-16 sm:pt-[72px] pb-24 md:pb-16">
      <!-- HERO SECTION -->
      <section class="relative overflow-hidden pt-space-lg pb-space-xl">
        <div class="absolute -top-32 -left-20 w-96 h-96 rounded-full bg-secondary-container/20 dark:bg-sky-900/20 blur-3xl pointer-events-none"></div>
        <div class="absolute top-1/2 right-0 w-[480px] h-[480px] rounded-full bg-tertiary-fixed/30 dark:bg-emerald-900/20 blur-3xl pointer-events-none"></div>
        
        <div class="max-w-7xl mx-auto px-margin relative z-10">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-space-xl items-center">
            <!-- Left Column: Copy & Value Proposition -->
            <div class="lg:col-span-7 flex flex-col items-start space-y-space-md">
              <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-surface-container-high dark:bg-slate-800 text-primary-container dark:text-sky-300 font-label-sm text-label-sm shadow-sm">
                <span class="material-symbols-outlined text-sm text-secondary">spa</span>
                <span>Holistic Movement &amp; Hormone Harmony</span>
              </div>

              <!-- Headline with handwritten flourish -->
              <div class="relative">
                <h1 class="font-display text-4xl sm:text-5xl lg:text-display text-primary-container dark:text-white leading-tight tracking-tight font-semibold">
                  Start your active &amp; healthy life, <br/>
                  <span class="relative inline-block text-secondary">
                    in every phase.
                    <svg class="absolute -bottom-2 left-0 w-full h-3 text-secondary-container" fill="none" preserveAspectRatio="none" viewBox="0 0 200 12">
                      <path d="M2 9.5C60 2.5 140 2.5 198 9.5" stroke="currentColor" stroke-linecap="round" stroke-width="3"></path>
                    </svg>
                  </span>
                </h1>
                <div class="mt-space-xs flex items-center gap-2 text-secondary font-headline-sm italic">
                  <span class="font-normal font-sans tracking-wide">"Karina, that's me!"</span>
                  <svg class="w-6 h-6 text-secondary" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="9"></circle>
                    <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                    <line x1="9" x2="9.01" y1="9" y2="9"></line>
                    <line x1="15" x2="15.01" y1="9" y2="9"></line>
                  </svg>
                </div>
              </div>

              <!-- Subtitle -->
              <p class="font-body-lg text-body-lg text-on-surface-variant dark:text-slate-300 max-w-xl leading-relaxed">
                Boutique Pilates Reformer, functional strength, and personalized female hormone coaching tailored to your rhythm — in Nairobi (Karen), Salzburg-Anif, and Online Worldwide.
              </p>

              <!-- Studio Location Pills -->
              <div class="flex flex-wrap items-center gap-2 pt-1">
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low dark:bg-slate-800 text-on-surface dark:text-slate-300 font-label-sm text-label-sm shadow-sm">
                  <span class="material-symbols-outlined text-sm text-secondary">location_on</span> Nairobi (Karen)
                </span>
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low dark:bg-slate-800 text-on-surface dark:text-slate-300 font-label-sm text-label-sm shadow-sm">
                  <span class="material-symbols-outlined text-sm text-secondary">landscape</span> Salzburg-Anif
                </span>
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low dark:bg-slate-800 text-on-surface dark:text-slate-300 font-label-sm text-label-sm shadow-sm">
                  <span class="material-symbols-outlined text-sm text-secondary">public</span> Online Worldwide
                </span>
              </div>

              <!-- CTAs -->
              <div class="flex flex-wrap items-center gap-space-sm pt-space-xs">
                <router-link to="/book" class="inline-flex items-center justify-center gap-2 bg-primary-container hover:bg-primary text-on-primary font-label-lg text-label-lg px-8 py-3.5 rounded-full shadow-md transition-all active:scale-[0.98]">
                  <span>Book a Session</span>
                  <span class="material-symbols-outlined text-lg">arrow_forward</span>
                </router-link>
                <router-link to="/services" class="inline-flex items-center justify-center bg-surface-container-lowest dark:bg-slate-800 text-primary-container dark:text-white font-label-lg text-label-lg px-7 py-3.5 rounded-full shadow-sm hover:bg-surface-container-low dark:hover:bg-slate-700 transition-all border border-outline-variant/30 dark:border-slate-700">
                  Explore Services
                </router-link>
              </div>

              <!-- Key Metrics -->
              <div class="grid grid-cols-3 gap-space-md pt-space-md w-full max-w-lg">
                <div class="flex flex-col">
                  <span class="font-headline-lg text-3xl font-bold text-primary-container dark:text-white">25+</span>
                  <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Years Experience</span>
                </div>
                <div class="flex flex-col">
                  <span class="font-headline-lg text-3xl font-bold text-primary-container dark:text-white">1,200+</span>
                  <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Private Sessions / yr</span>
                </div>
                <div class="flex flex-col">
                  <span class="font-headline-lg text-3xl font-bold text-primary-container dark:text-white">Master</span>
                  <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Pilates Instructor</span>
                </div>
              </div>
            </div>

            <!-- Right Column: Karina Profile Feature Card -->
            <div class="lg:col-span-5 relative flex justify-center">
              <div class="relative w-full max-w-md rounded-3xl p-3 bg-surface-container-lowest dark:bg-slate-900 shadow-xl border border-outline-variant/30 dark:border-slate-800">
                <div class="relative rounded-2xl overflow-hidden bg-surface-container-low aspect-[4/5] flex items-center justify-center">
                  <img 
                    alt="Karina Trainer Profile" 
                    class="w-full h-full object-cover" 
                    src="https://images.unsplash.com/photo-1594381898411-846e7d193883?auto=format&fit=crop&w=800&q=80"
                    @error="e => e.target.src = 'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80'"
                  />
                  <!-- Organic Hand-annotated stickers -->
                  <div class="absolute top-4 left-4 bg-surface-container-lowest/90 dark:bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-full shadow-sm flex items-center gap-1.5">
                    <span class="material-symbols-outlined text-sm text-secondary">wb_sunny</span>
                    <span class="font-label-sm text-label-sm text-on-surface dark:text-slate-200 font-medium">Outdoor mover</span>
                  </div>
                  <div class="absolute top-4 right-4 bg-surface-container-lowest/90 dark:bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-full shadow-sm flex items-center gap-1.5">
                    <span class="material-symbols-outlined text-sm text-tertiary-container dark:text-emerald-400">favorite</span>
                    <span class="font-label-sm text-label-sm text-on-surface dark:text-slate-200 font-medium">Mum of 2</span>
                  </div>
                  <div class="absolute bottom-16 left-4 bg-surface-container-lowest/90 dark:bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-full shadow-sm flex items-center gap-1.5">
                    <span class="material-symbols-outlined text-sm text-secondary">explore</span>
                    <span class="font-label-sm text-label-sm text-on-surface dark:text-slate-200 font-medium">Alps &amp; Kenya</span>
                  </div>
                  <div class="absolute bottom-16 right-4 bg-surface-container-lowest/90 dark:bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-full shadow-sm flex items-center gap-1.5">
                    <span class="material-symbols-outlined text-sm text-primary-container dark:text-sky-300">sentiment_very_satisfied</span>
                    <span class="font-label-sm text-label-sm text-on-surface dark:text-slate-200 font-medium">Happy &amp; cheerful</span>
                  </div>
                </div>

                <!-- Floating Next Available Slot bar -->
                <div class="-mt-6 mx-2 relative z-20 bg-primary-container dark:bg-slate-800 text-on-primary rounded-2xl p-space-md shadow-lg flex items-center justify-between border border-white/10">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-secondary-container/20 flex items-center justify-center shrink-0">
                      <span class="material-symbols-outlined text-xl text-secondary-container dark:text-sky-300">alarm_on</span>
                    </div>
                    <div>
                      <span class="font-label-sm text-label-sm text-secondary-container dark:text-sky-300 uppercase tracking-wider block">Next Available Slot</span>
                      <span class="font-headline-sm text-headline-sm font-semibold text-white">Tomorrow, 09:30 AM</span>
                      <span class="text-body-sm text-body-sm text-surface-container-high dark:text-slate-300 block">Karen Studio (1:1 Reformer)</span>
                    </div>
                  </div>
                  <router-link to="/book" class="bg-secondary-container dark:bg-sky-400 text-primary-container dark:text-slate-900 px-3.5 py-1.5 rounded-full font-label-sm text-label-sm hover:opacity-90 shrink-0 font-semibold">
                    Reserve
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- QUICK BOOKING BAR / LIVE AVAILABILITY STRIP -->
      <section class="relative z-20 -mt-6 max-w-7xl mx-auto px-margin w-full" id="quick-booking">
        <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl shadow-xl p-space-md lg:p-space-lg flex flex-col lg:flex-row items-center justify-between gap-space-md border border-outline-variant/30 dark:border-slate-800">
          <!-- Studio Location -->
          <div class="flex-1 w-full flex items-center gap-3 bg-surface-container-low dark:bg-slate-800 px-4 py-3 rounded-2xl">
            <span class="material-symbols-outlined text-secondary text-2xl">location_city</span>
            <div class="flex flex-col min-w-0">
              <label class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Studio Sanctuary</label>
              <select v-model="quickBooking.location" class="bg-transparent font-headline-sm text-headline-sm text-primary-container dark:text-white focus:outline-none cursor-pointer pr-4 font-semibold">
                <option value="Karen">Nairobi (Karen Tree Lane)</option>
                <option value="Salzburg">Salzburg-Anif Sanctuary</option>
                <option value="Online">Online Studio Live</option>
              </select>
            </div>
          </div>

          <!-- Service Discipline -->
          <div class="flex-1 w-full flex items-center gap-3 bg-surface-container-low dark:bg-slate-800 px-4 py-3 rounded-2xl">
            <span class="material-symbols-outlined text-secondary text-2xl">sports_gymnastics</span>
            <div class="flex flex-col min-w-0">
              <label class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Experience / Discipline</label>
              <select v-model="quickBooking.service" class="bg-transparent font-headline-sm text-headline-sm text-primary-container dark:text-white focus:outline-none cursor-pointer pr-4 font-semibold">
                <option value="reformer">1:1 Pilates Reformer</option>
                <option value="personal">1:1 Functional Training</option>
                <option value="hormone">Hormone Metabolic Deep Dive</option>
                <option value="menomove">MenoMove Outdoor Group</option>
                <option value="duo">Duo Reformer Session</option>
              </select>
            </div>
          </div>

          <!-- Date Selection -->
          <div class="flex-1 w-full flex items-center gap-3 bg-surface-container-low dark:bg-slate-800 px-4 py-3 rounded-2xl">
            <span class="material-symbols-outlined text-secondary text-2xl">calendar_month</span>
            <div class="flex flex-col min-w-0">
              <label class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Preferred Day</label>
              <input v-model="quickBooking.date" class="bg-transparent font-headline-sm text-headline-sm text-primary-container dark:text-white focus:outline-none cursor-pointer font-semibold" type="date"/>
            </div>
          </div>

          <!-- Find Slots CTA -->
          <div class="w-full lg:w-auto shrink-0">
            <button @click="findAvailableSlots" class="w-full lg:w-auto inline-flex items-center justify-center gap-2 bg-primary-container hover:bg-primary text-on-primary font-label-lg text-label-lg px-8 py-4 rounded-2xl shadow-md transition-all active:scale-[0.98]" type="button">
              <span class="material-symbols-outlined">search</span>
              <span>Find Available Slots</span>
            </button>
          </div>
        </div>

        <!-- Availability Feedback Preview -->
        <div v-if="showAvailabilityPreview" class="mt-space-sm bg-surface-container dark:bg-slate-800 p-space-md rounded-2xl shadow-sm flex flex-col md:flex-row items-center justify-between gap-space-md border border-outline-variant/30 dark:border-slate-700 animate-fadeIn">
          <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-tertiary-container dark:text-emerald-400 text-2xl">event_available</span>
            <p class="font-body-md text-body-md text-on-surface dark:text-slate-200">
              <strong class="text-primary-container dark:text-white font-semibold">3 Slots Open</strong> for {{ quickBooking.location }}: 
              <span class="font-mono text-secondary">09:30 AM</span>, 
              <span class="font-mono text-secondary">11:00 AM</span>, and 
              <span class="font-mono text-secondary">04:30 PM</span>.
            </p>
          </div>
          <router-link to="/book" class="text-primary-container dark:text-sky-300 hover:underline font-label-md text-label-md flex items-center gap-1 font-semibold">
            Book now <span class="material-symbols-outlined text-sm">chevron_right</span>
          </router-link>
        </div>
      </section>

      <!-- SECTION: CORE PILLARS & FEATURED SERVICES -->
      <section class="py-space-xl max-w-7xl mx-auto px-margin w-full" id="services">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-space-lg gap-space-sm">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container-high dark:bg-slate-800 text-primary-container dark:text-sky-300 font-label-sm text-label-sm mb-2">
              <span>Curated Offerings</span>
            </div>
            <h2 class="font-headline-lg text-3xl font-bold text-primary-container dark:text-white">
              Tailored to your body and rhythm
            </h2>
            <p class="font-body-md text-body-md text-on-surface-variant dark:text-slate-400 max-w-xl mt-1">
              Whether you are navigating peri-menopause, seeking athletic pelvic floor alignment, or craving outdoor endorphins, every session is personally led by Karina.
            </p>
          </div>

          <div class="bg-surface-container-low dark:bg-slate-800 p-1 rounded-full flex items-center shrink-0">
            <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400 px-3 py-1">
              Active currency: <strong>{{ bookingStore.currency.value }}</strong>
            </span>
          </div>
        </div>

        <!-- 4 Pillars Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-space-md">
          <!-- Card 1 -->
          <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-space-md shadow-md hover:shadow-xl transition-all duration-300 flex flex-col justify-between group border border-outline-variant/30 dark:border-slate-800">
            <div>
              <div class="rounded-2xl overflow-hidden aspect-[4/3] mb-space-md bg-surface-container-low relative">
                <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?auto=format&fit=crop&w=800&q=80" @error="e => e.target.src = 'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80'"/>
                <span class="absolute top-3 left-3 bg-surface-container-lowest/90 dark:bg-slate-900/90 backdrop-blur-sm px-2.5 py-1 rounded-full font-label-sm text-label-sm text-primary-container dark:text-white font-semibold">1:1 Private</span>
              </div>
              <div class="flex items-center justify-between text-secondary font-label-sm text-label-sm mb-1">
                <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">schedule</span> 60 mins</span>
                <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">location_on</span> Studio / Home</span>
              </div>
              <h3 class="font-headline-md text-xl font-bold text-primary-container dark:text-white mb-2 group-hover:text-secondary transition-colors">
                1:1 Personal Training &amp; Posture
              </h3>
              <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400 leading-relaxed mb-space-md">
                Custom functional strength, joint mobility, and spine health. Perfect for rehabilitation, athletic conditioning, and post-injury longevity.
              </p>
            </div>
            <div class="pt-space-sm bg-surface-container-low/50 dark:bg-slate-800/40 -mx-space-md -mb-space-md p-space-md rounded-b-3xl mt-space-sm flex items-center justify-between">
              <div>
                <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400 block">From</span>
                <div class="font-headline-sm text-headline-sm font-bold text-primary-container dark:text-white">
                  {{ bookingStore.currency.value === 'KES' ? 'KES 6,500' : '€75' }}
                </div>
              </div>
              <router-link to="/book" class="bg-primary-container hover:bg-primary text-on-primary w-10 h-10 rounded-full flex items-center justify-center shadow-sm active:scale-95 transition-all">
                <span class="material-symbols-outlined text-lg">calendar_add_on</span>
              </router-link>
            </div>
          </div>

          <!-- Card 2 -->
          <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-space-md shadow-md hover:shadow-xl transition-all duration-300 flex flex-col justify-between group border border-outline-variant/30 dark:border-slate-800">
            <div>
              <div class="rounded-2xl overflow-hidden aspect-[4/3] mb-space-md bg-surface-container-low relative">
                <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80" @error="e => e.target.src = 'https://images.unsplash.com/photo-1594381898411-846e7d193883?auto=format&fit=crop&w=800&q=80'"/>
                <span class="absolute top-3 left-3 bg-secondary-container dark:bg-sky-400 text-primary-container dark:text-slate-900 px-2.5 py-1 rounded-full font-label-sm text-label-sm font-semibold">Most Popular</span>
              </div>
              <div class="flex items-center justify-between text-secondary font-label-sm text-label-sm mb-1">
                <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">schedule</span> 60 mins</span>
                <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">tune</span> Reformer Core</span>
              </div>
              <h3 class="font-headline-md text-xl font-bold text-primary-container dark:text-white mb-2 group-hover:text-secondary transition-colors">
                Pilates Reformer &amp; Alignment
              </h3>
              <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400 leading-relaxed mb-space-md">
                Decompress the spine and sculpt deep postural stabilizers on premium Allegro 2 Reformer carriages.
              </p>
            </div>
            <div class="pt-space-sm bg-surface-container-low/50 dark:bg-slate-800/40 -mx-space-md -mb-space-md p-space-md rounded-b-3xl mt-space-sm flex items-center justify-between">
              <div>
                <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400 block">From</span>
                <div class="font-headline-sm text-headline-sm font-bold text-primary-container dark:text-white">
                  {{ bookingStore.currency.value === 'KES' ? 'KES 6,500' : '€45' }}
                </div>
              </div>
              <router-link to="/services/reformer" class="bg-primary-container hover:bg-primary text-on-primary w-10 h-10 rounded-full flex items-center justify-center shadow-sm active:scale-95 transition-all">
                <span class="material-symbols-outlined text-lg">calendar_add_on</span>
              </router-link>
            </div>
          </div>

          <!-- Card 3 -->
          <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-space-md shadow-md hover:shadow-xl transition-all duration-300 flex flex-col justify-between group border border-outline-variant/30 dark:border-slate-800">
            <div>
              <div class="rounded-2xl overflow-hidden aspect-[4/3] mb-space-md bg-surface-container-low relative">
                <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80"/>
                <span class="absolute top-3 left-3 bg-tertiary-fixed dark:bg-emerald-400 text-tertiary-container dark:text-slate-900 px-2.5 py-1 rounded-full font-label-sm text-label-sm font-semibold">Specialty Coaching</span>
              </div>
              <div class="flex items-center justify-between text-secondary font-label-sm text-label-sm mb-1">
                <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">schedule</span> 75 mins</span>
                <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">public</span> In-Person / Zoom</span>
              </div>
              <h3 class="font-headline-md text-xl font-bold text-primary-container dark:text-white mb-2 group-hover:text-secondary transition-colors">
                Female Hormone &amp; Perimenopause
              </h3>
              <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400 leading-relaxed mb-space-md">
                Sync movement, circadian nutrition, cortisol management, and restorative recovery across hormonal phases.
              </p>
            </div>
            <div class="pt-space-sm bg-surface-container-low/50 dark:bg-slate-800/40 -mx-space-md -mb-space-md p-space-md rounded-b-3xl mt-space-sm flex items-center justify-between">
              <div>
                <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400 block">From</span>
                <div class="font-headline-sm text-headline-sm font-bold text-primary-container dark:text-white">
                  {{ bookingStore.currency.value === 'KES' ? 'KES 7,500' : '€85' }}
                </div>
              </div>
              <router-link to="/book" class="bg-primary-container hover:bg-primary text-on-primary w-10 h-10 rounded-full flex items-center justify-center shadow-sm active:scale-95 transition-all">
                <span class="material-symbols-outlined text-lg">calendar_add_on</span>
              </router-link>
            </div>
          </div>

          <!-- Card 4 -->
          <div class="bg-surface-container-lowest dark:bg-slate-900 rounded-3xl p-space-md shadow-md hover:shadow-xl transition-all duration-300 flex flex-col justify-between group border border-outline-variant/30 dark:border-slate-800">
            <div>
              <div class="rounded-2xl overflow-hidden aspect-[4/3] mb-space-md bg-surface-container-low relative">
                <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80"/>
                <span class="absolute top-3 left-3 bg-surface-container-high dark:bg-slate-800 text-primary-container dark:text-sky-300 px-2.5 py-1 rounded-full font-label-sm text-label-sm font-semibold">Community Outdoor</span>
              </div>
              <div class="flex items-center justify-between text-secondary font-label-sm text-label-sm mb-1">
                <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">schedule</span> 60 mins</span>
                <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">nature</span> Karura / Karen</span>
              </div>
              <h3 class="font-headline-md text-xl font-bold text-primary-container dark:text-white mb-2 group-hover:text-secondary transition-colors">
                Outdoor Endorphins &amp; MenoMove
              </h3>
              <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400 leading-relaxed mb-space-md">
                Breathe in natural negative ions and build bone density in uplifting open-air group conditioning.
              </p>
            </div>
            <div class="pt-space-sm bg-surface-container-low/50 dark:bg-slate-800/40 -mx-space-md -mb-space-md p-space-md rounded-b-3xl mt-space-sm flex items-center justify-between">
              <div>
                <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400 block">From</span>
                <div class="font-headline-sm text-headline-sm font-bold text-primary-container dark:text-white">
                  {{ bookingStore.currency.value === 'KES' ? 'KES 3,200' : '€25' }}
                </div>
              </div>
              <router-link to="/book" class="bg-primary-container hover:bg-primary text-on-primary w-10 h-10 rounded-full flex items-center justify-center shadow-sm active:scale-95 transition-all">
                <span class="material-symbols-outlined text-lg">calendar_add_on</span>
              </router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- ABOUT KARINA SECTION -->
      <section class="py-space-xl bg-surface-container-low/50 dark:bg-slate-900/60 w-full" id="about">
        <div class="max-w-7xl mx-auto px-margin">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            <div class="lg:col-span-6 relative">
              <div class="rounded-3xl overflow-hidden shadow-2xl bg-surface-container-lowest dark:bg-slate-800 aspect-square max-w-lg mx-auto">
                <img 
                  alt="Karina Coaching" 
                  class="w-full h-full object-cover" 
                  src="https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=1000&q=80"
                  @error="e => e.target.src = 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?auto=format&fit=crop&w=800&q=80'"
                />
              </div>
            </div>
            <div class="lg:col-span-6 space-y-6">
              <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary-container/40 dark:bg-sky-950/60 text-secondary dark:text-sky-300 font-label-sm text-label-sm">
                <span>The Human Touch</span>
              </div>
              <h2 class="font-headline-lg text-3xl sm:text-4xl font-bold text-primary-container dark:text-white tracking-tight">
                Movement is Medicine. <br/>
                Compassion is the Method.
              </h2>
              <p class="font-body-lg text-body-lg text-on-surface-variant dark:text-slate-300 leading-relaxed">
                With more than two decades guiding bodies across Europe and East Africa, Karina believes that true physical transformation never comes from punishing the body — it comes from honoring its innate wisdom and seasons.
              </p>
              <div class="grid grid-cols-2 gap-4 pt-2">
                <div class="p-4 rounded-2xl bg-surface-container-lowest dark:bg-slate-800 shadow-sm border border-outline-variant/20 dark:border-slate-700">
                  <span class="material-symbols-outlined text-secondary text-2xl mb-1">psychology</span>
                  <h4 class="font-label-md text-label-md font-semibold text-primary-container dark:text-white">Bio-Individual Care</h4>
                  <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400 mt-1">No cookie-cutter routines. Every movement is tailored to your hormonal state.</p>
                </div>
                <div class="p-4 rounded-2xl bg-surface-container-lowest dark:bg-slate-800 shadow-sm border border-outline-variant/20 dark:border-slate-700">
                  <span class="material-symbols-outlined text-secondary text-2xl mb-1">nature_people</span>
                  <h4 class="font-label-md text-label-md font-semibold text-primary-container dark:text-white">Sanctuary Spaces</h4>
                  <p class="font-body-sm text-body-sm text-on-surface-variant dark:text-slate-400 mt-1">Lush Karen gardens and tranquil Salzburg studios engineered for calm focus.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- TESTIMONIALS & RETREATS SECTION -->
      <section class="py-space-xl max-w-7xl mx-auto px-margin w-full">
        <div class="text-center max-w-2xl mx-auto mb-12">
          <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-widest block mb-2">Member Voices</span>
          <h2 class="font-headline-lg text-3xl font-bold text-primary-container dark:text-white">
            Transformations rooted in joy
          </h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-surface-container-lowest dark:bg-slate-900 p-6 rounded-3xl shadow-sm border border-outline-variant/30 dark:border-slate-800 flex flex-col justify-between">
            <p class="font-body-md text-body-md text-on-surface dark:text-slate-300 italic mb-6">
              "Training with Karina on the Reformer relieved my chronic lower back tension within four sessions. Her attention to spinal alignment is unlike any instructor I've ever met."
            </p>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-secondary-fixed flex items-center justify-center font-bold text-primary">AN</div>
              <div>
                <h5 class="font-label-md text-label-md font-semibold text-primary-container dark:text-white">Amina N.</h5>
                <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Karen Member • 1:1 Reformer</span>
              </div>
            </div>
          </div>

          <div class="bg-surface-container-lowest dark:bg-slate-900 p-6 rounded-3xl shadow-sm border border-outline-variant/30 dark:border-slate-800 flex flex-col justify-between">
            <p class="font-body-md text-body-md text-on-surface dark:text-slate-300 italic mb-6">
              "The hormone coaching program helped me navigate early peri-menopause brain fog and fatigue. Karina is empowering, knowledgeable, and genuinely warm."
            </p>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-secondary-container flex items-center justify-center font-bold text-primary-container">CK</div>
              <div>
                <h5 class="font-label-md text-label-md font-semibold text-primary-container dark:text-white">Claire K.</h5>
                <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Online Worldwide • Hormone Deep Dive</span>
              </div>
            </div>
          </div>

          <div class="bg-surface-container-lowest dark:bg-slate-900 p-6 rounded-3xl shadow-sm border border-outline-variant/30 dark:border-slate-800 flex flex-col justify-between">
            <p class="font-body-md text-body-md text-on-surface dark:text-slate-300 italic mb-6">
              "Her outdoor MenoMove sessions are the highlight of my Saturday mornings in Nairobi. You finish energized, smiling, and grounded in nature."
            </p>
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-tertiary-fixed flex items-center justify-center font-bold text-tertiary-container">SM</div>
              <div>
                <h5 class="font-label-md text-label-md font-semibold text-primary-container dark:text-white">Sophie M.</h5>
                <span class="font-label-sm text-label-sm text-on-surface-variant dark:text-slate-400">Nairobi Member • MenoMove Outdoor</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ ACCORDION SECTION -->
      <section class="py-space-xl bg-surface-container-low/40 dark:bg-slate-900/40 w-full" id="faq">
        <div class="max-w-4xl mx-auto px-margin">
          <div class="text-center mb-10">
            <span class="font-eyebrow text-eyebrow text-secondary uppercase tracking-widest block mb-2">Common Inquiries</span>
            <h2 class="font-headline-lg text-3xl font-bold text-primary-container dark:text-white">Frequently Asked Questions</h2>
          </div>
          <div class="space-y-4">
            <div 
              v-for="(faq, index) in faqs" 
              :key="index"
              class="bg-surface-container-lowest dark:bg-slate-900 rounded-2xl p-5 shadow-sm border border-outline-variant/30 dark:border-slate-800 transition-all cursor-pointer"
              @click="faq.open = !faq.open"
            >
              <div class="flex items-center justify-between">
                <h4 class="font-label-lg text-label-lg font-semibold text-primary-container dark:text-white">{{ faq.question }}</h4>
                <span class="material-symbols-outlined text-secondary transition-transform duration-300" :class="{ 'rotate-180': faq.open }">
                  expand_more
                </span>
              </div>
              <div v-show="faq.open" class="mt-3 pt-3 border-t border-outline-variant/20 dark:border-slate-800 text-on-surface-variant dark:text-slate-300 font-body-sm leading-relaxed">
                {{ faq.answer }}
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- FOOTER -->
    <footer class="bg-primary-container text-on-primary dark:bg-slate-950 dark:border-t dark:border-slate-800 py-16">
      <div class="max-w-7xl mx-auto px-margin grid grid-cols-1 md:grid-cols-4 gap-10">
        <div>
          <h4 class="font-headline-sm text-headline-sm font-bold text-white mb-2">YOUR TRAINER</h4>
          <span class="font-eyebrow text-eyebrow text-secondary-container uppercase tracking-widest block mb-4">by Karina</span>
          <p class="font-body-sm text-body-sm text-surface-container-high dark:text-slate-400 leading-relaxed">
            Nurturing athletic confidence, endocrine harmony, and mindful movement across every stage of womanhood.
          </p>
        </div>
        <div>
          <h5 class="font-label-md text-label-md font-semibold text-white mb-3">Sanctuary Locations</h5>
          <ul class="space-y-2 text-surface-container-high dark:text-slate-400 font-body-sm text-body-sm">
            <li>• Karen Tree Lane Studio, Nairobi</li>
            <li>• Salzburg-Anif Alpine Sanctuary</li>
            <li>• Live Interactive Zoom Worldwide</li>
          </ul>
        </div>
        <div>
          <h5 class="font-label-md text-label-md font-semibold text-white mb-3">Navigation</h5>
          <ul class="space-y-2 text-surface-container-high dark:text-slate-400 font-body-sm text-body-sm">
            <li><router-link to="/services" class="hover:underline">All Services</router-link></li>
            <li><router-link to="/book" class="hover:underline">Schedule &amp; Book</router-link></li>
            <li><router-link to="/bookings" class="hover:underline">My Pass &amp; Bookings</router-link></li>
            <li><router-link to="/login" class="hover:underline">Client Portal Login</router-link></li>
          </ul>
        </div>
        <div>
          <h5 class="font-label-md text-label-md font-semibold text-white mb-3">Contact &amp; Bookings</h5>
          <p class="font-body-sm text-body-sm text-surface-container-high dark:text-slate-400 mb-3">
            WhatsApp Concierge: <br/>
            <span class="font-mono text-secondary-container">+254 712 345 678</span>
          </p>
          <router-link to="/book" class="inline-block bg-secondary-container text-primary-container px-4 py-2 rounded-full font-label-sm text-label-sm font-semibold hover:opacity-90">
            Book Online
          </router-link>
        </div>
      </div>
      <div class="max-w-7xl mx-auto px-margin pt-10 mt-10 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between text-surface-container-high/60 dark:text-slate-500 font-body-sm text-xs">
        <p>© 2026 Your Trainer by Karina. All rights reserved.</p>
        <p>Crafted for holistic somatic longevity &amp; joy.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import AppNavbar from '@/components/AppNavbar.vue';
import { useBookingStore } from '@/stores/bookingStore';
import { useThemeStore } from '@/stores/themeStore';
import { useAuthStore } from '@/stores/authStore';

const router = useRouter();
const bookingStore = useBookingStore();
const themeStore = useThemeStore();
const authStore = useAuthStore();

const selectedLocation = ref('Nairobi (Karen)');
const showAvailabilityPreview = ref(false);

const quickBooking = reactive({
  location: 'Karen',
  service: 'reformer',
  date: new Date().toISOString().split('T')[0]
});

const faqs = reactive([
  {
    question: 'How do I know which session is right for me?',
    answer: 'If you are dealing with chronic back tension or want to build pelvic/core stability, 1:1 Reformer is the gold standard. For holistic hormone and energy regulation, our Hormone Deep Dive combines metabolic nutrition and somatic movement.',
    open: true
  },
  {
    question: 'What is your cancellation & reschedule policy?',
    answer: 'We understand schedules shift. You can reschedule any session free of charge up to 24 hours prior to your scheduled time via your client dashboard or WhatsApp.',
    open: false
  },
  {
    question: 'Can I pay via M-Pesa or Card?',
    answer: 'Yes! We support seamless automated M-Pesa STK push for Kenyan residents, as well as Visa, Mastercard, and international bank transfers in both KES and EUR.',
    open: false
  },
  {
    question: 'Do you offer multi-session packs?',
    answer: 'Yes. 5-session and 10-session wellness passes receive a 15% discount and remain valid for up to 6 months across both Karen and Salzburg studios.',
    open: false
  }
]);

function findAvailableSlots() {
  showAvailabilityPreview.value = true;
  bookingStore.showToast('Checking real-time slots...', 'info');
}
</script>
