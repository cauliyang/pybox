"""Test suite for the pybox package."""


class MockResponse:
    """Mock response object for testing"""

    def __init__(self, json_data, status_code):
        """Initialize the mock response object"""
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """Return the json data"""
        return self.json_data
