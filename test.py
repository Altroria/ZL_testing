import time


def deco01(f):
    def wrapper(*args, **kwargs):
        print("this is deco01")
        start_time = time.time()
        f(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        print("time is %d ms" % execution_time)
        print("deco01 end here")

    return wrapper


def deco02(f):
    def wrapper(*args, **kwargs):
        print("this is deco02")
        f(*args, **kwargs)

        print("deco02 end here")

    return wrapper


@deco01
@deco02
def f(a, b):
    print("be on")
    time.sleep(1)
    print("result is %d" % (a + b))


if __name__ == '__main__':
    f(3, 4)
