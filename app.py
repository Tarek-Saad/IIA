from flask import Flask
from src.controllers.http.ConceptOrderController import graph_controller
from src.controllers.http.GetLOsController import LO_controller
from src.controllers.http.random_losController import concept_controller
from src.controllers.http.SelectionController import selection_controller
from src.controllers.http.LOChildFetcherController import lo_child_controller


app = Flask(__name__)

# Register all Blueprints with unique names to avoid conflicts
app.register_blueprint(graph_controller, url_prefix='/graph', name='graph_blueprint')  # For concept order related routes
app.register_blueprint(LO_controller, url_prefix='/learning-objects', name='lo_blueprint')  # For learning object related routes
app.register_blueprint(concept_controller, url_prefix='/random-lo', name='concept_blueprint')  # For random learning object related routes
app.register_blueprint(selection_controller, url_prefix="/api")
app.register_blueprint(lo_child_controller, url_prefix="/fetch")

if __name__ == "__main__":
    app.run(debug=True)
