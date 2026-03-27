<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../store/auth'

const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  try {
    error.value = ''
    await authStore.login(email.value, password.value)
  } catch (err) {
    error.value = 'Credenciales invalidas'
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo">
        <span class="icon">🐾</span>
        <h1>Pet Insurance</h1>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Correo Electrónico</label>
          <input 
            id="email" 
            v-model="email" 
            type="email" 
            placeholder="ejemplo@correo.com" 
            required
            :disabled="authStore.loading"
          >
        </div>

        <div class="form-group">
          <label for="password">Contraseña</label>
          <input 
            id="password" 
            v-model="password" 
            type="password" 
            placeholder="••••••••" 
            required
            :disabled="authStore.loading"
          >
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" :disabled="authStore.loading" class="btn-primary">
          <span v-if="authStore.loading" class="spinner"></span>
          {{ authStore.loading ? 'Entrando...' : 'Iniciar Sesión' }}
        </button>
      </form>

    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #eee;
}

.login-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  padding: 40px;
  border-radius: 24px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  background: radial-gradient(circle at top left, #4f46e5 0%, #1e1b4b 100%);
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 8px;
}

.logo .icon {
  font-size: 2.5rem;
}

.logo h1 {
  font-size: 1.8rem;
  font-weight: 800;
  letter-spacing: -1px;
}

.subtitle {
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 32px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.9);
}

.form-group input {
  width: 100%;
  padding: 14px 18px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.form-group input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.15);
  border-color: #818cf8;
  box-shadow: 0 0 0 4px rgba(129, 140, 248, 0.2);
}

.error-message {
  padding: 12px;
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #fca5a5;
  border-radius: 12px;
  font-size: 0.9rem;
  margin-bottom: 24px;
}

.btn-primary {
  width: 100%;
  padding: 16px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary:hover:not(:disabled) {
  background: #4f46e5;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.foot-notes {
  margin-top: 32px;
  text-align: center;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
}
</style>
