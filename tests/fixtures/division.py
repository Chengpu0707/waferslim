class Division:
    def __init__(self, throw_on_divide_by_zero=True):
        self.throw_on_divide_by_zero = throw_on_divide_by_zero

    def x(self, x):
        self.x = float(x)
    
    def y(self, y):
        self.y = float(y)

    def divide(self):
        if self.y == 0:
            if self.throw_on_divide_by_zero:
                raise ValueError("divide by zero")
        return self.x / self.y