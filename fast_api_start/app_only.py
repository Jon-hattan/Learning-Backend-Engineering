from fastapi import FastAPI, HTTPException
from typing import Any

app = FastAPI(root_path="/api/v1")
# root path is set 

@app.get("/")
async def root():
    return {"message":"Hello World!"}

"""
FASTAPI itself doesnt run, need a ASGI Server
- Use Uvicorn
uvicorn main:app --reload
--> main is the filename
--> app is the FastAPI object
--> --reload param means it auto restarts on code changes.
"""
app.state.data = [
    {
        "campaign_id": 1,
        "name" : "Summer Launch",
        "due date": "yes"
    }, 
    {
        "campaign_id": 2,
        "name" : "Winter Launch",
        "due date": "yes"
    }

]
app.state.campaign_count = 2

@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": app.state.data}


@app.get("/campaigns/{id}")
async def read_campaign(id: int):
    for campaign in app.state.data:
        if campaign["campaign_id"] == id:
            return {"campaign": campaign}
    # should raise 404 error if no campaign with that id is found
    raise HTTPException(status_code=404, detail="Campaign not found")


@app.post("/campaigns")
async def create_campaign(body: dict[str, Any]):
    app.state.campaign_count+=1
    new = {
        "campaign_id": app.state.campaign_count,
        "name" : body.get("name"),
        "due date": "yes"
    }
    app.state.data.append(new)
    return {"campaign": new}

@app.put("/campaigns/{id}")
async def update_campaign(id: int, body: dict[str, Any]):
    updated = False
    for i, campaign in enumerate(app.state.data):
        if campaign["campaign_id"] == id:
            app.state.data[i] = body
            updated = True
    if updated:
        return {"campaign_added" : body}
    else:
        raise HTTPException(status_code=404, detail="id not found")


@app.delete("/campaigns/{id}")
async def delete_campaign(id: int):
    updated = False
    for i, campaign in enumerate(app.state.data):
        if campaign["campaign_id"] == id:
            return {"campaign_removed" : app.state.data.pop(i)}

    raise HTTPException(status_code=404, detail="id not found")
