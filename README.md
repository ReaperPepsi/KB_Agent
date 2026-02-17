# KB_Agent

A Python-based DBA automation tool that scrapes Microsoft SQL Server Knowledge Base (KB) patch data from the web, cleanses and normalizes it, inserts it into a SQL Server database, and generates server compliance reports. Designed to help database administrators track patch levels across SQL Server instances and identify servers that are not running the latest cumulative updates.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Installation](#installation)
- [Usage](#usage)
- [Logging](#logging)
- [SQL Scripts](#sql-scripts)
- [Dependencies](#dependencies)

---

## Overview

KB_Agent automates the process of keeping a SQL Server patch catalog up to date. The pipeline has three main stages:

1. **Web Scraping** — Fetches the latest SQL Server build numbers and release dates from [sqlserverbuilds.blogspot.com](https://sqlserverbuilds.blogspot.com/) for SQL Server versions 2014 through 2025.
2. **Data Cleansing & Normalization** — Validates and normalizes the raw scraped data using regular expressions, structures it by SQL Server version, and saves it to a JSON file.
3. **Database Insertion** — Connects to a SQL Server instance via ODBC and inserts the cleaned patch data into a staging/catalog table.

A set of SQL Server scripts then powers compliance reporting, allowing DBAs to compare the currently installed version on each server against the latest available patch for that major version.

---

## Project Structure

```
DBA_python/
├── config/
│   ├── config.example.yaml        # Template for configuration (copy and fill in)
│   └── config.dev.yaml            # Active dev configuration (gitignored)
├── logs/
│   ├── logger.py                  # Centralized logging setup
│   ├── db.log                     # Database operation logs
│   ├── web_scrapping.log          # Web scraping logs
│   └── data_cleansing.log         # Data cleansing logs
├── src/
│   ├── app.py                     # Main entry point — orchestrates the full pipeline
│   ├── core/
│   │   ├── db/
│   │   │   ├── connectors/
│   │   │   │   └── sql_connector.py   # SQLConnector class (pyodbc wrapper)
│   │   │   └── models/
│   │   │       └── insert_data.py     # Helper for building INSERT commands
│   │   └── scraping/
│   │       ├── test_scrapping.py      # Web scraping logic (requests + BeautifulSoup)
│   │       └── kb_list.json           # Raw scraped output (auto-generated)
│   ├── data_cleansing/
│   │   ├── data_normalizer.py         # Regex-based cleansing and version normalization
│   │   └── kb_list_cleansed.json      # Cleansed output (auto-generated)
│   └── SQLServer/
│       ├── 01_Create_Item_Catalogs.sql         # DDL: all catalog and server tables
│       ├── 02_Insert_Data.sql                  # DML: seed/reference data inserts
│       ├── 03_Initial_Version_Comparison.sql   # Ad-hoc version comparison query
│       ├── 04_Server_Compliance_Report.sql     # View: ServerCompliance
│       └── 05_Complaince_Report_StoredProcedure.sql  # SP: compliance report
├── tests/
│   └── tests.py                   # Unit/integration tests
├── requirements_overview.txt      # Python package list
└── README.md
```

---

## How It Works

### 1. Web Scraping (`src/core/scraping/test_scrapping.py`)

- `check_connection(url)` — Sends a GET request to the target URL with timeout handling. Raises or logs errors for HTTP failures and timeouts.
- `kb_scrapping(response)` — Parses the HTML response using BeautifulSoup, locates the version-specific `<table>` elements (SQL 2014–2025), and extracts KB numbers and release dates from each row.
- `insert_data(kb_list)` — Serializes the raw scraped data to `kb_list.json` and returns it as a Python dict.

### 2. Data Cleansing & Normalization (`src/data_cleansing/data_normalizer.py`)

- `data_cleansing(scraped_json)` — Applies regex patterns to validate KB strings (format `XX.X.XXXX.X`) and dates (format `YYYY-MM-DD`). Invalid rows are skipped and logged.
- `data_normalizer(kb_list)` — Maps the cleaned list back to version keys (`SQL_2025`, `SQL_2022`, ..., `SQL_2014`) to produce a structured dictionary.
- `create_cleansed_json(cleansed_data)` — Persists the normalized data to `kb_list_cleansed.json` and returns it for further processing.

### 3. Database Insertion (`src/core/db/connectors/sql_connector.py`, `src/app.py`)

- `SQLConnector` wraps a `pyodbc` connection. It supports `create_connection()`, `execute_query(query, params)`, and `close()`, with logging and error handling at each step.
- `get_insert_parameter(normalized_data)` — Extracts `(KB, release_date)` tuples from the normalized JSON.
- `insert_data_sql(parameters)` — Iterates over the parameter list and executes a parameterized `INSERT INTO dbo.KB_Test` statement, committing each row and logging failures without stopping the run.

---

## Database Schema

The SQL Server database (`KB_Project_Dev`) consists of the following tables:

| Table | Description |
|---|---|
| `Test_Customer` | Customer/client registry |
| `tbl_Status_Catalog` | Instance status codes (active, removed, transferred, etc.) |
| `tbl_Version_Catalog` | KB catalog — stores major, minor, build, and revision version numbers along with release date |
| `tbl_Environment_Catalog` | Server environment types (dev, staging, prod, etc.) |
| `tbl_Backup_Catalog` | Backup strategy types |
| `tbl_serverlist` | Inventory of SQL Server instances, linked to customer, status, version, environment, and backup tables |

### Compliance View (`dbo.ServerCompliance`)

A SQL view that uses a CTE (`Latest_Version`) to find the most recent patch for each major SQL Server version. For each active server in the inventory, it compares the installed version against the latest available patch and outputs either `'Compliant'` or `'Not Compliant'`.

---

## Configuration

Copy the example config and fill in your SQL Server connection details:

```bash
cp config/config.example.yaml config/config.dev.yaml
```

Edit `config/config.dev.yaml`:

```yaml
database:
  server: "localhost"          # SQL Server host/IP (TCP/IP)
  database: "KB_Project_Dev"   # Target database name
  username: "your_sql_user"    # SQL Server login
  password: "your_password"

logging:
  level: "INFO"
  file: "./logs/app.log"

env:
  name: "dev"

sources:
  ms_kb_url: "https://sqlserverbuilds.blogspot.com/"
```

> **Note:** `config.dev.yaml` is gitignored and should never be committed. Only `config.example.yaml` belongs in source control.

The SQL connector uses **ODBC Driver 18 for SQL Server** with `TrustServerCertificate=yes`. Make sure this driver is installed on the machine running the script.

---

## Installation

**Requirements:** Python 3.13+, SQL Server with ODBC Driver 18

```bash
# Clone the repository
git clone <repo-url>
cd DBA_python

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# Install dependencies
pip install -r requirements_overview.txt
```

**Python packages installed:**

| Package | Version | Purpose |
|---|---|---|
| `beautifulsoup4` | 4.14.3 | HTML parsing for web scraping |
| `requests` | 2.32.5 | HTTP client for fetching web pages |
| `pyodbc` | 5.3.0 | SQL Server connectivity via ODBC |
| `PyYAML` | 6.0.3 | YAML config file parsing |
| `soupsieve` | 2.8 | CSS selector support for BeautifulSoup |
| `urllib3` | 2.6.2 | HTTP transport layer |
| `certifi` | 2025.11.12 | SSL certificate bundle |
| `charset-normalizer` | 3.4.4 | Encoding detection |
| `idna` | 3.11 | Internationalized domain names |
| `typing_extensions` | 4.15.0 | Backported type hints |

---

## Usage

**Set up the database first** by running the SQL scripts in order (see [SQL Scripts](#sql-scripts) below).

Then run the full pipeline from the project root:

```bash
python -m src.app
```

This will:
1. Scrape the latest KB data from `sqlserverbuilds.blogspot.com`
2. Cleanse and normalize the data
3. Insert the results into `dbo.KB_Test` in your configured SQL Server database

Logs for each stage are written to the `logs/` directory.

---

## Logging

The project uses a centralized logger (`logs/logger.py`) that writes to separate log files per module:

| Log File | Contents |
|---|---|
| `logs/db.log` | Database connection events, query execution, errors, and rollbacks |
| `logs/web_scrapping.log` | HTTP request status, scraping progress, and errors |
| `logs/data_cleansing.log` | Cleansing run details, validation errors, and normalization events |

Log format: `TIMESTAMP | LEVEL | MESSAGE`

---

## SQL Scripts

Run these scripts in order against your SQL Server instance to set up the schema:

| Script | Description |
|---|---|
| `01_Create_Item_Catalogs.sql` | Creates all tables: customer, status, version catalog, environment, backup, and server inventory |
| `02_Insert_Data.sql` | Inserts seed/reference data into catalog tables |
| `03_Initial_Version_Comparison.sql` | Ad-hoc query for a quick version comparison check |
| `04_Server_Compliance_Report.sql` | Creates the `dbo.ServerCompliance` view |
| `05_Complaince_Report_StoredProcedure.sql` | Creates a stored procedure wrapping the compliance report |

---

## Notes & Known Limitations

- File paths in `test_scrapping.py` and `data_normalizer.py` are currently hardcoded to `D:\DBA_python\...`. These should be updated to use relative paths or be driven from the config file for portability.
- The scraper targets specific `<table>` indices on the source page. If the page layout changes, the index numbers may need to be adjusted.
- The project uses two branches: `main` and `dev`. Active development happens on `dev`.
- No sensitive data is committed to the repository
- Configuration is environment-specific
- This project is intended as a learning, experimentation, and reference platform
