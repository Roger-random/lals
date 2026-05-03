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


class warning_light:
    def __init__(self):
        self.base_inner_diameter = 33
        self.base_outer_diameter = 37
        self.tip_outer_diameter = 32
        self.base_height = 9
        self.funnel_height = 26
        self.tip_height = 32
        self.thickness = (self.base_outer_diameter - self.base_inner_diameter) / 2

    def inside_cavity(self):
        funnel_rise = self.tip_height - self.base_height - self.thickness
        funnel_inside_radius = (self.tip_outer_diameter / 2) - self.thickness
        return (
            cq.Workplane("XY")
            .circle(radius=self.base_inner_diameter / 2)
            .extrude(self.base_height)
            .faces(">Z")
            .workplane()
            .circle(radius=self.base_inner_diameter / 2)
            .workplane(offset=funnel_rise)
            .circle(radius=funnel_inside_radius)
            .loft()
        )

    def cover(self):
        return self.inside_cavity().faces("<Z").shell(thickness=self.thickness)

    def cover_vase(self):
        return self.cover() + self.inside_cavity()


wl = warning_light()

show_object(wl.cover_vase(), options={"color": "aliceblue", "alpha": 0.25})
