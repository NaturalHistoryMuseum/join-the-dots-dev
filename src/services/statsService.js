import { api, API_URL } from './api';

export async function getStatsGeneric(route) {
  const resp = await api
    .get(`${API_URL}/${route}`, { withCredentials: true })
    .then((response) => {
      return response.data;
    });
  return resp;
}
