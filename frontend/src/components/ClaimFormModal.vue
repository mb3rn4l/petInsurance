<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import ClaimService from '../services/ClaimService'
import PetService from '../services/PetService'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'saved'])

const router = useRouter()

const pets = ref([])
const loading = ref(false)
const error = ref('')

const claim = ref({
  pet: '',
  invoice_date: '',
  date_of_event: '',
  amount: ''
})
const invoiceFile = ref(null)
const fileInputRef = ref(null)

const fetchPets = async () => {
  try {
    const response = await PetService.getAll()
    pets.value = response.data
    if (pets.value.length > 0 && !claim.value.pet) {
      claim.value.pet = pets.value[0].id
    }
  } catch (err) {
    error.value = 'No se pudieron cargar tus mascotas.'
  }
}

watch(() => props.modelValue, (open) => {
  if (open) {
    error.value = ''
    claim.value = {
      pet: '',
      invoice_date: '',
      date_of_event: '',
      amount: ''
    }
    invoiceFile.value = null
    if (fileInputRef.value) fileInputRef.value.value = ''
    fetchPets()
  }
})

const close = () => {
  emit('update:modelValue', false)
}

const handleFileChange = (e) => {
  invoiceFile.value = e.target.files[0]
}

const handleSubmit = async () => {
  if (!invoiceFile.value) {
    error.value = 'Debes subir una factura.'
    return
  }

  const formData = new FormData()
  formData.append('pet', claim.value.pet)
  formData.append('invoice', invoiceFile.value)
  formData.append('invoice_date', claim.value.invoice_date)
  formData.append('date_of_event', claim.value.date_of_event)
  formData.append('amount', claim.value.amount)

  try {
    loading.value = true
    error.value = ''
    await ClaimService.create(formData)
    
    emit('saved')
    close()
  } catch (err) {
    if (err.response?.data) {
        const apiErrors = err.response.data
        const firstKey = Object.keys(apiErrors)[0]
        error.value = Array.isArray(apiErrors[firstKey]) ? apiErrors[firstKey][0] : apiErrors[firstKey]
    } else {
        error.value = 'Error al crear el reclamo. Verifica los datos y el archivo.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="overlay" @click.self="close">
        <div class="modal" role="dialog" aria-modal="true">

          <div class="modal-header">
            <div>
              <h2>📝 Crear Reclamo</h2>
              <p>Solicita tu reembolso cargando la factura médica.</p>
            </div>
            <button class="btn-close" @click="close" aria-label="Cerrar">✕</button>
          </div>

          <div class="modal-body">
            
            <div v-if="pets.length === 0 && !loading" class="no-pets-warning">
              <span class="icon">⚠️</span>
              <h4>Sin mascotas</h4>
              <p>Registra al menos una mascota antes de crear un reclamo.</p>
              <button type="button" class="btn-link" @click="close(); router.push('/pets')">
                Ir a Mis Mascotas
              </button>
            </div>

            <form v-else @submit.prevent="handleSubmit" class="main-form">
              <div class="form-group">
                <label for="pet">Mascota Afectada</label>
                <select id="pet" v-model="claim.pet" required :disabled="loading">
                  <option v-for="p in pets" :key="p.id" :value="p.id">
                    {{ p.name }} ({{ p.species === 'DOG' ? 'Perro' : p.species === 'CAT' ? 'Gato' : 'Otro' }})
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label for="invoice">Archivo de Factura</label>
                <div class="file-upload">
                  <input id="invoice" type="file" ref="fileInputRef" @change="handleFileChange" accept=".pdf,image/*" required :disabled="loading" />
                  <div class="file-custom">
                    <span class="file-icon">📁</span>
                    {{ invoiceFile ? invoiceFile.name : 'Haz clic para seleccionar PDF/Imagen' }}
                  </div>
                </div>
              </div>

              <div class="form-grid">
                <div class="form-group">
                  <label for="invoice_date">Fecha de la Factura</label>
                  <input id="invoice_date" v-model="claim.invoice_date" type="date" required :disabled="loading" />
                </div>
                <div class="form-group">
                  <label for="date_of_event">Fecha del Evento</label>
                  <input id="date_of_event" v-model="claim.date_of_event" type="date" required :disabled="loading" />
                </div>
              </div>

              <div class="form-group">
                <label for="amount">Monto Solicitado (COP)</label>
                <div class="input-with-symbol">
                  <span class="symbol">$</span>
                  <input id="amount" v-model="claim.amount" type="number" step="0.01" placeholder="Ej. 150000" required :disabled="loading" />
                </div>
              </div>

              <div v-if="error" class="error-box">
                <strong>Error: </strong> {{ error }}
              </div>

              <div class="modal-footer">
                <button type="button" @click="close" class="btn-cancel" :disabled="loading">Cancelar</button>
                <button type="submit" class="btn-submit" :disabled="loading">
                  <span v-if="loading" class="spinner"></span>
                  {{ loading ? 'Enviando...' : 'Enviar Solicitud' }}
                </button>
              </div>
            </form>
            
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/* ---- Overlay ---- */
.overlay {
  position: fixed; inset: 0; background: rgba(15, 23, 42, 0.55);
  display: flex; align-items: center; justify-content: center;
  z-index: 200; padding: 20px; backdrop-filter: blur(6px);
}

/* ---- Modal box ---- */
.modal {
  background: white; border-radius: 28px; width: 100%; max-width: 580px;
  box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.3); overflow: hidden;
}

/* ---- Header ---- */
.modal-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  padding: 28px 32px 20px; border-bottom: 1px solid #f1f5f9;
}
.modal-header h2 { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0 0 4px; }
.modal-header p  { font-size: 0.9rem; color: #64748b; margin: 0; }

.btn-close {
  background: #f1f5f9; border: none; width: 36px; height: 36px; border-radius: 10px;
  cursor: pointer; font-size: 1rem; flex-shrink: 0; transition: all 0.2s; color: #475569;
}
.btn-close:hover { background: #e2e8f0; color: #1e293b; }

/* ---- Body / Form ---- */
.modal-body { padding: 24px 32px 32px; }

.main-form { display: flex; flex-direction: column; gap: 20px; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

label {
  display: block; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.5px; color: #475569; margin-bottom: 8px;
}

input, select {
  width: 100%; padding: 12px 16px; background: #f8fafc; border: 1.5px solid #e2e8f0;
  border-radius: 12px; font-size: 0.95rem; color: #1e293b; transition: all 0.2s; box-sizing: border-box;
}
input:focus, select:focus { outline: none; background: white; border-color: #6366f1; box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1); }

/* File upload */
.file-upload { position: relative; cursor: pointer; }
.file-upload input { opacity: 0; position: absolute; z-index: 2; width: 100%; height: 100%; cursor: pointer; }
.file-custom { 
  padding: 16px; background: #f8fafc; border: 1.5px dashed #cbd5e1;
  border-radius: 12px; text-align: center; color: #64748b; font-size: 0.9rem;
  transition: all 0.2s; display: flex; flex-direction: column; align-items: center; gap: 8px;
}
.file-icon { font-size: 1.5rem; }
.file-upload:hover .file-custom, .file-upload input:focus + .file-custom {
  border-color: #6366f1; background: #eef2ff; color: #4f46e5;
}

/* Input symbol */
.input-with-symbol { position: relative; }
.symbol { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); color: #64748b; font-weight: 700; font-size: 1.1rem; }
.input-with-symbol input { padding-left: 36px; }

/* Warnings & Errors */
.no-pets-warning { text-align: center; padding: 32px 24px; background: #fffbeb; border: 1.5px solid #fef3c7; border-radius: 16px; color: #b45309; }
.no-pets-warning .icon { font-size: 2.5rem; display: block; margin-bottom: 12px; }
.no-pets-warning h4 { font-size: 1.1rem; margin: 0 0 8px; color: #92400e; font-weight: 800; }
.btn-link { margin-top: 16px; background: white; border: 1px solid #fde68a; color: #b45309; padding: 8px 16px; border-radius: 8px; font-weight: 700; cursor: pointer; }
.btn-link:hover { background: #fef3c7; }

.error-box { padding: 12px 16px; background: #fef2f2; border-left: 4px solid #ef4444; border-radius: 8px; color: #991b1b; font-size: 0.875rem; }

/* ---- Footer ---- */
.modal-footer { display: flex; justify-content: flex-end; gap: 12px; padding-top: 12px; }

.btn-cancel {
  padding: 12px 24px; background: #f1f5f9; border: none; border-radius: 12px;
  font-size: 0.95rem; font-weight: 600; color: #475569; cursor: pointer; transition: background 0.2s;
}
.btn-cancel:hover { background: #e2e8f0; }

.btn-submit {
  padding: 12px 28px; background: #6366f1; color: white; border: none; border-radius: 12px;
  font-size: 0.95rem; font-weight: 700; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 8px;
}
.btn-submit:hover:not(:disabled) { background: #4f46e5; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(99,102,241,0.3); }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  width: 18px; height: 18px; border: 2px solid rgba(255,255,255,0.35); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); }}

/* ---- Transition ---- */
.modal-enter-active, .modal-leave-active { transition: all 0.25s ease; }
.modal-enter-active .modal, .modal-leave-active .modal { transition: all 0.25s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal, .modal-leave-to .modal { transform: translateY(20px) scale(0.97); }

@media (max-width: 540px) {
  .form-grid { grid-template-columns: 1fr; }
  .modal-body { padding: 20px; }
  .modal-header { padding: 20px; }
}
</style>
