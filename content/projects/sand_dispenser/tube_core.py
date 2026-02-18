"""
MIT License

Copyright (c) 2025 Roger Cheng

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


class tube_core:
    def __init__(self):
        # Extra margin for 3D printed parts to fit.
        self.print_margin = 0.2

        # Measured dimensions of tube
        self.tube_diameter_inner = 101.5
        self.tube_diameter_outer = 109

        # Extra margin to make ends easy to mount/dismount from tube.
        self.tube_margin = 0.25

    def end_fit_test(self):
        flange_thickness = 1.6
        flange_height = 10

        inner_flange = (
            cq.Workplane("XY")
            .circle(radius=self.tube_diameter_inner / 2 - self.tube_margin)
            .circle(
                radius=self.tube_diameter_inner / 2
                - self.tube_margin
                - flange_thickness
            )
            .extrude(flange_height)
        )

        outer_flange = (
            cq.Workplane("XY")
            .circle(
                radius=self.tube_diameter_outer / 2
                + self.tube_margin
                + flange_thickness
            )
            .circle(radius=self.tube_diameter_outer / 2 + self.tube_margin)
            .extrude(flange_height)
        )

        bottom_plate = (
            cq.Workplane("XY")
            .circle(
                radius=self.tube_diameter_outer / 2
                + self.tube_margin
                + flange_thickness
            )
            .circle(radius=self.tube_diameter_inner / 2 - flange_height)
            .extrude(-flange_thickness)
        )
        return inner_flange + outer_flange + bottom_plate


tc = tube_core()

show_object(tc.end_fit_test(), options={"color": "green", "alpha": 0.25})
