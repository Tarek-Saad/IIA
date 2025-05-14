# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Neo4j configuration with environment variable fallbacks
NEO4J_URI = os.environ.get("NEO4J_URI", "neo4j+s://4d1755c6.databases.neo4j.io")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "hk5V6qc2C-MhV8K7Eo05QWxD5nDUmk_R6qLAs_PoUqg")

# PostgreSQL configuration with environment variable fallback
POSTGRESS_URI = os.environ.get("POSTGRESS_URI", "postgresql://learningPath_owner:npg_wxF56SGTMWbC@ep-patient-lake-a8rcnxyp-pooler.eastus2.azure.neon.tech/learningPath?sslmode=require")
