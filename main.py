from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Error(BaseModel):
    code: int
    message: str


class User(BaseModel):
    id: int
    name: str
    email: str
    address: str | None = None


class Users(BaseModel):
    users: List[User] = []


class GetUsersResponse(BaseModel):
    users: List[User] = []


class PostUsersRequest(BaseModel):
    name: str
    email: str


class PostUsersResponse(BaseModel):
    id: int
    name: str
    email: str


@app.get("/users")
async def get_users(limit: int = 20, name: str | None = None) -> GetUsersResponse:
    return GetUsersResponse(users=[])


@app.post("/users", status_code=201, responses={"default": {"model": PostUsersRequest}})
async def create_pet(user: PostUsersRequest):
    return PostUsersResponse(id=1, name=user.name, email=user.email)
