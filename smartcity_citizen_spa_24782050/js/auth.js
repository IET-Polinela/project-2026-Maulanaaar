/**
 * Mengecek apakah user sudah login berdasarkan access_token.
 */
function isLoggedIn() {
    return localStorage.getItem("access_token") !== null;
}

/**
 * Setup form login.
 * Wajib memakai preventDefault agar halaman tidak reload.
 */
function setupLoginForm() {
    const loginForm = document.getElementById("login-form");

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const usernameInput = document.getElementById("username");
        const passwordInput = document.getElementById("password");
        const loginButton = document.getElementById("login-button");
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        setLoginMessage("", "");

        if (!username || !password) {
            setLoginMessage("warning", "Username dan password wajib diisi.");
            return;
        }

        loginButton.disabled = true;
        loginButton.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2"></span>
            Memproses...
        `;

        const result = await requestAPI("/token/", "POST", {
            username: username,
            password: password
        });

        loginButton.disabled = false;
        loginButton.innerHTML = `
            <i class="bi bi-box-arrow-in-right me-1"></i>
            Login
        `;

        if (result.ok && result.status === 200) {
            localStorage.setItem("access_token", result.data.access);
            localStorage.setItem("refresh_token", result.data.refresh);
            localStorage.setItem("username", username);

            setLoginMessage("success", "Login berhasil. Token berhasil disimpan.");

            setTimeout(function () {
                window.location.hash = "#dashboard";
            }, 600);
        } else {
            const errorMessage = result.data?.detail || "Login gagal. Periksa username dan password.";

            setLoginMessage("danger", errorMessage);
        }
    });
}

/**
 * Menampilkan pesan login tanpa menyisipkan teks API sebagai HTML mentah.
 */
function setLoginMessage(type, message) {
    const loginMessage = document.getElementById("login-message");

    if (!loginMessage) {
        return;
    }

    loginMessage.innerHTML = "";

    if (!type || !message) {
        return;
    }

    const alertElement = document.createElement("div");
    alertElement.className = `alert alert-${type}`;
    alertElement.textContent = message;
    loginMessage.appendChild(alertElement);
}

/**
 * Logout user dengan menghapus token dari localStorage.
 */
function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("username");

    window.location.hash = "#login";

    if (typeof handleRoute === "function") {
        handleRoute();
    }
}
