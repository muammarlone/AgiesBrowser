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

# PERSISTENT SENTINEL & ONE-SHOT HYBRID MODE
    # Logic: If args are present, run ONCE. If not, run DAEMON.
    
    if len(sys.argv) > 1:
        # --- MODE A: ONE-SHOT (Legacy/CLI) ---
        target_url = sys.argv[1]
        target_content = sys.argv[2] if len(sys.argv) > 2 else ""
        
        # Execute Scan
        result = asyncio.run(scan(target_url, target_content))
        
        # Output to Stdout
        print(json.dumps(result))
        
        # GENIUS FIX: Force Write Evidence to Disk (The "Black Box" Protocol)
        with open("evidence_dump.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
            
    else:
        # --- MODE B: SENTINEL DAEMON (New Architecture) ---
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
                
                # Log to evidence file (append mode for stream)
                with open("evidence_stream.log", "a", encoding="utf-8") as f:
                    f.write(json.dumps(result) + "\n")
                
            except json.JSONDecodeError:
                err = {"error": "Invalid JSON Input"}
                print(json.dumps(err))
                sys.stdout.flush()
            except Exception as e:
                err = {"error": f"Bridge Error: {str(e)}"}
                print(json.dumps(err))
                sys.stdout.flush()
