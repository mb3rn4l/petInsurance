<template>
  <div class="dashboard">
    <header class="header">
      <div class="logo">🐾 Pet Insurance Admin</div>
      <div class="user-info">
        <span>Admin Panel</span>
        <button @click="authStore.logout()" class="btn-logout">Cerrar Sesión</button>
      </div>
    </header>
    <main class="content">
      <div class="card">
        <h1>Panel de Administración</h1>
        <p>Gestiona usuarios, roles y configuraciones del sistema.</p>
        <div class="admin-grid">
          <div class="admin-stat">
            <h4>Total Usuarios</h4>
            <span class="value">150</span>
          </div>
          <div class="admin-stat">
            <h4>Reclamos Pendientes</h4>
            <span class="value">12</span>
          </div>
          <div class="admin-stat">
            <h4>Ingresos Mensuales</h4>
            <span class="value">$1,200</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from '../store/auth'
const authStore = useAuthStore()
</script>

<style scoped>
.dashboard { min-height: 100vh; background: #f8fafc; }
.header { height: 80px; background: white; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
.logo { font-size: 1.5rem; font-weight: 800; color: #1e293b; }
.user-info { display: flex; align-items: center; gap: 20px; }
.btn-logout { background: transparent; padding: 8px 16px; border: 1px solid #e2e8f0; border-radius: 8px; cursor: pointer; }
.content { padding: 40px; max-width: 1200px; margin: 0 auto; }
.card { background: white; padding: 32px; border-radius: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
.admin-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 32px; }
.admin-stat { padding: 24px; background: #eef2ff; border-radius: 12px; border-left: 4px solid #6366f1; }
.admin-stat h4 { font-size: 0.8rem; text-transform: uppercase; color: #4f46e5; margin-bottom: 8px; }
.admin-stat .value { font-size: 1.5rem; font-weight: 800; color: #1e1b4b; }
</style>
