import os
import struct
import numpy as np


# Right now we have fields that support just the int datatype
class DataFile:
    def __init__(self, pFileName=None):

        self._fileName = pFileName
        if pFileName is None:
            self._file = None
        else:
            self.create_file(pFileName)

    def create_file(self, pFileName):
        self._fileName = pFileName

        # If the file already exists open it in read mode so that the existing data doesn't get erased. Else
        # create the file.
        if os.path.isfile(pFileName):
            self._file = open(pFileName, "rb+")
            self._file.seek(0, os.SEEK_END)
        else:
            self._file = open(pFileName, "wb+")

        return self._file

    def write_field(self, pFieldId, pValue):
        self._file.write(struct.pack('i', pFieldId))
        self._file.write(struct.pack('i', pValue))
        self._file.flush()

    # Since everything is to be brought in-memory, we read the entire file.
    def read_file(self):
        # Move to the beginning of the file.
        self._file.seek(0, os.SEEK_SET)
        readData = np.fromfile(self._file, dtype=int)
        return [readData[x:x + 2] for x in range(0, len(readData), 2)]