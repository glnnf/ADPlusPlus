"""
FastAPI
Be in directory
1. first create venv

python -m venv .venv

2. Activate Virtual Env
powershell:

.venv\Scripts\Activate.ps1

3. Add .venv to gitignore
4. Install FastAPI (be in proper dir)

pip install "fastapi[standard]"

5. Deactivate when done working

deactivate

"""
#deactivate when done

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",  # Default Vite port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["+"],
)

@app.get("/")
async def root():
    return {"message": "hello world"}

