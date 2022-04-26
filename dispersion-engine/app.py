# Webserver
from flask import Flask, jsonify, request, render_template, send_from_directory
import warnings, os, json
from dfs import dfs_steps, test

warnings.filterwarnings("ignore", category=UserWarning)

# http://localhost:5000
HOST = '0.0.0.0'
PORT = 5000

app = Flask(__name__, template_folder='templates')

# Web Server home page
@app.route("/")
def index():
    return render_template("index.html")

# Fav icon
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# DFS
@app.route("/api/dfs", methods=['POST'])
def runBFS():
    parameters = request.get_json()
    json_graph = parameters['graph']
    json_robotGroup = parameters['robotGroup']
    start = parameters['start']
    robotSize = parameters['robotSize']

    graph = {}
    for key in json_graph:
        graph[key] = json_graph[key]

    step = dfs_steps(json_graph, json_robotGroup, start, robotSize)
    
    if step == (None,None):
        return jsonify()
    else:
        graph = json.loads(step[1].jsonify())
        robotGroup = json.loads(step[0].jsonify())
        graph.update(robotGroup)
        return json.dumps(graph)



#Test

@app.route("/api/test", methods=['POST'])
def runTest():
    parameters = request.get_json()
    json_graph = parameters['graph']
    start = parameters['start']
    robotGroup = parameters['robotGroup']
    robotSize = parameters['robotSize']
    graphType = parameters['graphType']

    graph = {}
    for key in json_graph:
        graph[key] = json_graph[key]

    step = test(json_graph, start, robotGroup, robotSize, graphType)
    return jsonify(step)

if __name__ == '__main__':
    app.run(host=HOST,debug=True,port=PORT)