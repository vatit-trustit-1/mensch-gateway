from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return """Hello, World! We're live."""

@app.route('/eventstream', methods=['GET', 'POST'])
def eventstream():
    content = request.get_json()    
    print(json.dumps(content, indent=4, sort_keys=True))
    return "OK"