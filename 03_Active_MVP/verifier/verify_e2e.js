// Automated End-to-End Verification of Transformation Logic
const fs = require('fs');
const path = require('path');

const KEEPA_EPOCH_OFFSET_SECONDS = 1293840000;

function keepaEpochToISO(keepaMinutes) {
  if (!keepaMinutes || isNaN(keepaMinutes)) return "N/A";
  const num = parseInt(keepaMinutes, 10);
  if (num < 1000) return "N/A";
  const ms = (num * 60 + KEEPA_EPOCH_OFFSET_SECONDS) * 1000;
  try {
    const d = new Date(ms);
    return isNaN(d.getTime()) ? "N/A" : d.toISOString().split("T")[0];
  } catch (e) {
    return "N/A";
  }
}

function formatKeepaPrice(val) {
  if (!val || isNaN(val)) return "N/A";
  const num = parseFloat(val);
  if (num <= 0) return "N/A";
  return num > 1000 && Number.isInteger(num) ? (num / 100).toFixed(2) : num.toFixed(2);
}

// Read sample CSV
const csvPath = path.join(__dirname, 'sample_keepa_dump.csv');
const rawText = fs.readFileSync(csvPath, 'utf8');
const lines = rawText.trim().split('\n');
const headers = lines[0].split(',');

console.log('=== VERIFYING KEEPA TRANSFORMATION ENGINE ===');
console.log(`[*] Loaded sample CSV with ${lines.length - 1} products and ${headers.length} columns.`);

const records = lines.slice(1).map(line => {
  const values = line.split(',');
  const row = {};
  headers.forEach((h, i) => row[h.trim()] = values[i] ? values[i].trim() : '');
  
  return {
    "ASIN": row["ASIN"] || "N/A",
    "Title": row["Title"] || "Unknown",
    "Current BSR": row["Sales Rank: Current"] || "N/A",
    "90-Day Avg BSR": row["Sales Rank: 90 days avg."] || "N/A",
    "Buy Box Price ($)": formatKeepaPrice(row["Buy Box: Current"]),
    "90-Day Avg Price ($)": formatKeepaPrice(row["Buy Box: 90 days avg."]),
    "Buy Box Share (%)": row["Buy Box %"] || "N/A",
    "FBA Sellers Count": row["Count of retrieved live offers: FBA"] || "N/A",
    "Total Offers": row["New Offer Count: Current"] || "N/A",
    "Last Price Date (ISO)": keepaEpochToISO(row["Sales Rank: Last Price Change"])
  };
});

// Assertions
assert(records.length === 5, 'Should parse exactly 5 records');
assert(records[0].ASIN === 'B08N5WRWNW', 'ASIN should match');
assert(records[0]['Buy Box Price ($)'] === '29.99', 'Price 2999 cents should format to 29.99');
assert(records[0]['Last Price Date (ISO)'].startsWith('2024-'), 'Epoch 7050000 should convert to 2024 ISO date');
assert(Object.keys(records[0]).length === 10, 'Must prune to exactly 10 columns');

function assert(condition, message) {
  if (!condition) {
    console.error('[-] FAILED ASSERTION:', message);
    process.exit(1);
  }
}

console.log('[+] All 5 products successfully parsed.');
console.log(`[+] Pruned 15 columns down to 10 core metrics.`);
console.log(`[+] Sample Converted Row 1:`, JSON.stringify(records[0], null, 2));
console.log('=== VERIFICATION PASSED (EXIT CODE 0) ===');
