# tip №1 
# itertools.repeat() работает быстрее чем range() для циклов 
# определенное количество повторений, когда вам не нужна переменная итерации
min(random() for i in range(10_000)) # 1.03 msec  
min(random() for _ in repeat(None, 10_000)) # 841 usec

# tip №2
# все три примера делают одно и тоже  (is just a cute way of writing)
# 1
times = partial(repeat, None)  
# 2
times = lambda n: repeat(None, n) 
# 3
def times(n): 
  return repeat(None, n)
  
# tip №3 
# в python2 используй для обхода словаря
for k, v in d.iteritems():
# в python3 используй  https://www.python.org/dev/peps/pep-3106/
for k, v in d.items():

# tip №4
# Не используйте конструкцию :
try:
  some_function()
  # здесь огромное количество кода...
except BaseException:
  do_smth
# без явно на то необходимости, чаще всего вам прийдется отлавливать 
# конкретное исключение, например:
try:
  some_var = some_dict['some_key']
except KeyError:
  some_dict['some_key'] = 'some value'
# это позволит избежать ошибок при отладке, а так же ваш код будет более понятен
# мне удалось найти 2 случая, когда реально нужно отлавливать BaseException
# при реализации демона на python, нужно выводить трейсбек в сислог, что бы понять
# почему ваш демон упал (приведу код для python2):
try:
  self.run()
except BaseException as err:
  syslog.syslog(syslog.LOG_ERR, 'Произошла ошибка при вызове функции run демона. Traceback:')
  syslog.syslog(syslog.LOG_ERR, '-' * 100)
  ex_type, ex, tb = sys.exc_info()    
  for obj in traceback.extract_tb(tb):
    syslog.syslog(syslog.LOG_ERR, 'Файл: {}, строка: {}, вызов: {}'.format(obj[0], obj[1], obj[2]))
    syslog.syslog(syslog.LOG_ERR, '----->>>  {}'.format(obj[3]))
  syslog.syslog(syslog.LOG_ERR, 'Ошибка: {}.'.format(err))
  syslog.syslog(syslog.LOG_ERR, '-' * 100)
# в python 3 нет необходимости вызывать sys.exc_info() для получения объекта traceback 
# объект traceback включен в экземпляр объекта exception, поэтому его можно получить так:
tb = err.__traceback__
# так же его можно записать так: 
raise Exception("Произошла ошибка").with_traceback(traceback_obj)
# второй кейс, при проектировании Rest API с помощью DRF, во вьюхе при выполнении логики нужно отлавливать 
# любой fuckup кода и вызывать APIException()
