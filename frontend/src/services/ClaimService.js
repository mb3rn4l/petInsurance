import api from './api'

export default {
  getAll() { return api.get('claims/') },
  getAllFiltered(qs = '') { return api.get(`claims/${qs}`) },
  get(id) { return api.get(`claims/${id}/`) },
  create(formData) {
    return api.post('claims/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  delete(id) { return api.delete(`claims/${id}/`) },
  getReviewList() { return api.get('claims/review/') },
  submitReview(id, data) { return api.post(`claims/${id}/review/`, data) },
}
