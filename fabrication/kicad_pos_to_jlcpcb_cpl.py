#!/usr/bin/python3

# Copyright 2022 Carsten Andrich <base64decode("Y2Fyc3Rlblx4NDBhbmRyaWNoXHgyZW5hbWU=")>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Converts KiCAD v6 position files to JLCPCB's CPL format.
"""

from collections import OrderedDict
import csv
import sys

# rows of KiCAD position file
KICAD_ROWS = ["Ref", "Val", "Package", "PosX", "PosY", "Rot", "Side"]

# translation from KiCAD rows to JCLPCB's CPL row expectations
TRANSLATION = OrderedDict([
    ("Ref",     "Designator"),
    ("Val",     "Value"),
    ("Package", "Footprint"),
    ("PosX",    "Mid X"),
    ("PosY",    "Mid Y"),
    ("Side",    "Layer"),
    ("Rot",     "Rotation")
])

with \
open(sys.argv[1], "rt") as infile, \
open(sys.argv[2], "wt") as outfile:
    # read input (KiCAD position file) and verify rows
    reader = csv.DictReader(infile)
    if reader.fieldnames != KICAD_ROWS:
        raise ValueError(f"unexpected input rows: {reader.fieldnames}")

    # write output header
    writer = csv.DictWriter(outfile, fieldnames=TRANSLATION.values())
    writer.writeheader()

    # translate and write output
    for kicad in reader:
        jlcpcb = {}
        for kicad_field, jlcpcb_field in TRANSLATION.items():
            jlcpcb[jlcpcb_field] = kicad[kicad_field]
        writer.writerow(jlcpcb)

