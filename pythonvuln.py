# vulnerable_app.py

from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/execute/<command>')
def execute_command(command):
    """Vulnerable endpoint that executes shell commands."""
    try:
        # INSECURE: Directly using user input in subprocess.
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return f"Command executed successfully:\n{result}"
    except subprocess.CalledProcessError as e:
        return f"Error executing command:\n{e.output}", 500
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500

@app.route('/file/<filename>')
def read_file(filename):
    """Vulnerable endpoint that reads files."""
    try:
        # INSECURE: Path traversal vulnerability.
        filepath = os.path.join("/", filename) #This is bad.
        with open(filepath, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/sqli')
def sql_injection():
    """Simulated SQL Injection vulnerability."""
    user_id = request.args.get('id')
    if user_id:
        # INSECURE: Vulnerable to SQL injection (simulated).
        # In a real application, this would be a database query.
        result = f"Simulated query: SELECT * FROM users WHERE id = {user_id}"
        return result
    else:
        return "Please provide an 'id' parameter."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)