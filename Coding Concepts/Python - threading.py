# note that the first thread begins right here!

import threading
import time

# the Thread object requires a function be passed to it
def foo(arg):
    print(arg)
    time.sleep(1)

x = threading.Thread(target=foo, args=('Hi',))
x.start()  # start the second thread

print('done.')


####################

# global list object. Note that it isn't safe to use global objects
# from different threads (unless you use 'locks'). I think this is 
# because 
ls = []

i = 0
def foo2():
    for _ in range(5):
        ls.append(i)
        i += 1
        time.sleep(0.1)

j = 0
def foo3():
    for _ in range(5):
        ls.append(j)
        j += 1
        time.sleep(0.2)

a = threading.Thread(target=foo2)
b = threading.Thread(target=foo3)

a.start()
b.start()

# at this point you won't print out a full list, because 
# 'print(ls)' will be reached before the threads finish
# running
print(ls)


# however, in this case, the list will be full. the .join 
# method pauses further code execution until the thread is
# completed

ls = []
i, j = 0, 0

a.start()
b.start()

a.join()
b.join()

print(ls)

# join is used often to ensure a thread has finished running
# by a certain point in the code.



