from fastapi import FastAPI

from api.routes.dossiers import router as dossiers_router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


#Configure CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(dossiers_router)