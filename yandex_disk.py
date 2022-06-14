import requests

class YandexDisk():
    yd_api_uri = 'https://cloud-api.yandex.net/'

    def __init__(self, token):
        self.__headers = {'Content-Type': 'application/json',
        'Authorization': f'OAuth {token}'}

    def mkdir(self, dir_path):
        self.__mkdir_method = 'v1/disk/resources'
        self.__mkdir_uri = self.yd_api_uri + self.__mkdir_method
        self.__mkdir_params = {'path': dir_path}
        res = requests.put(url=self.__mkdir_uri, headers=self.__headers, params=self.__mkdir_params)
        if res.status_code == 201:
            print('. ', end=' ')
        if res.status_code == 409:
            print('. ', end=' ')
    
    def upload_photo_to_disk(self, file_path, image_url):
        self.__upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        self.__upload_params = {'url': f'{image_url}', 
                        'path': f'disk:/{file_path}', 
                        'overwrite': 'true'}
        res = requests.post(url=self.__upload_url, params=self.__upload_params, headers=self.__headers)