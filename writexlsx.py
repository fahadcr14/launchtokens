
import pandas as pd 
import os
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
                df.to_excel(filename, index=False)  # Save updated DataFrame to Excel
                return
        updated_df = pd.concat([df, new_row], ignore_index=True)
        updated_df.to_excel(filename, index=False)

    else:
        # Write DataFrame to Excel
        new_row.to_excel(filename, index=False)


