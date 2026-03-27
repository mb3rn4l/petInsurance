import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: '/pets',
    name: 'Pets',
    component: () => import('../views/Pets.vue'),
    meta: { requiresAuth: true, requiresRole: ['CUSTOMER', 'ADMIN'] },
  },
  {
    path: '/claims',
    name: 'Claims',
    component: () => import('../views/ClaimsList.vue'),
    meta: { requiresAuth: true, requiresRole: ['CUSTOMER', 'ADMIN'] },
  },

  {
    path: '/support/claims',
    name: 'SupportClaims',
    component: () => import('../views/SupportClaims.vue'),
    meta: { requiresAuth: true, requiresRole: ['SUPPORT', 'ADMIN'] },
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
    meta: { requiresAuth: true, requiresRole: ['ADMIN'] },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login' })
  } else if (to.meta.requiresRole) {
    if (!to.meta.requiresRole.includes(user.role)) {
      if (user.role === 'CUSTOMER') next({ name: 'Pets' })
      else if (user.role === 'SUPPORT') next({ name: 'SupportClaims' })
      else if (user.role === 'ADMIN') next({ name: 'Admin' })
      else next({ name: 'Login' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
