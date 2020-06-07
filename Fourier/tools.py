import time

def timer(function):
    """Print the duration of a function making use of decorators."""
    def function_(*args,**kwargs):
        """Tested function."""
        ti=time.time()
        result=function(*args,**kwargs)
        tf=time.time()
        dt=tf-ti
        print("[TIMER]: "+str(function.__name__)+" took "+str(dt)+" seconds.")
        return result
    return function_
