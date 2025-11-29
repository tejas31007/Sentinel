from flask import Flask, jsonify, render_template
from collections import Counter
import os

app = Flask(__name__)

# Path to the log file your C++ Sentinel creates
LOG_FILE = "dashboard_data.txt"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    try:
        if not os.path.exists(LOG_FILE):
            return jsonify({"status": "no_data", "data": {}})

        # Read the file
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()

        # Count attacks per IP
        ips = [line.strip() for line in lines if line.strip()]
        counts = Counter(ips)
        
        # Sort by most frequent attackers (Top 10)
        top_attackers = dict(counts.most_common(10))

        return jsonify(top_attackers)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    # Run on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)