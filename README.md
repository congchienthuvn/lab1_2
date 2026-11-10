# Tiki Products ETL Pipeline to PostgreSQL

A robust and modular Python-based ETL (Extract, Transform, Load) pipeline designed to extract product data from multiple JSON files, parse and transform the attributes into structured database columns, and securely load them into a PostgreSQL database.

---

## Project Structure

The project follows a clean, professional separation-of-concerns architecture:

```text
lab1_2/
├── data/                 # Directory containing source JSON files (Tiki products)
├── .gitignore            # Git ignore file
├── config.py             # Configuration loader from database.ini
├── database.ini          # Secure database connection credentials
├── loader.py             # ETL pipeline logic (Extract, transform, load with transaction management)
├── main.py               # Application entry point
├── models.py             # Database schema DDL definitions
├── pyproject.toml        # Project metadata and dependencies
└── README.md             # Project documentation