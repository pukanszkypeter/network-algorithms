# Webserver
from flask import Flask, jsonify, request, render_template, send_from_directory
import warnings
import os

from dfs import dfs_steps

warnings.filterwarnings("ignore", category=UserWarning)

# http://localhost:5000
HOST = '0.0.0.0'
PORT = 5000

app = Flask(__name__, template_folder='templates')

# Web Server home page
@app.route("/")
def index():
    return render_template("index.html")


# DFS
@app.route("/api/dfs", methods=['POST'])
def runBFS():
    parameters = request.get_json()
    json_graph = parameters['graph']
    start = parameters['start']

    graph = {}
    for key in json_graph:
        graph[int(key)] = json_graph[key]

    steps = dfs_steps.step(json_graph, start)
    if steps == None:
        return jsonify([])
    else:
        return jsonify(steps)    

# Fav icon
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host=HOST,debug=True,port=PORT)