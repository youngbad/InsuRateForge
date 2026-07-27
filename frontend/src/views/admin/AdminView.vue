<script setup lang="ts">
import { reactive } from 'vue';
import { useQuery } from '@tanstack/vue-query';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import InputText from 'primevue/inputtext';
import Select from 'primevue/select';
import ToggleSwitch from 'primevue/toggleswitch';
import StatusBadge from '@/components/common/StatusBadge.vue';
import { listUsers } from '@/api/users';
import { useNotificationsStore } from '@/stores/notifications';

interface AdminSettings {
  refreshWindowMinutes: number;
  approvalThreshold: string;
  enableShadowPricing: boolean;
  enforceMfa: boolean;
}

const notifications = useNotificationsStore();
const usersQuery = useQuery({ queryKey: ['users'], queryFn: listUsers });
const settings = reactive<AdminSettings>({
  refreshWindowMinutes: 30,
  approvalThreshold: '$75,000',
  enableShadowPricing: true,
  enforceMfa: true
});

const refreshOptions = [15, 30, 60, 120];

function saveSettings() {
  notifications.success('Settings saved', 'Administration controls were updated for the active workspace.');
}
</script>

<template>
  <div class="page-shell">
    <header class="page-header">
      <div class="page-header__title">
        <h1>Administration</h1>
        <p>Manage user access, security guardrails, and platform-wide operating settings.</p>
      </div>
    </header>

    <section class="grid-2">
      <Card class="surface-card table-compact">
        <template #title>Access directory</template>
        <template #subtitle>Current user roles across pricing, underwriting, and operations</template>
        <template #content>
          <DataTable :value="usersQuery.data.value ?? []" responsive-layout="scroll">
            <Column field="name" header="User" />
            <Column field="team" header="Team" />
            <Column field="role" header="Role" />
            <Column header="Last login">
              <template #body="{ data }">
                {{ new Date(data.lastLogin).toLocaleString() }}
              </template>
            </Column>
            <Column header="Security posture">
              <template #body="{ data }">
                <StatusBadge :label="data.role === 'Platform Admin' ? 'Active' : 'Healthy'" />
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>

      <Card class="surface-card">
        <template #title>Platform controls</template>
        <template #subtitle>Govern refresh tokens, approval thresholds, and pricing experiments</template>
        <template #content>
          <div class="admin-settings">
            <div class="admin-settings__field">
              <label for="refresh-window">Refresh window</label>
              <Select id="refresh-window" v-model="settings.refreshWindowMinutes" :options="refreshOptions" fluid />
            </div>
            <div class="admin-settings__field">
              <label for="approval-threshold">Auto-approval threshold</label>
              <InputText id="approval-threshold" v-model="settings.approvalThreshold" fluid />
            </div>
            <div class="admin-settings__toggle">
              <div>
                <strong>Shadow pricing</strong>
                <p>Compare experimental pricing output without exposing it to underwriters.</p>
              </div>
              <ToggleSwitch v-model="settings.enableShadowPricing" />
            </div>
            <div class="admin-settings__toggle">
              <div>
                <strong>Enforce MFA</strong>
                <p>Require multi-factor authentication for all administrative roles.</p>
              </div>
              <ToggleSwitch v-model="settings.enforceMfa" />
            </div>
            <Button label="Save settings" icon="pi pi-save" @click="saveSettings" />
          </div>
        </template>
      </Card>
    </section>
  </div>
</template>

<style scoped>
.admin-settings {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.admin-settings__field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.admin-settings__toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem;
  border-radius: 1rem;
  background: var(--surface-muted);
  border: 1px solid var(--surface-border);
}

.admin-settings__toggle p,
.admin-settings__toggle strong {
  margin: 0;
}

.admin-settings__toggle p {
  margin-top: 0.25rem;
  color: var(--text-muted);
}
</style>
