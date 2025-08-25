import pandas as pd 


df = pd.read_csv(
    r'D:\data-analyst_roadmap\Porjects\Retail-Sales-Analysis\data\Superstore.csv',
    encoding='latin1'  # or 'ISO-8859-1'
)

df['Order Date']=pd.to_datetime(df['Order Date'], format ='%m/%d/%Y')
df['Ship Date']=pd.to_datetime(df['Ship Date'], format ='%m/%d/%Y')


df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Quantity']= pd.to_numeric(df['Quantity'] , errors='coerce')
df['Discount'] =pd.to_numeric(df['Discount'] , errors='coerce')
df['Profit'] = pd.to_numeric(df['Profit'], errors= 'coerce')

df.to_csv(
    r'D:\data-analyst_roadmap\Porjects\Retail-Sales-Analysis\data\Superstore_clean.csv',
    index=False
)

print("Clean CSV ready for MySQL import!")