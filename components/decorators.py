# Декоратор для реализации маршрутизации сайта
class AppRoute:

    def __init__(self, routes, url):
        '''Сохраняем значение параметра что передался в класс'''
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        '''Декоратор Колабл'''
        self.routes[self.url] = cls()
        #cls - view которую мы декорируем
