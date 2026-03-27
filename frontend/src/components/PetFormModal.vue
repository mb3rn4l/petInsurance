<script setup>
import { ref, watch } from 'vue'
import PetService from '../services/PetService'

const props = defineProps({
  pet: {
    type: Object,
    default: null
  },
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'saved'])

const form = ref({
  name: '',
  species: 'DOG',
  birth_date: '',
  coverage_start: new Date().toISOString().split('T')[0]
})
const loading = ref(false)
const error = ref('')

watch(() => props.modelValue, (open) => {
  if (open) {
    error.value = ''
    if (props.pet) {
      form.value = {
        name: props.pet.name,
        species: props.pet.species,
        birth_date: props.pet.birth_date,
        coverage_start: props.pet.coverage_start
      }
    } else {
      form.value = {
        name: '',
        species: 'DOG',
        birth_date: '',
        coverage_start: new Date().toISOString().split('T')[0]
      }
    }
  }
})

const close = () => emit('update:modelValue', false)

const handleSubmit = async () => {
  try {
    loading.value = true
    error.value = ''
    if (props.pet) {
      await PetService.update(props.pet.id, form.value)
    } else {
      await PetService.create(form.value)
    }
    emit('saved')
    close()
  } catch (err) {
    const detail = err.response?.data
    if (detail && typeof detail === 'object') {
      error.value = Object.values(detail).flat().join(' ')
    } else {
      error.value = 'Error al guardar. Verifica los campos.'
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
              <h2>{{ pet ? '✏️ Editar Mascota' : '🐾 Registrar Mascota' }}</h2>
              <p>{{ pet ? 'Actualiza los datos de tu mascota.' : 'Ingresa los datos para una nueva mascota.' }}</p>
            </div>
            <button class="btn-close" @click="close" aria-label="Cerrar">✕</button>
          </div>

          <form @submit.prevent="handleSubmit" class="modal-body">
            <div class="form-grid">

              <div class="form-group wide">
                <label for="m-name">Nombre</label>
                <input id="m-name" v-model="form.name" type="text"
                       placeholder="Ej. Boby" required :disabled="loading" />
              </div>

              <div class="form-group">
                <label for="m-species">Especie</label>
                <select id="m-species" v-model="form.species" required :disabled="loading">
                  <option value="DOG">🐶 Perro</option>
                  <option value="CAT">🐱 Gato</option>
                  <option value="OTHER">🐾 Otro</option>
                </select>
              </div>

              <div class="form-group">
                <label for="m-birth">Fecha de Nacimiento</label>
                <input id="m-birth" v-model="form.birth_date" type="date"
                       required :disabled="loading" />
              </div>

              <div class="form-group wide">
                <label for="m-coverage">Inicio de Cobertura</label>
                <input id="m-coverage" v-model="form.coverage_start" type="date"
                       required :disabled="loading" />
                <small>La cobertura tendrá una duración de 365 días.</small>
              </div>
            </div>

            <div v-if="error" class="error-box">{{ error }}</div>

            <div class="modal-footer">
              <button type="button" @click="close" class="btn-cancel">Cancelar</button>
              <button type="submit" class="btn-submit" :disabled="loading">
                <span v-if="loading" class="spinner"></span>
                {{ loading ? 'Guardando...' : (pet ? 'Guardar Cambios' : 'Registrar Mascota') }}
              </button>
            </div>
          </form>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/* ---- Overlay ---- */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
  padding: 20px;
  backdrop-filter: blur(6px);
}

/* ---- Modal box ---- */
.modal {
  background: white;
  border-radius: 28px;
  width: 100%;
  max-width: 560px;
  box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

/* ---- Header ---- */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 28px 32px 20px;
  border-bottom: 1px solid #f1f5f9;
}
.modal-header h2 { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0 0 4px; }
.modal-header p  { font-size: 0.9rem; color: #64748b; margin: 0; }

.btn-close {
  background: #f1f5f9;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1rem;
  flex-shrink: 0;
  transition: all 0.2s;
  color: #475569;
}
.btn-close:hover { background: #e2e8f0; color: #1e293b; }

/* ---- Body / Form ---- */
.modal-body {
  padding: 28px 32px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.form-group.wide { grid-column: span 2; }

label {
  display: block;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #475569;
  margin-bottom: 8px;
}

input, select {
  width: 100%;
  padding: 12px 16px;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.95rem;
  color: #1e293b;
  transition: all 0.2s;
  box-sizing: border-box;
}
input:focus, select:focus {
  outline: none;
  background: white;
  border-color: #6366f1;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

small { display: block; margin-top: 6px; color: #94a3b8; font-size: 0.78rem; }

.error-box {
  padding: 12px 16px;
  background: #fee2e2;
  border: 1px solid #fca5a5;
  border-radius: 10px;
  color: #b91c1c;
  font-size: 0.875rem;
}

/* ---- Footer ---- */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 4px;
}

.btn-cancel {
  padding: 12px 24px;
  background: #f1f5f9;
  border: none;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-cancel:hover { background: #e2e8f0; }

.btn-submit {
  padding: 12px 28px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}
.btn-submit:hover:not(:disabled) {
  background: #4f46e5;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99,102,241,0.3);
}
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.35);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); }}

/* ---- Transition ---- */
.modal-enter-active, .modal-leave-active { transition: all 0.25s ease; }
.modal-enter-active .modal, .modal-leave-active .modal { transition: all 0.25s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal, .modal-leave-to .modal { transform: translateY(20px) scale(0.97); }

@media (max-width: 540px) {
  .form-grid { grid-template-columns: 1fr; }
  .form-group.wide { grid-column: span 1; }
  .modal-body { padding: 20px; }
  .modal-header { padding: 20px; }
}
</style>
