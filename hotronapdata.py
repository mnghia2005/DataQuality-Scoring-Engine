import pandas as pd
import urllib
from sqlalchemy import create_engine


server = r'DESKTOP-EMDJA3J\CSDLTTCS'
database = 'DataQualityDB'


driver = '{ODBC Driver 17 for SQL Server}' 

params = urllib.parse.quote_plus(
    f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


try:
    df = pd.read_csv(ví dụ :'dirty_customer_data.csv')
    
    
    df.to_sql('customers', con=engine, if_exists='replace', index=False)
    print("Nạp 1000 dòng thành công mỹ mãn!")
except Exception as e:
    print(f"Đây là lỗi: {e}")