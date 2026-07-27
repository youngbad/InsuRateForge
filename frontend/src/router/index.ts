import { createRouter, createWebHistory } from 'vue-router';
import AuthLayout from '@/layouts/AuthLayout.vue';
import DefaultLayout from '@/layouts/DefaultLayout.vue';
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      component: AuthLayout,
      children: [
        {
          path: '',
          name: 'login',
          component: () => import('@/views/auth/LoginView.vue'),
          meta: { title: 'Sign in' }
        }
      ]
    },
    {
      path: '/',
      component: DefaultLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('@/views/dashboard/DashboardView.vue'),
          meta: { title: 'Dashboard', requiresAuth: true }
        },
        {
          path: 'quotes',
          name: 'quotes',
          component: () => import('@/views/quotes/QuotesListView.vue'),
          meta: { title: 'Quotes', requiresAuth: true }
        },
        {
          path: 'quotes/new',
          name: 'quote-create',
          component: () => import('@/views/quotes/QuoteDetailView.vue'),
          meta: { title: 'Create quote', requiresAuth: true }
        },
        {
          path: 'quotes/:id',
          name: 'quote-detail',
          component: () => import('@/views/quotes/QuoteDetailView.vue'),
          props: true,
          meta: { title: 'Quote detail', requiresAuth: true }
        },
        {
          path: 'portfolio',
          name: 'portfolio',
          component: () => import('@/views/portfolio/PortfolioView.vue'),
          meta: { title: 'Portfolio', requiresAuth: true }
        },
        {
          path: 'products',
          name: 'products',
          component: () => import('@/views/products/ProductsListView.vue'),
          meta: { title: 'Products', requiresAuth: true }
        },
        {
          path: 'products/:id',
          name: 'product-detail',
          component: () => import('@/views/products/ProductDetailView.vue'),
          props: true,
          meta: { title: 'Product detail', requiresAuth: true }
        },
        {
          path: 'admin',
          name: 'admin',
          component: () => import('@/views/admin/AdminView.vue'),
          meta: { title: 'Administration', requiresAuth: true }
        },
        {
          path: 'analytics',
          name: 'analytics',
          component: () => import('@/views/analytics/AnalyticsView.vue'),
          meta: { title: 'Analytics', requiresAuth: true }
        },
        {
          path: 'monitoring',
          name: 'monitoring',
          component: () => import('@/views/monitoring/MonitoringView.vue'),
          meta: { title: 'Monitoring', requiresAuth: true }
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ],
  scrollBehavior() {
    return { top: 0 };
  }
});

router.beforeEach((to) => {
  const authStore = useAuthStore();

  if (typeof document !== 'undefined' && typeof to.meta.title === 'string') {
    document.title = `${to.meta.title} · InsuRateForge`;
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return {
      name: 'login',
      query: { redirect: to.fullPath }
    };
  }

  if (to.name === 'login' && authStore.isAuthenticated) {
    return { name: 'dashboard' };
  }

  return true;
});

export default router;
