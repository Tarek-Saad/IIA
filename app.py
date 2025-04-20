from flask import Flask
from flask_cors import CORS
from src.controllers.http.ConceptOrderController import graph_controller
from src.controllers.http.GetLOsController import LO_controller
from src.controllers.http.random_losController import concept_controller
from src.controllers.http.SelectionController import selection_controller
from src.controllers.http.LOChildFetcherController import lo_child_controller
from src.controllers.http.generate_learning_analysisController import learning_analysis_controller

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, 
    origins=["http://localhost:3000", "http://192.168.1.195:3000", "https://codengo-4hyo2vs7x-tarek-saads-projects.vercel.app", "*"],
    allow_credentials=True,
    supports_credentials=True,
    resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://192.168.1.195:3000", "https://codengo-4hyo2vs7x-tarek-saads-projects.vercel.app", "*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"]
        }
    }
)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"], "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

# Register all Blueprints with unique names to avoid conflicts
app.register_blueprint(graph_controller, url_prefix='/graph', name='graph_blueprint')  # For concept order related routes
app.register_blueprint(LO_controller, url_prefix='/learning-objects', name='lo_blueprint')  # For learning object related routes
app.register_blueprint(concept_controller, url_prefix='/random-lo', name='concept_blueprint')  # For random learning object related routes
app.register_blueprint(selection_controller, url_prefix="/api")  # For selection
app.register_blueprint(lo_child_controller, url_prefix="/fetch")  # For getting sub LOs children
app.register_blueprint(learning_analysis_controller, url_prefix='/learning-analysis')  # To get the inputs of the algorithms (knowledgebase & goal)

# Default GET route for the root URL
@app.route('/')
def home():
    return "Welcome to the Learning Object API! Navigate to specific endpoints for further actionss ."


if __name__ == "__main__":
    app.run(debug=True)
