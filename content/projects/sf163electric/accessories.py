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


class accessories:
    def __init__(self):
        pass

    def exhaust_fan_ring(self):
        """
        The body features a trio of cosmetic nonfunctional fan grates that
        are held into their surrounding ring by an adhesive that has broken
        down due to age. Rather than gluing it back in, where the ring will
        still be against gravity, I thought I would try 3D-printing a ring
        beneath the outermost area of the ring to support it from beneath.
        This should work better when someone accidentally leans on it.
        """
        inner_radius = inch_to_mm(6 + 1 / 16) / 2
        outer_radius = inner_radius + inch_to_mm(1 / 16)

        # Outer height - metal wire diameter - height of the surround
        height = inch_to_mm(3 / 4 - 1 / 16) - 1

        ring = (
            cq.Workplane("XY").circle(outer_radius).circle(inner_radius).extrude(height)
        )
        return ring


a = accessories()

show_object(a.exhaust_fan_ring(), options={"color": "aliceblue", "alpha": 0.25})
