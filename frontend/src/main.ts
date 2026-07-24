import { createApp } from 'vue';
import { VueQueryPlugin, QueryClient } from '@tanstack/vue-query';
import Aura from '@primeuix/themes/aura';
import { createPinia } from 'pinia';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import VueApexCharts from 'vue3-apexcharts';
import App from './App.vue';
import router from './router';
import { useThemeStore } from './stores/theme';
import 'primeicons/primeicons.css';
import './styles.css';

const app = createApp(App);
const pinia = createPinia();
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 60_000
    },
    mutations: {
      retry: 0
    }
  }
});

app.use(pinia);
useThemeStore(pinia).initializeTheme();
app.use(router);
app.use(VueQueryPlugin, { queryClient });
app.use(PrimeVue, {
  ripple: true,
  inputVariant: 'filled',
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: '.app-dark'
    }
  }
});
app.use(ConfirmationService);
app.use(ToastService);
app.component('ApexChart', VueApexCharts);
app.mount('#app');
