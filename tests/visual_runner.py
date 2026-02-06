import os
import sys
import asyncio
import json

# Setup Visual Environment
os.environ["HEADLESS"] = "0"
os.environ["GADOS_VISUAL_MODE"] = "1"

print("==========================================")
print("   GADOS BROWSER - VISUAL TEST RUNNER")
print("==========================================")
print("Mode: HEADED (Visible)")
print("Evidence: ENABLED (Atomic Write)")

# Import the Bridge
try:
    import guardian_bridge
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import guardian_bridge

async def run_visual_suite():
    print("\n1. Launching Bridge (Headed Simulation)...")
    
    test_cases = [
        ("https://google.com", "Safe Search Content"),
        ("https://malware.test", "Malicious Payload Signature"),
        ("about:blank", "Empty Context")
    ]
    
    for url, content in test_cases:
        print(f"\n>> Navigating to: {url}")
        # In a real scenario, this would trigger the Electron Window
        # Here we invoke the logic which now Logs to Disk
        result = await guardian_bridge.scan(url, content)
        print(f"   Verdict: {result.get('status')} (Score: {result.get('score')})")
        
    print("\n[SUCCESS] Visual Suite Completed.")
    print("Evidence saved to: 'evidence_dump.json' and 'evidence_stream.log'")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_visual_suite())
