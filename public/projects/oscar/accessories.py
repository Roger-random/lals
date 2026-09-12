"""
MIT License

Copyright (c) 2026 Roger Cheng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import math
import cadquery as cq
import cadquery.selectors as sel
from cadquery import exporters

# When not running in CQ-Editor, turn log into print
if "log" not in globals():

    def log(*args):
        print(args)


# When not running in CQ-Editor, turn show_object into no-op
if "show_object" not in globals():

    def show_object(*args, **kwargs):
        pass


def inch_to_mm(length_inch: float):
    return length_inch * 25.4


class ns_oscar_accessories:
    def __init__(self):
        pass

    def volt_meter_box(self):
        """
        An enclosure for a commodity battery voltage meter and two magnets for
        holding it against Oscar's metal body where the locomotive engineer can
        see battery voltage.
        """
        box_outer = (
            cq.Workplane("XY")
            .rect(xLen=70, yLen=40)
            .workplane(offset=15)
            .rect(xLen=90, yLen=40)
            .loft()
            .faces(">Z")
            .workplane()
            .rect(xLen=90, yLen=40)
            .extrude(5)
            .edges("|Y")
            .edges("<<Z[1]")
            .fillet(2)
            .edges("|Z")
            .fillet(2)
        )

        box_inner = (
            cq.Workplane("XY")
            .rect(xLen=58, yLen=29)
            .workplane(offset=20)
            .rect(xLen=65, yLen=29)
            .loft()
        )

        magnet_slot = cq.Workplane("XY").circle(radius=15.5 / 2).extrude(
            -2.75
        ) + cq.Workplane("XY").circle(radius=2.75 / 2).extrude(-13)

        wire_slot = cq.Workplane("XZ").circle(radius=4).extrude(40)

        box = (
            box_outer
            - box_inner
            - magnet_slot.translate((35, 0, 20))
            - magnet_slot.translate((-35, 0, 20))
            - wire_slot.translate((0, 0, 20))
        )

        return box


noa = ns_oscar_accessories()

show_object(noa.volt_meter_box(), options={"color": "aliceblue", "alpha": 0.25})
