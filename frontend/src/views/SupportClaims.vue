<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import ClaimService from '../services/ClaimService'
import AppHeader from '../components/AppHeader.vue'

const authStore = useAuthStore()
const claims = ref([])
const loading = ref(true)

// Modal state
const showModal = ref(false)
const selectedClaim = ref(null)
const reviewForm = ref({ status: 'APPROVED', review_notes: '' })
const reviewLoading = ref(false)
const reviewError = ref('')

const fetchClaims = async () => {
  loading.value = true
  try {
    const response = await ClaimService.getReviewList()
    claims.value = response.data
  } catch (e) {
    console.error('Error cargando reclamos', e)
  } finally {
    loading.value = false
  }
}

const formatCurrency = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(val)

const openModal = (claim) => {
  selectedClaim.value = claim
  reviewForm.value = { status: 'APPROVED', review_notes: '' }
  reviewError.value = ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedClaim.value = null
}

const submitReview = async () => {
  if (reviewForm.value.status === 'REJECTED' && !reviewForm.value.review_notes.trim()) {
    reviewError.value = 'Las notas de revisión son obligatorias al rechazar un reclamo.'
    return
  }
  try {
    reviewLoading.value = true
    reviewError.value = ''
    await ClaimService.submitReview(selectedClaim.value.id, reviewForm.value)
    closeModal()
    fetchClaims() 
  } catch (e) {
    if (e.response?.data) {
      const errors = e.response.data
      reviewError.value = Object.values(errors).flat().join(' ')
    } else {
      reviewError.value = 'Error al procesar la revisión.'
    }
  } finally {
    reviewLoading.value = false
  }
}

onMounted(fetchClaims)
</script>

