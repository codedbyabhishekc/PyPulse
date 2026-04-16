from app.main import app
import json
from app.contracts.store import save_baseline

schema = app.openapi()
print(schema.keys())  # sanity check

save_baseline(schema)
print("Baseline saved")