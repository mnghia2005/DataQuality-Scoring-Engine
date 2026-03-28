import pyodbc
import pandas as pd

def connect_to_sql_server():
    server = r'DESKTOP-EMDJA3J\CSDLTTCS' 
    #nhớ sửa lại theo tên máy,tên server cài trong sql server management studio
    database = 'DataQualityDB' 
    # tên database đã tạo trong sql server management studio 
    driver = '{ODBC Driver 17 for SQL Server}'
    #ODBC data source, xem có cái này k
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    
    try:
        conn = pyodbc.connect(conn_str)
        query = "SELECT * FROM customers"
        
        df = pd.read_sql(query, conn)
        conn.close()
        
        if 'Join_Date' in df.columns:
            df['Join_Date'] = pd.to_datetime(df['Join_Date'], errors='coerce')
        
        return df

    except Exception as e:
        print(f' Lỗi kết nối rồi=((: {e}')
        return None


