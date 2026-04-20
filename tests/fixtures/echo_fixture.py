class EchoFixture(object):
    def __init__(self):
        self.prefix = 'hello '
        
    def echo(self, value):
        return self.prefix + value

    @staticmethod
    def static_echo(value):
        return value

    @classmethod
    def class_echo(cls, value):
        return value
