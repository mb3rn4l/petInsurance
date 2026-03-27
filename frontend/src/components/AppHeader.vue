<script setup>
import { useAuthStore } from '../store/auth'

const authStore = useAuthStore()

defineProps({
  /** Array de links de navegación: [{ to: '/path', label: 'Label' }] */
  navLinks: {
    type: Array,
    default: () => []
  },
  /** Badge opcional mostrado junto al logo (ej: 'Soporte') */
  roleBadge: {
    type: String,
    default: ''
  }
})
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <div class="logo">🐾 Pet Insurance</div>
      <span v-if="roleBadge" class="role-badge">{{ roleBadge }}</span>
    </div>

    <nav v-if="navLinks.length" class="main-nav">
      <router-link
        v-for="link in navLinks"
        :key="link.to"
        :to="link.to"
      >
        {{ link.label }}
      </router-link>
    </nav>

    <div class="header-right">
      <span class="user-email">{{ authStore.user?.email }}</span>
      <button @click="authStore.logout()" class="btn-logout">Cerrar Sesión</button>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  height: 80px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
  white-space: nowrap;
}

.role-badge {
  background: #fef3c7;
  color: #b45309;
  padding: 4px 14px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.main-nav {
  display: flex;
  gap: 8px;
}

/* Vue Router pone 'router-link-active' automáticamente */
.main-nav a {
  text-decoration: none;
  color: #64748b;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 10px;
  transition: all 0.2s;
  font-size: 0.95rem;
}

.main-nav a:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.main-nav a.router-link-active,
.main-nav a.router-link-exact-active {
  color: #6366f1;
  background: #eef2ff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-email {
  font-size: 0.9rem;
  color: #64748b;
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-logout {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #ef4444;
  padding: 7px 16px;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  background: #fee2e2;
  border-color: #fca5a5;
}

@media (max-width: 768px) {
  .app-header { padding: 0 16px; }
  .user-email { display: none; }
}
</style>
