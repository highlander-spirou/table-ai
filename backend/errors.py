class HeaderMissing(UserWarning):
    pass

class ClientNotFound(UserWarning):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.haha = 'haha'


class ClientTimeOut(UserWarning):
    def __init__(self, client_in_db, *args: object) -> None:
        super().__init__(*args)
        self.client_in_db = client_in_db

class ClientMaxUssage(UserWarning):
    pass

class DuplicateUploadFile(UserWarning):
    pass

class UploadedFileExisted(UserWarning):
    pass

class FileExceedUssage(UserWarning):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class FileExtensionInvalid(UserWarning):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ParquetConversionError(UserWarning):
    pass


class FileNotExisted(UserWarning):
    pass


class CohereNotResponse(UserWarning):
    pass


class RunQueryFail(UserWarning):
    def __init__(self, query, *args: object) -> None:
        self.query = query
        super().__init__(*args)