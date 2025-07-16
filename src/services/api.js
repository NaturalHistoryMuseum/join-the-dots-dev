import axios from 'axios';
import { getCookie } from './cookies';

// FOR LOCAL TESTING
const API_URL = 'http://localhost:5000/api/';
// FOR K8S
// const API_URL = 'https://jtd-qa.nhm.ac.uk/api/';

export const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to inject CSRF token into header
api.interceptors.request.use((config) => {
  // let csrfToken = getCookie('csrf_token');
  // console.log('got csrf token: ', csrfToken);

  // // If this is a refresh request, use the refresh CSRF token
  // if (config.url?.includes('/auth/refresh')) {
  //   csrfToken = getCookie('csrf_refresh_token');
  //   console.log('Using refresh CSRF token: ', csrfToken);
  // } else {
  //   console.log('Using access CSRF token: ', csrfToken);
  // }

  // if (csrfToken) {
  //   config.headers['X-CSRF-TOKEN'] = csrfToken;
  // }
  // return config;

  // Only set the CSRF header if it’s not already set manually (e.g. for /auth/refresh)
  if (!config.headers['X-CSRF-TOKEN']) {
    const csrfToken = getCookie('csrf_token');
    console.log('Interceptor using access CSRF token: ', csrfToken);
    if (csrfToken) {
      config.headers['X-CSRF-TOKEN'] = csrfToken;
    }
  } else {
    console.log(
      'Interceptor: using manually set CSRF token: ',
      config.headers['X-CSRF-TOKEN'],
    );
  }

  return config;
});

// //Adds interceptor for refresh token
// api.interceptors.response.use(
//   (response) => response,
//   async (error) => {
//     const originalRequest = error.config;
//     console.log('error in response');
//     console.log(error);
//     console.log(error.response);
//     if (
//       error.response?.status === 401 &&
//       !originalRequest._retry &&
//       !originalRequest.url.includes('refresh')
//     ) {
//       originalRequest._retry = true;
//       try {
//         console.log('try a refresh');
//         console.log('this is the csrf token', getCookie('csrf_refresh_token'));
//         await api.post(
//           `auth/refresh`,
//           {},
//           {
//             withCredentials: true,
//             headers: {
//               // This is deliberately set to bypass the request interceptor's default
//               'X-CSRF-TOKEN': getCookie('csrf_refresh_token'),
//             },
//           },
//         );
//         // Retry original request
//         return api(originalRequest);
//       } catch (refreshError) {
//         console.error('Token refresh failed:', refreshError);
//         // Call a logout function
//         logout();
//       }
//     }
//     return Promise.reject(error);
//   },
// );

export default api;
