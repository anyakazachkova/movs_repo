from fastapi import FastAPI, HTTPException
from enum import Enum
from fastapi import Header
from fastapi import Query
from pydantic import BaseModel
from typing import Union
from typing import List
from collections import OrderedDict
from fastapi.encoders import jsonable_encoder

app = FastAPI()

items = [] #пустой список, который будем дальше пополнять

#Реализация пути "/"
@app.get('/')
async def root():
    return {'message': 'Hello'}

#Реализация пути "/post"
@app.post('/post')
async def get_post():
    return {'id': '0', 'timestamp': '0'}

#Класс для пород собак
class DogType(str, Enum):
    dog1 = 'terrier'
    dog2 = 'bulldog'
    dog3 = 'dalmatian'

#Класс для собаки
class Dog(BaseModel):
    name: str
    pk: Union[int, None] = None
    kind: DogType

#Реализация записи собак
@app.post('/dog')
async def create_dog(dog: Dog):
    dog.pk = len(items)
    items.append(dog)
    return dog

#Реализация загрузки списка собак, в том числе отдельно по породам
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

#Реализация получения информации о собаке по id
@app.get('/dog/{pk}')
async def get_dog_by_pk(pk: int):
    if (pk < 0) or (pk > len(items)-1):
        raise HTTPException(status_code=404, detail="Dog not found")
    else:
        stored_dog_data = dict(items[pk])
        dog_info = OrderedDict(pk = pk, name = stored_dog_data['name'], kind = stored_dog_data['kind'])
        return dog_info


#Реализация обновления собаки по id
@app.patch('/dog/{pk}')
async def update_dog(pk: int, dog: Dog):
    if (pk < 0) or (pk > len(items)-1):
        raise HTTPException(status_code=404, detail="Dog not found")    
    else:
        stored_dog_data = dict(items[pk])
        stored_dog_model = Dog(name = stored_dog_data['name'], pk = pk, kind = stored_dog_data['kind'])
        new_data = dog.dict(exclude_unset=True)
        updated_dog = stored_dog_model.copy(update=new_data)
        items[pk] = jsonable_encoder(updated_dog)
        return updated_dog