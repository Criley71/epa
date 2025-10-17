import pandas as pd
from django.core.management.base import BaseCommand
from epa_app.models import siteData
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, '../../../../'))
CSV_PATH = os.path.join(PROJECT_ROOT, 'data', 'april-2022-near-road-site-list_public.csv')
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
EPA_API_EMAIL = os.getenv("EPA_API_EMAIL")
EPA_API_KEY = os.getenv("EPA_API_KEY")
POLLUTE_CODES = {'42101' : 'Carbon Monoxide (CO)', '42401' : 'Sulfer Dioxide (SO2)', '42602' : 'Nitrogen Dioxide (NO2)', '88101' : 'PM2.5'}
site_df = pd.read_csv(CSV_PATH)



def generate_year_chunks(start_date_str, end_year=2024):
    """
    start_date_str: CSV start date in 'm/d/y' format
    Returns a list of (bdate, edate) tuples in YYYYMMDD format
    """
    start_date = datetime.strptime(start_date_str, "%m/%d/%y")
    chunks = []

    # First chunk: start_date → Dec 31 of that year
    first_end = datetime(year=start_date.year, month=12, day=31)
    chunks.append((
        start_date.strftime("%Y%m%d"),
        min(first_end, datetime(end_year, 12, 31)).strftime("%Y%m%d")
    ))

    # Subsequent full years
    for year in range(start_date.year + 1, end_year + 1):
        bdate = datetime(year, 1, 1)
        edate = datetime(year, 12, 31)
        if bdate > datetime(end_year, 12, 31):
            break
        chunks.append((
            bdate.strftime("%Y%m%d"),
            min(edate, datetime(end_year, 12, 31)).strftime("%Y%m%d")
        ))

    return chunks
  
  
class Command(BaseCommand):
  count = 0
  help = 'Pull EPA data and save to database using sites from csv'
  def handle(self, *args, **options):
    all_data = []
    for _, row in site_df.iterrows():
      state, county, site = row['AQS ID'].split('-')
      site_id = f"{state}-{county}-{site}"
      for bdate, edate in generate_year_chunks(row['NO2     Start Date']):
        bdate_obj = datetime.strptime(bdate, "%Y%m%d").date()
        edate_obj = datetime.strptime(edate, "%Y%m%d").date()
        # Check if there are already entries for this site and date range
        existing = siteData.objects.filter(site_id=site_id, date__range=[bdate_obj, edate_obj])
        if existing.exists():
          print(f"Skipping {site_id} from {bdate} to {edate} (already in DB)")
          continue  # skip only this date range, not the whole site

        # Otherwise, make the API call
        try:
          response = requests.get(
            "https://aqs.epa.gov/data/api/dailyData/bySite",
            params={
              "email": EPA_API_EMAIL,
              "key": EPA_API_KEY,
              "param": 42602,
              "bdate": bdate,
              "edate": edate,
              "state": state,
              "county": county,
              "site": site
            },
            timeout=15
          )
          response.raise_for_status()
          data = response.json()
        except requests.exceptions.RequestException as e:
          print(f"Request failed for {site_id} ({bdate}-{edate}): {e}")
          continue  # skip this chunk and move on

        # Insert only rows that are not already in the DB
        for entry in data.get("Data", []):
          if not siteData.objects.filter(site_id=site_id, date=entry['date_local']).exists():
            siteData.objects.create(
                site_id=site_id,
                state=entry.get("state", "unknown"),
                county=entry.get("county", "unknown"),
                pollutant=entry.get("parameter", "unknown"),
                value=entry.get("arithmetic_mean", 0.0),
                units=entry.get("units_of_measure", "unknown"),
                date=entry.get("date_local")
            )
        #with open("epa_data.json", "w") as f:
          #json.dump(all_data, f, indent=4)
        #exit()
      #NO2_start_date = pd.to_datetime(row['NO2     Start Date'], format="%m/%d/%Y").strftime("%Y%m%d")
      #CO_start_date = pd.to_datetime(row['CO     Start Date'], format="%m/%d/%Y").strftime("%Y%m%d")
      #pm25_start_date = pd.to_datetime(row['Continuous PM2.5 Start Date'], format="%m/%d/%Y").strftime("%Y%m%d")
    

    self.stdout.write(self.style.SUCCESS('Data imported successfully!'))