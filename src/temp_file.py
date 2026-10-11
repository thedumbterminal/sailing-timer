import os
import tempfile
from datetime import datetime

TEMP_SUBDIRECTORY = "sailing-timer"


class TempFile:
    def __init__(self):
        self._file = tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            prefix=datetime.now().strftime("%Y-%m-%d_%H-%M-%S_"),
            suffix=".csv",
            delete=False,
            dir=TempFile.get_temp_directory(),
        )

    def get_file(self):
        return self._file

    def get_file_name(self):
        return self._file.name

    @staticmethod
    def get_temp_directory():
        directory = os.path.join(tempfile.gettempdir(), TEMP_SUBDIRECTORY)
        os.makedirs(directory, exist_ok=True)
        return directory
