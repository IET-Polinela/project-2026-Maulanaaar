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
 * Halaman Dashboard Citizen untuk Lab Session 12.
 */
function renderDashboardPage() {
    if (!isLoggedIn()) {
        window.location.hash = "#login";
        return;
    }

    const username = localStorage.getItem("username") || "Citizen";

    appContent.innerHTML = `
        <section class="page-section">
            <div class="container-fluid py-4">
                <div class="row g-4">
                    <!-- SIDEBAR KIRI -->
                    <div class="col-12 col-lg-3">
                        <div class="card sidebar-card mb-4">
                            <div class="card-body">
                                <h5 class="fw-bold mb-1">
                                    <i class="bi bi-person-circle text-primary me-2"></i>
                                    Citizen Portal
                                </h5>

                                <p class="text-muted small mb-3">
                                    Login sebagai <strong>${username}</strong>
                                </p>

                                <div class="alert alert-success py-2 mb-0">
                                    <small>
                                        <i class="bi bi-shield-check me-1"></i>
                                        JWT Authenticated
                                    </small>
                                </div>
                            </div>
                        </div>

                        <div class="card sidebar-card">
                            <div class="card-body">
                                <h5 class="fw-bold mb-3">
                                    <i class="bi bi-bar-chart-fill text-primary me-2"></i>
                                    Rekap Status
                                </h5>

                                <div class="d-flex justify-content-between align-items-center border-bottom py-2">
                                    <span>
                                        <i class="bi bi-file-earmark-text text-secondary me-1"></i>
                                        Draft
                                    </span>
                                    <span class="badge bg-secondary" id="summaryDraft">0</span>
                                </div>

                                <div class="d-flex justify-content-between align-items-center border-bottom py-2">
                                    <span>
                                        <i class="bi bi-send-check text-primary me-1"></i>
                                        Dilaporkan
                                    </span>
                                    <span class="badge bg-primary" id="summaryReported">0</span>
                                </div>

                                <div class="d-flex justify-content-between align-items-center border-bottom py-2">
                                    <span>
                                        <i class="bi bi-patch-check text-info me-1"></i>
                                        Terverifikasi
                                    </span>
                                    <span class="badge bg-info text-dark" id="summaryVerified">0</span>
                                </div>

                                <div class="d-flex justify-content-between align-items-center border-bottom py-2">
                                    <span>
                                        <i class="bi bi-hourglass-split text-warning me-1"></i>
                                        Diproses
                                    </span>
                                    <span class="badge bg-warning text-dark" id="summaryInProgress">0</span>
                                </div>

                                <div class="d-flex justify-content-between align-items-center pt-2">
                                    <span>
                                        <i class="bi bi-check-circle text-success me-1"></i>
                                        Selesai
                                    </span>
                                    <span class="badge bg-success" id="summaryResolved">0</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- KONTEN UTAMA -->
                    <div class="col-12 col-lg-9">
                        <div class="hero-card p-4 mb-4 shadow-sm">
                            <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3">
                                <div>
                                    <h2 class="fw-bold mb-2">
                                        <i class="bi bi-buildings-fill me-2"></i>
                                        Dashboard Laporan Citizen
                                    </h2>
                                    <p class="mb-0">
                                        Kelola laporan pribadi dan pantau Feed Kota secara real-time melalui Fetch API.
                                    </p>
                                </div>

                                <button type="button" class="btn btn-light fw-semibold" id="btnOpenCreateReport">
                                    <i class="bi bi-plus-circle me-1"></i>
                                    Tambah Laporan Baru
                                </button>
                            </div>
                        </div>

                        <div class="card content-card">
                            <div class="card-body">
                                <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-3">
                                    <div>
                                        <h4 class="fw-bold mb-1">
                                            <i class="bi bi-list-task text-primary me-2"></i>
                                            Daftar Laporan
                                        </h4>
                                        <p class="text-muted mb-0">
                                            Data diambil langsung dari API Django REST Framework.
                                        </p>
                                    </div>

                                    <div class="btn-group" role="group" aria-label="Tab Laporan">
                                        <button type="button" class="btn btn-primary" id="btnMyReports">
                                            <i class="bi bi-person-lines-fill me-1"></i>
                                            Laporan Saya
                                        </button>

                                        <button type="button" class="btn btn-outline-primary" id="btnFeed">
                                            <i class="bi bi-globe2 me-1"></i>
                                            Feed Kota
                                        </button>
                                    </div>
                                </div>

                                <div id="listMessage"></div>

                                <div id="reportListContainer" class="row g-3">
                                    <div class="col-12">
                                        <div class="alert alert-info mb-0">
                                            Memuat data laporan...
                                        </div>
                                    </div>
                                </div>

                                <div id="paginationContainer" class="mt-4 d-flex justify-content-center"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    `;

    if (typeof initializeDashboard === "function") {
        initializeDashboard();
    }
}

/**
 * Router utama SPA.
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