import json
import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Add parent directory to path to import guardian_bridge
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock GADOS dependencies BEFORE importing the bridge
sys.modules["src.AgentCitizens.guardian_service"] = MagicMock()
sys.modules["src.Services.Governance.governance_service"] = MagicMock()
sys.modules["src.KnowledgeMesh.graph_syncer"] = MagicMock()

import guardian_bridge

def test_bridge_output_schema():
    """Verify bridge generates correct JSON schema"""
    url = "https://example.com"
    content = "<html>Safe</html>"
    
    # Run the scan function directly
    # We need to mock the internal behavior if GADOS_AVAILABLE is False or True
    # Let's force GADOS_AVAILABLE to False to test fallback first, 
    # then True with mocked Evaluator to test success path.
    
    # Test Fallback (GADOS Offline)
    guardian_bridge.GADOS_AVAILABLE = False
    result = guardian_bridge.asyncio.run(guardian_bridge.scan(url, content))
    
    assert "status" in result
    assert "threatLevel" in result
    assert "score" in result
    assert isinstance(result["score"], int)
    
def test_bridge_mocked_success():
    """Verify bridge handles successful GADOS response"""
    guardian_bridge.GADOS_AVAILABLE = True
    
    # Mock the Evaluator class inside the bridge
    with patch("src.AgentCitizens.guardian_service.GuardianEvaluator") as MockEvaluator:
        instance = MockEvaluator.return_value
        instance.evaluate.return_value = {
            "overall": 0.85,
            "security": 0.9,
            "privacy": 0.8
        }
        
        result = guardian_bridge.asyncio.run(guardian_bridge.scan("http://safe.com", "content"))
        
        assert result["status"] == "secure"
        assert result["score"] == 85
        assert result["breakdown"]["overall"] == 0.85

def test_bridge_input_sanitization():
    """Verify malformed inputs don't crash the bridge logic"""
    # In a real subprocess call, shell injection is the worry. 
    # Here we test the python logic handles weird strings.
    weird_url = "https://example.com/foo'; DROP TABLE;"
    
    guardian_bridge.GADOS_AVAILABLE = False
    result = guardian_bridge.asyncio.run(guardian_bridge.scan(weird_url, ""))
    assert result["status"] != "error" # Should handle gracefull as fallback
