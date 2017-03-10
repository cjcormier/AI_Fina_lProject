class Log:
    can_log = True
    can_log_probs = False


    @staticmethod
    def allow_logging(new_log):
        Log.can_log = new_log

    @staticmethod
    def allow_prob_logging(new_log_prob):
        Log.can_log_prob = new_log_prob

    @staticmethod
    def log_probs(probs_message):
        if Log.can_log_probs:
            Log.log(probs_message)

    @staticmethod
    def log(*args):
        string = ''
        for element in args:
            string += str(element)
            string += ' '
        if Log.can_log:
            print(string[0:-1])

__all__ = ['Log']
