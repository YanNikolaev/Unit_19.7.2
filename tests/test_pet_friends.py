from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, long_name, long_animal_type
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0



def test_add_new_pet_with_valid_data(name='Пес', animal_type='доберман',age='3', pet_photo='images/pug.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Инокентий", "Ящерица", "3", "images/pug.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Инокентий', animal_type='Ящерица', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_add_new_pet_without_photo_valid_data(name='Василий', animal_type='Теленок', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    print(result)

def test_add_new_photo_for_pet_with_valid_data(pet_photo='images/dog.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_for_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] != ''
        assert 'jpeg' in result['pet_photo']
    else:
        raise Exception("There is no my pets for ")


def test_add_new_pet_without_photo_empty_data(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['name'] == ''
    print(result)
    """Это баг, с пустыми параметрами ожидаем негативный результат со статус кодом 400
     и результатом имя не равным пустой строке"""

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert not 'key' in result

def test_add_new_pet_with_invalid_data(name='1234', animal_type='1234',
                                     age='1234', pet_photo='images/pug.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert  int(result['name'])
"""Баг: имя, тип животного должны принимать только буквы,а возраст двузначное число.
 Ожидаем негативный результат со статус кодом 400 и невозможностью обернуть буквы в число"""


def test_add_new_pet_with_long_data(name=long_name, animal_type=long_animal_type,
                                     age='1234', pet_photo='images/pug.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert len(result['name']) > 100
"""Баг: имя и тип животного принимают более 100 символов каждый.
 Ожидаем негативный результат со статус кодом 400 и длинной имени и типа животного в ограниченном количестве """

def test_add_new_photo_for_pet_with_valid_data_format_png(pet_photo='images/doggy.png'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_for_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 500
        # assert result['pet_photo'] != ''
        # assert 'png' in result['pet_photo']
        print(result)
    else:
        raise Exception("There is no my pets for ")
"""Баг: в документации указано, что на фото животного принимаются катринки формата png.
Ожидаем позитивный результат со статус кодом 200"""

def test_add_new_photo_for_pet_with_invalid_data_format_txt(pet_photo='images/text.rtf'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_for_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 500
        # assert result['pet_photo'] != ''
        # assert 'png' in result['pet_photo']
        print(result)
    else:
        raise Exception("There is no my pets for ")
"""Баг: при добавлении фото недопустимого в документации формата мы ожидаем ошибку со сторыны клиента
со статус кодом 400"""

def test_unsuccessful_update_self_pet_negative_age(name='Борщ', animal_type='Голубь', age=-5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert int(result['age']) == age
        assert int(result['age']) < 0
    else:
        raise Exception("There is no my pets")
"""Баг: при обновлении информации о животном можно указать отрицательный возраст.
Ожидаем негативный результат со статус кодом 400."""

def test_unsuccessful_update_self_pet_with_empty_data(name=' ', animal_type=' ', age= ' '):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == ' '
        print(result)
    else:
        raise Exception("There is no my pets")
"""Баг: возможно обновить информациию о животном используя параметры с пустыми значениями.
Ожидаем негативный результат со статус кодом 400."""

def test_delete_pet_another_user(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    pet_id = result['pets'][0]['id']
    status_, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, pets = pf.get_list_of_pets(auth_key, 'pets')

    assert status_ == 200
    assert pet_id not in pets
"""Баг: функция дает возможность удалить питомца другого пользователя.
Ожидаем негативный результат со статус кодом 400"""
