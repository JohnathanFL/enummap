# enummap
Maps all (explicitly marked) enums found in a file to their string names, allowing for easy conversions.
(Temporarily linux/max only)

To use:
- castxml must be installed and in your PATH
- include EnumMap.hpp
- Mark any enums (including enum classes) that you want stringified with the STRINGIFY macro (or the attribute annotation("Stringify"))
- run enummap.py with your source file, desired output file, and any extra include directories needed by the source file (limitation of castxml)
- Add the output file to your build
- Profit.
