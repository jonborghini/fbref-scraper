from scraper.matches_scraper import fetch_page, extract_played_matches, process_and_save_match, read_existing_matches

import os
import time

base_url = 'https://fbref.com'

leagues = {
    'La Liga': 12,
    'Premier League': 9,
    'Serie A': 11,
    'Ligue 1': 13,
    'Bundesliga': 20,
}

seasons = ['2023-2024', '2022-2023', '2021-2022', '2020-2021', '2019-2020', '2018-2019']

def main():
    for league_name, league_id in leagues.items():
        for season in seasons:
            schedule_url = f"{base_url}/en/comps/{league_id}/{season}/schedule/{league_name}-Scores-and-Fixtures"
            print(f"Processing {league_name} for the {season} season.")
            soup = fetch_page(schedule_url)
            if not soup:
                continue
            matches_details = extract_played_matches(soup, season, league_id, base_url)
            output_dir = league_name.replace(" ", "_")
            os.makedirs(output_dir, exist_ok=True)
            csv_path = os.path.join(output_dir, f'{league_name}_{season}_matches.csv')
            existing_matches = read_existing_matches(csv_path)
            for match in matches_details:
                match_id = (match['Date'], match['Home_Team_ID'], match['Away_Team_ID'])
                if match_id not in existing_matches:
                    process_and_save_match(match, csv_path)
                    print(f"Added stats for {match['Home']} vs {match['Away']}")
                else:
                    print(f"Match {match['Home']} vs {match['Away']} on {match['Date']} already has data, skipping...")
            time.sleep(3.2)

if __name__ == "__main__":
    main()
