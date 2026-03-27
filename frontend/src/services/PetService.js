import api from './api'

export default {
  getAll() { return api.get('pets/') },
  get(id) { return api.get(`pets/${id}/`) },
  create(data) { return api.post('pets/', data) },
  update(id, data) { return api.put(`pets/${id}/`, data) },
  delete(id) { return api.delete(`pets/${id}/`) },
}
