import axios from 'axios';

// FOR LOCAL TESTING
// const API_URL = 'http://localhost:5000/api/stats';
// FOR K8S
const API_URL = 'https://jtd-qa.nhm.ac.uk/api/stats'

export async function getStatsGeneric(route) {
  const resp = await axios
    .get(`${API_URL}/${route}`, { withCredentials: true })
    .then((response) => {
      return response.data;
    });
  return resp;
}
