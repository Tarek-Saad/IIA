# test_get_lo_service.py

import pytest
from unittest.mock import MagicMock
from src.core.services.GetLOsService import GetLOService


@pytest.fixture
def mock_graph_service():
    # Mocking the GraphDB instance
    mock_graph_db = MagicMock()
    # Mocking the session and the result of the Cypher query
    mock_session = MagicMock()
    mock_graph_db.get_session.return_value.__enter__.return_value = mock_session

    # Sample response that would be returned from Neo4j query
    mock_session.run.return_value = [
        {"lo": "LO1"},
        {"lo": "LO2"},
        {"lo": "LO3"}
    ]

    # Instantiating the GetLOService with the mocked GraphDB
    lo_service = GetLOService()
    lo_service.graph_db = mock_graph_db  # Injecting the mock object
    return lo_service


def test_get_los_for_concept(mock_graph_service):
    # Concept name to be tested
    concept_name = "Data Structures"

    # Call the method to test
    los = mock_graph_service.get_los_related_to_concept(concept_name)

    # Assert that the LOs are returned correctly
    assert len(los) == 3  # We expect 3 LOs to be returned
    assert "LO1" in los
    assert "LO2" in los
    assert "LO3" in los
