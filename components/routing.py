class Router:

    def __init__(self, request, routes: dict):
        self.request = request
        self.routes = self.routes_process(routes)

    @staticmethod
    def routes_process(routes):
        print(f'1 - {routes}')
        res = []
        for path, view in routes.items():
            path_dict = {
                'path': [],
                'view': view
            }
            print(f'2 - {path_dict}')
            path = path.strip('/')
            path_list = path.split('/')
            is_var = False
            for part in path_list:
                value = part
                print(f'4 - {value}')
                if '<' in part:
                    value = part.strip('<').strip('>')
                    print(f'5 - {value}')
                    is_var = True
                path_dict['path'].append({'value': value, 'is_var': is_var})
                print(f'6 {path_dict}')
            res.append(path_dict)
            print(f'7 - {res}')
        return res

    def get_view(self, path, view_404):
        path_list = path.strip('/').split('/')
        print(f'8 - {path_list}')
        url_vars = {}
        for route in self.routes:
            print(f'9 - {route["path"]}')
            if len(path_list) == len(route['path']):
                print(len(path_list))
                check_list = [False]*len(path_list)
                print(f'10 - {check_list}')
                for i, part in enumerate(route['path']):
                    if part['is_var']:
                        # print(f'11 - {url_vars[part["value"]]}')
                        url_vars[part['value']] = path_list[i]
                        print(f'12 - {url_vars[part["value"]]}')
                        check_list[i] = True
                        print(f'13 - {url_vars[part["value"]]}')
                    else:
                        if part['value'] == path_list[i]:
                            print(f'11 - {part["value"]}')
                            check_list[i] = True
            else:
                continue

            if not (False in check_list):
                self.request['url_vars'] = url_vars
                print(f'15 - {self.request["url_vars"]}')
                print(f'16 - {route["view"]}')
                return route['view']
            else:
                continue
        return view_404



