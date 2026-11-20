// popup.js - Technical SEO & Schema Audit Logic

let currentAuditData = null;

// Tab Switching
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.content-panel').forEach(p => p.style.display = 'none');
    
    btn.classList.add('active');
    const targetTab = btn.getAttribute('data-tab');
    document.getElementById(`tab-${targetTab}`).style.display = 'flex';
  });
});

// Audit extraction function to inject into page DOM
function extractPageSEO() {
  const audit = {
    url: window.location.href,
    title: document.title || '',
    title_length: (document.title || '').length,
    description: '',
    canonical: '',
    robots: '',
    h1_tags: [],
    h2_tags: [],
    schemas: [],
    warnings: []
  };

  // Meta Description
  const metaDesc = document.querySelector('meta[name="description"]');
  if (metaDesc) {
    audit.description = metaDesc.getAttribute('content') || '';
  }

  // Canonical
  const canonicalEl = document.querySelector('link[rel="canonical"]');
  if (canonicalEl) {
    audit.canonical = canonicalEl.getAttribute('href') || '';
  }

  // Robots
  const robotsEl = document.querySelector('meta[name="robots"]');
  if (robotsEl) {
    audit.robots = robotsEl.getAttribute('content') || '';
  }

  // Headings
  document.querySelectorAll('h1').forEach(h => audit.h1_tags.push(h.innerText.trim()));
  document.querySelectorAll('h2').forEach(h => audit.h2_tags.push(h.innerText.trim()));

  // Schemas (JSON-LD)
  document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
    try {
      const data = JSON.parse(s.innerText);
      audit.schemas.push(data);
    } catch (e) {
      audit.warnings.push('Malformed JSON-LD schema detected in page markup.');
    }
  });

  // Evaluate Warnings
  if (!audit.title) {
    audit.warnings.push('Missing <title> tag.');
  } else if (audit.title_length > 60) {
    audit.warnings.push(`Title exceeds 60 characters (${audit.title_length} chars). Truncation risk on Google SERP.`);
  }

  if (!audit.description) {
    audit.warnings.push('Missing meta description tag.');
  } else if (audit.description.length > 160) {
    audit.warnings.push(`Meta description exceeds 160 characters (${audit.description.length} chars).`);
  }

  if (!audit.canonical) {
    audit.warnings.push('Missing <link rel="canonical"> tag.');
  }

  if (audit.h1_tags.length === 0) {
    audit.warnings.push('Missing primary H1 tag on page.');
  } else if (audit.h1_tags.length > 1) {
    audit.warnings.push(`Multiple H1 tags detected (${audit.h1_tags.length}). Recommended standard is a single unique H1.`);
  }

  return audit;
}

// Render Results into Popup UI
function renderAudit(data) {
  currentAuditData = data;

  // Title
  const titleEl = document.getElementById('meta-title');
  const titleCounter = document.getElementById('title-counter');
  titleEl.innerText = data.title || '(Not set)';
  titleCounter.innerText = `${data.title_length} chars`;

  // Description
  const descEl = document.getElementById('meta-desc');
  const descCounter = document.getElementById('desc-counter');
  descEl.innerText = data.description || '(Not set)';
  descCounter.innerText = `${data.description.length} chars`;

  // Canonical & Robots
  document.getElementById('meta-canonical').innerText = data.canonical || 'None';
  document.getElementById('meta-robots').innerText = data.robots || 'Default (index, follow)';

  // Warnings
  const warningList = document.getElementById('warning-list');
  warningList.innerHTML = '';
  if (data.warnings.length === 0) {
    warningList.innerHTML = '<div class="success-item">✓ Zero technical issues flagged. Clean structure!</div>';
  } else {
    data.warnings.forEach(w => {
      const item = document.createElement('div');
      item.className = 'warning-item';
      item.innerText = `⚠ ${w}`;
      warningList.appendChild(item);
    });
  }

  // Headings Tab
  document.getElementById('h1-count').innerText = data.h1_tags.length;
  const h1List = document.getElementById('h1-list');
  h1List.innerHTML = '';
  if (data.h1_tags.length === 0) {
    h1List.innerHTML = '<span style="color:#64748b;">No H1 tags found</span>';
  } else {
    data.h1_tags.forEach(text => {
      const el = document.createElement('div');
      el.className = 'heading-tag';
      el.innerText = text;
      h1List.appendChild(el);
    });
  }

  document.getElementById('h2-count').innerText = data.h2_tags.length;
  const h2List = document.getElementById('h2-list');
  h2List.innerHTML = '';
  if (data.h2_tags.length === 0) {
    h2List.innerHTML = '<span style="color:#64748b;">No H2 tags found</span>';
  } else {
    data.h2_tags.slice(0, 15).forEach(text => {
      const el = document.createElement('div');
      el.className = 'heading-tag';
      el.innerText = text;
      h2List.appendChild(el);
    });
    if (data.h2_tags.length > 15) {
      const more = document.createElement('div');
      more.style.color = '#64748b';
      more.style.fontSize = '10px';
      more.innerText = `+ ${data.h2_tags.length - 15} more H2 headings...`;
      h2List.appendChild(more);
    }
  }

  // Schemas Tab
  document.getElementById('schema-count').innerText = data.schemas.length;
  const schemaList = document.getElementById('schema-list');
  schemaList.innerHTML = '';
  if (data.schemas.length === 0) {
    schemaList.innerHTML = '<span style="color:#64748b;">No JSON-LD structured data detected</span>';
  } else {
    data.schemas.forEach((s, idx) => {
      const card = document.createElement('div');
      card.className = 'schema-card';
      const schemaType = s['@type'] || (Array.isArray(s['@graph']) ? 'Graph (' + s['@graph'].length + ' nodes)' : 'Unknown');
      card.innerHTML = `<div class="schema-type">#${idx + 1} @type: ${schemaType}</div><pre style="white-space:pre-wrap; word-break:break-all;">${JSON.stringify(s, null, 2).slice(0, 300)}...</pre>`;
      schemaList.appendChild(card);
    });
  }
}

