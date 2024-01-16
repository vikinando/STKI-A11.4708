from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from function import master_recommendation_function
import os

app = FastAPI()

# response = JSON
@app.get("/recommend/")
async def recommend(anime_name: str):
    recommendations = master_recommendation_function(anime_name)
    return {"recommendations": recommendations}

# endpoint for the htmx
@app.get("/ui")
async def ui():
    return FileResponse(os.path.join('public', 'index.html'))

# Response = html
@app.post("/recommend-html/")
async def recommend(anime_name: str = Form(...)):
    recommendations = master_recommendation_function(anime_name)
    html_content = "<table><tr><th>Recommendations</th></tr>"
    for rec in recommendations:
        html_content += f"<tr><td>{rec}</td></tr>"
    html_content += "</table>"
    return HTMLResponse(content=html_content)