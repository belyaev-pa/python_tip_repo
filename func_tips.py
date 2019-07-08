# tip 1 
# itertools.repeat() работает быстрее чем range() для циклов 
# определенное количество повторений, когда вам не нужна переменная итерации
min(random() for i in range(10_000)) # 1.03 msec  
min(random() for _ in repeat(None, 10_000)) # 841 usec


# tip 2
# все три примера делают одно и тоже  (is just a cute way of writing)
# 1
times = partial(repeat, None)  
# 2
times = lambda n: repeat(None, n) 
# 3
def times(n): 
  return repeat(None, n)
  
  
# tip 3 
# в python2 используй для обхода словаря
for k, v in d.iteritems():
# в python3 используй  https://www.python.org/dev/peps/pep-3106/
for k, v in d.items():

  
# tip 4
# Не используйте конструкцию :
try:
  some_function()
  # здесь огромное количество кода...
except Exception:
  do_smth
# без явно на то необходимости, чаще всего вам прийдется отлавливать 
# конкретное исключение, например:
try:
  some_var = some_dict['some_key']
except KeyError:
  some_dict['some_key'] = 'some value'
# это позволит избежать ошибок при отладке, а так же ваш код будет более понятен
# мне удалось найти 2 случая, когда реально нужно отлавливать Exception
# при реализации демона на python, нужно выводить трейсбек в сислог, что бы понять
# почему ваш демон упал (приведу код для python2):
try:
  self.run()
except Exception as err:
  syslog.syslog(syslog.LOG_ERR, 
                'Произошла ошибка при вызове функции run демона. Traceback:')
  syslog.syslog(syslog.LOG_ERR, '-' * 100)
  ex_type, ex, tb = sys.exc_info()    
  for obj in traceback.extract_tb(tb):
    syslog.syslog(syslog.LOG_ERR, 
                  'Файл: {}, строка: {}, вызов: {}'.format(obj[0], obj[1], obj[2]))
    syslog.syslog(syslog.LOG_ERR, '----->>>  {}'.format(obj[3]))
  syslog.syslog(syslog.LOG_ERR, 'Ошибка: {}.'.format(err))
  syslog.syslog(syslog.LOG_ERR, '-' * 100)
# в python 3 нет необходимости вызывать sys.exc_info() для получения объекта traceback 
# объект traceback включен в экземпляр объекта exception, поэтому его можно получить так:
tb = err.__traceback__
# так же его можно записать так: 
raise Exception("Произошла ошибка").with_traceback(traceback_obj)
# второй кейс, при проектировании Rest API с помощью DRF, 
# во вьюхе при выполнении логики нужно отлавливать 
# любой fuckup кода и вызывать APIException()


# tip 5
# не используйте в производственном коде следующую конструкцию:
from some_module import *
# скорее всего, когда вы используюте такую конструкцию вам просто лень
# списывать список того, что конкретно вы хотите имортировать, такое 
# допустимо при отладке, но вам так же будет лень переписать это потом
# или вы просто можете забыть.
# Использование подобной конструкции должно быть в первую очередь 
# подкреплено знаниями о том как Python обрабатывает исходный код
# вместо этого используйте
from some_module import Class1, Class2, Class3
from some_module import some_function1, some_function2
from some_module import some_function3, some_function4
# а так же можно собрать свой пакет, что бы понять о чем речь смотри пример:
# https://github.com/django/django/blob/master/django/db/models/__init__.py


# tip 6
# Не используй + для формирования строк, так как строки в python 
# являются immutable(неизменяемыми) объектами и каждый + будет формировать 
# новую строку в памяти. Так же для формирования строк необходимо использовать
# "новую" нотацию format() вместо старой % . https://www.python.org/dev/peps/pep-3101/
# Например для формирования строки из списка необходимо 
# воспользоваться такой конструкцией:
my string = ''.join(iterable)
# основное преимущество "новой" нотации над старой - сильная динамическая типизация


# tip 7
# Часто mutable(изменяемые) и immutable(неизменяемые) типы данных в Python порождают 
# много головной боли. Этот пример описывает то, о чем идет речь:
my_list = ['Hello']
print(my_list)
# Output: ['Hello']
my_list = your_list
my_list += ['World']
print(your_list)
# Output: ['Hello', 'World']
# перед вами типичная ошибка копирования


# tip 8 
# не используйте в качестве родителя для своих исключений BaseException
# для этого используется Exception, вот по этой причине:
# https://docs.python.org/3.7/library/exceptions.html#exception-hierarchy
# пример потенциальной ошибки
try:
    import sys
    sys.exit()
except BaseException:
    print ('Haha, but No!')
# свое исключение стоит создавать так:
class MyException(Exception): pass