// Client Export Functions
document.getElementById('btn-export-md').addEventListener('click', () => {
  if (!currentAuditData) return;
  const md = `# Technical SEO & Schema Audit Report
Generated by **Technical SEO & Schema Inspector** on ${new Date().toLocaleDateString()}

## Target URL
${currentAuditData.url || 'Active Tab'}

## 1. Meta & Core Signals
- **Title (${currentAuditData.title_length} chars):** ${currentAuditData.title || 'MISSING'}
- **Meta Description (${currentAuditData.description.length} chars):** ${currentAuditData.description || 'MISSING'}
- **Canonical URL:** ${currentAuditData.canonical || 'MISSING'}
- **Robots Directive:** ${currentAuditData.robots || 'index, follow (default)'}

## 2. Heading Architecture
- **H1 Count:** ${currentAuditData.h1_tags.length}
${currentAuditData.h1_tags.map(h => `  - \`${h}\``).join('\n')}
- **H2 Count:** ${currentAuditData.h2_tags.length}
${currentAuditData.h2_tags.slice(0, 10).map(h => `  - ${h}`).join('\n')}

## 3. Structured Data (JSON-LD)
- **Detected Schemas:** ${currentAuditData.schemas.length}
${currentAuditData.schemas.map((s, i) => `  - Schema #${i+1}: \`@type: ${s['@type'] || 'Custom'}\``).join('\n')}

## 4. Technical Issues & Recommendations
${currentAuditData.warnings.length === 0 ? '- No critical issues detected. Site complies with on-page best practices.' : currentAuditData.warnings.map(w => `- [ ] **CRITICAL / WARN:** ${w}`).join('\n')}

---
*Report generated for client delivery. Powered by Zero-Bloat Technical SEO Inspector.*
`;

  downloadFile('technical_seo_audit.md', md, 'text/markdown');
});

document.getElementById('btn-export-csv').addEventListener('click', () => {
  if (!currentAuditData) return;
  const rows = [
    ['Metric', 'Value', 'Status'],
    ['URL', `"${currentAuditData.url}"`, 'Audited'],
    ['Title', `"${(currentAuditData.title || '').replace(/"/g, '""')}"`, currentAuditData.title_length > 60 ? 'Warning: >60 chars' : 'Valid'],
    ['Meta Description', `"${(currentAuditData.description || '').replace(/"/g, '""')}"`, currentAuditData.description ? 'Present' : 'Missing'],
    ['Canonical', `"${currentAuditData.canonical || ''}"`, currentAuditData.canonical ? 'Present' : 'Missing'],
    ['H1 Count', currentAuditData.h1_tags.length, currentAuditData.h1_tags.length === 1 ? 'Optimal' : 'Flagged'],
    ['JSON-LD Schemas', currentAuditData.schemas.length, currentAuditData.schemas.length > 0 ? 'Detected' : 'None'],
    ['Total Issues Flagged', currentAuditData.warnings.length, currentAuditData.warnings.length === 0 ? 'Pass' : 'Action Required']
  ];

  const csv = rows.map(r => r.join(',')).join('\n');
  downloadFile('technical_seo_summary.csv', csv, 'text/csv');
});

function downloadFile(filename, content, type) {
  const blob = new Blob([content], { type: type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Initialization Logic
function init() {
  if (typeof chrome !== 'undefined' && chrome.tabs && chrome.scripting) {
    chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
      if (!tabs || tabs.length === 0) return;
      const tabId = tabs[0].id;

      chrome.scripting.executeScript({
        target: { tabId: tabId },
        function: extractPageSEO
      }, results => {
        if (results && results[0] && results[0].result) {
          renderAudit(results[0].result);
        } else {
          showFallback('Unable to access tab DOM. Make sure you are on a standard http/https page.');
        }
      });
    });
  } else {
    // Standalone / Test Environment Fallback
    const mockData = {
      url: window.location.href,
      title: "Best Wireless Headphones 2026 - Ultimate Buyer's Guide",
      title_length: 53,
      description: "Discover top-rated wireless headphones with active noise cancellation, deep bass, and 40-hour battery life.",
      canonical: "https://example.com/headphones-guide",
      robots: "index, follow",
      h1_tags: ["Top Wireless Headphones 2026", "Editor's Choice Over-Ear Pick"],
      h2_tags: ["Bose QuietComfort Ultra", "Sony WH-1000XM5", "AirPods Max 2", "Battery Life Shootout"],
      schemas: [{
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Bose QuietComfort Ultra",
        "offers": { "@type": "Offer", "price": "199.99", "priceCurrency": "USD" }
      }],
      warnings: ["Multiple H1 tags detected (2). Google prefers a single primary H1."]
    };
    renderAudit(mockData);
  }
}

function showFallback(msg) {
  document.getElementById('meta-title').innerText = msg;
}

document.addEventListener('DOMContentLoaded', init);
