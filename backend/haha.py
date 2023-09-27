from functools import wraps

class Test():
    def __init__(self, arg_1, arg_2) -> None:
        self.arg_1 = arg_1
        self.arg_2 = arg_2

    def verify_ownership(method):
        @wraps(method)
        def _verify_ownership(self, *args, **kwargs):
            if self.arg_1 == 1:
                raise Exception('Args invalid')
            else:
                method(self, *args, **kwargs)
        return _verify_ownership

    @verify_ownership
    def bar(self, external):
        print(f"calculate 1: {self.arg_1 + self.arg_2}")
        print(f"calculate 2: {external}")


obj = Test(1, 2)
obj.bar(1)
