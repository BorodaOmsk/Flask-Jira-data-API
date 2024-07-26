import requests
import pandas as pd
import urllib3
from flask import Flask, render_template,request,redirect,flash
import logging

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config.from_object('config.DevelopmentConfig')

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route('/')
def home():
    return render_template('index.html', title="Jira data")

@app.route("/customFields")
def customfield():

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.get(app.config['JIRA_URL'] + "/field", auth=(app.config['JIRA_USERS'], app.config['JIRA_PASSWORD']), verify=False)

    json_data = response.json()

    customFields_data =  pd.json_normalize(json_data) # Нормализуйте полуструктурированные данные JSON в плоскую таблицу.

    customFields_column_data = customFields_data[['name', 'schema.custom', 'schema.type']][customFields_data['custom'] == True]  # выбираем нужные нам колонки, при условии поле custom = True

    customFields_column_data['schema.custom'] = customFields_column_data['schema.custom'].str.replace(r'.*:', '', regex=True)  # убираем regexp лишние в поле schema.custom = com.atlassian.jira.plugin.system.customfieldtypes:

    customFields_result_data = customFields_column_data.to_html(table_id="table", index=False, bold_rows = True)


    html_customfield = f"""
        <html>
        <head>        
         <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
        </head>
        <header>
            <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
        </header>
        <body>
         <a href="http://127.0.0.1:5000/"> Home </a>
         <a href="http://127.0.0.1:5000/issueType"> Issue Type </a>       
         <a href="http://127.0.0.1:5000/statuses"> Statuses </a>
         <h1>Custom fields (пользовательские поля)</h1>
       
            
        {customFields_result_data}

        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
        <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready( function () {{
                $('#table').DataTable({{
                    // paging: false,
                   //  scrollY: 400,
                }});
            }});
        </script>
        </body>
        </html>
        """
    return html_customfield

@app.route("/issueType")
def issuetype():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    issuetype_data = requests.get(app.config['JIRA_URL'] + "/issuetype", auth=(app.config['JIRA_USERS'], app.config['JIRA_PASSWORD']), verify=False)

    json_data_issuetype = issuetype_data.json()

    result_data_issuetype = pd.json_normalize(json_data_issuetype)  # Нормализуйте полуструктурированные данные JSON в плоскую таблицу.

    result_column_issuetype = result_data_issuetype[['name', 'subtask']]  # выбираем нужные нам колонки, при условии поле custom = True

    result_column_issuetype['subtask'] = result_column_issuetype['subtask'].replace(True, 'sub-task').replace(False, 'standard')

    issuetype_result_data = result_column_issuetype.to_html(table_id="table2", index=False, bold_rows=True)

    html_issuetype = f"""
        <html>
        <head>        
         <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
        </head>
        <header>
            <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
        </header>
        <body>
         <a href="http://127.0.0.1:5000/"> Home </a>         
         <a href="http://127.0.0.1:5000/customFields"> Custom fields </a>         
         <a href="http://127.0.0.1:5000/statuses"> Statuses </a>
         
         <h1>Issue Type (Типы Issues)</h1>

        {issuetype_result_data}

        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
        <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready( function () {{
                $('#table2').DataTable({{
                    // paging: false,
                   //  scrollY: 400,
                }});
            }});
        </script>
        </body>
        </html>
        """
    return html_issuetype

@app.route("/statuses")
def statuses():
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        statuses_data = requests.get(app.config['JIRA_URL'] + "/status", auth=(app.config['JIRA_USERS'], app.config['JIRA_PASSWORD']), verify=False)

        json_data_statuses_data = statuses_data.json()

        result_data_statuses = pd.json_normalize(json_data_statuses_data)  # Нормализуйте полуструктурированные данные JSON в плоскую таблицу.

        result_data_column_statuses = result_data_statuses[['name', 'statusCategory.name']]  # выбираем нужные нам колонки

        statuses_result_data = result_data_column_statuses.to_html(table_id="table3", index=False, bold_rows=True)

        html_statuses = f"""
                <html>
                <head>        
                 <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
                </head>
                <header>
                    <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
                </header>
                <body>
                 <a href="http://127.0.0.1:5000/"> Home </a>

                 <a href="http://127.0.0.1:5000/customFields"> Custom fields </a>
                 
                 <a href="http://127.0.0.1:5000/issueType"> Issue Type </a>

                 <h1>Statuses (Статусы)</h1>

                {statuses_result_data}

                <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
                <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
                <script>
                    $(document).ready( function () {{
                        $('#table3').DataTable({{
                            // paging: false,
                           //  scrollY: 400,
                        }});
                    }});
                </script>
                </body>
                </html>
                """
        return html_statuses

app.logger.debug("Debug log level")
app.logger.info('Info level log')
app.logger.warning('Warning level log')
app.logger.error("Error!")
app.logger.critical("Program halt!")


if __name__ == '__main__':
    app.run()
