import os
from flask import Flask, render_template, jsonify, request
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import json
import requests

app = Flask(__name__)

if os.getenv("LOCAL_ENVIRONMENT", "False") == "True":
    COUCHDB_URL = "http://localhost:5984"
else:
    COUCHDB_URL = os.getenv('COUCHDB_URL')

COUCHDB_DB_NAME = os.getenv("COUCHDB_DB_NAME")
COUCHDB_DESIGN_DOC = os.getenv("COUCHDB_DESIGN_DOC")
COUCHDB_CPU_VIEW = os.getenv("COUCHDB_CPU_VIEW")
COUCHDB_GPU_VIEW = os.getenv("COUCHDB_GPU_VIEW")
COUCHDB_MEMORY_VIEW = os.getenv("COUCHDB_MEMORY_VIEW")
COUCHDB_STORAGE_VIEW = os.getenv("COUCHDB_STORAGE_VIEW")


def fetch(url):
    return requests.get(
        auth=HTTPBasicAuth(username=os.getenv('COUCHDB_USER'), password=os.getenv('COUCHDB_PASSWORD')),
        url=url,
        headers={'Content-type': 'application/json'}
    )


def convert_to_chart_data_format(db_rows):

    if len(db_rows) > 0:

        # Creating a DataFrame from the array of dictionaries
        df = pd.DataFrame(db_rows)

        # Expand the 'key' list into separate columns
        df[['date', 'group']] = pd.DataFrame(df['key'].tolist(), index=df.index)

        # Calculate 'value' as the sum divided by the count
        df['average'] = df.apply(lambda row: row['value']['sum'] / row['value']['count'], axis=1)

        df['average'] = df['average'].round(2)

        # Drop the original 'key' and 'value' columns as they are no longer needed
        df.drop(['key', 'value'], axis=1, inplace=True)

        df.rename(columns={"average": "value"}, inplace=True)

        df["date"] = df["date"] + "T23:59:59Z"

        # Reorder the columns to match the desired output format
        final_df = df[['group', 'date', 'value']]

        # Data in the required format
        chart_data = final_df.to_dict(orient='records')

        return chart_data

    else:

        return {
            "group": "",
            "date": "",
            "value": ""
        }


@app.route(rule='/', methods=['GET'])
@app.route(rule='/search', methods=['GET'])
def index():

    path = request.path

    if request.path == "/search":
        # Access GET parameters using request.args
        q_from = request.args.get('from')
        q_to = request.args.get('to')

        if q_from and q_to is not None:
            end_date = q_to + "T23:59:59Z"
            start_date = q_from
    else:
        end_date = (datetime.now()).strftime("%Y-%m-%d") + "T23:59:59Z"
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")  # 30 days ago

    # DB URLs to retrieve the average utilization from the last 30 days
    urls = [
        f'{COUCHDB_URL}/{COUCHDB_DB_NAME}/_design/{COUCHDB_DESIGN_DOC}/_view/{COUCHDB_CPU_VIEW}?startkey=["{start_date}"]&endkey=["{end_date}"]&inclusive_end=true&group_level=2',
        f'{COUCHDB_URL}/{COUCHDB_DB_NAME}/_design/{COUCHDB_DESIGN_DOC}/_view/{COUCHDB_GPU_VIEW}?startkey=["{start_date}"]&endkey=["{end_date}"]&inclusive_end=true&group_level=2',
        f'{COUCHDB_URL}/{COUCHDB_DB_NAME}/_design/{COUCHDB_DESIGN_DOC}/_view/{COUCHDB_MEMORY_VIEW}?startkey=["{start_date}"]&endkey=["{end_date}"]&inclusive_end=true&group_level=2',
        f'{COUCHDB_URL}/{COUCHDB_DB_NAME}/_design/{COUCHDB_DESIGN_DOC}/_view/{COUCHDB_STORAGE_VIEW}?startkey=["{start_date}"]&endkey=["{end_date}"]&inclusive_end=true&group_level=2',
    ]

    # Use ThreadPoolExecutor to make requests in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Map the function 'fetch' onto the urls and execute them concurrently
        responses = list(executor.map(fetch, urls))

    cpu_response = responses[0].json()
    gpu_response = responses[1].json()
    memory_response = responses[2].json()
    storage_response = responses[3].json()

    cpu_chart_data = convert_to_chart_data_format(cpu_response['rows'] if 'rows' in cpu_response else [])
    gpu_chart_data = convert_to_chart_data_format(gpu_response['rows'] if 'rows' in gpu_response else [])
    memory_chart_data = convert_to_chart_data_format(memory_response['rows'] if 'rows' in memory_response else [])
    storage_chart_data = convert_to_chart_data_format(storage_response['rows'] if 'rows' in storage_response else [])

    return render_template(
        template_name_or_list='index.html',
        chart_data={'cpu_chart_data': cpu_chart_data,
                    'gpu_chart_data': gpu_chart_data,
                    'memory_chart_data': memory_chart_data,
                    'storage_chart_data': storage_chart_data
                    },
        start_date=datetime.strptime(start_date, '%Y-%m-%d'),
        end_date=datetime.strptime(end_date.split("T")[0], '%Y-%m-%d')
    )


if __name__ == '__main__':
    if os.getenv("LOCAL_ENVIRONMENT", "False") == "True":
        app.run(debug=True)
