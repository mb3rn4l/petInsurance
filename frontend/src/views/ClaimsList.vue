<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useAuthStore } from '../store/auth'
import ClaimService from '../services/ClaimService'
import AppHeader from '../components/AppHeader.vue'
import ClaimFormModal from '../components/ClaimFormModal.vue'


const authStore = useAuthStore()
const allClaims = ref([])
const loading = ref(true)
const activeFilter = ref('ALL')
const showCreateModal = ref(false)
let pollInterval = null

const FILTERS = [
  { key: 'ALL',        label: 'Todos'             },
  { key: 'PROCESSING', label: 'En Procesamiento'  },
  { key: 'IN_REVIEW',  label: 'En Revisión'        },
  { key: 'APPROVED',   label: 'Aprobados'          },
  { key: 'REJECTED',   label: 'Rechazados'         },
]

const fetchClaims = async (silent = false) => {
  if (!silent) loading.value = true
  try {
    const params = activeFilter.value !== 'ALL' ? `?status=${activeFilter.value}` : ''
    const response = await ClaimService.getAllFiltered(params)
    allClaims.value = response.data
  } catch (e) {
    console.error('Error cargando reclamos:', e)
  } finally {
    loading.value = false
  }
}

watch(activeFilter, () => fetchClaims())

const STATUS_LABELS = {
  PROCESSING: 'En Procesamiento',
  IN_REVIEW:  'En Revisión',
  APPROVED:   'Aprobado',
  REJECTED:   'Rechazado',
}
const STATUS_CLASSES = {
  PROCESSING: 'st-processing',
  IN_REVIEW:  'st-review',
  APPROVED:   'st-approved',
  REJECTED:   'st-rejected',
}

const formatCurrency = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(val)

const formatDate = (d) => (d ? new Date(d).toLocaleDateString('es-CO') : '-')

const counts = computed(() => {
  const base = allClaims.value
  return {
    PROCESSING: base.filter(c => c.status === 'PROCESSING').length,
    IN_REVIEW:  base.filter(c => c.status === 'IN_REVIEW').length,
    APPROVED:   base.filter(c => c.status === 'APPROVED').length,
    REJECTED:   base.filter(c => c.status === 'REJECTED').length,
  }
})

// ------- lifecycle -------
onMounted(() => {
  fetchClaims()
  pollInterval = setInterval(() => fetchClaims(true), 30_000)
})
onUnmounted(() => clearInterval(pollInterval))
</script>

<template>
  <div class="dashboard">
    <AppHeader :nav-links="[
      { to: '/pets', label: 'Mascotas' },
      { to: '/claims', label: 'Reclamos' }
    ]" />

    <main class="content">
      <div class="summary-row">
        <div class="summary-card" :class="{ clickable: true, active: activeFilter === 'ALL' }" @click="activeFilter = 'ALL'">
          <span class="s-value">{{ allClaims.length }}</span>
          <span class="s-label">Total</span>
        </div>
        <div class="summary-card processing" @click="activeFilter = 'PROCESSING'" :class="{ active: activeFilter === 'PROCESSING' }">
          <span class="s-value">{{ counts.PROCESSING }}</span>
          <span class="s-label">En Proceso</span>
        </div>
        <div class="summary-card review" @click="activeFilter = 'IN_REVIEW'" :class="{ active: activeFilter === 'IN_REVIEW' }">
          <span class="s-value">{{ counts.IN_REVIEW }}</span>
          <span class="s-label">En Revisión</span>
        </div>
        <div class="summary-card approved" @click="activeFilter = 'APPROVED'" :class="{ active: activeFilter === 'APPROVED' }">
          <span class="s-value">{{ counts.APPROVED }}</span>
          <span class="s-label">Aprobados</span>
        </div>
        <div class="summary-card rejected" @click="activeFilter = 'REJECTED'" :class="{ active: activeFilter === 'REJECTED' }">
          <span class="s-value">{{ counts.REJECTED }}</span>
          <span class="s-label">Rechazados</span>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div>
            <h1>Mis Reclamos</h1>
            <p>Seguimiento de tus solicitudes de reembolso.</p>
          </div>
          <button @click="showCreateModal = true" class="btn-add">+ Nuevo Reclamo</button>
        </div>

        <div class="filter-bar">
          <button
            v-for="f in FILTERS"
            :key="f.key"
            :class="['filter-pill', activeFilter === f.key ? 'filter-active' : '']"
            @click="activeFilter = f.key"
          >
            {{ f.label }}
          </button>
        </div>

        <div v-if="loading" class="loader-container">
          <div class="spinner"></div>
        </div>

        <div v-else-if="allClaims.length === 0" class="empty-state">
          <span class="icon">📋</span>
          <h3>Sin reclamos para este filtro</h3>
          <p v-if="activeFilter === 'ALL'">Aún no has creado ningún reclamo.</p>
          <p v-else>No hay reclamos con el estado seleccionado.</p>
          <button v-if="activeFilter === 'ALL'" @click="showCreateModal = true" class="btn-add-inline">Crear tu primer reclamo</button>
        </div>

        <table v-else class="claims-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Mascota</th>
              <th>Fecha Factura</th>
              <th>Monto</th>
              <th>Estado</th>
              <th>Registrado</th>
              <th>Factura</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="claim in allClaims" :key="claim.id">
              <td class="id-col">#{{ claim.id }}</td>
              <td class="pet-col">{{ claim.pet_name }}</td>
              <td>{{ formatDate(claim.invoice_date) }}</td>
              <td class="amount-col">{{ formatCurrency(claim.amount) }}</td>
              <td>
                <span :class="['status-badge', STATUS_CLASSES[claim.status]]">
                  {{ STATUS_LABELS[claim.status] || claim.status }}
                </span>
              </td>
              <td class="date-col">{{ formatDate(claim.created_at) }}</td>
              <td>
                <a :href="claim.invoice" target="_blank" class="btn-invoice" title="Ver factura">📄</a>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="allClaims.some(c => c.status === 'REJECTED' && c.review_notes)" class="review-notes-section">
          <h3 class="notes-title">Notas de los Rechazos</h3>
          <div v-for="claim in allClaims.filter(c => c.status === 'REJECTED' && c.review_notes)" :key="'note-' + claim.id" class="note-card">
            <strong>#{{ claim.id }} — {{ claim.pet_name }}</strong>
            <p>{{ claim.review_notes }}</p>
          </div>
        </div>
      </div>
    </main>

    <ClaimFormModal v-model="showCreateModal" @saved="fetchClaims(true)" />
  </div>
