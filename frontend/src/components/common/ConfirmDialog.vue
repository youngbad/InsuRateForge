<script setup lang="ts">
import Button from 'primevue/button';
import PrimeConfirmDialog from 'primevue/confirmdialog';
</script>

<template>
  <PrimeConfirmDialog group="global">
    <template #container="{ message, acceptCallback, rejectCallback }">
      <div class="confirm-shell surface-card">
        <div class="confirm-shell__icon">
          <i :class="message.icon ?? 'pi pi-exclamation-triangle'"></i>
        </div>
        <div class="confirm-shell__copy">
          <h3>{{ message.header ?? 'Confirm action' }}</h3>
          <p>{{ message.message }}</p>
        </div>
        <div class="confirm-shell__actions">
          <Button label="Cancel" severity="secondary" outlined @click="rejectCallback" />
          <Button
            :label="message.acceptLabel ?? 'Continue'"
            :severity="message.acceptClass?.includes('danger') ? 'danger' : 'primary'"
            @click="acceptCallback"
          />
        </div>
      </div>
    </template>
  </PrimeConfirmDialog>
</template>

<style scoped>
.confirm-shell {
  width: min(100vw - 2rem, 28rem);
  padding: 1.4rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.confirm-shell__icon {
  width: 3rem;
  height: 3rem;
  display: grid;
  place-items: center;
  border-radius: 1rem;
  background: var(--warning-soft);
  color: #b45309;
  font-size: 1.15rem;
}

.confirm-shell__copy h3,
.confirm-shell__copy p {
  margin: 0;
}

.confirm-shell__copy p {
  margin-top: 0.5rem;
  color: var(--text-muted);
}

.confirm-shell__actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}
</style>
