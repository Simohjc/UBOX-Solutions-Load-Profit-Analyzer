# 🚛 UBOX Solutions – Load Profit Analyzer

website: https://ubox-solutions-load-profit-analyzer-mfdxvubiu267xohphbg4ma.streamlit.app/

A Streamlit web app built for **[UBOX Solutions](https://uboxsolutions.com)**, a Houston, TX-based cargo van delivery and last-mile logistics company, to quickly analyze the profitability of a load before accepting it — factoring in fuel cost, deadhead miles, driver pay, tolls, and maintenance. Every analyzed load is permanently saved to a PostgreSQL database, so nothing is lost when the session ends.

![UBOX Solutions](file_logo.png)

## Features

- **Load Information form** — enter pickup/delivery location, pickup/drop-off date & time, load pay, miles, fuel price, driver pay, tolls, and maintenance cost per mile
- **Instant profitability analysis** — total miles, net profit, net profit per mile, total expenses, operating margin, and deadhead percentage
- **Revenue & Expense breakdown** — gallons needed, revenue per mile, profit after fuel, fuel cost, maintenance cost, and more
- **Automatic load rating** — GREAT / ACCEPTABLE / LOW PROFIT / POOR based on net profit per mile
- **Deadhead rating** — Excellent / Good / High / Very High based on deadhead percentage
- **Persistent database storage** — every submitted load is saved to a PostgreSQL database using an object-oriented data model (a `Load` class) and `psycopg2`, so history survives app restarts, not just the current session
- **Load history tracking** — every analyzed load is saved for the session, with duplicate-submission protection and empty-input validation
- **History table** with color-coded columns (highlighting net profit per mile and total expenses), horizontally scrollable for smaller screens
- **CSV export** — download your full load history for record-keeping
- **Custom branded UI** — UBOX Solutions logo, color theme, and styled cards throughout

## Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — UI framework
- [Pandas](https://pandas.pydata.org/) — data handling and CSV export
- [PostgreSQL](https://www.postgresql.org/) — persistent database storage
- [psycopg2](https://www.psycopg.org/) — PostgreSQL adapter for Python

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL running locally (or accessible remotely)
- pip

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

3. Create a PostgreSQL database (default name used in the app: `ubox_loads`).

4. Update the database connection details in `final_load_app.py` with your own PostgreSQL credentials:
   ```python
   conn = psycopg2.connect(
       host="localhost",
       dbname="ubox_loads",
       user="postgres",
       password="your_password_here"
   )
   ```

5. Make sure the logo file (`file_logo.png`) is in the same folder as the app script.

### Running the App

```bash
streamlit run final_load_app.py
```

The app will open automatically in your browser at `http://localhost:8501`. On first run, it will automatically create the `tracking_loads` table if it doesn't already exist.

## Usage

1. Fill in the **Load Information** form — pickup/delivery details, load pay, miles, fuel price, driver pay, tolls, and maintenance cost.
2. Click **Analyse Load** to see the full profitability breakdown.
3. Review the automatic **GREAT LOAD / ACCEPTABLE LOAD / LOW PROFIT LOAD / POOR LOAD** rating and deadhead efficiency rating.
4. Every analyzed load is automatically added to your **history table** below, and permanently saved to the PostgreSQL database in the background.
5. Click **Download History as CSV** to export your data, or **Clear History** to reset the on-screen session view (this does not delete the underlying database records).

## Data Persistence

Unlike a typical Streamlit app where data only lives for the current browser session, this app writes every submitted load to a PostgreSQL table called `tracking_loads`, using an object-oriented `Load` class and parameterized SQL queries (protecting against SQL injection). This means:

- Load history is never lost, even after closing the app, restarting the computer, or redeploying
- The database serves as a permanent, queryable record of every load ever submitted
- The on-screen table remains a lightweight, session-based preview for immediate review

## Project Structure

```
python_course/
├── final_load_app.py   # Main Streamlit application
├── file_logo.png        # UBOX Solutions logo
└── README.md
```

## Roadmap / Ideas for Future Improvements

- Load the on-screen history table directly from PostgreSQL instead of session state, so it persists across page refreshes too
- Multi-load comparison view
- Per-driver or per-truck filtering
- Editable/deletable individual history rows, synced with the database
- User authentication so multiple dispatchers can log in and track their own loads

## License

This project is proprietary to UBOX Solutions. All rights reserved.

## Contact

For questions or support, reach out to UBOX Solutions.

🌐 [uboxsolutions.com](https://uboxsolutions.com)
