<template>
  <div class="auth-layout">
    <div class="auth-layout__backdrop"></div>
    <div class="auth-layout__content">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.auth-layout {
  position: relative;
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1.5rem;
  overflow: hidden;
  background:
    radial-gradient(circle at 20% 20%, rgba(37, 99, 235, 0.24), transparent 28%),
    radial-gradient(circle at 80% 0%, rgba(124, 58, 237, 0.18), transparent 26%),
    var(--app-bg);
}

.auth-layout__backdrop {
  position: absolute;
  inset: 0;
  background-image: linear-gradient(rgba(148, 163, 184, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148, 163, 184, 0.08) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(circle at center, rgba(0, 0, 0, 0.9), transparent 90%);
}

.auth-layout__content {
  position: relative;
  z-index: 1;
  width: min(100%, 1120px);
}
</style>
