// Centralized API utility for case, breed, and sex endpoints
import axios from 'axios';
import { ref } from 'vue';

const axiosInstance = axios.create({
  timeout: 10000 // Increased from 2000ms to 10000ms
});

// CASES
export async function fetchCases(query = '') {
  const params = {};
  if (query && query.trim()) {
    params.fuzzy_match = query.trim();
  }
  const res = await axiosInstance.get('/api/case', { params });
  return res.data;
}

export async function fetchCase(id) {
  const res = await axiosInstance.get(`/api/case/${id}`);
  return res.data;
}

export async function addCase(caseData) {
  const res = await axiosInstance.post('/api/case', caseData);
  return res.data;
}

export async function updateCase(id, caseData) {
  const res = await axiosInstance.put(`/api/case/${id}`, caseData);
  return res.data;
}

export async function deleteCase(id) {
  const res = await axiosInstance.delete(`/api/case/${id}`);
  return res.data;
}

// BREEDS
export async function fetchBreeds() {
  const res = await axiosInstance.get('/api/breed');
  return res.data;
}

export async function fetchBreedById(breedId) {
  const res = await axiosInstance.get(`/api/breed/${breedId}`);
  return res.data;
}

export async function fetchBreedByName(breedName) {
  const res = await axiosInstance.get(`/api/breed/by_name/${encodeURIComponent(breedName)}`);
  return res.data;
}

// SEXES
export async function fetchSexes() {
  const res = await axiosInstance.get('/api/sex');
  return res.data;
}

// SPECIES
export async function fetchSpecies() {
  const res = await axiosInstance.get('/api/species');
  return res.data;
}

// BREEDS BY SPECIES
export async function fetchBreedsBySpecies(species) {
  const res = await axiosInstance.get('/api/breed', { params: { species } });
  return res.data;
}

// ROOT ENDPOINT
export async function fetchApiRoot() {
  const res = await axiosInstance.get('/api/');
  return res.data;
}

// Utility for consistent error messages
export function getApiErrorMessage(err, defaultMsg) {
  let msg = defaultMsg;
  if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
    msg = 'Request timed out. The backend may be unreachable.';
  } else if (err.message === 'Network Error') {
    msg = 'Network error. The backend may be unreachable.';
  } else if (err.code === 'ERR_BAD_RESPONSE') {
    msg = 'The backend did not respond correctly. It may be down or misconfigured.';
  } else if (err.code === 'ECONNREFUSED') {
    msg = 'Connection refused. The backend server is not running or not reachable.';
  } else if (err.response && err.response.status === 500) {
    msg = 'Internal server error (500). The backend encountered an error.';
  } else if (err.response && err.response.data && err.response.data.detail) {
    msg = err.response.data.detail;
  }
  return msg;
}

// Composable for consistent API error handling and popup state
export function useApiErrorHandler() {
  const showPopup = ref(false);
  const popupMessage = ref('');

  function handleError(err, defaultMsg) {
    popupMessage.value = getApiErrorMessage(err, defaultMsg);
    showPopup.value = true;
  }

  function closePopup() {
    showPopup.value = false;
    popupMessage.value = '';
  }

  return {
    showPopup,
    popupMessage,
    handleError,
    closePopup
  };
}
