/**
 * File utama aplikasi Lab Session 12.
 * Berisi logic Fetch API, render card laporan, pagination,
 * summary sidebar, serta modal tambah/edit laporan.
 */

console.log("Smart City Citizen SPA berhasil dimuat.");

let currentTab = "my_reports";
let currentPage = 1;
let editingReportId = null;
let reportModalInstance = null;

/**
 * Fungsi dipanggil dari router.js setelah halaman dashboard dirender.
 */
function initializeDashboard() {
    currentTab = "my_reports";
    currentPage = 1;
    editingReportId = null;

    const modalElement = document.getElementById("reportModal");
    if (modalElement) {
        reportModalInstance = new bootstrap.Modal(modalElement);
    }

    setupDashboardButtons();
    setupModalButtons();

    loadDashboardData(currentTab, currentPage);
}

/**
 * Setup tombol tab, tombol tambah laporan, dan navigasi dashboard.
 */
function setupDashboardButtons() {
    const btnMyReports = document.getElementById("btnMyReports");
    const btnFeed = document.getElementById("btnFeed");
    const btnOpenCreateReport = document.getElementById("btnOpenCreateReport");

    if (btnMyReports) {
        btnMyReports.onclick = function () {
            currentTab = "my_reports";
            currentPage = 1;
            updateTabButtonState();
            loadDashboardData(currentTab, currentPage);
        };
    }

    if (btnFeed) {
        btnFeed.onclick = function () {
            currentTab = "feed";
            currentPage = 1;
            updateTabButtonState();
            loadDashboardData(currentTab, currentPage);
        };
    }

    if (btnOpenCreateReport) {
        btnOpenCreateReport.onclick = function () {
            openCreateReportModal();
        };
    }
}

/**
 * Setup tombol pada modal.
 * Tombol harus type="button" agar tidak menyebabkan reload halaman.
 */
function setupModalButtons() {
    const btnSaveDraft = document.getElementById("btnSaveDraft");
    const btnSubmitReport = document.getElementById("btnSubmitReport");

    if (btnSaveDraft) {
        btnSaveDraft.onclick = function () {
            submitReport("DRAFT");
        };
    }

    if (btnSubmitReport) {
        btnSubmitReport.onclick = function () {
            submitReport("REPORTED");
        };
    }
}

/**
 * Mengubah tampilan aktif pada tombol tab.
 */
function updateTabButtonState() {
    const btnMyReports = document.getElementById("btnMyReports");
    const btnFeed = document.getElementById("btnFeed");

    if (!btnMyReports || !btnFeed) {
        return;
    }

    if (currentTab === "my_reports") {
        btnMyReports.className = "btn btn-primary";
        btnFeed.className = "btn btn-outline-primary";
    } else {
        btnMyReports.className = "btn btn-outline-primary";
        btnFeed.className = "btn btn-primary";
    }
}

/**
 * Mengambil data laporan dari API berdasarkan tab dan halaman.
 */
