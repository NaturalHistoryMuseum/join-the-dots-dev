import axios from 'axios';

// FOR LOCAL TESTING
const API_URL = 'http://localhost:5000/api/data';
// FOR K8S
// const API_URL = 'https://jtd-qa.nhm.ac.uk/api/data'

export async function getGeneric(route) {
  const resp = await axios
    .get(`${API_URL}/${route}`, { withCredentials: true })
    .then((response) => {
      return response.data;
    });
  return resp;
}

export async function downloadCSV(view) {
  try {
    const response = await fetch(`${API_URL}/export-view/${view}`);
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = view + '.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  } catch (error) {
    console.error('Error downloading CSV:', error);
  }
}

export async function downloadLtCjson() {
  try {
    const response = await axios.get(`${API_URL}/export-ltc-json`, {
      responseType: 'blob',
      withCredentials: true,
    });
    const blob = new Blob([response.data], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const date = new Date();
    a.setAttribute(
      'download',
      `LtC JtD Export - ${date.toLocaleString()}.json`,
    );
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading JSON:', error);
  }
}

export async function markRescoreOpen(units) {
  try {
    const response = await axios.post(
      `${API_URL}/mark-rescore-open`,
      { units: units },
      {
        headers: { 'Content-Type': 'application/json' },
        withCredentials: true,
      },
    );
    return response.data;
  } catch (error) {
    console.error('Error marking rescore open:', error);
    throw error;
  }
}
export async function markRescoreComplete(rescore_session_id) {
  try {
    const response = await axios.post(
      `${API_URL}/end-rescore/${rescore_session_id}`,
      {
        withCredentials: true,
      },
    );
    return response.data;
  } catch (error) {
    console.error('Error completing rescore:', error);
    throw error;
  }
}

export async function completeCats(
  rescore_session_units_id,
  category_ids_arr,
  new_val,
) {
  try {
    const response = await axios.post(
      `${API_URL}/complete-category`,
      {
        rescore_session_units_id: rescore_session_units_id,
        category_ids_arr: category_ids_arr,
        new_val: new_val,
      },
      {
        withCredentials: true,
      },
    );
    return response.data;
  } catch (error) {
    console.error('Error completing rescore:', error);
    throw error;
  }
}

export async function submitDraftRrank(rank_draft) {
  try {
    const response = await axios.post(
      `${API_URL}/submit-draft-rank`,
      rank_draft,
      {
        headers: { 'Content-Type': 'application/json' },
        withCredentials: true,
      },
    );
    return response.data;
  } catch (error) {
    console.error('Error submitting draft rank:', error);
    throw error;
  }
}

export async function submitDataGeneric(route, data_json) {
  try {
    const response = await axios.post(`${API_URL}/${route}`, data_json, {
      headers: { 'Content-Type': 'application/json' },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    console.error('Error submitting data:', error);
    throw error;
  }
}
