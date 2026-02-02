import sys
import os
import json
import asyncio
from typing import Dict, Any

# Add CollaborationHub to path
sys.path.append(r"C:\Corporate\CollaborationHub")

IMPORT_ERROR = None

try:
    from src.AgentCitizens.guardian_service import get_guardian_service
    from src.Services.Governance.governance_service import GovernanceService
    from src.KnowledgeMesh.graph_syncer import GraphSyncer
    GADOS_AVAILABLE = True
except ImportError as e:
    GADOS_AVAILABLE = False
    IMPORT_ERROR = str(e)

async def scan(url: str, content: str) -> Dict[str, Any]:
    if not GADOS_AVAILABLE:
        # Fallback to local heuristic if GADOS is offline/unreachable
        return {
            "status": "warning", 
            "threatLevel": "medium", 
            "score": 60,
            "message": f"GADOS Core Unreachable. Active Defense running locally. Error: {IMPORT_ERROR}",
            "timestamp": "Now"
        }

    # Mock Dependencies for connecting to existing GADOS Service
    # In a real scenario, we might connect to the running service via RPC
    # Here we instantiate a fresh service for the "Check"
    # Assuming stateless evaluation for the "Evaluator" part
    
    # Mocking dependencies if they require real DB connections that might fail
    class MockGraphSyncer:
        pass
        
    class MockGovernanceService:
        pass

    try:
        # Try to use the factory
        # We might need to mock the inputs if the real ones fail to init
        # For now, we assume we can instantiate or we patch
        
        # Instantiate directly to avoid heavy dependency chain if possible
        # Or Just use the Evaluator directly?
        from src.AgentCitizens.guardian_service import GuardianEvaluator
        evaluator = GuardianEvaluator()
        
        # Create a "Change Context" from the URL/Content
        # We treat visiting a URL as "Ingesting Content"
        context = {
            "agent": "Aegis-Browser-User",
            "diff": content, # Evaluate the content of the page
            "files_changed": [url],
            "change_type": "BROWSER_NAVIGATION"
        }
        
        scores = evaluator.evaluate(context)
        overall = scores.get("overall", 0.0)
        
        # Determine Verdict
        if overall >= 0.7:
             status = "secure"
             level = "low"
        elif overall >= 0.5:
             status = "warning"
             level = "medium"
        else:
             status = "danger"
             level = "high"
             
        return {
            "status": status,
            "threatLevel": level,
            "score": int(overall * 100),
            "breakdown": scores,
            "timestamp": "Now"
        }

    except Exception as e:
        return {
            "status": "error",
            "threatLevel": "high",
            "score": 0,
            "message": f"Guardian Execution Failed: {str(e)}",
            "timestamp": "Now"
        }

if __name__ == "__main__":
    # Expect JSON input from stdin or args
    # Usage: python guardian_bridge.py <URL> <Content>
    # Or just stdin
    
    target_url = sys.argv[1] if len(sys.argv) > 1 else "about:blank"
    # Basic simulation of content fetch if not provided (Electron should provide it)
    target_content = sys.argv[2] if len(sys.argv) > 2 else "<html><body>Safe Content</body></html>"
    
    result = asyncio.run(scan(target_url, target_content))
    print(json.dumps(result))
