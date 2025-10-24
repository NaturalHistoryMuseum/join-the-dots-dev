import { getApi } from '@/services/api';

export async function getStatsGeneric(route) {
  const api = getApi();
  const resp = await api
    .get(`/${route}`, { withCredentials: true })
    .then((response) => {
      return response.data;
    });
  return resp;
}
