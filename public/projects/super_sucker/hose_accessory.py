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


class hose_accessory:
    def __init__(self):
        # Extra margin for 3D printed parts to fit.
        self.print_margin = 0.2

        self.handle_outer_radius = inch_to_mm(4 + 7 / 8) / 2
        self.hose_inner_radius = inch_to_mm(5 + 1 / 16) / 2

        pass

    def adapter_sleeve(self, sleeve_length, sleeve_twist_angle, sleeve_gap_width=3):

        sleeve_shell = (
            cq.Workplane("XY")
            .circle(radius=self.handle_outer_radius)
            .circle(radius=self.hose_inner_radius)
            .extrude(sleeve_length)
            .faces("+Z")
            .fillet(inch_to_mm(1 / 32))
        )

        sleeve_slot = (
            cq.Workplane("XY")
            .rect(
                xLen=self.hose_inner_radius * 2,
                yLen=sleeve_gap_width,
                centered=(False, True),
            )
            .workplane(offset=sleeve_length)
            .transformed(rotate=(0, 0, sleeve_twist_angle))
            .rect(
                xLen=self.hose_inner_radius * 2,
                yLen=sleeve_gap_width,
                centered=(False, True),
            )
            .loft()
        )

        return sleeve_shell - sleeve_slot


ha = hose_accessory()

adapter_sleeve = ha.adapter_sleeve(
    sleeve_length=inch_to_mm(2.75), sleeve_twist_angle=45, sleeve_gap_width=1
)

show_object(adapter_sleeve, options={"color": "green", "alpha": 0.25})
