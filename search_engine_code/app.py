from flask import Flask, render_template, jsonify, request
from controller import Controller
application = Flask(__name__)
 
@application.route("/")
def hello():
    return render_template('index.html', form = {'v': 'test'})

@application.route("/search", methods=['POST'])
def search():
    ctrl = Controller()    
    query = request.form.get("query")
    result = ctrl.search(query)
    return jsonify({"result": result})

@application.route("/suggestions")
def get_suggestions():
    query = request.args.get("query")
    return query + ' test'
 
if __name__ == "__main__":
    application.run()