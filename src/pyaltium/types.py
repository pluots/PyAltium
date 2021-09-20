"""
types.py

Everything needed to interact with SchLib files
"""

import olefile
from .helpers import (
    altium_string_split,
    altium_value_from_key,
    sch_sectionkeys_to_list
)

class AltiumFileType():
    """
    This class will generally not be exposed. Simply
    intended to set up children
    """
    _file_name = None
    _header_dict = None
    _section_keys_dict = None
    _items_list = None

    def __init__(self, file_name=None) -> None:
        if file_name is not None:
            self.set_file_name(file_name)

    def __respr__(self):
        return self._file_name

    def set_file_name(self, file_name: str) -> None:
        assert olefile.isOleFile(file_name)
        self._file_name = file_name
        self._update_header_and_section_keys()
        self._update_item_list()

    def _update_header_and_section_keys(self) -> None:
        """Just update class's _header_dict object"""
        with olefile.OleFileIO(self._file_name) as ole:
            # Open the fileheader stream
            fh = ole.openstream('FileHeader')
            fh_str = fh.read().decode('utf8')

            # Open the sectionkeys stream
            sk = ole.openstream('SectionKeys')
            sk_str = sk.read().decode('utf8')


        self._header_dict = altium_string_split(fh_str)
        self._section_keys_dict = altium_string_split(sk_str)


    def _update_item_list(self) -> None:
        """Generate a list. This will happen in the inherited class"""
        raise NotImplementedError()


class SchLib(AltiumFileType):
    """Main object to interact with schlib"""

    def _update_item_list(self) -> None:
        """Override main class, just update the list of items"""
        d = self._header_dict

        # Get the component count so we know what to look for
        item_count = int(altium_value_from_key(d, 'CompCount'))

        self._items_list = []

        sec_keys = sch_sectionkeys_to_list(self._section_keys_dict)

        # Loop through each item listed in the fileheader
        for i in range(0, item_count - 1):
            libref = altium_value_from_key(d, 'LibRef' + str(i))
            description = altium_value_from_key(d, 'CompDescr' + str(i))
            partcount = int(altium_value_from_key(d, 'PartCount' + str(i))) - 1

            if libref in sec_keys:
                sectionkey = sec_keys[libref]
            else:
                sectionkey = libref

            self._items_list.append({
                'libref': libref,
                'description': description,
                'partcount': partcount,
                'sectionkey': sectionkey
            })


    def list_items(self) -> list:
        return self._items_list
            



class SchLibItem():
    def __init__(self):
        pass

    # def __respr__(self):
    #     pass


class PcbLib(AltiumFileType):
    """Main object to interact with PCBLib"""
    def _update_item_list(self) -> None:
        pass

    def list_items(self) -> list:
        pass



class PcbLibItem():
    def __init__(self):
        pass

    # def __respr__(self):
    #     pass
