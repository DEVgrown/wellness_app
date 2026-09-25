<template>
  <main class="flex-1 flex flex-col relative w-full bg-surface min-h-screen pb-safe">
    <div class="max-w-md mx-auto w-full px-4 pt-4 pb-12 space-y-6">
      <!-- Brand Logo Header -->
      <div class="flex flex-col items-center justify-center pt-2">
        <div class="relative flex items-center justify-center w-24 h-24 rounded-full bg-surface-container-lowest shadow-md p-2 transition-transform active:scale-95 duration-200">
          <div class="w-full h-full rounded-full bg-secondary-fixed/40 flex items-center justify-center text-primary">
            <svg class="w-14 h-14" fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="5" viewBox="0 0 100 100">
              <circle cx="42" cy="24" r="10"></circle>
              <path d="M26 34 C44 33, 52 42, 40 55 C34 62, 35 74, 46 80"></path>
              <circle cx="62" cy="24" r="10" stroke="#7DA2D0"></circle>
              <path d="M46 34 C64 33, 72 42, 60 55 C54 62, 55 74, 66 80" stroke="#7DA2D0"></path>
            </svg>
          </div>
          <span class="absolute -bottom-1 -right-1 flex h-6 w-6 items-center justify-center rounded-full bg-secondary-fixed text-on-secondary-fixed text-xs shadow-sm">
            <span class="material-symbols-outlined text-[16px]">verified</span>
          </span>
        </div>
      </div>

      <!-- Warm Handwritten Intro & Photo Bento Card -->
      <div class="relative w-full rounded-2xl bg-surface-container-lowest shadow-sm p-4 overflow-hidden flex flex-col items-center">
        <!-- Atmospheric subtle ambient aura -->
        <div class="absolute -top-12 -left-12 w-44 h-44 rounded-full bg-secondary-fixed/40 blur-2xl pointer-events-none"></div>
        <div class="absolute -bottom-10 -right-10 w-44 h-44 rounded-full bg-tertiary-fixed/30 blur-2xl pointer-events-none"></div>

        <!-- Script flourish greeting -->
        <div class="relative z-10 w-full flex items-baseline justify-between px-2 pt-1 pb-3">
          <div>
            <p class="font-eyebrow text-eyebrow text-secondary uppercase tracking-widest">Meet Your Movement Coach</p>
            <p class="font-headline-md text-headline-md text-primary font-bold">Karina, that's me! 👋</p>
          </div>
          <div class="flex items-center space-x-1 bg-surface-container-high text-on-secondary-fixed-variant px-2.5 py-1 rounded-full text-xs font-label-sm">
            <span class="material-symbols-outlined text-[14px]">local_fire_department</span>
            <span>25+ Yrs</span>
          </div>
        </div>

        <!-- Trainer Hero Portrait Container with Playful Motifs -->
        <div class="relative w-full aspect-[4/4.2] rounded-xl overflow-hidden shadow-inner bg-surface-container-low mb-3">
          <img 
            alt="Karina smiling warmly in movement studio attire" 
            class="w-full h-full object-cover object-top" 
            src="https://images.unsplash.com/photo-1594381898411-846e7d193883?auto=format&fit=crop&w=800&q=80"
            @error="e => e.target.src = 'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80'"
          />
          <!-- Tactile Floating Motifs / Badges -->
          <div class="absolute top-3 left-3 bg-surface-container-lowest/90 backdrop-blur-sm rounded-full py-1.5 px-3 flex items-center space-x-1.5 shadow-sm text-primary">
            <svg class="w-4 h-4 text-secondary fill-none stroke-current" stroke-width="2" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="4"></circle>
              <path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41m14.14-14.14l-1.41 1.41"></path>
            </svg>
            <span class="font-label-sm text-label-sm font-semibold">Outdoor mover</span>
          </div>
          <div class="absolute top-3 right-3 bg-surface-container-lowest/90 backdrop-blur-sm rounded-full py-1.5 px-3 flex items-center space-x-1.5 shadow-sm text-primary">
            <span class="material-symbols-outlined text-[16px] text-error">favorite</span>
            <span class="font-label-sm text-label-sm font-semibold">Mum of 2</span>
          </div>
          <div class="absolute bottom-3 left-3 bg-surface-container-lowest/90 backdrop-blur-sm rounded-full py-1.5 px-3 flex items-center space-x-1.5 shadow-sm text-primary">
            <span class="material-symbols-outlined text-[16px] text-secondary">explore</span>
            <span class="font-label-sm text-label-sm font-semibold">Alps & Kenya</span>
          </div>
          <div class="absolute bottom-3 right-3 bg-primary text-on-primary rounded-full py-1.5 px-3 flex items-center space-x-1.5 shadow-md">
            <span class="material-symbols-outlined text-[16px] text-secondary-fixed">sentiment_very_satisfied</span>
            <span class="font-label-sm text-label-sm font-semibold">Happy & cheerful</span>
          </div>
        </div>

        <!-- Micro Credential Row -->
        <div class="w-full flex items-center justify-center space-x-2 py-1.5 px-3 rounded-lg bg-surface-container text-primary font-label-sm text-label-sm text-center">
          <span class="material-symbols-outlined text-[16px] text-secondary shrink-0">workspace_premium</span>
          <span class="truncate">Certified Pilates Master & Co-Founder Master in Motion</span>
        </div>
      </div>

      <!-- Narrative & Mission Statement -->
      <div class="text-center px-2 space-y-2">
        <h1 class="font-headline-lg-mobile text-headline-lg-mobile text-primary font-bold tracking-tight">
          Start your active & healthy life, in every phase.
        </h1>
        <p class="font-body-md text-body-md text-on-surface-variant max-w-sm mx-auto">
          Personal training, Pilates Reformer & hormone coaching tailored to your body — in Salzburg, Nairobi & online worldwide.
        </p>
      </div>

      <!-- Studio Presence Badges / Location Pill Carousel -->
      <div class="flex flex-wrap items-center justify-center gap-2 pt-1">
        <div class="flex items-center space-x-1.5 bg-surface-container-lowest shadow-sm rounded-full px-3.5 py-1.5 text-on-surface">
          <span class="text-base">🏔️</span>
          <span class="font-label-sm text-label-sm font-medium">Salzburg-Anif</span>
        </div>
        <div class="flex items-center space-x-1.5 bg-surface-container-lowest shadow-sm rounded-full px-3.5 py-1.5 text-on-surface">
          <span class="text-base">🦒</span>
          <span class="font-label-sm text-label-sm font-medium">Nairobi (Karen)</span>
        </div>
        <div class="flex items-center space-x-1.5 bg-surface-container-lowest shadow-sm rounded-full px-3.5 py-1.5 text-on-surface">
          <span class="text-base">🌐</span>
          <span class="font-label-sm text-label-sm font-medium">Online Worldwide</span>
        </div>
      </div>

      <!-- Primary Interactive Conversion Stack -->
      <div class="w-full space-y-3 pt-2">
        <!-- Primary CTA: Booking -->
        <button 
          @click="startBooking"
          class="w-full h-14 rounded-full bg-primary-container text-on-primary font-label-lg text-label-lg flex items-center justify-between px-6 shadow-md transition-all duration-200 active:scale-[0.98] hover:shadow-lg" 
          type="button"
        >
          <span class="flex items-center space-x-2">
            <span class="material-symbols-outlined text-[20px] text-secondary-fixed">calendar_today</span>
            <span>Book Your First Session</span>
          </span>
          <span class="material-symbols-outlined text-[22px]">arrow_forward</span>
        </button>

        <!-- Social / Quick Sign-In Tile -->
        <button 
          @click="continueToHome"
          class="w-full h-12 rounded-full bg-surface-container-lowest text-primary font-label-md text-label-md flex items-center justify-center space-x-2 shadow-sm transition-all duration-200 active:scale-[0.98]" 
          type="button"
        >
          <span class="material-symbols-outlined text-[18px] text-secondary">fingerprint</span>
          <span>Continue with Google or Apple</span>
        </button>

        <!-- Guest / Direct Discovery Action -->
        <div class="flex items-center justify-center pt-1">
          <button 
            @click="continueToHome"
            class="text-secondary font-label-md text-label-md hover:text-primary transition-colors flex items-center space-x-1 py-1" 
            type="button"
          >
            <span>Continue as guest</span>
            <span class="material-symbols-outlined text-[16px]">chevron_right</span>
          </button>
        </div>
      </div>

      <!-- Trust Bar Stamp -->
      <div class="pt-4 flex flex-col items-center justify-center space-y-2 text-center text-on-surface-variant">
        <div class="flex items-center space-x-1">
          <span class="material-symbols-outlined text-[18px] text-secondary">spa</span>
          <span class="font-label-sm text-label-sm font-semibold tracking-wide text-primary">Mindful Movement • Hormone Harmony • Vitality</span>
        </div>
        <p class="font-body-sm text-body-sm text-outline">Over 1,200 private coaching hours delivered each year</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

function startBooking() {
  router.push('/services');
}

function continueToHome() {
  router.push('/home');
}
</script>
