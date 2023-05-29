from flask import Flask, request, jsonify
import activities

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
    return "Hello World!"

@app.route('/allRuns', methods=['POST'])
def get_all_runs():
    """
    Get the data for all runs
    """
    results = activities.all_runs()

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=False)


