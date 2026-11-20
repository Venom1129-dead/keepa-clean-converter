// Freelancer Connects-ROI & Proposal Win-Rate Cockpit Logic

const STORAGE_KEY = 'freelancer_connects_proposals_v1';

// Default Sample Proposals if empty
const DEFAULT_PROPOSALS = [
  { id: 1, date: '2026-11-18', title: 'Shopify Liquid Custom Product Filter', category: 'Web Dev', connects: 40, contractValue: 750, status: 'Won' },
  { id: 2, date: '2026-11-19', title: 'SaaS Onboarding Email Sequence', category: 'Copywriting', connects: 50, contractValue: 400, status: 'Interviewed' },
  { id: 3, date: '2026-11-19', title: 'Figma to Tailwind Next.js Dashboard', category: 'Frontend', connects: 65, contractValue: 1200, status: 'Won' },
  { id: 4, date: '2026-11-20', title: 'Python Web Scraping Bot for Zillow', category: 'Python', connects: 45, contractValue: 250, status: 'Lost' },
  { id: 5, date: '2026-11-21', title: 'Technical SEO Audit & Schema Markup', category: 'SEO', connects: 30, contractValue: 350, status: 'Submitted' }
];

let proposals = [];

function loadProposals() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (raw) {
    try {
      proposals = JSON.parse(raw);
    } catch (e) {
      proposals = [...DEFAULT_PROPOSALS];
    }
  } else {
    proposals = [...DEFAULT_PROPOSALS];
    saveProposals();
  }
  render();
}

function saveProposals() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(proposals));
}

// Recalculate KPIs
function updateKPIs() {
  const total = proposals.length;
  const won = proposals.filter(p => p.status === 'Won');
  const winRate = total > 0 ? ((won.length / total) * 100).toFixed(1) : '0.0';
  
  const connectPrice = parseFloat(document.getElementById('eval-connect-price').value) || 0.15;
  const feePct = (parseFloat(document.getElementById('eval-fee-pct').value) || 15) / 100;
  
  const totalConnects = proposals.reduce((acc, p) => acc + (parseInt(p.connects) || 0), 0);
  const totalSpend = (totalConnects * connectPrice).toFixed(2);
  
  const grossBillings = won.reduce((acc, p) => acc + (parseFloat(p.contractValue) || 0), 0);
  const platformFees = grossBillings * feePct;
  const netRevenue = (grossBillings - platformFees - parseFloat(totalSpend)).toFixed(2);
  
  const cac = won.length > 0 ? (parseFloat(totalSpend) / won.length).toFixed(2) : totalSpend;

  document.getElementById('kpi-win-rate').innerText = `${winRate}%`;
  document.getElementById('kpi-win-ratio').innerText = `${won.length} won / ${total} bids`;
  document.getElementById('kpi-connects-count').innerText = totalConnects.toLocaleString();
  document.getElementById('kpi-connects-spend').innerText = `$${totalSpend} spent`;
  document.getElementById('kpi-net-revenue').innerText = `$${parseFloat(netRevenue).toLocaleString('en-US', {minimumFractionDigits: 2})}`;
  document.getElementById('kpi-gross-revenue').innerText = `$${grossBillings.toLocaleString('en-US', {minimumFractionDigits: 2})} gross billings`;
  document.getElementById('kpi-cac').innerText = `$${cac}`;
}

// Quick Bid Evaluator Calculation
function updateBidEvaluator() {
  const contractVal = parseFloat(document.getElementById('eval-contract-value').value) || 0;
  const connects = parseInt(document.getElementById('eval-connects').value) || 0;
  const hours = parseFloat(document.getElementById('eval-hours').value) || 1;
  const connectPrice = parseFloat(document.getElementById('eval-connect-price').value) || 0.15;
  const feePct = (parseFloat(document.getElementById('eval-fee-pct').value) || 15) / 100;

  const connectsCost = connects * connectPrice;
  const fee = contractVal * feePct;
  const net = contractVal - fee - connectsCost;
  const hourly = hours > 0 ? (net / hours) : 0;
  const maxBreakeven = connectPrice > 0 ? Math.floor((contractVal * (1 - feePct)) / connectPrice) : 0;

  document.getElementById('eval-res-connect-cost').innerText = `$${connectsCost.toFixed(2)}`;
  document.getElementById('eval-res-platform-fee').innerText = `$${fee.toFixed(2)}`;
  document.getElementById('eval-res-net-payout').innerText = `$${net.toFixed(2)}`;
  document.getElementById('eval-res-hourly').innerText = `$${hourly.toFixed(2)} / hr`;
  document.getElementById('eval-res-breakeven').innerText = maxBreakeven.toLocaleString();
}

