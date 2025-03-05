from flask import Flask
from src.controllers.http.ConceptOrderController import graph_controller
from src.controllers.http.GetLOsController import LO_controller
from src.controllers.http.random_losController import concept_controller

app = Flask(__name__)

# Register all Blueprints
app.register_blueprint(graph_controller)  # For concept order related routes
app.register_blueprint(LO_controller)  # For learning object related routes
app.register_blueprint(concept_controller)  # For random learning object related routes

if __name__ == "__main__":
    app.run(debug=True)
