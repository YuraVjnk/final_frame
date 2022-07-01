# Обработка GET-запроса с параметрами
from abc import ABCMeta, abstractmethod


class Request(metaclass=ABCMeta):

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            # Делим параметры через &
            params = data.split('&')
            for item in params:
                # Делим ключ и значение через =
                k, v = item.split('=')
                result[k] = v
        return result

    @abstractmethod
    def get_request_params(self, environ):
        pass


class GetRequests(Request):

    dict_value = 'get_params'

    def get_request_params(self, environ):
        # Получаем параметры запроса
        query_string = environ['QUERY_STRING']
        # Превращаем параметры в словарь
        get_params = GetRequests.parse_input_data(query_string)
        return get_params


# Обработка POST-запроса с параметрами
class PostRequests(Request):

    dict_value = 'data'

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        # Получаем длину тела
        content_length_data = env.get('CONTENT_LENGTH')
        # Приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        # Считываем данные, если они есть
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        if data:
            # Декодируем данные
            data_str = data.decode(encoding='utf-8')
            # Собираем их в словарь
            return self.parse_input_data(data_str)
        return {}

    def get_request_params(self, environ):
        # Получаем данные
        data = self.get_wsgi_input_data(environ)
        # Превращаем данные в словарь
        data = self.parse_wsgi_input_data(data)
        return data


class GetRequestClass:

    def __new__(cls, method):
        if method == 'POST':
            return PostRequests()
        if method == 'GET':
            return GetRequests()


# Обработка Гет запроса с параметрами

# class GetRequests:
#
#     @staticmethod
#     def parse_input_data(data: str):
#         result = {}
#         if data:
#             # Делим параметры амперсандом через сплит
#             params = data.split('&')
#             for item in params:
#                 # Делим параметры = через сплит
#                 k, v = item.split('=')
#                 result[k] = v
#         return result
#
#     @staticmethod
#     def get_request_params(environ):
#         # Получаем параметры запроса
#         query_string = environ['QUERY_STRING']
#         # Превращаем параметры в словарь
#         get_params = GetRequests.parse_input_data(query_string)
#         return get_params
#
#
# class PostRequests:
#
#     @staticmethod
#     def parse_input_data(data: str):
#         result = {}
#         if data:
#             # Делим параметры амперсандом через сплит
#             params = data.split('&')
#             for item in params:
#                 # Делим параметры = через сплит
#                 k, v = item.split('=')
#                 result[k] = v
#         return result
#
#     @staticmethod
#     def get_wsgi_input_data(env) -> bytes:
#         # Получаем длину запроса
#         content_lenght_data = env.get('CONTENT_LENGTH')
#         # Приводим к числовому значению
#         content_lenght = int(content_lenght_data) if content_lenght_data else 0
#         # Считываем данные если они есть
#         data = env['wsgi.input'].read(content_lenght) if content_lenght > 0 else b''
#         return data
#
#     def parse_wsgi_input_data(self, data: bytes) -> dict:
#         result = {}
#         if data:
#             # Декодируем данные
#             data_str = data.decode(encoding='utf-8')
#             # Собираем словарь
#             result = self.parse_input_data(data_str)
#             return result
#
#     def get_request_params(self, environ):
#         # Получаем данные
#         data = self.get_wsgi_input_data(environ)
#         # Превращаем данные в словарь
#         data = self.parse_wsgi_input_data(data)
#         return data
