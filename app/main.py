from fastapi import FastAPI
from app.routes import example

app = FastAPI()

app.include_router(example.router)
from app.routes import stock
app.include_router(stock.router)
from app.routes import analysis
app.include_router(analysis.router)
