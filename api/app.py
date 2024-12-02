from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from api.control.routers import auth, users, todos, teams
from api.control.schemas.utils_schemas import Message


from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(teams.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)

@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "🤖 Headquarters started! 🤖"}


@app.get("/pagex", status_code=HTTPStatus.OK, response_class=HTMLResponse)
def render_page():
    return """
        <html>
            <head>
                <title>Headquarters</title>
            </head>
            <body>
                <h1>Agents & Bots</h1>
            </body>
        </html>
        """

app.mount("/pdfs", StaticFiles(directory="api/bots/bot_boa_vindas/bot/pdf_output"), name="pdfs")

@app.get("/pdf/{pdf_name}")
def get_pdf(pdf_name: str):
    pdf_path = f"api/pdf_output/{pdf_name}"
    return FileResponse(pdf_path)