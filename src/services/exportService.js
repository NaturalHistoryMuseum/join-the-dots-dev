import api from '@/services/api';

export async function downloadCSV(view) {
  try {
    const response = await api.get(`/export-view/${view}`);
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
    const response = await api.get(`export/export-ltc-json`, {
      responseType: 'blob',
      withCredentials: true,
      // timeout: 100000,
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

export async function downloadCustomExport(config) {
  try {
    const response = await api.post(`export/data-export`, config, {
      responseType: 'blob',
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
      timeout: 120000,
    });
    const blob = new Blob([response.data], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `JtD ${config.selected_data_type === 'ltc' ? 'LtC' : 'Data'} Export - ${new Date().toLocaleString()}.${config.selected_data_type === 'ltc' ? 'json' : config.selected_data_type}`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading custom export:', error);
  }
}
