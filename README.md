# 🚛 UBOX Solutions – Load Profit Analyzer

**Live app:** https://ubox-solutions-load-profit-analyzer-mfdxvubiu267xohphbg4ma.streamlit.app/

A Streamlit web app built for **[UBOX Solutions](https://uboxsolutions.com)**, a Houston, TX-based cargo van delivery and last-mile logistics company, to quickly analyze the profitability of a load before accepting it — factoring in fuel cost, deadhead miles, driver pay, tolls, and maintenance. Every analyzed load is permanently saved to a cloud PostgreSQL database (Neon), so nothing is lost when the session ends, the app restarts, or it's redeployed.

![UBOX Solutions](file_logo.png)

## Features

- **Load Information form** — pickup/delivery location, pickup/drop-off date & time, load pay, miles, fuel price, driver pay, tolls, and maintenance cost per mile
- **Instant profitability analysis** — total miles, net profit, net profit per mile, total expenses, operating margin, and deadhead percentage
- **Revenue & Expense breakdown** — gallons needed, revenue per mile, profit after fuel, fuel cost, maintenance cost, and more
- **Automatic load rating** — GREAT / ACCEPTABLE / LOW PROFIT / POOR based on net profit per mile
- **Deadhead rating** — Excellent / Good / High / Very High based on deadhead percentage
- **Persistent cloud database storage** — every submitted load is saved to a PostgreSQL database (hosted on [Neon](https://neon.tech)) using an object-oriented data model (a `Load` class) and `psycopg2`, so history survives restarts and redeployments, not just the current session
- **Session-based load history** — every analyzed load is also shown for the current session, with duplicate-submission protection and empty-input validation
- **History table** with color-coded columns (highlighting net profit per mile and total expenses), horizontally scrollable for smaller screens
- **CSV export** — download the session's load history for record-keeping
- **Custom branded UI** — UBOX Solutions logo, color theme, and styled cards throughout
- **Secure credential handling** — database credentials are never stored in code; they're managed through Streamlit secrets, both locally and in production

## Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — UI framework
- [Pandas](https://pandas.pydata.org/) — data handling and CSV export
- [PostgreSQL](https://www.postgresql.org/) — relational database
- [Neon](https://neon.tech) — serverless, cloud-hosted PostgreSQL (free tier)
- [psycopg2](https://www.psycopg.org/) — PostgreSQL adapter for Python
- [Git](https://git-scm.com/) / [GitHub](https://github.com) — version control
- [Streamlit Community Cloud](https://share.streamlit.io) — hosting/deployment

## Architecture

┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ Streamlit UI │ ──▶ │ Load class + │ ──▶ │ Neon PostgreSQL │
│ (form, metrics, │ │ add_load() │ │ (cloud, always │
│ CSV export) │ │ via psycopg2 │ │ on, persistent) │
└─────────────────┘ └──────────────────┘ └─────────────────┘


Every submitted load flows through an object-oriented `Load` class before being written to the database with a parameterized SQL `INSERT` (protecting against SQL injection). The database connection string is read from Streamlit secrets (`st.secrets["DATABASE_URL"]`) rather than being hardcoded, so real credentials never appear in the source code or the public GitHub history.

## Getting Started

### Prerequisites

- Python 3.9+
- pip
- A free [Neon](https://neon.tech) account (or any PostgreSQL database)
- Git

### Installation

1. Clone the repository:
```bash
   git clone https://github.com/Simohjc/UBOX-Solutions-Load-Profit-Analyzer.git
   cd UBOX-Solutions-Load-Profit-Analyzer
```

2. Install dependencies:
```bash
   pip install streamlit pandas psycopg2-binary
```

3. Create a free PostgreSQL database on [Neon](https://neon.tech) and copy your connection string from the "Connect" panel on your project dashboard. It will look like:

postgresql://neondb_owner:xxxxx@ep-xxxx.neon.tech/neondb?sslmode=require


4. Create a `.streamlit/secrets.toml` file in the project root (this file is git-ignored and never committed) with:
```toml
   DATABASE_URL = "postgresql://neondb_owner:xxxxx@ep-xxxx.neon.tech/neondb?sslmode=require"
```

5. Make sure the logo file (`file_logo.png`) is in the same folder as the app script.

### Running the App

```bash
streamlit run final_load_app.py
```

The app opens automatically at `http://localhost:8501`. On first run, it automatically creates the `tracking_loads` table if it doesn't already exist.

### Deploying to Streamlit Community Cloud

1. Push the repo to GitHub (excluding `.streamlit/secrets.toml`, which is git-ignored by design).
2. Deploy the app on [share.streamlit.io](https://share.streamlit.io), pointing to `final_load_app.py`.
3. In the app's **Settings → Secrets**, paste the same `DATABASE_URL` line used locally.
4. Streamlit Cloud installs dependencies from `requirements.txt` automatically, including `psycopg2-binary`.

## Usage

1. Fill in the **Load Information** form — pickup/delivery details, load pay, miles, fuel price, driver pay, tolls, and maintenance cost.
2. Click **Analyse Load** to see the full profitability breakdown.
3. Review the automatic **GREAT LOAD / ACCEPTABLE LOAD / LOW PROFIT LOAD / POOR LOAD** rating and deadhead efficiency rating.
4. Every analyzed load is added to the on-screen **history table** and permanently written to the Neon database in the background.
5. Click **Download History as CSV** to export the current session's data, or **Clear History** to reset the on-screen view (this does not delete the underlying database records — the database is the permanent record).

## Project Structure

UBOX-Solutions-Load-Profit-Analyzer/
├── final_load_app.py # Main Streamlit application
├── file_logo.png # UBOX Solutions logo
├── requirements.txt # Python dependencies
├── .gitignore # Excludes .streamlit/secrets.toml from version control
└── README.md


## Project History

This project started as a simple Streamlit form for calculating load profitability and grew step by step into a full-stack application with real persistence and deployment:

1. **Core calculator** — Streamlit form and profitability math (net profit, profit per mile, deadhead %, operating margin)
2. **Branding & UX** — custom UBOX Solutions logo, color theme, styled metric cards, and a scrollable, color-coded history table
3. **Session-based history** — in-memory load history with duplicate-entry prevention, input validation, and CSV export
4. **Deployment** — published live on Streamlit Community Cloud
5. **Object-oriented data model** — introduced a `Load` class to represent each submitted load cleanly
6. **Database persistence** — connected the app to PostgreSQL with `psycopg2`, so every load is permanently saved, not just held in the browser session
7. **Cloud migration** — moved the database from local PostgreSQL to [Neon](https://neon.tech), a serverless cloud PostgreSQL provider, so the live deployed app can actually reach it
8. **Secrets management** — replaced hardcoded database credentials with Streamlit secrets, both locally and in production, so no password is ever exposed in the public repo
9. **Version control** — set up Git from scratch and connected the local project to this GitHub repository

## Roadmap / Ideas for Future Improvements

- Load the on-screen history table directly from PostgreSQL instead of session state, so it persists across page refreshes too
- Multi-load comparison view
- Per-driver or per-truck filtering
- Editable/deletable individual history rows, synced with the database
- User authentication (signup/login) with `bcrypt` password hashing, so multiple dispatchers can log in and track their own loads

## License

This project is proprietary to UBOX Solutions. All rights reserved.

## Contact

For questions or support, reach out to UBOX Solutions.

🌐 [uboxsolutions.com](https://uboxsolutions.com)

## Author

Mohamed El Khair — [LinkedIn](https://www.linkedin.com/in/mohamed-elkhair/) · [GitHub](https://github.com/Simohjc) · [Portfolio](https://simohjc.github.io/Portfolio-dataAna/)