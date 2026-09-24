import { createRouter, createWebHistory } from 'vue-router';
import LandingPageView from '@/views/LandingPageView.vue';
import WelcomeView from '@/views/WelcomeView.vue';
import HomeView from '@/views/HomeView.vue';
import ServicesView from '@/views/ServicesView.vue';
import ServiceDetailView from '@/views/ServiceDetailView.vue';
import BookSessionView from '@/views/BookSessionView.vue';
import CheckoutView from '@/views/CheckoutView.vue';
import MyBookingsView from '@/views/MyBookingsView.vue';
import AuthView from '@/views/AuthView.vue';

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
    component: CheckoutView
  },
  {
    path: '/bookings',
    name: 'bookings',
    component: MyBookingsView
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
    redirect: '/bookings'
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

export default router;
