from flask import Flask
from src.controllers.http.ConceptOrderController import graph_controller

app = Flask(__name__)
app.register_blueprint(graph_controller)

if __name__ == "__main__":
    app.run(debug=True)
