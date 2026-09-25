import { createRouter, createWebHistory } from 'vue-router';
import LandingPageView from '@/views/LandingPageView.vue';
import WelcomeView from '@/views/WelcomeView.vue';
import HomeView from '@/views/HomeView.vue';
import ServicesView from '@/views/ServicesView.vue';
import ServiceDetailView from '@/views/ServiceDetailView.vue';
import BookSessionView from '@/views/BookSessionView.vue';
import CheckoutView from '@/views/CheckoutView.vue';
import MyBookingsView from '@/views/MyBookingsView.vue';
import ProfileView from '@/views/ProfileView.vue';
import AuthView from '@/views/AuthView.vue';

// Admin Portal Modular Components
import AdminLayout from '@/layouts/AdminLayout.vue';
import AdminOverviewView from '@/views/admin/AdminOverviewView.vue';
import AdminServicesView from '@/views/admin/AdminServicesView.vue';
import AdminSessionsView from '@/views/admin/AdminSessionsView.vue';
import AdminBookingsView from '@/views/admin/AdminBookingsView.vue';
import AdminCustomersView from '@/views/admin/AdminCustomersView.vue';
import AdminProfileView from '@/views/admin/AdminProfileView.vue';

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingPageView
  },
  {
    path: '/welcome',
    name: 'welcome',
    component: WelcomeView
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
    path: '/services',
    name: 'services',
    component: ServicesView
  },
  {
    path: '/services/:id',
    name: 'service-detail',
    component: ServiceDetailView
  },
  {
    path: '/book/:serviceId?',
    name: 'book',
    component: BookSessionView
  },
  {
    path: '/checkout',
    name: 'checkout',
    component: CheckoutView,
    meta: { requiresAuth: true }
  },
  {
    path: '/bookings',
    name: 'bookings',
    component: MyBookingsView,
    meta: { requiresAuth: true }
  },
  
  // Dedicated Multi-Page Admin Portal
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAdmin: true },
    children: [
      { path: '', redirect: '/admin/overview' },
      { path: 'overview', name: 'admin-overview', component: AdminOverviewView },
      { path: 'services', name: 'admin-services', component: AdminServicesView },
      { path: 'sessions', name: 'admin-sessions', component: AdminSessionsView },
      { path: 'bookings', name: 'admin-bookings', component: AdminBookingsView },
      { path: 'customers', name: 'admin-customers', component: AdminCustomersView },
      { path: 'profile', name: 'admin-profile', component: AdminProfileView },
    ]
  },
  {
    path: '/admin-dashboard',
    redirect: '/admin/overview'
  },
  {
    path: '/login',
    name: 'login',
    component: AuthView
  },
  {
    path: '/signup',
    name: 'signup',
    component: AuthView
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
});

// Global Navigation Guard for Authentication & Administrator Verification
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('karina_auth_token');
  const userStr = localStorage.getItem('karina_auth_user');
  let user = null;
  try {
    user = userStr ? JSON.parse(userStr) : null;
  } catch (e) {
    user = null;
  }
  const isAuthenticated = Boolean(token && user);

  // Check routes requiring general client authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      return next({ path: '/login', query: { redirect: to.fullPath } });
    }
  }

  // Check routes requiring administrative privileges (SEC-003: strict boolean check)
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    const isStaff = Boolean(user && (user.is_staff === true || user.is_superuser === true));

    if (!isAuthenticated) {
      return next({ path: '/login', query: { redirect: to.fullPath } });
    }
    if (!isStaff) {
      return next({ path: '/home' });
    }
  }
  next();
});

export default router;
