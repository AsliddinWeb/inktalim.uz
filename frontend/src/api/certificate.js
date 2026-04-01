// Sertifikat API — student endpointlari

import api from './axios.js'

/**
 * Kurs uchun sertifikat olish yoki mavjudini qaytarish.
 * Kurs 100% tugatilgan bo'lmasa → 403 xatosi.
 */
export function getCertificate(courseId) {
  return api.get(`/student/certificates/courses/${courseId}/certificate`)
}

/**
 * Foydalanuvchining barcha sertifikatlari ro'yxati.
 */
export function getAllCertificates() {
  return api.get('/student/certificates')
}

/**
 * PDF sertifikatni yuklab olish.
 * responseType: 'blob' — binary data sifatida olinadi.
 */
export function downloadCertificate(certNumber) {
  return api.get(`/student/certificates/download/${certNumber}`, {
    responseType: 'blob',
  })
}
