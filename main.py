from typing import List

from fastapi import Depends, FastAPI, HTTPException

import database
import schemas
import models
from database import db_state_default

app = FastAPI()

@app.get("/movies/", response_model=List[schemas.Movie])
def get_movies():
    return list(models.Movie.select())
    # movies = crud.get_movies()
    # return movies

@app.post("/movies/", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieBase):
    movie = models.Movie.create(**movie.dict())
    return movie

@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int):
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int):
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_movie.delete_instance()
    return db_movie

@app.get("/actors/", response_model=List[schemas.Actor])
def get_actors():
    return list(models.Actor.select())

# Pobieranie pojedynczego aktora
@app.get("/actors/{actor_id}", response_model=schemas.Actor)
def get_actor(actor_id: int):
    actor = models.Actor.get_or_none(models.Actor.id == actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Aktor nie istnieje")
    return actor

# Dodawanie aktora
@app.post("/actors/", response_model=schemas.Actor)
def add_actor(actor: schemas.ActorCreate):
    new_actor = models.Actor.create(**actor.dict())
    return new_actor

# Usuwanie aktora
@app.delete("/actors/{actor_id}")
def delete_actor(actor_id: int):
    actor = models.Actor.get_or_none(models.Actor.id == actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Aktor nie istnieje")
    
    actor.delete_instance()
    return {"message": "Aktor usunięty"}

### 🔹 PRZYPISANIE AKTORA DO FILMU ###

@app.post("/movies/{movie_id}/actors/")
def assign_actor_to_movie(movie_id: int, actor_data: dict):
    actor_id = actor_data.get("actor_id")

    movie = models.Movie.get_or_none(models.Movie.id == movie_id)
    actor = models.Actor.get_or_none(models.Actor.id == actor_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Film nie istnieje")
    
    if not actor:
        raise HTTPException(status_code=404, detail="Aktor nie istnieje")

    movie.actors.add(actor)  
    return {"message": f"Aktor {actor.name} {actor.surname} przypisany do filmu {movie.title}"}