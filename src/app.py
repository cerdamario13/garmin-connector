from flask import Flask, request, jsonify
from flask_cors import CORS
import activities

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def hello_world():
    return "Hello World!"

@app.route('/allRuns', methods=['GET'])
def get_all_runs():
    """
    Get the data for all runs
    """
    results = activities.all_runs()

    return jsonify(results)

@app.route('/runSummaries', methods=['GET'])
def get_run_summaries():
    """
    Get summaries for all runs

    total_distance
    total_calories
    total_time
    average_distance_per_activity
    average_calories_per_activity
    average_heart_rate_per_activity
    """

    results = activities.all_runs_summaries()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=False)


