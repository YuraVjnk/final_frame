from datetime import date

from simba_framework.templator import render
from components.models import Engine, MapperRegistry
from components.decorators import AppRoute
from components.cbv import ListView, CreateView
from components.unit_of_work import UnitOfWork
from jsonpickle import dumps, loads

site = Engine()
routes = {}
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


# Класс-контроллер - Главная страница
@AppRoute(routes=routes, url='/')
class Index:
    def __call__(self, request):
        mapper = MapperRegistry.get_current_mapper('category')
        return '200 OK', render('index.html', objects_list=mapper.all(), geo=request.get('geo', None))


# Класс-контроллер - Страница "О проекте"
@AppRoute(routes=routes, url='/about/')
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


# Класс-контроллер - Страница "Расписания"
@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


# Класс-контроллер - Страница 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# Класс-контроллер - Страница "Список курсов"
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    def __call__(self, request):
        mapper = MapperRegistry.get_current_mapper('category')
        try:
            category = mapper.find_by_id(int(request['get_params']['id']))
            # category_n = site.find_category_by_id(int(request['request_params']['id']))
            # category = site.find_category_by_id(
            #     int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# Класс-контроллер - Страница "Создать курс"
@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1
    mapper = MapperRegistry.get_current_mapper('category')

    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = self.mapper.find_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['get_params']['id'])
                print(f'ахх {request}')
                category = self.mapper.find_by_id(self.category_id)

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# # Класс-контроллер - Страница "Создать категорию"
# @AppRoute(routes=routes, url='/create-category/')
# class CreateCategory:
#     def __call__(self, request):
#
#         if request['method'] == 'POST':
#
#             print(request)
#             data = request['data']
#
#             name = data['name']
#             name = site.decode_value(name)
#
#             category_id = data.get('category_id')
#
#             category = None
#             if category_id:
#                 category = site.find_category_by_id(int(category_id))
#
#             new_category = site.create_category(name, category)
#
#             site.categories.append(new_category)
#
#             return '200 OK', render('index.html',
#                                     objects_list=site.categories)
#         else:
#             categories = site.categories
#             return '200 OK', render('create_category.html',
#                                     categories=categories)

# Класс-контроллер - Страница "Создать студента"
@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student')
        site.students.append(new_obj)
        schema = {'name': name}
        new_obj.mark_new(schema)
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory(CreateView):
    template_name = 'create_category.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_category()
        site.categories.append(new_obj)

        schema = {'name': name}
        new_obj.mark_new(schema)
        UnitOfWork.get_current().commit()


# # Класс-контроллер - Страница "Список категорий"
# @AppRoute(routes=routes, url='/category-list/')
# class CategoryList:
#     def __call__(self, request):
#         return '200 OK', render('category_list.html',
#                                 objects_list=site.categories)


# Класс-контроллер - Страница "Список студентов"
@AppRoute(routes=routes, url='/student-list/')
class StudentsListView(ListView):
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        # UnitOfWork.get_current().commit()
        return mapper.all()


@AppRoute(routes=routes, url='/category-list/')
class CategoryList(ListView):
    template_name = 'category_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()


# Класс-контроллер - Страница "Добавить студента на курс"
@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


@AppRoute(routes=routes, url='/api/<cat>/')
class CourseApi:

    def __call__(self, request):
        mapper = MapperRegistry.get_current_mapper('category')
        cat_id_d = request.get('url_vars')
        cat_id = cat_id_d.get('cat')
        cat = mapper.find_by_id(int(cat_id))

        return '200 OK', BaseSerializer(cat).save()
