const appContent = document.getElementById("app-content");
const navMenu = document.getElementById("nav-menu");

/**
 * Mengatur tampilan navbar berdasarkan status login.
 */
function renderNavbar() {
    if (isLoggedIn()) {
        const username = localStorage.getItem("username") || "Citizen";

        navMenu.innerHTML = `
            <li class="nav-item">
                <a class="nav-link" href="#login">
                    <i class="bi bi-box-arrow-in-right me-1"></i>
                    Login
                </a>
            </li>

            <li class="nav-item">
                <a class="nav-link" href="#dashboard">
                    <i class="bi bi-speedometer2 me-1"></i>
                    Dashboard
                </a>
            </li>

            <li class="nav-item">
                <span class="nav-link text-white">
                    <i class="bi bi-person-circle me-1"></i>
                    ${username}
                </span>
            </li>

            <li class="nav-item">
                <button class="btn btn-outline-light btn-sm ms-lg-2" onclick="logout()">
                    <i class="bi bi-box-arrow-right me-1"></i>
                    Logout
                </button>
            </li>
        `;
    } else {
        navMenu.innerHTML = `
            <li class="nav-item">
                <a class="nav-link" href="#login">
                    <i class="bi bi-box-arrow-in-right me-1"></i>
                    Login
                </a>
            </li>

            <li class="nav-item">
                <a class="nav-link" href="#dashboard">
                    <i class="bi bi-speedometer2 me-1"></i>
                    Dashboard
                </a>
            </li>
        `;
    }
}

/**
 * Halaman Login Citizen.
 */
function renderLoginPage() {
    appContent.innerHTML = `
        <section class="page-section d-flex align-items-center justify-content-center">
            <div class="row w-100 justify-content-center">
                <div class="col-12 col-md-8 col-lg-5">
                    <div class="card content-card shadow-sm">
                        <div class="card-body p-4 p-md-5">
                            <div class="text-center mb-4">
                                <div class="stat-icon mb-3">
                                    <i class="bi bi-shield-lock-fill"></i>
                                </div>

                                <h3 class="fw-bold">Login Citizen</h3>

                                <p class="text-muted mb-0">
                                    Masuk menggunakan akun Citizen untuk mengakses portal Smart City.
                                </p>
                            </div>

                            <div id="login-message"></div>

                            <form id="login-form">
                                <div class="mb-3">
                                    <label for="username" class="form-label">Username</label>
                                    <div class="input-group">
                                        <span class="input-group-text">
                                            <i class="bi bi-person"></i>
                                        </span>
                                        <input 
                                            type="text" 
                                            id="username" 
                                            class="form-control" 
                                            placeholder="Masukkan username" 
                                            required
                                        >
                                    </div>
                                </div>

                                <div class="mb-4">
                                    <label for="password" class="form-label">Password</label>
                                    <div class="input-group">
                                        <span class="input-group-text">
                                            <i class="bi bi-key"></i>
                                        </span>
                                        <input 
                                            type="password" 
                                            id="password" 
                                            class="form-control" 
                                            placeholder="Masukkan password" 
                                            required
                                        >
                                    </div>
                                </div>

                                <button type="submit" id="login-button" class="btn btn-primary w-100">
                                    <i class="bi bi-box-arrow-in-right me-1"></i>
                                    Login
                                </button>
                            </form>

                            <div class="alert alert-info mt-4 mb-0">
                                <small>
                                    Gunakan akun Citizen yang sudah berhasil dibuat pada Lab Session 10.
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    `;

    setupLoginForm();
}

/**
 * Halaman Dashboard Citizen.
 * Layout responsive:
 * - Desktop: kiri 25%, tengah 50%, kanan 25%
 * - Mobile: semua kolom menjadi 100% dan menumpuk ke bawah
 */
