const API_BASE_URL = "http://127.0.0.1:8000/api";

/**
 * Fungsi pembungkus Fetch API.
 * Digunakan untuk semua komunikasi frontend SPA ke backend Django DRF.
 * Token JWT otomatis diambil dari localStorage dan dikirim sebagai Bearer Token.
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

    try {
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

    } catch (error) {
        console.error("Gagal terhubung ke API:", error);

        return {
            ok: false,
            status: 0,
            data: {
                detail: "Tidak dapat terhubung ke server API."
            }
        };
    }
}

/**
 * Helper khusus GET.
 */
async function getAPI(endpoint) {
    return await requestAPI(endpoint, "GET");
}

/**
 * Helper khusus POST.
 */
async function postAPI(endpoint, bodyData) {
    return await requestAPI(endpoint, "POST", bodyData);
}

/**
 * Helper khusus PUT.
 */
async function putAPI(endpoint, bodyData) {
    return await requestAPI(endpoint, "PUT", bodyData);
}

/**
 * Helper khusus PATCH.
 */
async function patchAPI(endpoint, bodyData) {
    return await requestAPI(endpoint, "PATCH", bodyData);
}

/**
 * Helper khusus DELETE.
 */
async function deleteAPI(endpoint) {
    return await requestAPI(endpoint, "DELETE");
}