</template>

<style scoped>
.dashboard { min-height: 100vh; background: #f1f5f9; }

/* Summary cards */
.content { padding: 32px 40px; max-width: 1300px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; }
.summary-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
.summary-card { background: white; padding: 20px 16px; border-radius: 16px; text-align: center; cursor: pointer; border: 2px solid transparent; transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.summary-card:hover { border-color: #e2e8f0; transform: translateY(-2px); }
.summary-card.active { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
.s-value { display: block; font-size: 2.2rem; font-weight: 800; color: #1e293b; }
.s-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; font-weight: 600; }
.summary-card.processing.active { border-color: #6366f1 !important; }
.summary-card.review { .s-value { color: #b45309; } }
.summary-card.approved { .s-value { color: #059669; } }
.summary-card.rejected { .s-value { color: #dc2626; } }

/* Main card */
.card { background: white; padding: 32px; border-radius: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.card-header h1 { font-size: 2rem; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.card-header p { color: #64748b; font-size: 0.95rem; }
.btn-add { background: #6366f1; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 700; font-size: 0.95rem; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.btn-add:hover { background: #4f46e5; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(99,102,241,0.25); }

/* Filter bar */
.filter-bar { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; padding-bottom: 24px; border-bottom: 1px solid #f1f5f9; }
.filter-pill { padding: 8px 18px; border-radius: 999px; border: 1.5px solid #e2e8f0; background: white; font-size: 0.85rem; font-weight: 600; color: #64748b; cursor: pointer; transition: all 0.2s; }
.filter-pill:hover { border-color: #6366f1; color: #6366f1; }
.filter-active { background: #6366f1 !important; border-color: #6366f1 !important; color: white !important; }

/* Loader & empty */
.loader-container { display: flex; justify-content: center; padding: 60px; }
.spinner { width: 40px; height: 40px; border: 3px solid #f1f5f9; border-top-color: #6366f1; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.empty-state { text-align: center; padding: 60px 20px; }
.empty-state .icon { font-size: 3rem; display: block; margin-bottom: 12px; }
.empty-state h3 { color: #475569; margin-bottom: 8px; font-size: 1.2rem; }
.empty-state p { color: #94a3b8; }
.btn-add-inline { display: inline-block; margin-top: 16px; background: #6366f1; color: white; border: none; padding: 10px 24px; border-radius: 10px; cursor: pointer; font-weight: 700; font-size: 0.9rem; transition: background 0.2s; }
.btn-add-inline:hover { background: #4f46e5; }

/* Table */
.claims-table { width: 100%; border-collapse: separate; border-spacing: 0; }
.claims-table th { text-align: left; padding: 12px 16px; border-bottom: 2px solid #f1f5f9; color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700; }
.claims-table td { padding: 16px; border-bottom: 1px solid #f8fafc; color: #334155; vertical-align: middle; font-size: 0.95rem; }
.claims-table tr:last-child td { border-bottom: none; }
.claims-table tbody tr { transition: background 0.15s; }
.claims-table tbody tr:hover td { background: #fafafe; }

.id-col { font-weight: 800; color: #94a3b8; font-size: 0.85rem; }
.pet-col { font-weight: 700; color: #1e293b; }
.amount-col { font-weight: 800; }
.date-col { color: #94a3b8; font-size: 0.85rem; }

/* Status badges */
.status-badge { padding: 5px 14px; border-radius: 999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.3px; white-space: nowrap; }
.st-processing { background: #eef2ff; color: #4f46e5; }
.st-review     { background: #fffbeb; color: #b45309; }
.st-approved   { background: #d1fae5; color: #065f46; }
.st-rejected   { background: #fee2e2; color: #991b1b; }

.btn-invoice { font-size: 1.2rem; text-decoration: none; cursor: pointer; transition: transform 0.2s; display: inline-block; }
.btn-invoice:hover { transform: scale(1.25); }

/* Review notes */
.review-notes-section { margin-top: 32px; padding-top: 24px; border-top: 1px solid #f1f5f9; }
.notes-title { font-size: 1rem; font-weight: 700; color: #1e293b; margin-bottom: 16px; }
.note-card { background: #fef2f2; border-left: 4px solid #dc2626; border-radius: 12px; padding: 16px 20px; margin-bottom: 12px; }
.note-card strong { font-size: 0.9rem; color: #991b1b; display: block; margin-bottom: 6px; }
.note-card p { color: #475569; font-size: 0.9rem; margin: 0; }

@media (max-width: 768px) {
  .summary-row { grid-template-columns: repeat(3, 1fr); }
  .content { padding: 20px; }
}
</style>
