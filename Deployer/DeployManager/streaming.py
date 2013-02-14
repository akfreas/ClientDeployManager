import logging

class LogStreamer(logging.Handler):


    def __init__(self, include_html=False):
        logging.Handler.__init__(self)
        self.logfile = open("log.txt", "w")

    def emit(self, record):
        print record
        self.logfile.write(record.getMessage())
        self.logfile.close()
