import asyncio
import logging
import json
from flask import Flask, request
from github_handler import handle

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route('/')
def hello_world():
    return """Hello, World! We're live."""

@app.route('/eventstream', methods=['GET', 'POST'])
def eventstream():
    content = request.get_json()    
    asyncio.run(handle(content))
    
    return "OK"