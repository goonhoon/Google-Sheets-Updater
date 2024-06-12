import gspread
from google.oauth2.service_account import Credentials
import pybomb

# Define route to Google api. Create the .json file on the Google API page.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '_____.json'

# Authenticate and initialize gspread client
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open the spreadsheet and worksheet
spreadsheet_id = '_________'
sheet_name = 'Adamos'

sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

# Initialize the Giant Bomb API through Pybomb
bomb_api = '________'
games_client = pybomb.GamesClient(bomb_api)


# Get the names and years columns (A=1, B=2...)
names = sheet.col_values(2)
years = sheet.col_values(3)

# Iterate over each row and update empty cells in column C with release year
for i, (name, year) in enumerate(zip(names, years)):
    if not year:
        # Search for the game using pybomb
        response = games_client.quick_search(
            name=name,
            return_fields='original_release_date',
            sort_by='name',
            desc=True
        )

        # Extract the release date
        if response.results:
            full_date = response.results[0]['original_release_date']
            # Extract only the year (YYYY) from the full_date (YYYY-MM-DD)
            if full_date is not None:
              year = full_date.split('-')[0]
              row = i + 1
              sheet.update_cell(row, 3, year)
              print(f"Updated row {row} with release year {year}")
            else:
              print(f"No release date found for game: {name}")

print("Update completed!")