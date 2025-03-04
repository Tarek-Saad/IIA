from flask import Flask
from src.controllers.http.ConceptOrderController import graph_controller
from src.controllers.http.GetLOsController import LO_controller
from src.controllers.http.random_losController import concept_controller

app = Flask(__name__)
app.register_blueprint(concept_controller)

if __name__ == "__main__":
    app.run(debug=True)
