const API_BASE_URL = "http://127.0.0.1:8000/api";

/**
 * Fungsi pembungkus fetch untuk komunikasi ke backend Django.
 * Fungsi ini otomatis mengambil access_token dari localStorage
 * dan memasukkannya ke header Authorization.
 */
async function requestAPI(endpoint, method = "GET", bodyData = null) {
    const accessToken = localStorage.getItem("access_token");

    const headers = {
        "Content-Type": "application/json"
    };

    if (accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }

    const config = {
        method: method,
        headers: headers
    };

    if (bodyData !== null) {
        config.body = JSON.stringify(bodyData);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    let data = null;

    try {
        data = await response.json();
    } catch (error) {
        data = null;
    }

    return {
        ok: response.ok,
        status: response.status,
        data: data
    };
}