function fetchData(endpoint, method = 'GET', headers = {}, body = null) {
    // Prepend '/api/v1/' to the endpoint
    const url = `/api/v1/${endpoint}`;

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: method,
            headers: headers,
            body: body ? JSON.stringify(body) : null,
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                resolve(data);
            })
            .catch(error => {
                reject(error);
            });
    });
}

// Example usage:
// const apiUrl = '/api/data';  // Replace with your API endpoint
// const requestData = {
//     param1: 'value1',
//     param2: 'value2'
// };
//
// fetchData(apiUrl, 'POST', {
//     'Content-Type': 'application/json'
// }, requestData)
//     .then(data => {
//         console.log('Data received:', data);
//     })
//     .catch(error => {
//         console.error('Error fetching data:', error);
//     });
