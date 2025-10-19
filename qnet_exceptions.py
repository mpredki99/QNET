class QNetException(Exception):
    def __init__(
        self,
        *args: object,
        type: str = "QNet Error",
        message: str = "Unknown error occured."
    ) -> None:
        super().__init__(*args)
        self.type = type
        self.message = message


class InputFilesError(QNetException):
    def __init__(
        self,
        *args: object,
        type: str = "Import files error",
        message: str = "Unknown error occured during import files."
    ) -> None:
        super().__init__(*args, type=type, message=message)


class AdjustmentError(QNetException):
    def __init__(
        self,
        *args: object,
        type: str = "Adjustment error",
        message: str = "Unknown error occured during the adjustment."
    ) -> None:
        super().__init__(*args, type=type, message=message)


class ReportError(QNetException):
    def __init__(
        self,
        *args: object,
        type: str = "Report error",
        message: str = "Unknown error occured during export the report file."
    ) -> None:
        super().__init__(*args, type=type, message=message)


class OutputError(QNetException):
    def __init__(
        self,
        *args: object,
        type: str = "Output error",
        message: str = "Unknown error occured during creating the output."
    ) -> None:
        super().__init__(*args, type=type, message=message)
