from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-bot', methods=['POST'])
def run_bot():
    try:
        # Call the Python script (bot.py)
        result = subprocess.run(['python', 'bot.py'], capture_output=True, text=True)
        return jsonify({'message': 'Bot executed successfully!', 'output': result.stdout})
    except Exception as e:
        return jsonify({'message': 'Error executing bot.', 'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)