<template>
  <div class="dashboard">
    <AppHeader role-badge="Soporte" />

    <main class="content">
      <div class="card">
        <div class="card-header">
          <div>
            <h1>Revisión de Reclamos</h1>
            <p>Reclamos en estado <span class="badge-in-review">En Revisión</span> pendientes de decisión.</p>
          </div>
          <div class="stats">
            <div class="stat-pill">
              <span class="count">{{ claims.length }}</span>
              <span class="label">Pendientes</span>
            </div>
          </div>
        </div>

        <div v-if="loading" class="loader-container">
          <div class="spinner"></div>
        </div>

        <div v-else-if="claims.length === 0" class="empty-state">
          <span class="icon">✅</span>
          <h3>Sin reclamos pendientes</h3>
          <p>No hay reclamos en estado IN_REVIEW en este momento.</p>
        </div>

        <table v-else class="claims-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Mascota</th>
              <th>Cliente (ID)</th>
              <th>Monto</th>
              <th>Fecha Factura</th>
              <th>Fecha Evento</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="claim in claims" :key="claim.id">
              <td class="id-col">#{{ claim.id }}</td>
              <td class="pet-col">{{ claim.pet_name }}</td>
              <td class="owner-col">Usuario #{{ claim.owner }}</td>
              <td class="amount-col">{{ formatCurrency(claim.amount) }}</td>
              <td>{{ claim.invoice_date }}</td>
              <td>{{ claim.date_of_event }}</td>
              <td>
                <button @click="openModal(claim)" class="btn-review">Revisar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- Modal de revisión -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h2>Revisar Reclamo #{{ selectedClaim?.id }}</h2>
          <button class="modal-close" @click="closeModal">✕</button>
        </div>

        <div class="modal-body">
          <!-- Claim details -->
          <div class="claim-details">
            <div class="detail-row">
              <span>Mascota:</span>
              <strong>{{ selectedClaim?.pet_name }}</strong>
            </div>
            <div class="detail-row">
              <span>Monto:</span>
              <strong>{{ formatCurrency(selectedClaim?.amount || 0) }}</strong>
            </div>
            <div class="detail-row">
              <span>Fecha Factura:</span>
              <strong>{{ selectedClaim?.invoice_date }}</strong>
            </div>
            <div class="detail-row">
              <span>Fecha Evento:</span>
              <strong>{{ selectedClaim?.date_of_event }}</strong>
            </div>
            <div class="detail-row">
              <span>Factura:</span>
              <a :href="selectedClaim?.invoice" target="_blank" class="invoice-link">Ver Documento 📄</a>
            </div>
          </div>

          <hr class="divider" />

          <!-- Decision form -->
          <div class="review-section">
            <label class="review-label">Decisión</label>
            <div class="decision-toggle">
              <button
                :class="['decision-btn', reviewForm.status === 'APPROVED' ? 'active-approve' : '']"
                @click="reviewForm.status = 'APPROVED'"
                type="button"
              >
                ✅ Aprobar
              </button>
              <button
                :class="['decision-btn', reviewForm.status === 'REJECTED' ? 'active-reject' : '']"
                @click="reviewForm.status = 'REJECTED'"
                type="button"
              >
                ❌ Rechazar
              </button>
            </div>

            <div class="form-group" :class="{ required: reviewForm.status === 'REJECTED' }">
              <label>
                Notas de Revisión
                <span v-if="reviewForm.status === 'REJECTED'" class="req">*requerido</span>
              </label>
              <textarea
                v-model="reviewForm.review_notes"
                :placeholder="reviewForm.status === 'REJECTED'
                  ? 'Explica el motivo del rechazo...'
                  : 'Notas adicionales (opcional)'"
                rows="4"
              ></textarea>
            </div>

            <div v-if="reviewError" class="error-box">{{ reviewError }}</div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeModal" class="btn-cancel">Cancelar</button>
          <button
            @click="submitReview"
            :class="['btn-confirm', reviewForm.status === 'APPROVED' ? 'btn-approve' : 'btn-reject']"
            :disabled="reviewLoading"
          >
            <span v-if="reviewLoading" class="spinner-sm"></span>
            {{ reviewLoading ? 'Procesando...' : (reviewForm.status === 'APPROVED' ? 'Confirmar Aprobación' : 'Confirmar Rechazo') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard { min-height: 100vh; background: #f8fafc; }

/* Content */
.content { padding: 40px; max-width: 1400px; margin: 0 auto; }
.card { background: white; padding: 36px; border-radius: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08); }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; }
.card-header h1 { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
.badge-in-review { background: #fffbeb; color: #b45309; padding: 2px 10px; border-radius: 999px; font-size: 0.85rem; font-weight: 700; }

.stats { display: flex; gap: 16px; }
.stat-pill { display: flex; flex-direction: column; align-items: center; background: #f1f5f9; padding: 12px 24px; border-radius: 16px; }
.stat-pill .count { font-size: 2rem; font-weight: 800; color: #1e293b; line-height: 1; }
.stat-pill .label { font-size: 0.75rem; text-transform: uppercase; color: #64748b; margin-top: 4px; }

/* Loader */
.loader-container { display: flex; justify-content: center; padding: 60px; }
.spinner { width: 40px; height: 40px; border: 3px solid #f1f5f9; border-top-color: #6366f1; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Empty */
.empty-state { text-align: center; padding: 60px; color: #94a3b8; }
.empty-state .icon { font-size: 3.5rem; display: block; margin-bottom: 12px; }

/* Table */
.claims-table { width: 100%; border-collapse: separate; border-spacing: 0; }
.claims-table th { text-align: left; padding: 14px 16px; border-bottom: 2px solid #f1f5f9; color: #64748b; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700; }
.claims-table td { padding: 16px; border-bottom: 1px solid #f8fafc; color: #334155; vertical-align: middle; }
.claims-table tr:hover td { background: #fafafe; }

.id-col { font-weight: 800; color: #94a3b8; }
.pet-col { font-weight: 700; color: #1e293b; }
.owner-col { font-size: 0.85rem; color: #64748b; }
.amount-col { font-weight: 800; color: #059669; }

.btn-review { background: #eef2ff; color: #4f46e5; border: none; padding: 8px 20px; border-radius: 10px; font-weight: 700; font-size: 0.9rem; cursor: pointer; transition: all 0.2s; }
.btn-review:hover { background: #6366f1; color: white; transform: translateY(-1px); }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(4px); padding: 20px; }
.modal { background: white; border-radius: 24px; width: 100%; max-width: 560px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); }

.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 24px 28px; border-bottom: 1px solid #f1f5f9; }
.modal-header h2 { font-size: 1.5rem; font-weight: 800; color: #1e293b; }
.modal-close { background: #f1f5f9; border: none; width: 32px; height: 32px; border-radius: 8px; cursor: pointer; font-size: 1rem; transition: all 0.2s; }
.modal-close:hover { background: #e2e8f0; }

.modal-body { padding: 28px; }

.claim-details { background: #f8fafc; border-radius: 16px; padding: 20px; margin-bottom: 24px; display: flex; flex-direction: column; gap: 10px; }
.detail-row { display: flex; justify-content: space-between; font-size: 0.9rem; color: #475569; }
.detail-row strong { color: #1e293b; }
.invoice-link { color: #6366f1; font-weight: 600; text-decoration: none; }
.invoice-link:hover { text-decoration: underline; }

.divider { border: none; border-top: 1px solid #f1f5f9; margin: 0 0 24px; }

.review-section { display: flex; flex-direction: column; gap: 20px; }
.review-label { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #475569; }

.decision-toggle { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.decision-btn { padding: 14px; border: 2px solid #e2e8f0; border-radius: 12px; background: white; cursor: pointer; font-size: 0.95rem; font-weight: 600; transition: all 0.2s; color: #64748b; }
.decision-btn:hover { border-color: #cbd5e1; }
.active-approve { border-color: #059669 !important; background: #d1fae5 !important; color: #065f46 !important; }
.active-reject { border-color: #dc2626 !important; background: #fee2e2 !important; color: #991b1b !important; }

.form-group label { display: block; font-size: 0.85rem; font-weight: 700; color: #334155; margin-bottom: 8px; }
.req { color: #ef4444; font-weight: 400; font-size: 0.78rem; margin-left: 6px; }
textarea { width: 100%; padding: 12px 16px; border: 1.5px solid #e2e8f0; border-radius: 12px; resize: vertical; font-family: inherit; font-size: 0.95rem; color: #1e293b; transition: all 0.2s; box-sizing: border-box; }
textarea:focus { outline: none; border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }

.error-box { padding: 12px 16px; background: #fee2e2; border-radius: 10px; color: #b91c1c; font-size: 0.85rem; border: 1px solid #fca5a5; }

.modal-footer { display: flex; justify-content: flex-end; gap: 12px; padding: 20px 28px; border-top: 1px solid #f1f5f9; }
.btn-cancel { padding: 12px 24px; background: #f1f5f9; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; color: #475569; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-confirm { padding: 12px 28px; border: none; border-radius: 12px; font-weight: 700; cursor: pointer; font-size: 1rem; transition: all 0.2s; display: flex; align-items: center; gap: 8px; color: white; }
.btn-approve { background: #059669; }
.btn-approve:hover:not(:disabled) { background: #047857; }
.btn-reject { background: #dc2626; }
.btn-reject:hover:not(:disabled) { background: #b91c1c; }
.btn-confirm:disabled { opacity: 0.6; cursor: not-allowed; }
.spinner-sm { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.8s linear infinite; }
</style>
