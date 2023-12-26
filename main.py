from fastapi import FastAPI, Request
import models
from database import engine
from routes import router_purchase, router_buyer, router_websocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

app.include_router(router_purchase)
app.include_router(router_buyer)
app.include_router(router_websocket)
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    http_protocol = request.headers.get("x-forwarded-proto", "http")
    ws_protocol = "wss" if http_protocol == "https" else "ws"
    server_urn = request.url.netloc
    return templates.TemplateResponse("main.html",
                                      {"request": request,
                                       "http_protocol": http_protocol,
                                       "ws_protocol": ws_protocol,
                                       "server_urn": server_urn})