async function loadDashboardData(tab = "my_reports", page = 1) {
    const reportListContainer = document.getElementById("reportListContainer");
    const listMessage = document.getElementById("listMessage");

    if (!reportListContainer) {
        return;
    }

    currentTab = tab;
    currentPage = page;

    updateTabButtonState();

    listMessage.innerHTML = "";

    reportListContainer.innerHTML = `
        <div class="col-12">
            <div class="alert alert-info d-flex align-items-center mb-0">
                <span class="spinner-border spinner-border-sm me-2"></span>
                Memuat data laporan...
            </div>
        </div>
    `;

    const result = await getAPI(`/reports/?tab=${tab}&page=${page}`);

    if (!result.ok) {
        if (result.status === 401) {
            reportListContainer.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-danger mb-0">
                        Sesi login tidak valid. Silakan login ulang.
                    </div>
                </div>
            `;
            return;
        }

        reportListContainer.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger mb-0">
                    Gagal mengambil data laporan dari API.
                </div>
            </div>
        `;
        return;
    }

    const paginatedData = result.data;
    const reports = paginatedData.results || [];

    renderList(reports);
    renderPagination(paginatedData);

    await loadSummaryStats();
}

/**
 * Mengubah array JSON dari API menjadi Bootstrap Cards.
 */
function renderList(reports) {
    const reportListContainer = document.getElementById("reportListContainer");

    if (!reportListContainer) {
        return;
    }

    if (!reports || reports.length === 0) {
        const message = currentTab === "my_reports"
            ? "Belum ada laporan pribadi yang dibuat."
            : "Belum ada laporan publik pada Feed Kota.";

        reportListContainer.innerHTML = `
            <div class="col-12">
                <div class="alert alert-warning mb-0">
                    <i class="bi bi-info-circle me-1"></i>
                    ${message}
                </div>
            </div>
        `;
        return;
    }

    reportListContainer.innerHTML = reports.map(function (report) {
        const progress = getStatusProgress(report.status);
        const statusLabel = getStatusLabel(report.status);
        const statusBadgeClass = getStatusBadgeClass(report.status);
        const progressClass = getProgressClass(report.status);
        const updatedAt = formatDate(report.updated_at);

        const reporterName = report.is_owner ? "Anda" : (report.reporter || "Warga Anonim");

        const editButton = (
            currentTab === "my_reports" &&
            report.is_owner === true &&
            report.status === "DRAFT"
        ) ? `
            <button type="button" class="btn btn-sm btn-outline-primary" onclick="editDraft(${report.id})">
                <i class="bi bi-pencil-square me-1"></i>
                Edit Draft
            </button>
        ` : "";

        return `
            <div class="col-12">
                <div class="card report-card">
                    <div class="card-body">
                        <div class="d-flex flex-column flex-md-row justify-content-between gap-2 mb-2">
                            <div>
                                <h5 class="fw-bold mb-1">
                                    ${escapeHtml(report.title)}
                                </h5>

                                <div class="text-muted small">
                                    <i class="bi bi-person-circle me-1"></i>
                                    ${escapeHtml(reporterName)}
                                    <span class="mx-1">•</span>
                                    <i class="bi bi-clock-history me-1"></i>
                                    ${updatedAt}
                                </div>
                            </div>

                            <div>
                                <span class="badge ${statusBadgeClass} badge-status">
                                    ${statusLabel}
                                </span>
                            </div>
                        </div>

                        <div class="mb-2">
                            <span class="badge bg-light text-dark border">
                                <i class="bi bi-tag me-1"></i>
                                ${escapeHtml(report.category)}
                            </span>

                            <span class="badge bg-light text-dark border">
                                <i class="bi bi-geo-alt me-1"></i>
                                ${escapeHtml(report.location)}
                            </span>
                        </div>

                        <p class="text-muted mb-3">
                            ${escapeHtml(report.description)}
                        </p>

                        <div class="mb-3">
                            <div class="d-flex justify-content-between align-items-center mb-1">
                                <small class="text-muted">Progress Status</small>
                                <small class="fw-semibold">${progress}%</small>
                            </div>

                            <div class="progress">
                                <div 
                                    class="progress-bar ${progressClass}" 
                                    role="progressbar" 
                                    style="width: ${progress}%;" 
                                    aria-valuenow="${progress}" 
                                    aria-valuemin="0" 
                                    aria-valuemax="100">
                                </div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-end">
                            ${editButton}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join("");
}

/**
 * Membuat tombol pagination berdasarkan response DRF.
 */
function renderPagination(paginatedData) {
    const paginationContainer = document.getElementById("paginationContainer");

    if (!paginationContainer) {
        return;
    }

    const totalCount = paginatedData.count || 0;
    const totalPages = Math.ceil(totalCount / 10);

    if (totalPages <= 1) {
        paginationContainer.innerHTML = "";
        return;
    }

    const previousDisabled = paginatedData.previous ? "" : "disabled";
    const nextDisabled = paginatedData.next ? "" : "disabled";

    paginationContainer.innerHTML = `
        <nav aria-label="Navigasi halaman laporan">
            <ul class="pagination mb-0">
                <li class="page-item ${previousDisabled}">
                    <button class="page-link" type="button" onclick="goToPage(${currentPage - 1})">
                        Previous
                    </button>
                </li>

                <li class="page-item active">
                    <span class="page-link">
                        Halaman ${currentPage} dari ${totalPages}
                    </span>
                </li>

                <li class="page-item ${nextDisabled}">
                    <button class="page-link" type="button" onclick="goToPage(${currentPage + 1})">
                        Next
                    </button>
                </li>
            </ul>
        </nav>
    `;
}

/**
 * Pindah halaman pagination.
 */
function goToPage(page) {
    if (page < 1) {
        return;
    }

    loadDashboardData(currentTab, page);
}

/**
 * Mengambil semua laporan milik user dengan page_size besar
 * untuk menghitung rekap status pada sidebar.
 */
async function loadSummaryStats() {
    const result = await getAPI("/reports/?tab=my_reports&page_size=1000");

    if (!result.ok) {
        return;
    }

    const reports = result.data.results || [];

    const totalDraft = reports.filter(report => report.status === "DRAFT").length;
    const totalReported = reports.filter(report => report.status === "REPORTED").length;
    const totalVerified = reports.filter(report => report.status === "VERIFIED").length;
    const totalInProgress = reports.filter(report => report.status === "IN_PROGRESS").length;
    const totalResolved = reports.filter(report => report.status === "RESOLVED").length;

    setTextContent("summaryDraft", totalDraft);
    setTextContent("summaryReported", totalReported);
    setTextContent("summaryVerified", totalVerified);
    setTextContent("summaryInProgress", totalInProgress);
    setTextContent("summaryResolved", totalResolved);
}

/**
 * Membuka modal untuk membuat laporan baru.
 */
function openCreateReportModal() {
    editingReportId = null;

    const reportForm = document.getElementById("reportForm");
    const reportModalLabel = document.getElementById("reportModalLabel");

    if (reportForm) {
        reportForm.reset();
    }

    setInputValue("reportId", "");
    setInputValue("reportTitle", "");
    setInputValue("reportCategory", "");
    setInputValue("reportLocation", "");
    setInputValue("reportDescription", "");

    if (reportModalLabel) {
        reportModalLabel.innerHTML = `
            <i class="bi bi-plus-circle me-2"></i>
            Tambah Laporan Baru
        `;
    }

    if (reportModalInstance) {
        reportModalInstance.show();
    }
}

/**
 * Membuka modal edit draft.
 * Data lama diambil dari API lalu dimasukkan ke form.
 */
async function editDraft(id) {
    const result = await getAPI(`/reports/${id}/`);

    if (!result.ok) {
        alert("Gagal mengambil data draft.");
        return;
    }

    const report = result.data;

    if (report.status !== "DRAFT") {
        alert("Hanya laporan berstatus DRAFT yang dapat diedit.");
        return;
    }

    editingReportId = id;

    setInputValue("reportId", report.id);
    setInputValue("reportTitle", report.title);
    setInputValue("reportCategory", report.category);
    setInputValue("reportLocation", report.location);
    setInputValue("reportDescription", report.description);

    const reportModalLabel = document.getElementById("reportModalLabel");
    if (reportModalLabel) {
        reportModalLabel.innerHTML = `
            <i class="bi bi-pencil-square me-2"></i>
            Edit Draft Laporan
        `;
    }

    if (reportModalInstance) {
        reportModalInstance.show();
    }
}

/**
 * Submit form laporan.
 * Jika editingReportId null = POST laporan baru.
 * Jika editingReportId ada = PUT update draft lama.
 */
async function submitReport(targetStatus) {
    const title = document.getElementById("reportTitle").value.trim();
    const category = document.getElementById("reportCategory").value.trim();
    const location = document.getElementById("reportLocation").value.trim();
    const description = document.getElementById("reportDescription").value.trim();

    if (!title || !category || !location || !description) {
        alert("Semua field laporan wajib diisi.");
        return;
    }

    const payload = {
        title: title,
        category: category,
        location: location,
        description: description,
        status: targetStatus
    };

    let result = null;

    if (editingReportId === null) {
        if (targetStatus === "DRAFT") {
            result = await postAPI("/reports/", payload);
        } else {
            const draftPayload = {
                ...payload,
                status: "DRAFT"
            };

            const createResult = await postAPI("/reports/", draftPayload);

            if (!createResult.ok || createResult.status !== 201) {
                alert("Gagal membuat laporan baru.");
                return;
            }

            const newReportId = createResult.data.id;

            result = await patchAPI(`/reports/${newReportId}/`, {
                status: "REPORTED"
            });
        }
    } else {
        result = await putAPI(`/reports/${editingReportId}/`, payload);
    }

    if (result.ok && (result.status === 200 || result.status === 201)) {
        closeAndResetModal();

        currentTab = "my_reports";
        currentPage = 1;

        await loadDashboardData(currentTab, currentPage);
    } else {
        let errorMessage = "Gagal menyimpan laporan.";

        if (result.data) {
            if (result.data.detail) {
                errorMessage = result.data.detail;
            } else {
                errorMessage = JSON.stringify(result.data);
            }
        }

        alert(errorMessage);
    }
}

/**
 * Menutup modal dan reset form setelah berhasil submit.
 */
function closeAndResetModal() {
    const reportForm = document.getElementById("reportForm");

    if (reportModalInstance) {
        reportModalInstance.hide();
    }

    if (reportForm) {
        reportForm.reset();
    }

    editingReportId = null;

    setInputValue("reportId", "");
}

/**
 * Helper progress berdasarkan status.
 */
function getStatusProgress(status) {
    const progressMap = {
        "DRAFT": 20,
        "REPORTED": 40,
        "VERIFIED": 60,
        "IN_PROGRESS": 80,
        "RESOLVED": 100
    };

    return progressMap[status] || 0;
}

/**
 * Helper label status.
 */
function getStatusLabel(status) {
    const labelMap = {
        "DRAFT": "DRAFT",
        "REPORTED": "REPORTED",
        "VERIFIED": "VERIFIED",
        "IN_PROGRESS": "IN PROGRESS",
        "RESOLVED": "RESOLVED"
    };

    return labelMap[status] || status;
}

/**
 * Helper warna badge status.
 */
function getStatusBadgeClass(status) {
    const badgeMap = {
        "DRAFT": "bg-secondary",
        "REPORTED": "bg-primary",
        "VERIFIED": "bg-info text-dark",
        "IN_PROGRESS": "bg-warning text-dark",
        "RESOLVED": "bg-success"
    };

    return badgeMap[status] || "bg-dark";
}

/**
 * Helper warna progress bar.
 */
function getProgressClass(status) {
    const progressMap = {
        "DRAFT": "bg-secondary",
        "REPORTED": "bg-primary",
        "VERIFIED": "bg-info",
        "IN_PROGRESS": "bg-warning",
        "RESOLVED": "bg-success"
    };

    return progressMap[status] || "bg-dark";
}

/**
 * Format tanggal agar mudah dibaca.
 */
function formatDate(dateString) {
    if (!dateString) {
        return "-";
    }

    const date = new Date(dateString);

    return date.toLocaleString("id-ID", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}

/**
 * Helper set value input.
 */
function setInputValue(id, value) {
    const element = document.getElementById(id);

    if (element) {
        element.value = value || "";
    }
}

/**
 * Helper set text content.
 */
function setTextContent(id, value) {
    const element = document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}

/**
 * Escape HTML sederhana agar teks dari API aman ditampilkan ke DOM.
 */
function escapeHtml(value) {
    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}