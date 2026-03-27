<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import PetService from '../services/PetService'
import AppHeader from '../components/AppHeader.vue'
import PetFormModal from '../components/PetFormModal.vue'

const authStore = useAuthStore()
const pets = ref([])
const loading = ref(true)

const showModal = ref(false)
const editingPet = ref(null)

const fetchPets = async () => {
  try {
    loading.value = true
    const response = await PetService.getAll()
    pets.value = response.data
  } catch (error) {
    console.error('Error fetching pets:', error)
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  editingPet.value = null
  showModal.value = true
}

const openEdit = (pet) => {
  editingPet.value = pet
  showModal.value = true
}

const deletePet = async (id) => {
  if (confirm('¿Estás seguro de que deseas eliminar esta mascota?')) {
    try {
      await PetService.delete(id)
      fetchPets()
    } catch {
      alert('Error al eliminar la mascota')
    }
  }
}

onMounted(fetchPets)
</script>

<template>
  <div class="dashboard">
    <AppHeader :nav-links="[
      { to: '/pets', label: 'Mascotas' },
      { to: '/claims', label: 'Reclamos' }
    ]" />

    <main class="content">
      <div class="card">
        <div class="card-header">
          <div>
            <h1>Mis Mascotas</h1>
            <p>Gestiona tus mascotas y sus coberturas de seguro.</p>
          </div>
          <button @click="openCreate" class="btn-add">
            <span>+</span> Registrar Mascota
          </button>
        </div>

        <div v-if="loading" class="loader-container">
          <div class="spinner"></div>
        </div>

        <div v-else-if="pets.length === 0" class="empty-state">
          <span class="icon">🔍</span>
          <h3>No tienes mascotas registradas</h3>
          <p>Comienza registrando tu primera mascota para contratar un seguro.</p>
          <button @click="openCreate" class="btn-add-inline">Registrar primera mascota</button>
        </div>

        <div v-else class="pet-grid">
          <div v-for="pet in pets" :key="pet.id" class="pet-card">
            <div class="pet-actions">
              <button @click="openEdit(pet)" class="btn-icon" title="Editar">✏️</button>
              <button @click="deletePet(pet.id)" class="btn-icon btn-delete" title="Eliminar">🗑️</button>
            </div>
            <span class="pet-icon">{{ pet.species === 'DOG' ? '🐶' : pet.species === 'CAT' ? '🐱' : '🐾' }}</span>
            <h3>{{ pet.name }}</h3>
            <p class="species">{{ pet.species === 'DOG' ? 'Perro' : pet.species === 'CAT' ? 'Gato' : 'Otro' }}</p>
            <div class="coverage-info">
              <div class="info-row">
                <span>Nacimiento:</span>
                <strong>{{ pet.birth_date }}</strong>
              </div>
              <div class="info-row">
                <span>Inicio Cobertura:</span>
                <strong>{{ pet.coverage_start }}</strong>
              </div>
              <div class="info-row highlight">
                <span>Fin Cobertura:</span>
                <strong>{{ pet.coverage_end }}</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <PetFormModal
      v-model="showModal"
      :pet="editingPet"
      @saved="fetchPets"
    />
  </div>
</template>

<style scoped>
.dashboard { min-height: 100vh; background: #f8fafc; }

.content { padding: 40px; max-width: 1200px; margin: 0 auto; }
.card { background: white; padding: 32px; border-radius: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; }
.card-header h1 { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.card-header p { color: #64748b; }

.btn-add {
  background: #6366f1;
  color: white;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
  white-space: nowrap;
}
.btn-add:hover { background: #4f46e5; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3); }

.loader-container { display: flex; justify-content: center; padding: 60px; }
.spinner { width: 40px; height: 40px; border: 3px solid #f1f5f9; border-top-color: #6366f1; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state { text-align: center; padding: 60px; color: #94a3b8; }
.empty-state .icon { font-size: 4rem; display: block; margin-bottom: 16px; }
.empty-state h3 { color: #475569; margin-bottom: 8px; }
.empty-state p { margin-bottom: 24px; }
.btn-add-inline {
  background: #6366f1;
  color: white;
  padding: 12px 28px;
  border-radius: 12px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.2s;
}
.btn-add-inline:hover { background: #4f46e5; }

.pet-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 24px; }
.pet-card { background: #f8fafc; border-radius: 20px; padding: 24px; border: 1px solid #f1f5f9; position: relative; transition: all 0.3s ease; text-align: center; }
.pet-card:hover { background: white; transform: translateY(-6px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); border-color: #e2e8f0; }

.pet-actions { position: absolute; top: 16px; right: 16px; display: flex; gap: 8px; }
.btn-icon { background: white; border: 1px solid #e2e8f0; width: 32px; height: 32px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; transition: all 0.2s; }
.btn-icon:hover { background: #f1f5f9; transform: scale(1.1); }
.btn-delete:hover { background: #fee2e2; border-color: #fca5a5; }

.pet-icon { font-size: 3.5rem; display: block; margin-bottom: 12px; }
.pet-card h3 { font-size: 1.4rem; font-weight: 800; color: #1e293b; margin-bottom: 4px; }
.species { color: #6366f1; font-weight: 700; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px; }

.coverage-info { background: white; padding: 16px; border-radius: 12px; border: 1px solid #f1f5f9; }
.info-row { display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 8px; color: #64748b; }
.info-row:last-child { margin-bottom: 0; }
.info-row strong { color: #334155; }
.info-row.highlight { margin-top: 12px; padding-top: 12px; border-top: 1px dashed #e2e8f0; color: #059669; }
.info-row.highlight strong { color: #059669; }
</style>
