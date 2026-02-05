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
    # PERSISTENT SENTINEL MODE
    # Reads JSON requests from Stdin forever.
    # Solves "Spawn Storm" by keeping one process alive.
    
    # sys.stdin is treated as a stream of newline-delimited JSON
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        try:
            req = json.loads(line)
            url = req.get("url", "about:blank")
            content = req.get("content", "")
            
            # Execute Scan
            result = asyncio.run(scan(url, content))
            
            # Write Response
            print(json.dumps(result))
            sys.stdout.flush() # CRITICAL: Ensure Electron gets the data immediately
            
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON Input"}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": f"Bridge Error: {str(e)}"}))
            sys.stdout.flush()
