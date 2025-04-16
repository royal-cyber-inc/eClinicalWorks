import requests
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

def fhir_json_proxy():
    target_url = "https://royal-cyber-inc.github.io/eClinicalWorks/jwks.fhir.json"
    response = requests.get(target_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Error fetching file"}, 500

@app.get("/", response_class=Response)
async def root():
    jwks_data = fhir_json_proxy()
    headers = {"Content-Type": "application/fhir+json"}
    
    # Handle error tuple
    if isinstance(jwks_data, tuple):
        return JSONResponse(content={"error": jwks_data[0]}, status_code=jwks_data[1])
    
    return JSONResponse(content=jwks_data, headers=headers)

@app.head("/")
async def head_root():
    headers = {"Content-Type": "application/fhir+json"}
    return Response(status_code=200, headers=headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
