function getAccessToken() {
  return localStorage.getItem('access_token');
}

function authorizedFetch(url, options = {}) {
  const headers = new Headers(options.headers || {});
  const token = getAccessToken();
  if (token) {
    headers.set('Authorization', 'Bearer ' + token);
  }
  return fetch(url, { ...options, headers });
}

function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  return fetch('/api/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ refresh_token: refreshToken })
  })
  .then(response => response.json())
  .then(data => {
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
      return data.access_token;
    } else {
      throw new Error('Failed to refresh token');
    }
  });
}

function authorizedFetchWithRetry(url, options = {}) {
  return authorizedFetch(url, options)
    .then(response => {
      if (response.status === 401) {
        // Attempt to refresh the token
        return refreshAccessToken()
          .then(() => authorizedFetch(url, options)); // Retry the original request
      }
      return response;
    });
}