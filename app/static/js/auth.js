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

async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  const response = await fetch('/api/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ refresh_token: refreshToken })
  });
  const data = await response.json();
  if (data.access_token) {
    localStorage.setItem('access_token', data.access_token);
    return data.access_token;
  } else {
    throw new Error('Failed to refresh token');
  }
}

async function authorizedFetchWithRetry(url, options = {}) {
  const response = await authorizedFetch(url, options);
  if (response.status === 401) {
    // Attempt to refresh the token
    await refreshAccessToken();
    return authorizedFetch(url, options); // Retry the original request
  }
  return response;
}