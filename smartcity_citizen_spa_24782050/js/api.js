const API_BASE_URL = (
    window.SMARTCITY_API_BASE_URL ||
    localStorage.getItem("SMARTCITY_API_BASE_URL") ||
    "http://103.151.63.86:8004/api"
).replace(/\/$/, "");

/**
 * Fungsi pembungkus Fetch API.
 * Digunakan untuk semua komunikasi frontend SPA ke backend Django DRF.
 * Token JWT otomatis diambil dari localStorage dan dikirim sebagai Bearer Token.
 *
 * Catatan:
 * - API_BASE_URL sudah berisi /api dan bisa dioverride saat deploy
 * - Jadi endpoint cukup ditulis seperti "/token/" atau "/reports/"
 * - Contoh override di index.html:
 *   window.SMARTCITY_API_BASE_URL = "https://nama-backend.onrender.com/api";
 */
async function requestAPI(endpoint, method = "GET", bodyData = null, allowRefresh = true) {
    const accessToken = localStorage.getItem("access_token");
    const isLoginRequest = endpoint.startsWith("/token/");
    const isRefreshRequest = endpoint.startsWith("/token/refresh/");

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

        if (response.status === 401 && !isLoginRequest && !isRefreshRequest) {
            if (allowRefresh && await refreshAccessToken()) {
                return await requestAPI(endpoint, method, bodyData, false);
            }

            clearSessionAndRedirect();
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
 * Silent refresh access token menggunakan refresh_token.
 * Sesuai skenario AUTH-05 Lab Session 15.
 */
async function refreshAccessToken() {
    const refreshToken = localStorage.getItem("refresh_token");

    if (!refreshToken) {
        return false;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                refresh: refreshToken
            })
        });

        if (!response.ok) {
            return false;
        }

        const data = await response.json();

        if (!data.access) {
            return false;
        }

        localStorage.setItem("access_token", data.access);
        return true;
    } catch (error) {
        console.error("Gagal refresh access token:", error);
        return false;
    }
}

/**
 * Bersihkan sesi saat access dan refresh token sama-sama tidak valid.
 */
function clearSessionAndRedirect() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("username");

    if (window.location.hash !== "#login") {
        alert("Sesi login tidak valid atau sudah habis. Silakan login ulang.");
        window.location.hash = "#login";
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
