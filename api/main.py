from fastapi import FastAPI
from api.routers import product
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(product.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
