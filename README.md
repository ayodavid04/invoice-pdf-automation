<img width="1280" height="724" alt="Screenshot 2026-01-22 173112" src="https://github.com/user-attachments/assets/65fe07a1-0bc4-46ce-bc32-dd936051ff3b" />
# Client Invoice PDF Automation & Analytics Pipeline

## Overview

This project is an **end-to-end data engineering and analytics pipeline** that simulates a real-world business workflow: generating client invoices as PDFs, extracting and validating structured data from those PDFs, loading the data into a PostgreSQL database (Neon), building an analytics-ready SQL layer, and visualizing the results in **Power BI**.

The system is designed to mirror how invoice data would be handled in a production environment — with data quality checks, reproducibility, and BI consumption in mind.

---

## High-Level Architecture

**PDF Generation → Parsing & Validation → ETL Pipeline → PostgreSQL (Neon) → SQL Analytics Layer → Power BI Dashboard**

Each stage is intentionally separated to reflect real-world data engineering best practices.

---

## Step 1: Invoice PDF Generation

### Purpose

To simulate real client billing data without relying on sensitive or proprietary datasets.

### What Happens

* A Python script generates **50 realistic invoice PDFs**
* Each invoice includes:

  * Client name
  * Invoice number
  * Invoice date
  * Due date
  * Subtotal
  * Tax
  * Total
* Dates and monetary values are randomized within realistic ranges
* PDFs are saved to a local input directory for downstream processing

### Why This Matters

This step ensures the pipeline works with **unstructured inputs (PDFs)** — one of the most common real-world data ingestion problems.

---

## Step 2: PDF Parsing & Data Extraction

### Purpose

Convert unstructured PDF invoices into structured, machine-readable data.

### What Happens

* Each PDF is read and parsed using a dedicated parser module
* Text fields are extracted using deterministic rules
* Raw extracted values are normalized into a Python dictionary per invoice

### Key Challenges Addressed

* PDFs are not databases — parsing requires defensive logic
* Missing or malformed fields are expected and handled

---

## Step 3: Validation & Data Quality Checks

### Purpose

Prevent bad or incomplete data from contaminating analytics.

### Validation Rules

For each invoice record:

* Required fields must exist:

  * Invoice number
  * Client name
  * Invoice date
  * Total
* Monetary fields are coerced to numeric types
* Dates are coerced to datetime
* Computed totals (`subtotal + tax`) are compared to the stated total

### Flags Generated

* `has_all_required_fields`
* `total_mismatch` (tolerance applied)

These flags are later used in analytics and auditing.

---

## Step 4: ETL Pipeline Orchestration

### Purpose

Coordinate the full flow from raw PDFs to analytics-ready data.

### What Happens

* A single pipeline entrypoint:

  1. Loads PDFs
  2. Extracts raw invoice data
  3. Validates and normalizes records
  4. Writes clean data to PostgreSQL (Neon)
  5. Generates a locked analytics dataset

### Design Decisions

* Modular pipeline stages (parse, validate, load)
* Central logging for observability
* Idempotent execution (safe re-runs)

---

## Step 5: PostgreSQL (Neon) Data Storage

### Purpose

Persist structured invoice data in a cloud-hosted relational database.

### Schema Design

* Invoices stored in normalized tables
* Explicit data types for dates and monetary values
* Designed for analytics and BI consumption

### Why Neon

* Serverless PostgreSQL
* Production-like cloud environment
* Direct compatibility with BI tools

---

## Step 6: Locked Analytics Dataset (Python)

### Purpose

Create a **single source of truth** for analytics.

### What Happens

* All invoice records are loaded into a Pandas DataFrame
* Types are re-validated
* Derived fields are computed:

  * `computed_total`
  * `total_mismatch`
  * `has_all_required_fields`
* A locked CSV dataset is written to disk for reproducibility

### Why This Exists

* Guarantees analytics consistency
* Enables debugging and auditing
* Mirrors how analytics snapshots are created in real data teams

---

## Step 7: SQL Analytics Layer

### Purpose

Move business logic **out of the dashboard** and into SQL.

### What Was Built

Reusable SQL views, including:

* Client revenue breakdown
* Monthly revenue trends
* Invoice counts and averages
* KPI-ready aggregates

### Benefits

* BI tools remain thin and fast
* Metrics are consistent across tools
* Analytics logic is version-controlled

---

## Step 8: Power BI Dashboard

### Purpose

Present insights in a clear, executive-ready format.

### Dashboard Features

* Total revenue
* Average invoice value
* Invoice counts
* Client contribution breakdown
* Monthly revenue trends

### Key Design Choice

Power BI connects **directly to SQL views** in PostgreSQL — no CSV imports, no manual refresh logic.

---

## Tech Stack

* **Python**: PDF generation, parsing, ETL, analytics locking
* **PostgreSQL (Neon)**: Cloud data warehouse
* **SQL**: Analytics and KPI layer
* **Power BI**: Visualization and reporting
* **Git/GitHub**: Version control and documentation

---

## What This Project Demonstrates

* End-to-end data engineering thinking
* Working with unstructured data (PDFs)
* Data quality and validation practices
* Analytics-layer-first design
* BI tool integration with a real database

---

## Future Improvements

* Incremental loading
* Error quarantining for failed invoices
* Automated tests for validation rules
* Deployment via CI/CD

---

## Evidence

See `/docs/screenshots` for:

* Pipeline execution
* SQL analytics views
* Database tables
* Power BI dashboard

---

## How to Run (High Level)

1. Generate PDFs
2. Run the ETL pipeline
3. Verify data in PostgreSQL
4. Refresh Power BI dashboard

---

**This project is intentionally built to resemble a real production analytics workflow, not a tutorial example.**
