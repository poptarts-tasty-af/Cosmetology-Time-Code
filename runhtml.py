import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

GITHUB_RAW_URL = 'https://raw.githubusercontent.com/poptarts-tasty-af/Student-Cosmo-Logs/main/Student_Logs/master_log.json'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_api_data():
    try:
        response = requests.get(GITHUB_RAW_URL)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Could not fetch data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
