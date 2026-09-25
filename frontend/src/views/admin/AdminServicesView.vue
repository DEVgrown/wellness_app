<template>
  <div class="space-y-6 animate-fadeIn">
    <!-- Top Action Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h3 class="font-headline-sm text-xl font-bold text-primary-container dark:text-white">
          Wellness Offerings Catalog
        </h3>
        <p class="font-body-sm text-xs text-on-surface-variant dark:text-slate-400">
          Manage services, dual-currency pricing (KES &amp; EUR), durations, badges, and capacity
        </p>
      </div>

      <button
        @click="openModal()"
        class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all self-start sm:self-auto"
        type="button"
      >
        <span class="material-symbols-outlined text-sm">add</span>
        <span>Add New Offering</span>
      </button>
    </div>

    <!-- Notification Banner -->
    <div v-if="notice" class="p-3.5 rounded-2xl flex items-center justify-between gap-2 text-xs font-medium" :class="noticeType === 'error' ? 'bg-red-50 text-red-800 dark:bg-red-950/50 dark:text-red-300' : 'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300'">
      <span>{{ notice }}</span>
      <button @click="notice = ''" class="font-bold">&times;</button>
    </div>

    <!-- Search & Category Filters -->
    <div class="flex flex-col sm:flex-row items-center gap-3">
      <div class="relative w-full sm:w-80">
        <span class="material-symbols-outlined absolute left-3 top-2.5 text-on-surface-variant text-base">search</span>
        <input
          v-model="search"
          type="text"
          placeholder="Search by title or description..."
          class="w-full pl-9 pr-4 py-2 rounded-2xl bg-surface-container-lowest dark:bg-slate-900 border border-outline-variant/30 dark:border-slate-800 text-xs font-body-sm focus:outline-none focus:ring-2 focus:ring-primary-container/30"
        />
      </div>

      <div class="flex items-center gap-2 overflow-x-auto w-full pb-1 no-scrollbar">
        <button
          v-for="cat in categories"
          :key="cat.id"
          @click="selectedCategory = cat.id"
          :class="selectedCategory === cat.id ? 'bg-primary-container text-white dark:bg-sky-500 dark:text-slate-950 font-bold' : 'bg-surface-container-low dark:bg-slate-800 text-on-surface-variant dark:text-slate-300'"
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
              <span class="material-symbols-outlined text-xs">groups</span> {{ srv.capacity || 'Group' }}
            </span>
          </div>

          <h4 class="font-headline-sm text-base font-bold text-primary-container dark:text-white mb-1">
            {{ srv.title }}
          </h4>

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
              @click="openModal(srv)"
              class="px-3 py-1.5 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container font-label-sm text-xs font-semibold text-primary-container dark:text-white border border-outline-variant/30 dark:border-slate-700 transition-all flex items-center gap-1"
              type="button"
            >
              <span class="material-symbols-outlined text-xs">edit</span>
              <span>Edit</span>
            </button>
            <button
              @click="removeService(srv)"
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

    <!-- Service Add/Edit Modal (Teleported to body for guaranteed viewport centering) -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center p-3.5 sm:p-4 bg-black/60 backdrop-blur-sm overflow-y-auto animate-fadeIn">
        <div class="bg-surface-container-lowest dark:bg-slate-900 w-full max-w-2xl rounded-3xl border border-outline-variant/30 dark:border-slate-800 shadow-2xl flex flex-col max-h-[85vh] sm:max-h-[88vh] overflow-hidden my-auto">
          
          <!-- Sticky Header -->
          <div class="shrink-0 px-5 sm:px-7 py-4 border-b border-outline-variant/20 dark:border-slate-800 flex items-center justify-between bg-surface-container-lowest dark:bg-slate-900">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-full bg-secondary-container/40 dark:bg-sky-950 text-secondary dark:text-sky-300 flex items-center justify-center">
                <span class="material-symbols-outlined text-lg">spa</span>
              </div>
              <h3 class="font-headline-sm text-base sm:text-lg font-bold text-primary-container dark:text-white">
                {{ isEditing ? 'Edit Offering' : 'Create New Wellness Offering' }}
              </h3>
            </div>
            <button @click="showModal = false" class="w-8 h-8 rounded-full bg-surface-container-low dark:bg-slate-800 hover:bg-surface-container flex items-center justify-center text-on-surface dark:text-slate-300 font-bold transition-colors">
              &times;
            </button>
          </div>

          <!-- Scrollable Body with form fields -->
          <form id="serviceForm" @submit.prevent="submitService" class="flex-1 min-h-0 overflow-y-auto p-5 sm:p-7 space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="sm:col-span-2">
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Title *</label>
                <input v-model="form.title" type="text" required placeholder="e.g. Restorative Sound Bath" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Category *</label>
                <select v-model="form.category" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white">
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
                <input v-model.number="form.duration_minutes" type="number" min="15" step="5" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Price (KES) *</label>
                <input v-model.number="form.price_kes" type="number" min="0" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Price (EUR) *</label>
                <input v-model.number="form.price_eur" type="number" min="0" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Capacity Label</label>
                <input v-model="form.capacity" type="text" placeholder="Small Group (4–8)" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div>
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Badge</label>
                <input v-model="form.badge" type="text" placeholder="Popular, Masterclass..." class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div class="sm:col-span-2">
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Location Display Name</label>
                <input v-model="form.location_display" type="text" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div class="sm:col-span-2">
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Image URL</label>
                <input v-model="form.image_url" type="url" class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white" />
              </div>

              <div class="sm:col-span-2">
                <label class="block font-label-sm text-xs font-semibold mb-1 text-on-surface dark:text-slate-300">Description *</label>
                <textarea v-model="form.description" rows="3" required class="w-full px-3.5 py-2.5 rounded-xl bg-surface-container-low dark:bg-slate-800 border border-outline-variant/30 dark:border-slate-700 text-xs focus:outline-none focus:ring-2 focus:ring-primary-container/20 text-on-surface dark:text-white"></textarea>
              </div>
            </div>
          </form>

          <!-- Sticky Action Footer -->
          <div class="shrink-0 px-5 sm:px-7 py-3.5 border-t border-outline-variant/20 dark:border-slate-800 flex items-center justify-end gap-3 bg-surface-container-lowest dark:bg-slate-900 pb-safe">
            <button @click="showModal = false" type="button" class="px-4 py-2 rounded-full font-label-sm text-xs font-semibold text-on-surface-variant hover:bg-surface-container-low transition-colors">
              Cancel
            </button>
            <button form="serviceForm" :disabled="submitting" type="submit" class="px-5 py-2.5 rounded-full bg-primary-container hover:bg-primary text-white font-label-sm text-xs font-bold shadow-xs active:scale-95 transition-all disabled:opacity-50">
              {{ submitting ? 'Saving...' : (isEditing ? 'Save Changes' : 'Create Offering') }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { getAdminServices, createAdminService, updateAdminService, deleteAdminService } from '@/services/api';

const services = ref([]);
const search = ref('');
const selectedCategory = ref('all');
const showModal = ref(false);
const isEditing = ref(false);
const editingId = ref(null);
const submitting = ref(false);
const notice = ref('');
const noticeType = ref('success');

const categories = [
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

const form = reactive({
  title: '',
  category: 'pilates',
  duration_minutes: 60,
  price_kes: 3500,
  price_eur: 40,
  capacity: 'Small Group (4–8)',
  badge: '',
  location_display: 'Karen Studio Sanctuary, Nairobi',
  location_type: 'all nairobi',
  image_url: 'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80',
  description: ''
});

const filteredServices = computed(() => {
  return services.value.filter(s => {
    const matchCat = selectedCategory.value === 'all' || s.category === selectedCategory.value;
    const q = search.value.toLowerCase().trim();
    const matchSearch = !q || s.title.toLowerCase().includes(q) || (s.description || '').toLowerCase().includes(q);
    return matchCat && matchSearch;
  });
});

async function loadServices() {
  try {
    services.value = await getAdminServices();
  } catch (e) {
    console.error('Failed to load services:', e);
  }
}

function openModal(item = null) {
  if (item) {
    isEditing.value = true;
    editingId.value = item.id;
    form.title = item.title;
    form.category = item.category;
    form.duration_minutes = item.duration_minutes;
    form.price_kes = item.price_kes;
    form.price_eur = item.price_eur;
    form.capacity = item.capacity;
    form.badge = item.badge;
    form.location_display = item.location_display;
    form.location_type = item.location_type;
    form.image_url = item.image_url;
    form.description = item.description;
  } else {
    isEditing.value = false;
    editingId.value = null;
    form.title = '';
    form.category = 'pilates';
    form.duration_minutes = 60;
    form.price_kes = 3500;
    form.price_eur = 40;
    form.capacity = 'Small Group (4–8)';
    form.badge = '';
    form.location_display = 'Karen Studio Sanctuary, Nairobi';
    form.location_type = 'all nairobi';
    form.image_url = 'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80';
    form.description = '';
  }
  showModal.value = true;
}

async function submitService() {
  submitting.value = true;
  try {
    if (isEditing.value) {
      await updateAdminService(editingId.value, form);
      notice.value = `Updated "${form.title}" successfully.`;
    } else {
      await createAdminService(form);
      notice.value = `Created offering "${form.title}".`;
    }
    noticeType.value = 'success';
    showModal.value = false;
    await loadServices();
  } catch (err) {
    notice.value = err.message || 'Action failed.';
    noticeType.value = 'error';
  } finally {
    submitting.value = false;
  }
}

async function removeService(srv) {
  if (!confirm(`Are you sure you want to delete "${srv.title}"? Associated time slots will also be removed.`)) return;
  try {
    await deleteAdminService(srv.id);
    notice.value = `Deleted "${srv.title}".`;
    noticeType.value = 'success';
    await loadServices();
  } catch (e) {
    notice.value = e.message;
    noticeType.value = 'error';
  }
}

onMounted(() => {
  loadServices();
});
</script>
