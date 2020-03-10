#!/use/bin/env python
# coding: utf-8

from flask import Flask, request, jsonify
from flask import render_template
from flask import url_for
import requests
import work104
import webbrowser
import random

app = Flask(__name__, static_url_path='/static', static_folder='./static')
# url_for('static', filename='css/mystyle.css')
app.config['JSON_AS_ASCII'] = False

# Used to redirect
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/tmp_dev')
def tmp_dev():
    return render_template('tmp_dev.html')

@app.route('/css')
def css():
    return render_template('mystyle.html')

# Input "Keyword", "page", "save_sep" and "cache" 
@app.route('/index.html')
def index_html():
    with open(r'./work_dir/.title_count.txt', 'w') as f:
        f.write('0')
    return render_template('index.html',my_dict = '/mydict',
                                        synonym_dict = '/syndict',
                                        columns = '/col'
                          )

@app.route('/start_search', methods=['GET', 'POST'])
def start_search():
    if request.method == 'GET':
        with open(r'./work_dir/.file_status.txt', 'w') as f:
            f.write('0')
        kyword = request.args.get('keyword')
        pages = str(request.args.get('page'))
        cache = str(request.args.get('cache'))
        save_separately = str(request.args.get('sep')) # may be None or 1
        save_separately = '1' if save_separately == '1' else '0'
        save_separately_str = '是' if save_separately == '1' else '否'
        
        print(kyword, pages, cache, save_separately)
        
        # Need to put the 4 parameters to the template
        return render_template('start_search.html', kyword=kyword,
                                                    pages=pages,
                                                    cache=cache,
                                                    save_separately_str=save_separately_str,
                                                    save_separately=save_separately
                              )
    elif request.method == 'POST':
        kyword = request.form.get('keyword')
        pages = str(request.form.get('page'))
        cache = str(request.form.get('cache'))
        save_separately = str(request.form.get('sep'))
        save_separately_str = '是' if save_separately == '1' else '否'
        print('POST')
        print(kyword, pages, cache, save_separately)
        
        # Execute crawler process
        #work104.main()
        
        # modify conf file
        conf = """kyword=%s
pages=%s
save_separately=%s
cache=%s"""%(kyword, pages, save_separately, cache)
        
        with open(r'./config/conf.txt', 'w') as f:
            f.write(conf)
        
        return render_template('start_search_confirmed.html', 
                               kyword=kyword,                                                 
                               pages=pages,
                               cache=cache,
                               save_separately_str=save_separately_str,
                               save_separately=save_separately
                              )

@app.route('/processing')
def processing():
    title_amount = 0
    title_count = 0
    process_line = 0
    pct = 0
    file_status = '0'
    with open(r'./work_dir/.file_status.txt', 'r') as f:
        file_status = f.read().split('\n')[0]
    
    try:
        with open(r'./work_dir/.title_amount.txt', 'r') as f:
            title_amount = int(f.read().split('\n')[0])
        with open(r'./work_dir/.title_count.txt', 'r') as f:
            title_count = int(f.read().split('\n')[0])
        process_line = int((title_count / title_amount) * 10)
        pct = (title_count / title_amount) * 100
    except:
        process_line = 5
        pct = 50
    
    return render_template('processing.html',
                           file_status=file_status,
                           process_line=process_line,
                           process_line_t='▇',
                           pct='%.2f'%(pct)
                          )

@app.route('/execution')
def execution():
    return work104.main()

@app.route('/mydict')
def mydict():
    return render_template('mydict.html')

@app.route('/syndict')
def syndict():
    return render_template('syndict.html')

