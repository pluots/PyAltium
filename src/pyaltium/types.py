"""
types.py

Everything needed to interact with SchLib files
"""

import olefile
import pdb
from .helpers import (
    altium_string_split,
    altium_value_from_key,
    sch_sectionkeys_to_list
)

"""Magic Strings"""

SCHLIB_HEADER = 'HEADER=Protel for Windows - Schematic Library Editor Binary File Version 5.0'
PCBLIB_HEADER = 'PCB 6.0 Binary Library File'
MAX_READ_SIZE_BYTES = 65536

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
        """
        Check if file is valid (to the best of our ability) then update
        generic information
        """
        assert olefile.isOleFile(file_name)
        assert self._verify_file_type(file_name)
        self._file_name = file_name
        self._update_header_and_section_keys()
        self._update_item_list()

    def _update_header_and_section_keys(self) -> None:
        """Just update class's _header_dict object"""
        raise NotImplementedError()

    def _update_item_list(self) -> None:
        """Generate a list. This will happen in the inherited class"""
        raise NotImplementedError()

    def _verify_file_type(self, fname: str) -> bool:
        raise NotImplementedError()


class SchLib(AltiumFileType):
    """Main object to interact with schlib"""

    def _verify_file_type(self, fname:str) -> bool:
        """Check if our magic string is in the header"""
        with olefile.OleFileIO(fname) as ole:
            # Open the fileheader stream
            fh = ole.openstream('FileHeader')
            fh_str = fh.read(128).decode('utf8')

        return SCHLIB_HEADER in fh_str

    def _update_header_and_section_keys(self) -> None:
        """Just update class's _header_dict object"""
        with olefile.OleFileIO(self._file_name) as ole:
            # Open the fileheader stream
            fh = ole.openstream('FileHeader')
            fh_str = fh.read(MAX_READ_SIZE_BYTES).decode('utf8')

            # Open the sectionkeys stream
            sk = ole.openstream('SectionKeys')
            sk_str = sk.read(MAX_READ_SIZE_BYTES).decode('utf8')

        self._header_dict = altium_string_split(fh_str)
        self._section_keys_dict = altium_string_split(sk_str)

    def _update_item_list(self) -> None:
        """
        Override main class, just update the list of items
        
        Most of this information is kept in the file header. However, we need
        to get some information from sectionkeys.
        """
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
            


# class SchLibItem():
#     def __init__(self):
#         pass

    # def __respr__(self):
    #     pass


class PcbLib(AltiumFileType):
    """Main object to interact with PCBLib"""

    def _verify_file_type(self, fname: str) -> bool:
        """Check if our magic string is in the header"""
        with olefile.OleFileIO(fname) as ole:
            # Open the fileheader stream
            fh = ole.openstream('FileHeader')
            fh_str = fh.read(128).decode('utf8')

        return PCBLIB_HEADER in fh_str

    def _update_header_and_section_keys(self) -> None:
        """Just update class's _header_dict object"""
        with olefile.OleFileIO(self._file_name) as ole:
            # Open the fileheader stream
            fh = ole.openstream('FileHeader')
            fh_str = fh.read(MAX_READ_SIZE_BYTES).decode('utf8')

            # Open the sectionkeys stream
            sk = ole.openstream('SectionKeys')
            sk_str = sk.read(MAX_READ_SIZE_BYTES).decode('utf8')

        self._header_dict = altium_string_split(fh_str)
        self._section_keys_dict = altium_string_split(sk_str)

    def _update_item_list(self) -> None:
        with olefile.OleFileIO(self._file_name) as ole:
            # Just list storages. We will need to add something to integrate
            # SectionKeys at some point, but the PCBLib flavor of that
            # file makes 0 sense (yet)
            storages_list = ole.listdir(streams=False, storages=True)

            self._items_list = []

            # Need to select only items in storages_list with len 1 (any more
            # would be a subdir) then select 0th element (to get list of str
            # rather than list of list of str)
            for lib_item in (s for s in storages_list if len(s) == 1):
                # Ignore this metadata stream
                if ('fileversioninfo' in lib_item[0].lower()) or ('library' in lib_item[0].lower()):
                    continue

                # We want the paramaters stream within our storage
                lib_item.append('Parameters')

                param_bytestring = ole.openstream(
                    lib_item).read(MAX_READ_SIZE_BYTES)

                # First 4 bytes seem to be random noise
                param_bytestring = param_bytestring[4:]

                # Note: don't really want to ignore errors but
                # '3LED ArrayVertical 2mm TH' has a mystery character
                params_list = altium_string_split(
                    param_bytestring.decode('utf8', errors="ignore"))

                footprintref = altium_value_from_key(params_list, 'PATTERN')
                description = altium_value_from_key(params_list, 'DESCRIPTION')
                
                height_tmp = altium_value_from_key(params_list, 'HEIGHT').lower()

                if 'mm' in height_tmp:
                    height = round(float(height_tmp.replace('mm','')), 2)

                if 'mil' in height_tmp:
                    height = round(float(height_tmp.replace('mil', '')) * 0.0254, 2)

                self._items_list.append({
                    'footprintref': footprintref,
                    'description': description,
                    'height': height,
                })

            

    def list_items(self) -> list:
        return self._items_list



# class PcbLibItem():
#     def __init__(self):
#         pass

    # def __respr__(self):
    #     pass
