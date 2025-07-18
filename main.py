from fastapi import FastAPI
from app.routes.analysis import router as analysis_router
from app.routes.portfolio import router as portfolio_router
from app.routes.stock import router as stock_router
from app.routes.compare import router as compare_router
from app.routes.repartition import router as repartition_router
from app.routes.suivi_local import router as suivi_local_router

app = FastAPI()

app.include_router(analysis_router)
app.include_router(portfolio_router)
app.include_router(stock_router)
app.include_router(compare_router)
app.include_router(repartition_router)
app.include_router(suivi_local_router)



