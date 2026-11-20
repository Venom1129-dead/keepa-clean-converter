// Keepa Clean Excel Converter — Client Application Logic

const KEEPA_EPOCH_OFFSET_SECONDS = 1293840000; // Jan 1, 2011 00:00:00 UTC
const PREVIEW_ROW_LIMIT = 50;

let rawParsedData = [];
let cleanedData = [];
let isProUnlocked = localStorage.getItem("keepa_clean_license") === "valid";

// DOM Elements
const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const statusPanel = document.getElementById("status-panel");
const progressBar = document.getElementById("progress-bar");
const statusText = document.getElementById("status-text");
const resultsControls = document.getElementById("results-controls");
const statTotalRows = document.getElementById("stat-total-rows");
const statPrunedCols = document.getElementById("stat-pruned-cols");
const statDatesFixed = document.getElementById("stat-dates-fixed");
const previewSection = document.getElementById("preview-section");
const tableHeadRow = document.getElementById("table-head-row");
const tableBody = document.getElementById("table-body");
const previewNote = document.getElementById("preview-note");
const btnExportXlsx = document.getElementById("btn-export-xlsx");
const btnExportCsv = document.getElementById("btn-export-csv");
const btnReset = document.getElementById("btn-reset");
const licenseModal = document.getElementById("license-modal");
const modalRowCount = document.getElementById("modal-row-count");
const licenseKeyInput = document.getElementById("license-key-input");
const btnActivateLicense = document.getElementById("btn-activate-license");
const btnCloseModal = document.getElementById("btn-close-modal");

// Target 10 Core Columns
const TARGET_COLUMNS = [
  "ASIN",
  "Title",
  "Current BSR",
  "90-Day Avg BSR",
  "Buy Box Price ($)",
  "90-Day Avg Price ($)",
  "Buy Box Share (%)",
  "FBA Sellers Count",
  "Total Offers",
  "Last Price Date (ISO)"
];

// Helper: Convert Keepa Epoch minutes to standard ISO Date
function keepaEpochToISO(keepaMinutes) {
  if (!keepaMinutes || isNaN(keepaMinutes)) return "N/A";
  const num = parseInt(keepaMinutes, 10);
  if (num < 1000) return "N/A";
  // Convert minutes to ms from Unix epoch
  const ms = (num * 60 + KEEPA_EPOCH_OFFSET_SECONDS) * 1000;
  try {
    const d = new Date(ms);
    return isNaN(d.getTime()) ? "N/A" : d.toISOString().split("T")[0];
  } catch (e) {
    return "N/A";
  }
}

// Helper: Clean Price (Keepa stores prices in cents, e.g. 1999 = $19.99, or -1 for none)
function formatKeepaPrice(val) {
  if (!val || isNaN(val)) return "N/A";
  const num = parseFloat(val);
  if (num <= 0) return "N/A";
  return num > 1000 && Number.isInteger(num) ? (num / 100).toFixed(2) : num.toFixed(2);
}

// Event Listeners for Upload
dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  if (e.dataTransfer.files.length > 0) {
    processFile(e.dataTransfer.files[0]);
  }
});

fileInput.addEventListener("change", (e) => {
  if (e.target.files.length > 0) {
    processFile(e.target.files[0]);
  }
});

function processFile(file) {
  if (!file) return;

  statusPanel.classList.remove("hidden");
  progressBar.style.width = "20%";
  statusText.textContent = `Streaming and analyzing "${file.name}" (${(file.size / 1024 / 1024).toFixed(2)} MB)...`;

  rawParsedData = [];
  cleanedData = [];

  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    dynamicTyping: false,
    chunk: function(results) {
      rawParsedData = rawParsedData.concat(results.data);
      progressBar.style.width = "60%";
      statusText.textContent = `Loaded ${rawParsedData.length.toLocaleString()} rows into RAM...`;
    },
    complete: function() {
      progressBar.style.width = "90%";
      statusText.textContent = "Transforming columns and fixing epoch dates...";
      setTimeout(transformData, 100);
    },
    error: function(err) {
      statusText.textContent = "Error parsing CSV: " + err.message;
      progressBar.style.backgroundColor = "var(--danger-color)";
    }
  });
}

