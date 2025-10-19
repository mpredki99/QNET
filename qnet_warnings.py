class QNetWarning(Warning):
    def __init__(
        self,
        *args: object,
        type: str = "QNet Warning",
        message: str = "Unknown warning occured.",
    ) -> None:
        super().__init__(*args)
        self.type = type
        self.message = message

    def __str__(self) -> str:
        return f"{self.type}: {self.message}"


class AdjustmentWarning(QNetWarning):
    def __init__(
        self,
        *args: object,
        type: str = "Adjustment Warinig",
        message: str = "Unknown warning occured during the adjustment.",
    ) -> None:
        super().__init__(*args, type=type, message=message)
