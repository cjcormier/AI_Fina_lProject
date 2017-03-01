

class Log:
    can_log = True

    @staticmethod
    def allow_logging(new_log):
        Log.can_log = new_log

    @staticmethod
    def log(*args):
        string = ''
        for element in args:
            string += str(element)
            string += ' '
        if Log.can_log:
            print(string[0:-1])
