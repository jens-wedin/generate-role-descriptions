import os
import csv
import logging
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("supabase_conversion.log"),
                        logging.StreamHandler()
                    ])

def upload_csv_to_supabase(csv_filepath, supabase_url, supabase_key, table_name="roles"):
    logging.info(f"Starting CSV to Supabase upload for file: {csv_filepath}")

    # Initialize Supabase client
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        logging.info("Supabase client initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing Supabase client: {e}")
        return

    # Read CSV and upload data
    try:
        with open(csv_filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                try:
                    # Supabase expects a dictionary where keys match table column names
                    data_to_insert = {key: value for key, value in row.items()}
                    
                    response = supabase.table(table_name).insert(data_to_insert).execute()
                    if response.data:
                        logging.info(f"Successfully inserted row {i+1} for role: {row.get('Role Name', 'Unknown')}")
                    else:
                        logging.warning(f"No data returned for row {i+1} for role: {row.get('Role Name', 'Unknown')}. Response: {response.status_code}")

                except Exception as e:
                    logging.error(f"Error inserting row {i+1} ({row.get('Role Name', 'Unknown')}) to Supabase: {e}")

        logging.info(f"Finished processing CSV file: {csv_filepath}. Check Supabase for data integrity.")

    except FileNotFoundError:
        logging.error(f"Error: CSV file not found at {csv_filepath}")
    except Exception as e:
        logging.error(f"Error reading or processing CSV file {csv_filepath}: {e}")

if __name__ == "__main__":
    # --- USER CONFIGURATION ---
    # Replace with your actual Supabase URL and Key
    # You can find these in your Supabase project settings -> API
    SUPABASE_URL = "YOUR_SUPABASE_URL"
    SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"
    # --------------------------

    csv_file = "/Users/jens.wedin/Documents/Visual Studio/generate-role-descriptions/roles_structured.csv"
    
    if SUPABASE_URL == "YOUR_SUPABASE_URL" or SUPABASE_KEY == "YOUR_SUPABASE_ANON_KEY":
        logging.error("Supabase URL or Key not configured. Please update the `SUPABASE_URL` and `SUPABASE_KEY` variables in `csv_to_supabase.py`.")
    else:
        upload_csv_to_supabase(csv_file, SUPABASE_URL, SUPABASE_KEY)
