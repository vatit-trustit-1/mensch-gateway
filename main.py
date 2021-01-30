from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return """Hello, World! We're live."""

@app.route('/eventstream', methods=['GET', 'POST'])
def eventstream():
    content = request.get_json()
    print(content)
    return "OK"