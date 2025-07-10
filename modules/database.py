import json
from modules.schemas import Character

class CharacterBook():
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.characters = []
        
        # Чтение json-файла и запись в список characters_data
        characters_data = []
        with open(filepath,'r+',encoding='utf-8') as f:
            characters_data = json.load(f)

        for data in characters_data:
            # Вычитываем данные из json и пополняем спискок characters объектами Character
            character = Character.model_validate(data)
            self.characters.append(character)
        
    def save(self):
        """
        Сохранение списка self.characters в json-файл
        """

        # character.model_dump(mode="json") для автоматической сериализации Enum. 
        # В противном случае model_dump выдаст для ключа "side": <Side.GOOD: 'Добро'>
        data_to_save = [
            character.model_dump(mode="json", exclude_none=True) 
            for character in self.characters]
        
        with open(self.filepath, "w", encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)

    def get(self, current_id: int):
        for character in self.characters:
            if character.id == current_id:
                return {'status': 'OK', 
                        'details': 'Character is found', 
                        'data': character.model_dump()}

        return {'status': 'ERROR', 'details': 'Character is not found'}

    def add(self, new_character: Character):

        # Проверка занятости ID 
        for character in self.characters:
            print(f"{character.name}: {character.id}")
            if character.id == new_character.id:
                return {'status': 'ERROR', 'details': 'The ID is already occupied'}

        self.characters.append(new_character)
        self.save()

        return {'status': 'OK', 'details': 'Successfully added'}

    def delete(self, current_id: int):
        for character in self.characters:
            if character.id == current_id:
                self.characters.remove(character)
                self.save()
                return {'status': 'OK', 'details': 'Successfully deleted'}
        return {'status': 'ERROR', 'details': 'The ID is not found'}

    def update(self, current_id: int, updated_character: Character, patch: bool = False):
        for i, character in enumerate(self.characters):
            if character.id == current_id:
                updated_data = updated_character.model_dump(exclude_unset=patch) 
                self.characters[i] = character.model_copy(update=updated_data)
                self.save()
            
                return {'status': 'OK', 'details': 'Successfully updated'}
            
        return {'status': 'ERROR', 'details': 'The ID is not found'}

    def get_all(self):
        datalist = []
        for character in self.characters:
            datalist.append(character.model_dump())

        return {'status': 'OK', 'details': 'All characters', 'data': datalist}

characters = CharacterBook('database.json')
