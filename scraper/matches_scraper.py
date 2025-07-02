import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def read_existing_matches(csv_path):
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        existing_matches = set(zip(df['Date'], df['Home_Team_ID'], df['Away_Team_ID']))
        return existing_matches
    return set()

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f'Failed to retrieve data from {url}')
        return None

def extract_match_details(row, base_url):
    home_team_link = row.select_one('td:nth-child(5) > a')['href']
    away_team_link = row.select_one('td:nth-child(9) > a')['href']
    home_team_id = extract_team_id_from_url(home_team_link)
    away_team_id = extract_team_id_from_url(away_team_link)
    details = {
        'Wk': row.select_one('th').text,
        'Day': row.select_one('td:nth-child(2)').text,
        'Date': row.select_one('td:nth-child(3) > a').text,
        'Time': row.select_one('td:nth-child(4) > span.venuetime').text.strip() if row.select_one('td:nth-child(4) > span.venuetime') else 'TBD',
        'Home': row.select_one('td:nth-child(5) > a').text,
        'Home_Team_ID': home_team_id,
        'Away': row.select_one('td:nth-child(9) > a').text,
        'Away_Team_ID': away_team_id,
        'Attendance': row.select_one('td:nth-child(10)').text if row.select_one('td:nth-child(10)') else None,
        'Venue': row.select_one('td:nth-child(11)').text if row.select_one('td:nth-child(11)') else None,
        'Referee': row.select_one('td:nth-child(12)').text if row.select_one('td:nth-child(12)') else None,
        'Match_Link': f"{base_url}{row.select_one('td:nth-child(13) > a')['href']}" if row.select_one('td:nth-child(13) > a') else None
    }
    return details

def extract_played_matches(soup, season, league_id, base_url):
    matches_details = []
    rows = soup.select(f'#sched_{season}_{league_id}_1 > tbody > tr')
    for row in rows:
        if row.select_one('td.center > a'):
            match_details = extract_match_details(row, base_url)
            matches_details.append(match_details)
    return matches_details


def fetch_and_extract_team_stats(match_url, home_team_id, away_team_id):
    soup = fetch_page(match_url)
    if not soup:
        return {}

    all_stats = {}
    tabs = ['Summary', 'Passing', 'Passing_Types', 'Defense', 'Possession', 'Misc']
    for tab_name in tabs:
        # Use data-stat attribute for unique identification
        stat_attributes = soup.select(f'#stats_{home_team_id}_{tab_name.lower()} > thead > tr:nth-child(2) > th[data-stat]')
        stat_names = [th['data-stat'] for th in stat_attributes if 'data-stat' in th.attrs][6:]

        home_stats = [td.text for td in soup.select(f'#stats_{home_team_id}_{tab_name.lower()} > tfoot > tr > td')[5:]]
        away_stats = [td.text for td in soup.select(f'#stats_{away_team_id}_{tab_name.lower()} > tfoot > tr > td')[5:]]
        
        # Combine stats with proper prefixing for home and away
        for i, stat_name in enumerate(stat_names):
            all_stats[f'{stat_name}_H'] = home_stats[i] if i < len(home_stats) else 'N/A'
            all_stats[f'{stat_name}_A'] = away_stats[i] if i < len(away_stats) else 'N/A'

    def safe_extract_text(selector):
        """Safely extract text content or attribute value."""
        element = soup.select_one(selector)
        if element:
            return element.text.strip()  
        return 'N/A'

    # Extract additional stats not in main tables
    additional_stats = {
        'possession_H': safe_extract_text('#team_stats > table > tbody > tr:nth-child(3) > td:nth-child(1) > div > div:nth-child(1) > strong'),
        'possession_A': safe_extract_text('#team_stats > table > tbody > tr:nth-child(3) > td:nth-child(2) > div > div:nth-child(1) > strong'),
        'corners_H': safe_extract_text('#team_stats_extra > div:nth-child(1) > div:nth-child(7)'),
        'corners_A': safe_extract_text('#team_stats_extra > div:nth-child(2) > div:nth-child(7)'),
        'saves_H': safe_extract_text(f'#keeper_stats_{home_team_id} > tbody > tr > td:nth-child(7)'),
        'saves_A': safe_extract_text(f'#keeper_stats_{away_team_id} > tbody > tr > td:nth-child(7)'),
    }

    all_stats.update(additional_stats)


    return all_stats


def extract_team_id_from_url(url):
    parts = url.split('/')
    if 'squads' in parts:
        squad_index = parts.index('squads') + 1
        return parts[squad_index]
    return None

def process_and_save_match(match, csv_path):
    home_team_id = match['Home_Team_ID']
    away_team_id = match['Away_Team_ID']
    match_url = match['Match_Link']
    team_stats = fetch_and_extract_team_stats(match_url, home_team_id, away_team_id)
    match.update(team_stats)
    match.pop('Match_Link', None)
    df_processed_match = pd.DataFrame([match])
    if os.path.exists(csv_path):
        df_processed_match.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df_processed_match.to_csv(csv_path, index=False)