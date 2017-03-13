import inspect
def get_current_function_name():
    return inspect.stack()[1][3]
class MyClass:
    def __init__(self):
        print(self.__class__.__name__)
        pass
    def function_one(self):
        print ("%s.%s invoked"%(self.__class__.__name__, get_current_function_name()))
if __name__ == "__main__":
    myclass = MyClass()
    myclass.function_one()
