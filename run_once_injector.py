import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from executions.execution_engine import ExecutionMemory

# Set path to your Sov B memory JSON
memory = ExecutionMemory("../runtime_memory/memory_log.json")

# Inject 160 memory entries to trigger archive
for i in range(160):
    memory.remember(f"Test {i}", f"Response for test {i}", tone="test", tag="inject")

print("✅ Memory archive test complete. 160 entries injected.")
8