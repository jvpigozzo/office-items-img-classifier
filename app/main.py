from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_router, item_router

description = """
This API facilitates efficient management and categorization of office item images, leveraging advanced visual recognition technology. 👁️🤖

## Items

You can **browse through and categorize items** with ease.

## Users

You have the ability to:

* **Create new user profiles**.
* **Access and review user information**.

"""

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "items",
        "description": "Manage items.",
    },
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="OfficeItemsApp",
    description=description,
    version="0.0.1",
    contact={
        "name": "João Vitor Pigozzo",
        "url": "https://github.com/jvpigozzo",
        "email": "jvpigozzo@gmail.com",
    },
)

origins = [
    "*",
]

# Add CORS middleware to the FastAPI app for development purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router.router)
app.include_router(item_router.router)
