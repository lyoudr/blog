from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from src.routes import (
    user,
    post,
    image,
    tag,
    follow,
    chatbot,
    auth,
)

app = FastAPI(
    title="Mind",
    docs_url="/docs",
    description="FastAPI Documentation",
    swagger_ui_parameters={"persistAuthorization": True, "tryItOutEnabled": True},
)
# Add GZip middleware
app.add_middleware(GZipMiddleware, minimum_size=500)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(image.router)
app.include_router(tag.router)
app.include_router(follow.router)
app.include_router(chatbot.router)
