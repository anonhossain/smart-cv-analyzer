from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from views import api

app = FastAPI()

# Serve static frontend files
#app.mount("/", StaticFiles(directory="./frontend/landing_page", html=True), name="static")
# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend" / "landing_page"
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="static"
)

# Allow frontend to communicate with backend (adjust origin if needed)
origins = ["http://127.0.0.1:5500/",]
# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Allows requests from the specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(api)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",  # Use localhost IP address
        port=8080,
        reload=True
    )
