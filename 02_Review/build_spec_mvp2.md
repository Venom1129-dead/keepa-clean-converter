# Build Spec: Shopify Supplier-to-Catalog CSV Normalizer & Image-SKU Mapper
- **Asset ID:** MVP_02
- **Target Revenue:** $19 one-time lifetime license
- **Target Build Time:** <3 hours
- **Dependencies:** Client-side HTML/JS/CSS (PapaParse + SheetJS). 0 external paid APIs.

---

## 1. Problem Statement & Proof-of-Wallet
Shopify store owners frequently post about broken CSV imports on `r/shopify` and `r/ecommerce`:
> *"Why is it so complicated/manual to make the CSV file? Each of our suppliers has a different file layout and it all needs to be Frankensteined to make it work."*
> *"Every time I export, the field names or formats aren't consistent... automated pipelines break, and I spend hours manually cleaning CSVs."*

Current alternatives are bloated monthly subscriptions like Matrixify ($20–$200/mo) or paying $15–$30/hour to virtual assistants on Upwork.

---

## 2. The 10% Wedge Solution
A fast, privacy-first client-side tool running 100% in RAM:
1. **Fuzzy Header Matcher:** Automatically detects incoming supplier columns (`item_title`, `wholesale_price`, `msrp`, `qty_on_hand`, `barcode`, `weight_lbs`) and maps them to valid Shopify standard schema (`Title`, `Variant Price`, `Variant Compare At Price`, `Variant Inventory Qty`, `Variant Barcode`, `Variant Grams`).
2. **Automatic Data Transformations:**
   - **Handle Generator:** Slugs title (`"Men's Running Shoes - Blue"` → `"mens-running-shoes-blue"`).
   - **Weight Unit Normalizer:** Detects lbs or oz and converts to Shopify standard grams (`grams = lbs * 453.592`).
   - **Price Margin Multiplier:** Allows applying a markup (e.g. `Price = Supplier Cost * 2.2` or `+$15`).
   - **Image-SKU Templater:** If supplier doesn't provide image URLs, dynamically generates CDN links from SKU: `https://mycdn.com/products/{SKU}.jpg`.
   - **Shopify Default Boilerplate Injection:** Fills required Shopify fields (`Published: TRUE`, `Variant Inventory Tracker: shopify`, `Variant Fulfillment Service: manual`, `Status: active`).
3. **Saved Supplier Presets:** Stores mapping configurations in browser `localStorage` (AliExpress, Faire, Doba, or Custom Vendor).
4. **Monetization Gate:**
   - Free Tier: Previews and exports first 25 products.
   - Pro Unlock ($19): Gumroad / Lemon Squeezy license key unlocks unlimited row exports and custom preset saving.

---

## 3. Architecture & File Tree
```plaintext
03_Active_MVP_02/
├── frontend/
│   ├── index.html        <-- Drag-and-drop zone + Column mapping table + Preview
│   ├── styles.css        <-- Clean modern dark UI
│   ├── app.js            <-- Mapping engine, transformations, preset manager
│   └── presets.json      <-- Pre-packaged mapping templates (Faire, AliExpress, Doba)
└── verifier/
    ├── sample_supplier_feed.csv  <-- Messy supplier CSV fixture
    ├── test_mapper.py            <-- Deterministic python unit tests for mapping logic
    └── verify_e2e.js             <-- Node E2E test verifying valid Shopify CSV output
```

---

## 4. Deterministic Acceptance Criteria
- [ ] Accepts messy supplier CSV with non-standard column names.
- [ ] Correctly maps at least 8 core fields to Shopify import spec.
- [ ] Generates valid URL handles without illegal characters or double hyphens.
- [ ] Converts lbs to grams deterministically.
- [ ] Generates valid Shopify import CSV matching official Shopify CSV documentation.
- [ ] Passes automated test suite with Exit Code 0.
