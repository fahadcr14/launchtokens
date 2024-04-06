
import pandas as pd 
import os
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

def read_excel_and_replace_sheet():
    try:
        # Read data from Excel file into a DataFrame
        df = pd.read_excel( r"cryptotokens.xlsx")
        spreadsheet_id = "1nrCJJHTGssyF45m7ujj1BXG2YBLRVHg9_qpMyWiid7I"
        range_name = "Sheet1"  
        # Authenticate with Google Sheets API
        credentials = service_account.Credentials.from_service_account_file(r"keys.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
        service = build("sheets", "v4", credentials=credentials)

        # Convert DataFrame to values list
        values_list = df.values.tolist()

        # Write data to the Google Sheets spreadsheet
        body = {"values": values_list}
        request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name, valueInputOption="RAW", body=body)
        response = request.execute()
        if response:
            return True
        else:
            return False
    except Exception as e:
        print(f'Error occured in read_excel_replace_sheet')
        return False




def sort_by_date(df):
    if 'upcoming_launch' in df.columns:
        df['upcoming_launch'] = pd.to_datetime(df['upcoming_launch'], errors='coerce')
        df = df.dropna(subset=['upcoming_launch'])  # Drop rows with invalid dates
        df = df.sort_values(by='upcoming_launch', ascending=True)  # Sort DataFrame by dates
        
        # Format dates as 'day month year'
        df['upcoming_launch'] = df['upcoming_launch'].apply(lambda x: x.strftime('%d %B %Y'))
        
        df.to_excel('sortedtokens.xlsx', index=False)  # Write sorted DataFrame to Excel
    return df
def write_to_excel(data):
    filename = f'cryptotokens.xlsx' 
    new_row = pd.DataFrame([data])

    if os.path.isfile(filename):
        df = pd.read_excel(filename)
        if 'token' in df.columns:
            # Check for duplicates based on job_title
            if data['token'] in df['token'].values:
                duplicate_index = df.index[df['token'] == data['token']].tolist()
                df.loc[duplicate_index[0]] = new_row.iloc[0]
                sorted_df=sort_by_date(df)
                sorted_df.to_excel(filename, index=False)  # Save updated DataFrame to Excel
                return
        updated_df = pd.concat([df, new_row], ignore_index=True)
        sorted_df=sort_by_date(updated_df)

        sorted_df.to_excel(filename, index=False)
        read_excel_and_replace_sheet( )


    else:
        # Write DataFrame to Excel
        new_row.to_excel(filename, index=False)
        read_excel_and_replace_sheet( )



