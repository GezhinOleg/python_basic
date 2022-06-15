from urllib import response
import requests


class VkUser():
    vk_api_uri = 'https://api.vk.com/method/'

    def __init__(self, token, api_version):
        self.__params = {'access_token': token,
        'v': api_version}
    
    def get_id(self, user_screen_name):
        self.__get_id_method = 'users.get'
        self.__get_id_url = self.vk_api_uri + self.__get_id_method
        self.__get_id_params = {
            'user_ids': user_screen_name}
        res = requests.get(url=self.__get_id_url, params={**self.__get_id_params, **self.__params}).json()['response']
        if not res:
            return res
        return res[0]['id']
    
    def get_user_data(self, user_screen_name):
        self.__get_user_data_method = 'users.get'
        self.__get_user_data_uri = self.vk_api_uri + self.__get_user_data_method
        self.__get_user_data_params = {'user_ids': user_screen_name,
        'fields': ' '}
        response = requests.get(url=self.__get_user_data_uri, params={**self.__params, **self.__get_user_data_params}).json()['response'][0]
        return response

    def get_photo_albums(self, user_id):
        self.__get_user_albums_method = 'photos.getAlbums'
        self.__get_user_albums_uri = self.vk_api_uri + self.__get_user_albums_method
        self.__get_user_albums_params = {'owner_id': user_id, 'need_system': 1}
        response = requests.get(url=self.__get_user_albums_uri, params={**self.__params, **self.__get_user_albums_params}).json()['response']['items']
        return response

    def get_all_photos_data(self, user_id, count=5):
        self.__get_user_all_photo_method = 'photos.getAll'
        self.__get_user_all_photo_uri = self.vk_api_uri + self.__get_user_all_photo_method
        self.__get_user_all_photo_params = {'owner_id': user_id, 'extended': 1, 'count': count}
        response = requests.get(url=self.__get_user_all_photo_uri, params={**self.__get_user_all_photo_params, **self.__params}).json()['response']['items']
        return response

    def get_photos_from_album(self, user_id, album_id='profile', count=5):
        self.__get_photo_from_album_method = 'photos.get'
        self.__get_photo_from_album_uri = self.vk_api_uri + self.__get_photo_from_album_method
        self.__get_photo_from_album_params = {'owner_id': user_id, 'album_id': album_id, 'extended': 1, 'count': count, 'rev': 1}
        response = requests.get(url = self.__get_photo_from_album_uri, params={**self.__params, **self.__get_photo_from_album_params}).json()['response']['items']
        return response

    def get_photos_with_user(self, user_id, count=5):
        self.__get_photos_with_user_method = 'photos.getUserPhotos'
        self.__get_photos_with_user_uri = self.vk_api_uri + self.__get_photos_with_user_method
        self.__get_photos_with_user_params = {'user_id': user_id, 'count': count, 'extended': 1}
        response = requests.get(url = self.__get_photos_with_user_uri, params={**self.__params, **self.__get_photos_with_user_params}).json()['response']['items']
        return response