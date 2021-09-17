"""
schlib.py

Everything needed to interact with SchLib files
"""

import olefile

class AltiumFileType():
    __file_name = None

    def __init__(self, file_name=None) -> None:
        if file_name is not None:
            self.set_file_name(file_name)

    def __respr__(self):
        return self.__file_name

    def set_file_name(self, file_name: str) -> None:
        assert olefile.isOleFile(file_name)
        self.__file_name = file_name
        self.__update_item_list()


class SchLib(AltiumFileType):
    """Main object to interact with schlib"""
    def __update_item_list(self) -> None:
        # with olefile.OleFileIO(self.__file_name) as ole:
        pass

    def list_items(self) -> list:
        pass



class SchLibItem():
    def __init__(self):
        pass

    # def __respr__(self):
    #     pass
