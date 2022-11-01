from fastapi import FastAPI
from enum import Enum
from fastapi import Header
from fastapi import Query
from pydantic import BaseModel
from typing import Union
from typing import List
from collections import OrderedDict

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello'}

@app.post('/post')
async def get_post():
    return {'id': '0', 'timestamp': '0'}


class DogType(str, Enum):
    dog1 = 'terrier'
    dog2 = 'bulldog'
    dog3 = 'dalmatian'


class Dog(BaseModel):
    name: str
    pk: Union[int, None] = None
    kind: DogType

@app.post('/dog')
async def create_dog(dog: Dog):
    dog.pk = 0
    return dog

@app.get('/dog')
async def get_dogs(kind: DogType = None):
    if kind == None:
        return {'message': kind}
    else:
        return {'dog': kind}



@app.get('/dog/{pk}')
async def get_dog_by_pk(pk: int):
    return OrderedDict([('pk', pk), ('name', 2), ('kind', 3)])

from fastapi.encoders import jsonable_encoder

@app.patch('/dog/{pk}', response_model=Dog)
async def update_dog(pk: int, dog: Dog):
    data = {'dog': pk}
    stored_model = Dog(**data)
    updated_data = dog.dict(exclude_unset=True)
    updated_item = stored_model.copy(update=updated_data)
    pk[pk] = jsonable_encoder(updated_item)
    return updated_item