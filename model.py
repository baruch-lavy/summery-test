from pydantic import BaseModel,Field,BeforeValidator,field_validator, ValidationError
from typing import Annotated,Any

    

class SoldierCreate(BaseModel):
    privet_number:int
    first_name:str
    last_name:str
    gender:str
    city:str
    distance:int
    is_assign:bool
    
    @field_validator('privet_number', mode='before')
    @classmethod
    def capitalize(cls, value: int):
        if not str(value).startswith('8'):
            print('privet number need to start wit 8')

    
class SoldierResponse(BaseModel):
    privet_number:int
    first_name:str
    last_name:str
    
class SoldierToassign(BaseModel):
    soldier_1:int
    soldier_2:int
    soldier_3:int
    soldier_4:int
    soldier_5:int
    soldier_6:int
    soldier_7:int
    soldier_8:int
    

class Config:
    orm_mode = True