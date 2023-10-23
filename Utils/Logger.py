import Constants

class Logger:
    @staticmethod
    def log(type, msg):
        if Constants.IS_LOG_ACTIVE and Constants.LOGGER_TYPES[type]:
            print("[",type,"]", *msg)