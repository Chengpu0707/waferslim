class EmployeeList:
    def __init__(self, arg=None):
        self.arg = arg

    def query(self):
        return (
            (("name", "Alice"), ("department", "Engineering"), ("arg", self.arg)),
            (("name", "Bob"),   ("department", "Marketing"), ("arg", self.arg)),
        )
