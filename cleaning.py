import pandas as pd


df = pd.read_csv('C:\\Users\\PANKAJ SHARMA\\Downloads\\CSV_files\\startup_funding\\startup_funding.csv')

# data cleaning(Preprocessing)
df['Investors Name'] = df['Investors Name'].fillna('Undisclosed')
df.drop(columns=['Remarks'], inplace=True)
df.set_index('Sr No', inplace=True)
df.rename(columns={
    'Date dd/mm/yyyy': 'date',
    'Startup Name': 'startup',
    'Industry Vertical': 'vertical',
    'SubVertical': 'subvertical',
    'City  Location': 'city',
    'Investors Name': 'investors',
    'InvestmentnType': 'round',
    'Amount in USD': 'amount'
}, inplace=True)
# In amount
df['amount'] = df['amount'].fillna('0')
df['amount'] = df['amount'].str.replace(',', '')
df['amount'] = df['amount'].str.replace('Undisclosed', '0')
df['amount'] = df['amount'].str.replace('Unknown', '0')
df['amount'] = df['amount'].str.replace('undisclosed', '0')
df = df[df['amount'].str.isdigit()]
df['amount'] = df['amount'].astype('float')


def to_inr(dollar):
    inr = dollar * 82.5
    return inr / 10000000


df['amount'] = df['amount'].apply(to_inr)
df['date'] = df['date'].str.replace('05/072018','05/07/2018')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df = df.dropna(subset=['date','startup','vertical','city','investors','round','amount'])

# df.to_csv('file_ka_new_name',index=False) to export files
