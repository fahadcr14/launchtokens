
import pandas as pd 
import os

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

    else:
        # Write DataFrame to Excel
        new_row.to_excel(filename, index=False)


