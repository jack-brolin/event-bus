from pydantic import BaseModel


class UserInput(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    permission: str

    class Config:
        orm_mode = True