// Render Table
function renderTable() {
  const tbody = document.getElementById('proposals-tbody');
  tbody.innerHTML = '';

  const connectPrice = parseFloat(document.getElementById('eval-connect-price').value) || 0.15;

  proposals.forEach(p => {
    const cost = ((p.connects || 0) * connectPrice).toFixed(2);
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${p.date || 'Today'}</td>
      <td><strong>${escapeHtml(p.title)}</strong></td>
      <td>${escapeHtml(p.category || 'General')}</td>
      <td>${p.connects}</td>
      <td class="text-red">$${cost}</td>
      <td>$${parseFloat(p.contractValue || 0).toLocaleString()}</td>
      <td>
        <select class="status-select" data-id="${p.id}">
          <option value="Submitted" ${p.status === 'Submitted' ? 'selected' : ''}>Submitted</option>
          <option value="Viewed" ${p.status === 'Viewed' ? 'selected' : ''}>Viewed</option>
          <option value="Interviewed" ${p.status === 'Interviewed' ? 'selected' : ''}>Interviewed</option>
          <option value="Won" ${p.status === 'Won' ? 'selected' : ''}>Won 🏆</option>
          <option value="Lost" ${p.status === 'Lost' ? 'selected' : ''}>Lost</option>
        </select>
      </td>
      <td>
        <button class="btn-link text-red delete-btn" data-id="${p.id}">Delete</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  // Attach status change events
  tbody.querySelectorAll('.status-select').forEach(sel => {
    sel.addEventListener('change', e => {
      const id = parseInt(e.target.dataset.id);
      const item = proposals.find(p => p.id === id);
      if (item) {
        item.status = e.target.value;
        saveProposals();
        updateKPIs();
      }
    });
  });

  // Attach delete events
  tbody.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      const id = parseInt(e.target.dataset.id);
      proposals = proposals.filter(p => p.id !== id);
      saveProposals();
      render();
    });
  });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.innerText = text;
  return div.innerHTML;
}

function render() {
  updateKPIs();
  updateBidEvaluator();
  renderTable();
}

// Add New Proposal Form
document.getElementById('form-log-proposal').addEventListener('submit', e => {
  e.preventDefault();
  const title = document.getElementById('prop-title').value.trim();
  const val = parseFloat(document.getElementById('prop-value').value) || 0;
  const connects = parseInt(document.getElementById('prop-connects').value) || 0;
  const status = document.getElementById('prop-status').value;
  const category = document.getElementById('prop-category').value.trim() || 'General';

  const newProp = {
    id: Date.now(),
    date: new Date().toISOString().split('T')[0],
    title: title,
    category: category,
    connects: connects,
    contractValue: val,
    status: status
  };

  proposals.unshift(newProp);
  saveProposals();
  render();

  // Reset title
  document.getElementById('prop-title').value = '';
});

// CSV Export
document.getElementById('btn-export-csv').addEventListener('click', () => {
  if (proposals.length === 0) {
    alert('No proposals recorded yet.');
    return;
  }
  const connectPrice = parseFloat(document.getElementById('eval-connect-price').value) || 0.15;
  const headers = ['ID', 'Date', 'Job Title', 'Category', 'Connects Spent', 'Connect Cost USD', 'Target Contract USD', 'Status'];
  const rows = proposals.map(p => [
    p.id,
    p.date,
    `"${(p.title || '').replace(/"/g, '""')}"`,
    `"${(p.category || '').replace(/"/g, '""')}"`,
    p.connects,
    ((p.connects || 0) * connectPrice).toFixed(2),
    p.contractValue,
    p.status
  ]);

  const csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `connects_roi_portfolio_${new Date().toISOString().split('T')[0]}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
});

// Reset Sample Data
document.getElementById('btn-clear-sample').addEventListener('click', () => {
  if (confirm('Reset to default sample proposals?')) {
    proposals = [...DEFAULT_PROPOSALS];
    saveProposals();
    render();
  }
});

// Dynamic Evaluator Bindings
['eval-contract-value', 'eval-connects', 'eval-hours', 'eval-connect-price', 'eval-fee-pct'].forEach(id => {
  document.getElementById(id).addEventListener('input', () => {
    updateBidEvaluator();
    updateKPIs();
  });
});

document.addEventListener('DOMContentLoaded', loadProposals);
