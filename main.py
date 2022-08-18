from fastapi import FastAPI
from app import models 
from app.database import engine 
from app import models
from app.routers import post, user, auth, vote 
from app.config import settings 
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Add routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get('/')
def hello():
    return {"Hello world!"}