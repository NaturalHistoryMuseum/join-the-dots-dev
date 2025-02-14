import axios from 'axios'

export async function getGeneric(route) {
  const resp = await axios.get(`http://localhost:5000/api/data/${route}`).then((response) => {
    return response.data
  })
  return resp
}

export async function downloadCSV(view) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/data/export-view/${view}`)
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
