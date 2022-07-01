import quopri

from simba_framework.framework_requests import GetRequests, PostRequests, GetRequestClass
from components.routing import Router


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE NOT FOUND'


class Framework:

    def __init__(self, routes_obj, fronts_obj):
        self.request = {}
        self.routes_lst = routes_obj
        self.fronts_applications = fronts_obj
        self.router = Router(self.request, self.routes_lst)

    def __call__(self, environ, start_response):
        # Адрес по которому пользователь перешл
        path = environ['PATH_INFO']

        # Добавляем слеш к адрессу
        if not path.endswith('/'):
            path = f'{path}/'

        # Получаем данные запроса
        method = environ['REQUEST_METHOD']
        self.request['method'] = method

        method_class = GetRequestClass(method)
        data = method_class.get_request_params(environ)
        self.request[method_class.dict_value] = Framework.decode_value(data)
        print(f'{method} : {Framework.decode_value(data)}')

        # if method == 'POST':
        #     data = PostRequests().get_request_params(environ)
        #     request['data'] = data
        #     # print(f'Получен пост запрос : {Framework.decode_value(data)}')
        # if method == 'GET':
        #     request_params = GetRequests().get_request_params(environ)
        #     request['get_params'] = request_params
        #     print(f'Получен гет параметры : {Framework.decode_value(request_params)}')

        # # Поиск нужной вьюхи нашего проекта
        # if path in self.routes_lst:
        #     view = self.routes_lst[path]
        # else:
        #     view = PageNotFound404()

        view = self.router.get_view(path, PageNotFound404())

        for front_app in self.fronts_applications:
            front_app(environ, self.request)

        # Запуск этой вьюхи
        code, body = view(self.request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', ''), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
