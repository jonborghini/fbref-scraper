# 📊 FBref Matches Scraper

This project is a Python-based web scraper that collects detailed match data from [FBref.com](https://fbref.com) for selected leagues and seasons, including results, venues, referees, attendance, and advanced team statistics.

## 🚀 Features

- Automatically scrapes played matches from top European leagues (La Liga, Premier League, Serie A, Bundesliga, Ligue 1)
- Supports multiple seasons (default: 2018–2019 to 2023–2024)
- Extracts detailed team-level stats (xG, possession, corners, passes, defense, etc.)
- Saves data to `.csv` files organized by league and season
- Prevents duplicates by checking existing data before writing

## 🧠 Technologies

- Python 3
- `requests`
- `beautifulsoup4`
- `pandas`

## 📁 Project Structure

```
fbref-scraper/
├── main.py                  # Main script to run the scraper
├── scraper/
│   ├── __init__.py          # Makes the scraper module importable
│   └── matches_scraper.py   # Contains all scraping logic
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── .gitignore               # Ignored files and folders
```

## ⚙️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/jonborghini/fbref-scraper.git
cd fbref-scraper
```

### 2. (Optional) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the scraper

```bash
python main.py
```

Scraped `.csv` files will be saved into folders named after each league, for example:

```
La_Liga/La Liga_2023-2024_matches.csv
```
## 🛠️ Customization

You can easily modify:
- The leagues to scrape (`leagues` dictionary in `main.py`)
- The seasons to scrape (`seasons` list in `main.py`)
- The stats or output formatting in `matches_scraper.py`

## 🔒 Duplicate Handling

The scraper checks if each match already exists in the corresponding CSV file and skips it to avoid duplication.

## ⏳ Notes on Delays and Responsiveness

FBref pages can be slow or inconsistent to load, and scraping large amounts of matches may take time.

- The scraper includes a delay (`time.sleep(3.2)`) between seasons to avoid overwhelming the server.
- If you're scraping multiple leagues and years, expect the process to take several minutes or more.
- Matches without complete stats will be skipped or partially filled depending on availability.
- Consider modifying the sleep duration or limiting seasons if you need quicker results.

Please use this tool responsibly to avoid overloading the FBref servers.

## 📚 Documentation

- 🗺️ [How to Add New Leagues](https://github.com/jonborghini/fbref-scraper/wiki/How-to-Add-New-Leagues)
- 📊 [Understanding the Stats](https://github.com/jonborghini/fbref-scraper/wiki/Understanding-the-Stats)

## 📈 Roadmap

- Add player-level stats scraper (per match)
- Export data to SQL / parquet
- CLI or web interface to choose league/season
- Jupyter Notebooks for data analysis & visualization

## 🧑‍💻 Author

**Jon Hidalgo**  
[GitHub](https://github.com/jonborghini)

## 📄 License

MIT License – free to use for personal, educational and professional purposes.
