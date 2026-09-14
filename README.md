# 🚛 UBOX Solutions – Load Profit Analyzer

A Streamlit web app for owner-operators and trucking companies to quickly analyze the profitability of a load before accepting it — factoring in fuel cost, deadhead miles, driver pay, tolls, and maintenance.

![UBOX Solutions](file_logo.png)

## Features

- **Load Information form** — enter pickup/delivery location, pickup/drop-off date & time, load pay, miles, fuel price, driver pay, tolls, and maintenance cost per mile
- **Instant profitability analysis** — total miles, net profit, net profit per mile, total expenses, operating margin, and deadhead percentage
- **Revenue & Expense breakdown** — gallons needed, revenue per mile, profit after fuel, fuel cost, maintenance cost, and more
- **Automatic load rating** — GREAT / ACCEPTABLE / LOW PROFIT / POOR based on net profit per mile
- **Deadhead rating** — Excellent / Good / High / Very High based on deadhead percentage
- **Load history tracking** — every analyzed load is saved for the session, with duplicate-submission protection and empty-input validation
- **History table** with color-coded columns (highlighting net profit per mile and total expenses), horizontally scrollable for smaller screens
- **CSV export** — download your full load history for record-keeping
- **Custom branded UI** — UBOX Solutions logo, color theme, and styled cards throughout

## Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — UI framework
- [Pandas](https://pandas.pydata.org/) — data handling and CSV export

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. Install dependencies:
   ```bash
   pip install streamlit pandas
   ```

3. Make sure the logo file (`file_logo.png`) is in the same folder as the app script.

### Running the App

```bash
streamlit run final_load_app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## Usage

1. Fill in the **Load Information** form — pickup/delivery details, load pay, miles, fuel price, driver pay, tolls, and maintenance cost.
2. Click **Analyse Load** to see the full profitability breakdown.
3. Review the automatic **GREAT LOAD / ACCEPTABLE LOAD / LOW PROFIT LOAD / POOR LOAD** rating and deadhead efficiency rating.
4. Every analyzed load is automatically added to your **history table** below.
5. Click **Download History as CSV** to export your data, or **Clear History** to start fresh.

## Project Structure

```
python_course/
├── final_load_app.py   # Main Streamlit application
├── file_logo.png        # UBOX Solutions logo
└── README.md
```

## Roadmap / Ideas for Future Improvements

- Persist load history to a database or file so it survives app restarts
- Multi-load comparison view
- Per-driver or per-truck filtering
- Editable/deletable individual history rows

## License

This project is proprietary to UBOX Solutions. All rights reserved.

## Contact

For questions or support, reach out to UBOX Solutions.
