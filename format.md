# Ole Overview

OLE is a Microsoft format that is basically a zip format. It contains a mix of "streams" (files) and "storages" (directories).

Lots of good information about Altium storage is here: https://github.com/vadmium/python-altium/blob/master/format.md

## SchLib

The top level is a storage for every symbol. For example:

```
pp.pprint(o.listdir(streams=False,storages=True))
[   ['BJT - NPN'],
    ['BJT - NPN_NumberedPins'],
    ['BJT - PNP'],
    ['BJT - PNP_NumberedPins'],
    ['Capacitor - Bipolar'],
    ['Capacitor - Feedthrough'],
    ['Capacitor - Unipolar'],
    ['Crystal - 2 Lead'],
    ['Crystal - 4 Lead GND'],
    ['Crystal - 4 Lead NC'],
```

In addition, there are three file streams with metadata:

```
>>> li = o.listdir(streams=True,storages=False)
>>> for i in li:
...     if len(i) == 1: print(i)
...
['FileHeader']
['SectionKeys']
['Storage']
```

### Metadata

#### FileHeader

This is a `|` separated file, starting with
`f  |HEADER=Protel for Windows - Schematic Library Editor Binary File Version 5.0`

Up next we have `|Weight=3892`, which is something to do with number of objects.

`|MinorVersion=2|UniqueID=AXPYTAHO` don't know what that means

```
FontIdCount=13
Size1=10
FontName1=Times New Roman
Size2=8
FontName2=Calibri
...
Size13=9
Rotation13=90
FontName13=Times New Roman
```

A list of all the fonts, their sizes, and optionally rotation.

```
UseMBCS=T
IsBOC=T
SheetStyle=9
BorderOn=T
SheetNumberSpaceSize=12
AreaColor=16317695
SnapGridOn=T
SnapGridSize=5
VisibleGridOn=T
VisibleGridSize=10
CustomX=18000
CustomY=18000
UseCustomSheet=T
ReferenceZonesOn=T
Display_Unit=0
CompCount=107
```

First two things: no clue. Rest: pretty self-explanatory

```
PartCount3=2
LibRef4=Oscillator - 6PIN, Programmable
CompDescr4=I2C Programmable Osc. with Diff Output
PartCount4=2
LibRef5=MOSFET - P-Channel, Enhancement-Mode, 3 Pin
CompDescr5=Numbered G1,S2,D3
PartCount5=2
LibRef6=MOSFET - P-Channel, Depletion-Mode, 3 Pin
PartCount6=2
LibRef7=MOSFET - N-Channel, Enhancement-Mode, 3 Pin
PartCount7=2
LibRef8=MOSFET - N-Channel, Depletion-Mode, 3 Pin
PartCount8=2
LibRef9=Inductor - Choke, Common Mode, 5 pin
PartCount9=2
```

The rest of the file is the actual components.

#### SectionKeys

Also a |sv type file.

```
>	  |KeyCount=26
LibRef0=Diode - Bridge Rectifier 1,2 DC
SectionKey0=Diode - Bridge Rectifier 1,2 DC
...
LibRef18=MOSFET - N-Channel, Enhancement-Mode, 3 Pin
SectionKey18=MOSFET - N-Channel, Enhancement
LibRef19=MOSFET - P-Channel, Depletion-Mode, 3 Pin
SectionKey19=MOSFET - P-Channel, Depletion-M
LibRef20=MOSFET - P-Channel, Enhancement-Mode, 3 Pin
SectionKey20=MOSFET - P-Channel, Enhancement
```

All the stuff that gets truncated in the main content section. This file is easy.
May not be present

#### Storage

It starts out as so:
`   |HEADER=Icon storage `
Presumably this is where images are kept

### Main Contents

The main content is a bunch of storages:

```
['Diode - TVS, 1xDiff'],
['Diode - TVS, 1xDiff Route Thro1'],
['Diode - TVS, 1xDiff Route Throu'],
['Diode - TVS, 2xDiff Route Throu'],
```

Note some names are truncated and stored as mentioned aboved.

Each of these storages contains a "Data" stream, and optionally a "PinTextData" stream. Both of these are pretty encoded and need some figuring out.

#### Data

Four bytes at the beginning followed by the first |RECORD

It appears that pin descriptions start with `00 xx`. Usually this follows `AllPinCount=n`,
but I also saw it someplace random once. They are separated with `|&|` (`7c 26 7c`).

UniqueID seems to always have `00 0B 00 00 00` after its value.

At the very end of the file, there is an extra `00`.

#### Pins
Pins are very weird

`00[^0]{2}0000010` seems to work as separator for whatever reason. Maybe use sep at end
of line.

These seem to be big endian. Position unit is 0.01 in (10 mil).

#### PinTextData

Starts with `1D 00 00 00`

Next has `|HEADER=PinTextData|Weight=n` where n is the number of pins.

`01 0a` is the separator

Next is a separator `00 00 01` that is the separator for all pins.

## PCBLib

### Name

The name seems to always start after the first 0x000000 followed by one more garbage
byte. Either of the following could start:

`xx 00 00 00 xx`
`xx xx 00 00 00 xx`

And they always end in:
`xx xx 00 00 00`

### Data

It seems like PCBLib components have pads stored similarly to schematics -
separated by `|&|`. This is also binary and will be tough to decode.

Seems like rotation is stored as a 64 bit float, little endian

#### Component.UniqueIDPrimitiveInformation/
This file just keeps track of pads in the footprint. It is basically readable.

#### Component.Parameters
This file tells you name, height, description, grid, and guide information. It
is parsable.

#### Component.Data
Starts with `xx 00 00 00 nn` where nn is the length of the name, which comes
next. Possibly more of these bytes are for name length.

After the name, it jumps immediately into a type.

##### Pads
Names start with an int giving their length

Indexing after the end of the name. Everything seems to be little endian.

Positions are 32 bit signed

Index 72:79 has X position, and 80:87 has the y position. These are 32 bit
ints in 1e-7 inches (2.54nm resolution). Multiply this value by 2.54e-6 to
get mm, 2.54e-6, 2.54e-3 to get um.

150:165 is rotation as degrees, float
