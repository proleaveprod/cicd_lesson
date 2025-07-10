from fastapi import APIRouter
from modules.schemas import Character
from modules.database import characters

router = APIRouter(prefix="/character")

@router.get('/{id}', 
         name='Получить персонажа по id',
         tags=['api/character'])
async def get_character(id_: int):
    return characters.get(id_)


@router.post('/', 
         name='Добавить нового персонажа',
         tags=['api/character'])
async def post_character(new_character: Character):
    return characters.add(new_character)


@router.put('/{id}', 
         name='Полное обновление данных персонажа по id',
         tags=['api/character'])
async def put_character(id_: int, updated_character: Character):
    return characters.update(id_, updated_character, patch=False)


@router.patch('/{id}', 
         name='Дополнение или правка данных персонажа по id',
         tags=['api/character'])
async def patch_character(id_: int, updated_character: Character):
    return characters.update(id_, updated_character, patch=True)


@router.delete('/{id}', 
         name='Удалить персонажа по id',
         tags=['api/character'])
async def delete_character(id_: int):
    return characters.delete(id_)
