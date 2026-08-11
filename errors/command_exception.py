from errors.app_exception import AppException
class CommandException(AppException):
    def __init__(self, failed_cmd: str, stderr: str):
        self.failed_cmd = failed_cmd
        self.stderr = stderr

        super().__init__(
            code=500, 
            detail=f"Command '{failed_cmd}' failed: {stderr}"
        )