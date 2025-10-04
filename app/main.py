from fastapi import FastAPI
from starlette.responses import HTMLResponse

from .api import router

app = FastAPI()

app.include_router(router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
        <html>
            <head>
                <title>Hello</title>
            </head>
            <body>
                <p>Привет</p>
                <p>Описание Api можно посмотреть на этом же host добавив '/docs'</p>
                <p>Сам репозиторий можно найти https://github.com/i-c-winner/driveusta-backend</p>
            </body>
        </html>
        """

