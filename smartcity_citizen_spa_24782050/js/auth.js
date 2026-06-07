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
        const loginMessage = document.getElementById("login-message");

        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        loginMessage.innerHTML = "";

        if (!username || !password) {
            loginMessage.innerHTML = `
                <div class="alert alert-warning">
                    Username dan password wajib diisi.
                </div>
            `;
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

            loginMessage.innerHTML = `
                <div class="alert alert-success">
                    Login berhasil. Token berhasil disimpan.
                </div>
            `;

            setTimeout(function () {
                window.location.hash = "#dashboard";
            }, 600);
        } else {
            const errorMessage = result.data?.detail || "Login gagal. Periksa username dan password.";

            loginMessage.innerHTML = `
                <div class="alert alert-danger">
                    ${errorMessage}
                </div>
            `;
        }
    });
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