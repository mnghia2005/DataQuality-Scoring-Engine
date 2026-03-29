import pyodbc
import pandas as pd

def connect_to_sql_server(server, database, driver):
    server = server
    #tên server cài trong sql server management studio
    database = database
    # tên database đã tạo trong sql server management studio 
    driver = driver
    #ODBC data source đã cài trên máy
    try:
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    
    except Exception as e:
        print(f'Lỗi tạo chuỗi kết nối: {e}')
        return None
    
    try:
        conn = pyodbc.connect(conn_str)
        
        conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-16le')
        conn.setdecoding(pyodbc.SQL_CHAR, encoding='latin1')
        conn.setencoding(encoding='utf-16le')

        query = "SELECT * FROM customers"
        
        df = pd.read_sql(query, conn)
        conn.close()
        
        if 'Join_Date' in df.columns:
            df['Join_Date'] = pd.to_datetime(df['Join_Date'], errors='coerce')
        
        return df

    except Exception as e:
        print(f' Lỗi kết nối rồi=((: {e}')
        return None


