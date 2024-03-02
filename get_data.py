import requests
import json
import csv
import os
from datetime import datetime, timedelta

Bearer = ""

def get_data(url):
    headers = {'Authorization': Bearer}
    response = requests.get(url, headers=headers)
    return response.json()

def save_to_csv(data, date):
    csv_header = ['country', 'currentRank', 'previousRank', 'peakRank', 'peakDate', 'appearancesOnChart', 'consecutiveAppearancesOnChart', 'rankingMetricValue', 'rankingMetricType', 'entryStatus', 'entryRank', 'entryDate', 'trackName', 'trackUri', 'displayImageUri', 'artistName', 'artistSpotifyUri', 'releaseDate']

    with open(f'dataset/data_{date}.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_header)
        for entry in data['entries']:
            chart_entry_data = entry['chartEntryData']
            track_metadata = entry['trackMetadata']
            artists = track_metadata['artists']
            if(len(artists) > 1):
                writer.writerow([
                    data['displayChart']['chartMetadata']['dimensions']['country'],
                    chart_entry_data['currentRank'],
                    chart_entry_data['previousRank'],
                    chart_entry_data['peakRank'],
                    chart_entry_data['peakDate'],
                    chart_entry_data['appearancesOnChart'],
                    chart_entry_data['consecutiveAppearancesOnChart'],
                    chart_entry_data['rankingMetric']['value'],
                    chart_entry_data['rankingMetric']['type'],
                    chart_entry_data['entryStatus'],
                    chart_entry_data['entryRank'],
                    chart_entry_data['entryDate'],
                    track_metadata['trackName'],
                    track_metadata['trackUri'],
                    track_metadata['displayImageUri'],
                    ', '.join([artist['name'] for artist in artists]),
                    ', '.join([artist['spotifyUri'] for artist in artists]),
                    track_metadata['releaseDate']
                ])

def save_json_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def main(start_date, n):
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = start_datetime - timedelta(weeks=n)
    current_date = start_datetime
    if not os.path.exists('dataset'):
        os.makedirs('dataset')
    if not os.path.exists('dataObjects'):
        os.makedirs('dataObjects')
    while current_date > end_date:
        url = f'https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-global-weekly/{current_date.strftime("%Y-%m-%d")}'
        print(f'Fetching data from {url}')
        data = get_data(url)
        save_json_to_file(data, f'dataObjects/data_{current_date.strftime("%Y-%m-%d")}.json')
        save_to_csv(data, current_date.strftime("%Y-%m-%d"))
        current_date -= timedelta(days=7)
        
main('2024-02-01',2)