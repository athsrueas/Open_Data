# How DataRepublican Tools Are Developed

*A technical, architectural, and process breakdown*

## Overview

**DataRepublican** is an independent, data-driven investigative platform focused on exposing U.S. government spending, nonprofit funding networks, and political finance using **public data**, **client-side computation**, and **open-source tooling**.

* X (Twitter): [https://x.com/DataRepublican](https://x.com/DataRepublican)
* Website: [https://datarepublican.com](https://datarepublican.com)
* Substack: [https://datarepublican.substack.com](https://datarepublican.substack.com)
* GitHub: [https://github.com/DataRepublican](https://github.com/DataRepublican)

The platform gained viral attention during and after the 2024 election cycle for making large, opaque government datasets *searchable, visual, and explorable* by the public.

---

## 1. Technical Stack

### Core Architecture

* **Static site architecture**
* **Client-side computation** (no backend query server)
* Optimized for transparency, speed, and resilience

### Languages & Frameworks

* **Ruby + Jekyll** (static site generation)

  * [https://jekyllrb.com](https://jekyllrb.com)
* **JavaScript** (interactive logic & visualization)
* **Python** (data ingestion, cleaning, preprocessing)
* **HTML / CSS**
* **Tailwind CSS** (styling)

  * [https://tailwindcss.com](https://tailwindcss.com)

### Tooling

* **Node.js + Yarn** (build tooling)
* **PostCSS** (CSS processing)
* **Playwright** (UI testing; present in repo)

---

## 2. Data Sources & Ingestion

### Primary Data Sources

#### Federal Spending

* **USAspending.gov**

  * [https://www.usaspending.gov](https://www.usaspending.gov)
  * Used for active federal grants, award amounts, recipients, locations
  * Accessed via API and bulk exports

#### Nonprofit & Charity Financials

* **IRS Form 990 / 990-PF**

  * [https://www.irs.gov/charities-non-profits/form-990-series](https://www.irs.gov/charities-non-profits/form-990-series)
* ~773,000 nonprofits
* ~1.3 million grants
* Joined via EIN (Employer Identification Number)

#### Political Donations

* **FEC filings**

  * [https://www.fec.gov/data](https://www.fec.gov/data)
* **ActBlue** (Democratic platform)
* **WinRed** (Republican platform)
* Filters:

  * Donations under $10
  * High-frequency donation patterns

#### Additional Datasets

* National Endowment for Democracy publications
* Protest funding records
* Historical documents (e.g., Soros tax returns)

---

## 3. Data Processing & Indexing

### Preprocessing Pipeline

1. Download raw public datasets
2. Normalize names, IDs, addresses
3. Deduplicate records
4. Join across datasets (grants ↔ nonprofits ↔ filings)
5. Export cleaned datasets as static files (JSON / CSV)

### Custom Inverted Index (Critical Innovation)

Instead of querying a database:

* All text fields are **tokenized**
* Keywords → list of matching rows
* Index built **offline**
* Shipped to the browser

**Result:**

* Instant full-text search
* No backend
* Massive performance gain

This is the key reason the site outperforms official government portals.

---

## 4. Visualization & UI/UX

### Visualization Libraries

* **D3.js** (implied; Sankey + network graphs)

  * [https://d3js.org](https://d3js.org)

### Core Visual Tools

#### Charity Explorer (Sankey Diagram)

> Visualizes how money flows between government → NGOs → sub-grantees

* Node width = money in/out
* Color-coded flows
* Expandable network depth

Example tool:
[https://datarepublican.com/charity-explorer](https://datarepublican.com/charity-explorer)

#### Charity Network Graph

> Directed graph of nonprofit relationships

* Breadth-first search expansion
* Alerts for high taxpayer funding
* Downloadable SVG output

[https://datarepublican.com/charity-graph](https://datarepublican.com/charity-graph)

#### Small Dollar Donation Analyzer

> Identifies suspicious donation patterns

* Streaming client-side search
* Real-time aggregation
* Flags:

  * > 25 donations → “High donation volume”

[https://datarepublican.com/small-dollar-donations](https://datarepublican.com/small-dollar-donations)

---

## 5. Infrastructure & Deployment

### Hosting

* **American Cloud**

  * [https://americancloud.com](https://americancloud.com)
* Chosen for:

  * U.S. hosting
  * Independence from Big Tech platforms

### Deployment Model

* Static files only
* No databases
* No server-side queries
* Users download datasets once; browser caches locally

### Performance Strategy

* Client-side execution
* Browser caching (IndexedDB / LocalStorage)
* Gzip-compressed assets
* Scales effortlessly under load

---

## 6. Automation & AI Usage

### Rule-Based Automation

* Donation volume anomaly detection
* Grant flow thresholds
* Taxpayer funding ratios

### AI / NLP Applications

* **Mission alignment analysis**

  * Compares grant descriptions to nonprofit mission statements
  * Flags off-mission or DEI-related spending

Tool example:
[https://datarepublican.com/dei-search](https://datarepublican.com/dei-search)

### Philosophy

> AI augments human investigation — it does not replace it.

Automation surfaces **leads**, humans interpret **context**.

---

## 7. Developer Profile

### Creator

* **Jennica Pounds** (initially anonymous as “DataRepublican”)

Coverage:

* Deseret News
  [https://www.deseret.com/politics/2025/03/11/datarepublican-jennica-pounds-uses-ai-to-help-doge-doxxed-by-rolling-stone/](https://www.deseret.com/politics/2025/03/11/datarepublican-jennica-pounds-uses-ai-to-help-doge-doxxed-by-rolling-stone/)
* Blaze Media
  [https://www.theblaze.com/news/datarepublican-exposes-uniparty-government-thriving-beyond-taxpayer-reach](https://www.theblaze.com/news/datarepublican-exposes-uniparty-government-thriving-beyond-taxpayer-reach)

### Background

* Software engineer
* Big-tech experience
* Deaf, non-verbal (uses ASL)
* Built project largely solo
* Later collaborated informally with DOGE analysts

### Ethos

* Radical transparency
* Public data only
* Open-source intelligence
* Citizen-led accountability

---

## 8. Why This Model Works

### Key Advantages

* No backend bottlenecks
* No vendor lock-in
* Auditable by anyone
* Extremely low operating cost
* Resistant to censorship or overload

### Core Insight

> **Most “hard” government data problems are UX + indexing problems, not access problems.**

---

## 9. Key Links (Quick Reference)

* Website: [https://datarepublican.com](https://datarepublican.com)
* X / Twitter: [https://x.com/DataRepublican](https://x.com/DataRepublican)
* GitHub: [https://github.com/DataRepublican](https://github.com/DataRepublican)
* Substack: [https://datarepublican.substack.com](https://datarepublican.substack.com)
* USAspending: [https://www.usaspending.gov](https://www.usaspending.gov)
* IRS 990 Data: [https://www.irs.gov/charities-non-profits/form-990-series](https://www.irs.gov/charities-non-profits/form-990-series)
* FEC Data: [https://www.fec.gov/data](https://www.fec.gov/data)
* D3.js: [https://d3js.org](https://d3js.org)
* American Cloud: [https://americancloud.com](https://americancloud.com)
want to go next.
