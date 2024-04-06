import pandas as pd

def sort_by_date(df):
    if 'upcoming_launch' in df.columns:
        df['upcoming_launch'] = pd.to_datetime(df['upcoming_launch'], errors='coerce')
        df = df.dropna(subset=['upcoming_launch'])  # Drop rows with invalid dates
        df = df.sort_values(by='upcoming_launch', ascending=True)  # Sort DataFrame by dates
        
        # Format dates as 'day month year'
        df['upcoming_launch'] = df['upcoming_launch'].apply(lambda x: x.strftime('%d %B %Y'))
        
        df.to_excel('sortedtokens.xlsx', index=False)  # Write sorted DataFrame to Excel
    return df

df = pd.read_excel(r'cryptotokens.xlsx')
sort_by_date(df)
