# GraphDB.py
from neo4j import GraphDatabase
from src.config.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

class GraphDB:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

    def get_session(self):
        return self.driver.session()

    def close(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        self.driver.close()

    def test_connection(self):
        """اختبار الاتصال بقاعدة البيانات"""
        with self.get_session() as session:
            result = session.run("RETURN 1 AS test")
            if result.single():
                print("Connection is working!")
            else:
                print("Connection failed!")

# استخدام الكود لاختبار الاتصال
graph_db = GraphDB()
graph_db.test_connection()
