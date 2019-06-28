# tip №1 
# itertools.repeat() is faster than range() for looping 
# a fixed number of times when you don't need the loop variable. 
min(random() for i in range(10_000)) # 1.03 msec per loop 
min(random() for _ in repeat(None, 10_000)) # 841 usec per loop

# tip №2
# this 3 is equil (is just a cute way of writing)
# 1
times = partial(repeat, None)  
# 2
times = lambda n: repeat(None, n) 
# 3
def times(n): 
  return repeat(None, n)
  
# tip №3 
# in python2 use 
for k, v in d.iteritems():
# in python3 use  https://www.python.org/dev/peps/pep-3106/
for k, v in d.items():
