from main import app
import json


with open("openapi.json", "w") as f:
    api_spec = app.openapi()
    f.write(json.dumps(api_spec))
