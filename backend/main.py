from fastapi import Depends, FastAPI

from sqlalchemy.orm import Session

import models
import crud
import schemas

from fastapi.middleware.cors import CORSMiddleware


from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # The origin of the frontend app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


todos: list[schemas.Todo] = []

@app.get("/", response_model=list[schemas.Todo])
async def get_todos(db: Session = Depends(get_db)) -> list[schemas.Todo]:
    return crud.get_todos(db)

@app.post("/",response_model=schemas.Todo)
async def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)