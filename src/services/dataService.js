import axios from 'axios'

// FOR LOCAL TESTING
const API_URL = 'http://localhost:5000/api/data'
// FOR K8S
// const API_URL = 'https://jtd-qa.nhm.ac.uk/api/data'

export async function getGeneric(route) {
  const resp = await axios.get(`${API_URL}/${route}`).then((response) => {
    return response.data
  })
  return resp
}

export async function downloadCSV(view) {
  try {
    const response = await fetch(`${API_URL}/export-view/${view}`)
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = view + '.csv'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  } catch (error) {
    console.error('Error downloading CSV:', error)
  }
}

export async function downloadLtCjson() {
  try {
    const response = await axios.get(`${API_URL}/export-ltc-json`, {
      responseType: 'blob',
    })
    const blob = new Blob([response.data], { type: 'application/json' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    const date = new Date()
    a.setAttribute('download', `LtC JtD Export - ${date.toLocaleString()}.json`)
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Error downloading JSON:', error)
  }
}
