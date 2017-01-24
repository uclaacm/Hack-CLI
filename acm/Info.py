class InfoField(object):
    def __init__(self, required=False, inputter=raw_input, interpreter=None, additionalInfo=None):
        self.required = required
        self.inputter = inputter
        self.interpreter = interpreter
        self.additionalInfo = additionalInfo

class Interpreter(object):
    @staticmethod
    def list(str):
        return [x.strip() for x in str.split(",") if len(str.strip()) > 0]