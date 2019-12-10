from flask import Flask, render_template, jsonify, request
from controller import Controller
application = Flask(__name__)
 
@application.route("/")
def index():
    isBuild = request.args.get('build')
    if (isBuild != None and isBuild == True):
        ctrl = Controller()
        ctrl.build_structure()
    return render_template('index.html')

@application.route("/suggestions")
def get_suggestions():
    ctrl = Controller()
    query = request.args.get("term")
    suggestions = ctrl.get_suggestions(query)
    result = []
    i = 1
    for suggestion in suggestions:
        result.append({'id': i, 'label': suggestion, 'value': suggestion})
        i += 1  
    return jsonify({"result": result})

@application.route("/search", methods=['POST'])
def search():
    ctrl = Controller()    
    query = request.form.get("query")
    result = ctrl.search(query)
    return jsonify({"result": result})
 
@application.route("/doc")
def get_document():
    ctrl = Controller()
    return jsonify({"result": ctrl.get_document(request.args.get("docId"))})

if __name__ == "__main__":
    application.run(host='0.0.0.0')