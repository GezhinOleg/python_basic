# ! coding: utf-8
# pip install requirements.txt


import json
from vkontakte import VkUser
from yandex_disk import YandexDisk
from datetime import datetime as dt
from  progress.bar import IncrementalBar

def main():
    vk_token = input('Enter VK-Token')
    yandex_disk_token = input('Enter Yandex Disk Token: ')
    vk_ipi_version = '5.131'
    vk_user = VkUser(vk_token, vk_ipi_version)
    yd_user = YandexDisk(yandex_disk_token)
    vk_user_id = get_user_id(vk_user)
    user_data = vk_user.get_user_data(vk_user_id)
    albums_data = vk_user.get_photo_albums(vk_user_id)
    albums_dict = get_folders_ids_dict(albums_data)
    album = get_user_album_choice(albums_dict)
    if album == 0:
        number_of_photos = input('Enter number of photos: ')
        photo_db = photos_data_dict(user_data=user_data, photos_data=vk_user.get_all_photos_data(user_id=vk_user_id, count=number_of_photos))
        links = get_photo_urls(photo_db)
        yd_user.mkdir('vk_photo')
        yd_user.mkdir('vk_photo/{} {}'.format(user_data['last_name'], user_data['first_name']))
        folder_path = '{}/Все фотографии'.format('vk_photo/{} {}'.format(user_data['last_name'], user_data['first_name']))
        yd_user.mkdir(folder_path)
        progress_bar = IncrementalBar('Upload: ', max = len(photo_db))
        for key, value in links.items():
            progress_bar.next()
            file_path = '{}/{}'.format(folder_path, str(key))
            yd_user.upload_photo_to_disk(file_path=file_path, image_url=value)
        create_json(db=photo_db, user_info=user_data)
        progress_bar.finish()
    else:
        number_of_photos = input('Enter number of photos: \n')
        photo_db = photos_data_dict(user_data=user_data, photos_data=vk_user.get_photos_from_album(user_id=vk_user_id, album_id=album, count=number_of_photos))
        links = get_photo_urls(photo_db)
        yd_user.mkdir('vk_photo')
        yd_user.mkdir('vk_photo/{} {}'.format(user_data['last_name'], user_data['first_name']))
        folder_path = 'vk_photo/{} {}/{}'.format(user_data['last_name'], user_data['first_name'], album)
        yd_user.mkdir(folder_path)
        progress_bar = IncrementalBar('Upload: ', max = len(photo_db))
        for key, value in links.items():
            progress_bar.next()
            file_path = '{}/{}'.format(folder_path, str(key))
            yd_user.upload_photo_to_disk(file_path=file_path, image_url=value)
        create_json(db=photo_db, user_info=user_data)
        progress_bar.finish
    print('Download finished')

def get_user_id(vk_user):
    user_id = input('Enter screen name or user-ID: ')
    while not vk_user.get_id(user_id):
        user_id = input('ID do not correct! \nEnter screen name or user-ID: ')
    print()
    return vk_user.get_id(user_id)

def photos_data_dict(user_data, photos_data):
    counter = 1
    collection = {}
    for item in photos_data:
        tmp_dict = {}
        tmp_dict['user_name'] = '{} {}'.format(user_data['first_name'], user_data['last_name'])
        tmp_dict['user_id'] = user_data['id']
        tmp_dict['date'], tmp_dict['time'] = decoding_timestamp(item['date'])
        tmp_dict['likes'] = item['likes']['count']
        type_list = ['w', 'z', 'y', 'r']
        for entry in item['sizes']:
            if entry['type'] in type_list:
                tmp_dict['url'] = entry['url']
        collection[counter] = tmp_dict
        counter += 1
    return collection

def get_folders_ids_dict(album_data):
    collection = {}
    for item in album_data:
        collection[item['title']] = item['id']
        if item['id'] == -7:
            collection[item['title']] = 'wall'
        if item['id'] == -6:
            collection[item['title']] = 'profile'
        if item['id'] == -15:
            collection[item['title']] = 'saved'
    return collection

def decoding_timestamp(timesatamp):
    date_obj = dt.fromtimestamp(timesatamp, tz=None)
    _date, _time = date_obj.strftime('%d/%m/%Y'), date_obj.strftime('%H:%M:%S')
    return _date, _time

def get_user_album_choice(collect):
    print('Ulbums: \n')
    print('0 --> All photos')
    keys = list(collect.keys())
    for index, value in enumerate(keys):
        print(f'{index+1} --> {value}')
    user_choice  = input('Enter your choice: ')
    while not user_choice.isdigit() or int(user_choice) not in range(len(keys)+1):
        user_choice  = input('Enter your choice: ')
    print()
    if user_choice == '0':
        return 0
    else:
        return collect[keys[int(user_choice)-1]]

def get_numbers_of_photo():
    numbers_of_photo = input('Enter number of photo: ')
    while not numbers_of_photo.isdigit() or int(numbers_of_photo) < 1:
        numbers_of_photo = input('Enter number of photo(only positine integer): ')
    return numbers_of_photo

def get_photo_urls(data_dict):
    links = {}
    for key, value in data_dict.items():
        if value['likes'] in links:
            links['{}({})'.format(value['likes'], value['time'])] = value['url']
        else:
            links[value['likes']] = value['url']
    return links
            
def create_json(db, user_info):
    file_name = '{}.json'.format(user_info['last_name'])
    with open(file_name, 'w') as output_file:
        json.dump(db, output_file, ensure_ascii=False, indent=2)
    
if __name__ == '__main__':
    main()