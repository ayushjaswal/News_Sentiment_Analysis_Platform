import sys
from News_Sentiment_Analysis.logging import logger

class NewsSentimentAnalysisException(Exception):
    """
    Custom exception class for network security related errors.
    """

    def __init__(self, message, details: sys):
        self.error_message = message
        self.error_details = details

        _, _, exx_tb = details.exc_info()

        self.lineno = exx_tb.tb_lineno
        self.file_name = exx_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occured in python script name: [{0}]; Line number: [{1}]; Error message: [{2}]".format(
            self.file_name, self.lineno, str(self.error_message)
        )