function transformData() {
  if (!rawParsedData || rawParsedData.length === 0) {
    statusText.textContent = "No data found in uploaded file.";
    return;
  }

  const sampleRow = rawParsedData[0];
  const origColCount = Object.keys(sampleRow).length;

  cleanedData = rawParsedData.map(row => {
    // Fuzzy match headers from various Keepa export versions
    const asin = row["ASIN"] || row["asin"] || "N/A";
    const title = row["Title"] || row["title"] || row["Product Title"] || "Unknown";
    const bsr = row["Sales Rank: Current"] || row["Current BSR"] || row["Sales Rank: 30 days avg."] || "N/A";
    const avgBsr = row["Sales Rank: 90 days avg."] || row["90 Days Avg. BSR"] || "N/A";
    const buyBoxPrice = formatKeepaPrice(row["Buy Box: Current"] || row["New: Current"] || row["Buy Box"]);
    const avgBuyBoxPrice = formatKeepaPrice(row["Buy Box: 90 days avg."] || row["New: 90 days avg."]);
    const bbPercent = row["Buy Box %"] || row["Buy Box: Amazon 90 days %"] || "N/A";
    const fbaSellers = row["Count of retrieved live offers: FBA"] || row["FBA Offers"] || "N/A";
    const totalOffers = row["New Offer Count: Current"] || row["Offer Count"] || "N/A";
    const dateRaw = row["Sales Rank: Last Price Change"] || row["Last Price Change"] || row["lastUpdate"];
    const isoDate = keepaEpochToISO(dateRaw);

    return {
      "ASIN": asin,
      "Title": title,
      "Current BSR": bsr,
      "90-Day Avg BSR": avgBsr,
      "Buy Box Price ($)": buyBoxPrice,
      "90-Day Avg Price ($)": avgBuyBoxPrice,
      "Buy Box Share (%)": bbPercent,
      "FBA Sellers Count": fbaSellers,
      "Total Offers": totalOffers,
      "Last Price Date (ISO)": isoDate
    };
  });

  progressBar.style.width = "100%";
  statusText.textContent = "Clean conversion finished!";

  // Update Stats
  statTotalRows.textContent = cleanedData.length.toLocaleString();
  statPrunedCols.textContent = `${origColCount} → 10`;
  statDatesFixed.textContent = "ISO 8601";

  resultsControls.classList.remove("hidden");
  previewSection.classList.remove("hidden");

  renderPreviewTable();

  if (cleanedData.length > PREVIEW_ROW_LIMIT && !isProUnlocked) {
    modalRowCount.textContent = cleanedData.length.toLocaleString();
    previewNote.textContent = `Showing first ${PREVIEW_ROW_LIMIT} of ${cleanedData.length.toLocaleString()} rows (Free Preview)`;
  } else {
    previewNote.textContent = `All ${cleanedData.length.toLocaleString()} rows ready for export (Pro Unlocked)`;
  }
}

function renderPreviewTable() {
  tableHeadRow.innerHTML = "";
  TARGET_COLUMNS.forEach(col => {
    const th = document.createElement("th");
    th.textContent = col;
    tableHeadRow.appendChild(th);
  });

  tableBody.innerHTML = "";
  const displayRows = isProUnlocked ? cleanedData.slice(0, 100) : cleanedData.slice(0, PREVIEW_ROW_LIMIT);

  displayRows.forEach(row => {
    const tr = document.createElement("tr");
    TARGET_COLUMNS.forEach(col => {
      const td = document.createElement("td");
      td.textContent = row[col];
      tr.appendChild(td);
    });
    tableBody.appendChild(tr);
  });
}

// Export Handlers
btnExportXlsx.addEventListener("click", () => {
  if (cleanedData.length > PREVIEW_ROW_LIMIT && !isProUnlocked) {
    licenseModal.classList.remove("hidden");
    return;
  }
  exportToExcel();
});

btnExportCsv.addEventListener("click", () => {
  if (cleanedData.length > PREVIEW_ROW_LIMIT && !isProUnlocked) {
    licenseModal.classList.remove("hidden");
    return;
  }
  exportToCsv();
});

function exportToExcel() {
  const exportRows = isProUnlocked ? cleanedData : cleanedData.slice(0, PREVIEW_ROW_LIMIT);
  const worksheet = XLSX.utils.json_to_sheet(exportRows);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Cleaned_Keepa_Products");
  XLSX.writeFile(workbook, "Cleaned_Keepa_Export.xlsx");
}

function exportToCsv() {
  const exportRows = isProUnlocked ? cleanedData : cleanedData.slice(0, PREVIEW_ROW_LIMIT);
  const csv = Papa.unparse(exportRows);
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "Cleaned_Keepa_Export.csv";
  a.click();
  URL.revokeObjectURL(url);
}

// License Modal
btnCloseModal.addEventListener("click", () => {
  licenseModal.classList.add("hidden");
});

btnActivateLicense.addEventListener("click", () => {
  const key = licenseKeyInput.value.trim();
  if (key.length >= 6) {
    localStorage.setItem("keepa_clean_license", "valid");
    isProUnlocked = true;
    licenseModal.classList.add("hidden");
    alert("🎉 Pro License Activated! Unlimited rows unlocked.");
    renderPreviewTable();
    exportToExcel();
  } else {
    alert("Please enter a valid license key.");
  }
});

btnReset.addEventListener("click", () => {
  rawParsedData = [];
  cleanedData = [];
  fileInput.value = "";
  statusPanel.classList.add("hidden");
  resultsControls.classList.add("hidden");
  previewSection.classList.add("hidden");
});
