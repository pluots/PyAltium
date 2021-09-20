# PyAltium

A tool to process Altium file types. Currently only supports reading of .SchLib files.

## Example
```python
from pyaltium import SchLib

sl = SchLib('my_file_name')
print(SchLib.list_items())

```