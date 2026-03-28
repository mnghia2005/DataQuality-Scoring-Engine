import pandas as pd
import json
import sqlite3


def run_quality_engine(db_path,rules_path):
    conn=sqlite3.connect(db_path)
    query="select * from customers"
    df=pd.read_sql(query,conn)
    conn.close()
    with open(rules_path,"r",encoding="utf-8") as f:
        config=json.load(f)

    rules=config["rules"]
    total_rows=len(df)
    print(f"Có{total_rows} dòng dữ liệu và {len(rules)} luật kiểm tra.\n")

    
    report_list = []
    total_weight = 0
    total_weighted_score = 0
    df['Error_Details'] = ""
    

    for rule in rules:
        rule_id=rule["rule_id"]
        col=rule["column"]
        rule_type=rule["type"]
        weight=rule.get("weight",1.0)

        passed=0
        error_msg=""

        if rule_type=="not_null":
            valid_df=df[df[col].notna()]
            passed=len(valid_df)
            error_msg = f"Thiếu {col}; "
            invalid_mask=df[col].isna()

        if rule_type=="range":
            valid_df = df[df[col].notna()]
            valid_df=valid_df[(valid_df[col]>=rule["min"]) & (valid_df[col]<=rule["max"])]
            passed=len(valid_df)
            error_msg = f"{col} ngoài khoảng {rule['min']}-{rule['max']}; "
            invalid_mask=df[col].isna() | (df[col]<rule["min"]) | (df[col]>rule["max"])

        if rule_type=="regex":
            valid_df = df[df[col].notna()]
            valid_df=valid_df[valid_df[col].astype(str).str.match(rule["pattern"])]
            passed=len(valid_df)
            error_msg = f"{col} sai định dạng; "
            invalid_mask=df[col].isna() | ~df[col].astype(str).str.match(rule["pattern"])

        df.loc[invalid_mask, 'Error_Details'] += error_msg

        rule_score = (passed / total_rows) * 100
        total_weighted_score += rule_score * weight
        total_weight += weight

        report_list.append({
                "Mã Luật": rule_id,
                "Cột Kiểm Tra": col,
                "Tiêu chí": rule_type.upper(),
                "Dòng Đạt": f"{passed}/{total_rows}",
                "Điểm Số (%)": round(rule_score, 2)
            })
        
    dirty_df = df[df['Error_Details'] != ""].copy()
    dirty_df=pd.DataFrame(dirty_df)
    report_df = pd.DataFrame(report_list)
    final_score = total_weighted_score / total_weight
    
    return report_df, final_score,dirty_df

