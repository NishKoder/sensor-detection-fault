import sys


def error_message_detail(error, error_detail: sys):  # type: ignore
    # The above code is getting the traceback object from the current exception.
    _, _, exc_tb = error_detail.exc_info()
    # The above code is getting the file name and line number of the error.
    file_name = exc_tb.tb_frame.f_code.co_filename  # type: ignore
    return "Error occurred while python script execution in this process: name[{0}] line number[{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)  # type: ignore
    )

class SensorException(Exception):
    
    def __init__(self, error, error_detail: sys):  # type: ignore
        # Calling the parent class's constructor.
        super().__init__(error)
        # Calling the function `error_message_detail` and passing in the error and error_detail.
        self.message = error_message_detail(error, error_detail)
    
    def __str__(self):  # type: ignore
        # Returning the message that was passed in.
        return self.message
        