function renderDashboardPage() {
    if (!isLoggedIn()) {
        window.location.hash = "#login";
        return;
    }

    const username = localStorage.getItem("username") || "Citizen";

    appContent.innerHTML = `
        <section class="page-section">
            <div class="container py-4">
                <div class="mb-4">
                    <h1 class="fw-bold mb-2">Dashboard Citizen</h1>
                    <p class="text-muted mb-0">
                        Portal ini digunakan oleh warga untuk mengakses layanan Smart City berbasis API.
                    </p>
                </div>

                <div class="alert alert-primary d-flex align-items-center mb-4" role="alert">
                    <i class="bi bi-person-check-fill me-2"></i>
                    <div>
                        Login sebagai: <strong>${username}</strong>
                    </div>
                </div>

                <div class="row g-4">
                    <!-- Kolom kiri: 25% desktop, 100% mobile -->
                    <div class="col-12 col-lg-3">
                        <div class="card content-card h-100 shadow-sm">
                            <div class="card-body">
                                <h4 class="fw-bold mb-3">
                                    <i class="bi bi-person-badge-fill text-primary me-2"></i>
                                    Profil Citizen
                                </h4>

                                <p class="text-muted mb-2">
                                    Username:
                                </p>

                                <h5 class="fw-bold mb-3">
                                    <i class="bi bi-person-circle me-1 text-primary"></i>
                                    ${username}
                                </h5>

                                <p class="text-muted mb-3">
                                    Status login berhasil menggunakan JWT.
                                </p>

                                <span class="badge bg-success">
                                    Authenticated
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Kolom tengah: 50% desktop, 100% mobile -->
                    <div class="col-12 col-lg-6">
                        <div class="card content-card h-100 shadow-sm">
                            <div class="card-body">
                                <h4 class="fw-bold mb-3">
                                    <i class="bi bi-clipboard-data-fill text-primary me-2"></i>
                                    Ringkasan Laporan
                                </h4>

                                <p class="text-muted">
                                    Data laporan nantinya dapat diambil dari endpoint API Django.
                                </p>

                                <div class="row g-3 mt-2">
                                    <div class="col-12 col-md-4">
                                        <div class="border rounded p-3 text-center bg-light">
                                            <h3 class="fw-bold mb-1">API</h3>
                                            <p class="text-muted mb-0">Backend DRF</p>
                                        </div>
                                    </div>

                                    <div class="col-12 col-md-4">
                                        <div class="border rounded p-3 text-center bg-light">
                                            <h3 class="fw-bold mb-1">JWT</h3>
                                            <p class="text-muted mb-0">Authentication</p>
                                        </div>
                                    </div>

                                    <div class="col-12 col-md-4">
                                        <div class="border rounded p-3 text-center bg-light">
                                            <h3 class="fw-bold mb-1">SPA</h3>
                                            <p class="text-muted mb-0">Frontend</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Kolom kanan: 25% desktop, 100% mobile -->
                    <div class="col-12 col-lg-3">
                        <div class="card content-card h-100 shadow-sm">
                            <div class="card-body">
                                <h4 class="fw-bold mb-3">
                                    <i class="bi bi-shield-lock-fill text-primary me-2"></i>
                                    Token Login
                                </h4>

                                <p class="text-muted mb-3">
                                    Access token dan refresh token tersimpan di localStorage setelah login berhasil.
                                </p>

                                <button class="btn btn-outline-primary btn-sm" onclick="logout()">
                                    <i class="bi bi-arrow-left-right me-1"></i>
                                    Ganti Akun
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    `;
}

/**
 * Router utama SPA.
 * Menggunakan hash-based routing:
 * #login
 * #dashboard
 */
function handleRoute() {
    renderNavbar();

    const hash = window.location.hash || "#login";

    if (hash === "#login") {
        renderLoginPage();
    } else if (hash === "#dashboard") {
        renderDashboardPage();
    } else {
        window.location.hash = "#login";
    }
}

window.addEventListener("hashchange", handleRoute);
window.addEventListener("DOMContentLoaded", handleRoute);