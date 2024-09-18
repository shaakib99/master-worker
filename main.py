from fastapi import FastAPI
from dotenv import load_dotenv

async def lifespan(app):
    load_dotenv()
    yield

app = FastAPI(lifespan=lifespan)
