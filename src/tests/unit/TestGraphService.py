import pytest
from unittest.mock import MagicMock
from src.core.services.GraphService import GraphService


# Mocking the GraphDB session
@pytest.fixture
def mock_graph_service():
    # Mocking the GraphDB instance
    mock_graph_db = MagicMock()
    # Mocking the session and the result of the Cypher query
    mock_session = MagicMock()
    mock_graph_db.get_session.return_value.__enter__.return_value = mock_session

    # Sample response that would be returned from Neo4j query
    mock_session.run.return_value = [
        {"prerequisite": "Algorithms"},
        {"prerequisite": "Searching Algorithms"},
    ]

    # Instantiating the GraphService with the mocked GraphDB
    graph_service = GraphService()
    graph_service.graph_db = mock_graph_db  # Injecting the mock object
    return graph_service


def test_get_relevant_concepts(mock_graph_service):
    # Input data for the test
    learning_goals = ["Searching"]
    knowledge_base = ["Introduction to Programming", "Variables"]

    # Call the method to test
    relevant_concepts = mock_graph_service.get_relevant_concepts(learning_goals, knowledge_base)

    # Assert that the expected concepts are in the result
    assert "Searching" in relevant_concepts
    assert "Algorithms" in relevant_concepts
    assert "Searching Algorithms" in relevant_concepts
    assert "Introduction to Programming" not in relevant_concepts
    assert "Variables" not in relevant_concepts

