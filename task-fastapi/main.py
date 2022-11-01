from fastapi import FastAPI, Request
from enum import Enum
from fastapi import Header
from fastapi import Query
from pydantic import BaseModel
from typing import Union
from typing import List
from collections import OrderedDict

app = FastAPI()

items = [] #пустой список, который будем дальше пополнять
#items = [{'pk': 0, 'name': 'anya', 'kind': 'dalmatian'}, {'pk': 1, 'name': 'string', 'kind': 'terrier'}, {'pk': 2, 'name': 'vasya', 'kind': 'bulldog'},]

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
    dog.pk = len(items)
    items.append(dog)
    return items



@app.get('/dog')
async def get_dogs(kind: DogType = None):
    if kind == None:
        return items
    else:
        answer = []
        for i in items:
            if i.kind == kind:
                answer.append(i)
        return answer


@app.get('/dog/{pk}')
async def get_dog_by_pk(pk: int):
    return items[pk]

from fastapi.encoders import jsonable_encoder

@app.patch('/dog/{pk}', response_model=Dog)
async def update_dog(pk: int, dog: Dog):
    stored_model = Dog(name=(items[pk]).name, pk=(items[pk]).pk, kind=(items[pk]).kind)
    updated_data = dog.dict(exclude_unset=True)
    updated_item = stored_model.copy(update=updated_data)
    items[pk] = jsonable_encoder(stored_model)
    return items

