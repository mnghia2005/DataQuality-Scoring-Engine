import os
from flask import Flask, render_template, request
from main import run_quality_engine

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def home(): 

    json_path = os.path.join(BASE_DIR, 'rules', 'dq_rules.json')
    report, score,dirty_df = run_quality_engine("company_data.db", json_path)
    report_html = report.to_html(classes="table table-bordered table-striped table-hover", index=False)
    
    dirty_dff=dirty_df.to_html(classes="table table-bordered table-striped table-hover", index=False)
    return render_template('index.html', table_data=report_html,table_dirty=dirty_dff, score=round(score, 2), nguoi_cham_diem="Nghĩa")
            
  
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)