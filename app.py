import os
import traceback
from flask import Flask, jsonify
from flask_cors import CORS
from src.controllers.http.ConceptOrderController import graph_controller
from src.controllers.http.GetLOsController import LO_controller
from src.controllers.http.random_losController import concept_controller
from src.controllers.http.SelectionController import selection_controller
from src.controllers.http.LOChildFetcherController import lo_child_controller
from src.controllers.http.generate_learning_analysisController import learning_analysis_controller

# Run startup script for Vercel
if os.environ.get("VERCEL") == "1":
    try:
        import vercel_startup
        vercel_startup.check_environment()
    except Exception as e:
        print(f"Error running startup script: {str(e)}")

app = Flask(__name__)


# Enable CORS for all routes with specific origins
# Enable CORS for all routes
def cors_origin_allowed(origin):
    # Allow localhost and development URLs
    if origin and (origin.startswith('http://localhost:') or 
                  origin.startswith('http://192.168.') or
                  origin.startswith('http://10.0.') or
                  'codengo' in origin or
                  'vercel.app' in origin):
        return True
    return False




# Register all Blueprints with unique names to avoid conflicts
app.register_blueprint(graph_controller, url_prefix='/graph', name='graph_blueprint')  # For concept order related routes
app.register_blueprint(LO_controller, url_prefix='/learning-objects', name='lo_blueprint')  # For learning object related routes
app.register_blueprint(concept_controller, url_prefix='/random-lo', name='concept_blueprint')  # For random learning object related routes
app.register_blueprint(selection_controller, url_prefix="/api")  # For selection
app.register_blueprint(lo_child_controller, url_prefix="/fetch")  # For getting sub LOs children
app.register_blueprint(learning_analysis_controller, url_prefix='/learning-analysis')  # To get the inputs of the algorithms (knowledgebase & goal)

# Global error handler
@app.errorhandler(Exception)
def handle_error(e):
    print(f"Error: {str(e)}")
    print(traceback.format_exc())
    return jsonify({
        "error": str(e),
        "type": type(e).__name__,
        "traceback": traceback.format_exc()
    }), 500

# Default GET route for the root URL
@app.route('/')
def home():
    # Test database connections
    try:
        from src.core.repositories.GraphDB import GraphDB
        db = GraphDB()
        db_status = "Connected" if db.test_connection() else "Failed"
    except Exception as e:
        db_status = f"Error: {str(e)}"
    
    # Get environment info
    env_info = {
        "FLASK_ENV": os.environ.get("FLASK_ENV", "development"),
        "DATABASE": db_status,
        "PYTHON_VERSION": os.environ.get("PYTHONVERSION", "unknown"),
        "VERCEL": os.environ.get("VERCEL", "0")
    }
    
    return jsonify({
        "message": "Welcome to the Learning Object API! Navigate to specific endpoints for further actions.",
        "status": "online",
        "environment": env_info
    })


if __name__ == "__main__":
    app.run(debug=True)
