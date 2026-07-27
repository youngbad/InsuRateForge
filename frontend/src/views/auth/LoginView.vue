<script setup lang="ts">
import { computed, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Checkbox from 'primevue/checkbox';
import InputText from 'primevue/inputtext';
import Message from 'primevue/message';
import Password from 'primevue/password';
import { useAuth } from '@/composables/useAuth';
import { useNotificationsStore } from '@/stores/notifications';
import type { AuthLoginPayload } from '@/types/models';

type LoginFormState = AuthLoginPayload;

const router = useRouter();
const route = useRoute();
const { login, status } = useAuth();
const notifications = useNotificationsStore();

const form = reactive<LoginFormState>({
  email: 'admin@insurateforge.com',
  password: 'Password123!',
  rememberMe: true
});
const submitted = ref(false);
const errorMessage = ref('');

const validationErrors = computed(() => ({
  email: submitted.value && !/^\S+@\S+\.\S+$/.test(form.email) ? 'Enter a valid email address.' : '',
  password:
    submitted.value && form.password.trim().length < 8
      ? 'Password must contain at least 8 characters.'
      : ''
}));

const isValid = computed(() => !validationErrors.value.email && !validationErrors.value.password);

async function submit() {
  submitted.value = true;
  errorMessage.value = '';

  if (!isValid.value) {
    return;
  }

  try {
    await login({ ...form });
    notifications.success('Welcome back', 'InsuRateForge workspace is ready.');
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/';
    await router.push(redirect);
  } catch {
    errorMessage.value = 'Unable to sign in. Verify your credentials or backend connectivity.';
    notifications.error('Sign-in failed', errorMessage.value);
  }
}
</script>

<template>
  <div class="login-view">
    <section class="login-view__content">
      <div class="login-view__hero">
        <span class="login-view__pill">Production-ready insurance pricing</span>
        <h1>Underwrite, price, and monitor every submission in one platform.</h1>
        <p>
          InsuRateForge gives underwriting, actuarial, and operations teams a shared workspace for
          quotes, portfolio control, and live platform telemetry.
        </p>
        <ul>
          <li><i class="pi pi-check-circle"></i> Guided quote creation and pricing breakdowns</li>
          <li><i class="pi pi-check-circle"></i> Portfolio and analytics workspaces for decision support</li>
          <li><i class="pi pi-check-circle"></i> Admin controls and operational monitoring in one shell</li>
        </ul>
      </div>

      <Card class="login-view__card surface-card">
        <template #title>Sign in to InsuRateForge</template>
        <template #subtitle>Use your platform account or the prefilled demo session.</template>
        <template #content>
          <form class="login-form" @submit.prevent="submit">
            <div class="login-form__field">
              <label for="email">Email</label>
              <InputText id="email" v-model="form.email" fluid placeholder="you@company.com" />
              <small v-if="validationErrors.email" class="login-form__error">{{ validationErrors.email }}</small>
            </div>

            <div class="login-form__field">
              <label for="password">Password</label>
              <Password
                id="password"
                v-model="form.password"
                fluid
                toggleMask
                :feedback="false"
                placeholder="Enter your password"
              />
              <small v-if="validationErrors.password" class="login-form__error">{{ validationErrors.password }}</small>
            </div>

            <div class="login-form__meta">
              <div class="login-form__remember">
                <Checkbox v-model="form.rememberMe" binary input-id="remember-me" />
                <label for="remember-me">Keep me signed in</label>
              </div>
              <span class="section-note">Demo: admin@insurateforge.com / Password123!</span>
            </div>

            <Message v-if="errorMessage" severity="error" :closable="false">{{ errorMessage }}</Message>

            <Button
              type="submit"
              label="Sign in"
              icon="pi pi-arrow-right"
              icon-pos="right"
              :loading="status === 'loading'"
              fluid
            />
          </form>
        </template>
      </Card>
    </section>
  </div>
</template>

<style scoped>
.login-view__content {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(360px, 460px);
  gap: 2rem;
  align-items: center;
}

.login-view__hero {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.login-view__hero h1,
.login-view__hero p,
.login-view__hero ul {
  margin: 0;
}

.login-view__hero h1 {
  font-size: clamp(2rem, 4vw, 3.5rem);
  line-height: 1.05;
}

.login-view__hero p,
.login-view__hero li {
  color: var(--text-muted);
  font-size: 1rem;
}

.login-view__hero ul {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  list-style: none;
  padding: 0;
}

.login-view__hero li {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.login-view__hero i {
  color: #22c55e;
}

.login-view__pill {
  width: fit-content;
  padding: 0.45rem 0.8rem;
  border: 1px solid rgba(37, 99, 235, 0.2);
  border-radius: 999px;
  background: rgba(37, 99, 235, 0.12);
  color: var(--surface-strong);
  font-weight: 600;
}

.login-view__card {
  padding: 0.5rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.login-form__field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.login-form__meta {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 0.75rem;
  align-items: center;
}

.login-form__remember {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  color: var(--text-muted);
}

.login-form__error {
  color: #dc2626;
}

@media (max-width: 960px) {
  .login-view__content {
    grid-template-columns: 1fr;
  }
}
</style>
