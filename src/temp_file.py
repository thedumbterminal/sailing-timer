import tempfile


class TempFile:
    def __init__(self):
        self._file = tempfile.NamedTemporaryFile(
            mode="w", newline="", suffix=".csv", delete=False
        )

    def get_file(self):
        return self._file

    def get_file_name(self):
        return self._file.name
