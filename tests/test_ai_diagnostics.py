import unittest
from unittest.mock import patch, Mock
import requests

from app.ai_diagnostics import get_ai_analysis


METRICS = {
    "cpu_percent": 20,
    "memory_percent": 40,
    "disk_percent": 30
}

STATUS = "HEALTHY"

EXPECTED_FALLBACK = {
    "summary": "AI analysis is temporarily unavailable. "
               "Current system status is HEALTHY.",
    "recommendation": "Check the system metrics and try again "
                      "when the AI service is available."
}


class TestAIDiagnostics(unittest.TestCase):

    @patch("app.ai_diagnostics.os.getenv", return_value="")
    def test_missing_api_key(self, mock_env):
        result = get_ai_analysis(METRICS, STATUS)
        self.assertEqual(result, EXPECTED_FALLBACK)

    @patch("app.ai_diagnostics.os.getenv", return_value="fake-key")
    @patch("app.ai_diagnostics.requests.post",
           side_effect=requests.exceptions.HTTPError)
    def test_invalid_api_key(self, mock_post, mock_env):
        result = get_ai_analysis(METRICS, STATUS)
        self.assertEqual(result, EXPECTED_FALLBACK)

    @patch("app.ai_diagnostics.os.getenv", return_value="fake-key")
    @patch("app.ai_diagnostics.requests.post",
           side_effect=requests.exceptions.Timeout)
    def test_api_timeout(self, mock_post, mock_env):
        result = get_ai_analysis(METRICS, STATUS)
        self.assertEqual(result, EXPECTED_FALLBACK)

    @patch("app.ai_diagnostics.os.getenv", return_value="fake-key")
    @patch("app.ai_diagnostics.requests.post")
    def test_invalid_ai_response(self, mock_post, mock_env):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [
                {"message": {"content": "invalid JSON"}}
            ]
        }
        mock_post.return_value = response

        result = get_ai_analysis(METRICS, STATUS)
        self.assertEqual(result, EXPECTED_FALLBACK)


if __name__ == "__main__":
    unittest.main()