# show how the dataframe looks like
@app.route('/col', methods=['GET', 'POST'])
def col():
    col_file_path = './config/col.txt'
    default_col = ['Job_company', 'Job_opening', 'Job_content', 'Job_require', 'Job_welfare', 'Job_contact', 'URL']
    rdata1 = ['XX股份有限公司', '資料工程師', '工作內容', '工作需求', '公司福利', '聯絡方式', 'http://ex.ample1']
    rdata2 = ['XX有限公司', '資料科學家', '工作內容', '工作需求', '公司福利', '聯絡方式', 'http://ex.ample2']
    rdata3 = ['...' for i in range(0, len(rdata1))]
    columns = []
    if request.method == 'GET':
        with open(col_file_path, 'r') as f:
            line = f.readlines()
            columns = [r.replace('\n', '') for r in line if r.replace('\n', '') != '']

        skill_columns = columns
        rdata1 += [str(random.randint(0,1)) for i in range(0, len(columns))]
        rdata2 += [str(random.randint(0,1)) for i in range(0, len(columns))]
        rdata3 += ['...' for i in range(0, len(columns))]
        columns = default_col + columns
        columns_len = len(columns)

        return render_template('col.html',
                               skill_columns=skill_columns,
                               skill_columns_len=len(skill_columns),
                               columns_len=columns_len,
                               columns=columns,
                               rdata1=rdata1,
                               rdata2=rdata2,
                               rdata3=rdata3
                               )
    elif request.method == 'POST':
        # Get the modified columns data from user
        columns_data = [d for d in request.form.getlist('skills[]') if d != '']
        columns_data_str = ''
        for n, d in enumerate(columns_data):
            columns_data_str += d + ('\n' if n < len(columns_data) - 1 else '')
        # print(columns_data_str)
        # Save the new columns in col file
        with open(col_file_path, 'w') as f:
            f.write(columns_data_str)
        print('Columns file modified.')

        with open(col_file_path, 'r') as f:
            line = f.readlines()
            columns = [r.replace('\n', '') for r in line if r.replace('\n', '') != '']

        skill_columns = columns
        rdata1 += [str(random.randint(0, 1)) for i in range(0, len(columns))]
        rdata2 += [str(random.randint(0, 1)) for i in range(0, len(columns))]
        rdata3 += ['...' for i in range(0, len(columns))]
        columns = default_col + columns
        columns_len = len(columns)

        return render_template('col.html',
                               skill_columns=skill_columns,
                               skill_columns_len=len(skill_columns),
                               columns_len=columns_len,
                               columns=columns,
                               rdata1=rdata1,
                               rdata2=rdata2,
                               rdata3=rdata3
                               )

@app.route('/col_edit')
def col_edit():
    col_file_path = './config/col.txt'
    default_col = ['Job_company', 'Job_opening', 'Job_content', 'Job_require', 'Job_welfare', 'Job_contact', 'URL']
    rdata1 = ['XX股份有限公司', '資料工程師', '工作內容', '工作需求', '公司福利', '聯絡方式', 'http://ex.ample1']
    rdata2 = ['XX有限公司', '資料科學家', '工作內容', '工作需求', '公司福利', '聯絡方式', 'http://ex.ample2']
    rdata3 = ['...' for i in range(0, len(rdata1))]
    columns = []
    with open(col_file_path, 'r') as f:
        line = f.readlines()
        columns = [r.replace('\n', '') for r in line if r.replace('\n', '') != '']

    skill_columns = columns
    rdata1 += [str(random.randint(0,1)) for i in range(0, len(columns))]
    rdata2 += [str(random.randint(0,1)) for i in range(0, len(columns))]
    rdata3 += ['...' for i in range(0, len(columns))]
    columns = default_col + columns
    columns_len = len(columns)

    return render_template('col_edit.html',
                           skill_columns=skill_columns,
                           skill_columns_len=len(skill_columns),
                           columns_len=columns_len,
                           columns=columns,
                           rdata1=rdata1,
                           rdata2=rdata2,
                           rdata3=rdata3
                           )

@app.route('/col_confirm', methods=['GET'])
def col_confirm():
    column_data = request.args.getlist('newcol[]')
    print(column_data)

    default_col = ['Job_company', 'Job_opening', 'Job_content', 'Job_require', 'Job_welfare', 'Job_contact', 'URL']
    rdata1 = ['XX股份有限公司', '資料工程師', '工作內容', '工作需求', '公司福利', '聯絡方式', 'http://ex.ample1']
    rdata2 = ['XX有限公司', '資料科學家', '工作內容', '工作需求', '公司福利', '聯絡方式', 'http://ex.ample2']
    rdata3 = ['...' for i in range(0, len(rdata1))]
    columns = [d for d in column_data if d != '']

    skill_columns = columns
    rdata1 += [str(random.randint(0, 1)) for i in range(0, len(columns))]
    rdata2 += [str(random.randint(0, 1)) for i in range(0, len(columns))]
    rdata3 += ['...' for i in range(0, len(columns))]
    columns = default_col + columns
    columns_len = len(columns)

    return render_template('col_confirm.html',
                           skill_columns=skill_columns,
                           skill_columns_len=len(skill_columns),
                           columns_len=columns_len,
                           columns=columns,
                           rdata1=rdata1,
                           rdata2=rdata2,
                           rdata3=rdata3
                           )

if __name__ == '__main__':
    webbrowser.open('http://localhost:5001/test')
    app.run(debug=True, host='0.0.0.0', port=5001)