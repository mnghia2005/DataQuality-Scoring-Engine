import pandas as pd
import urllib
from sqlalchemy import create_engine, types


server = r'DESKTOP-EMDJA3J\CSDLTTCS'
database = 'DataQualityDB'


driver = '{ODBC Driver 17 for SQL Server}' 

params = urllib.parse.quote_plus(
    f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


try:
    df = pd.read_csv('dirty_customer_data.csv')
    dinh_dang_cot = {
        'Full_Name': types.NVARCHAR(length=255), 
        'Email': types.VARCHAR(length=255),      
        'Phone': types.VARCHAR(length=20),         
    }
    
    df.to_sql(
        name='customers', 
        con=engine, 
        if_exists='replace', 
        index=False, 
        dtype=dinh_dang_cot 
    )
    print("Nạp 1000 dòng thành công ")
except Exception as e:
    print(f"Đây là lỗi: {e}")