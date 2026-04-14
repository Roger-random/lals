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


class signal_head:
    def __init__(self):
        # Extra margin for 3D printed parts to fit.
        self.print_margin = 0.2

        # Back plate dictating exterior profile of the signal head.
        self.plate_width = inch_to_mm(3)
        self.plate_length = inch_to_mm(8)
        self.plate_thickness = inch_to_mm(3 / 8)
        self.plate_end_radius = self.plate_width / 2

        # Hood that shades a single light
        self.hood_outer_diameter = inch_to_mm(1.5)
        self.hood_thickness = inch_to_mm(3 / 16)
        self.hood_length_lower = inch_to_mm(3 / 4)
        self.hood_length_upper = inch_to_mm(1 + 5 / 8)
        self.hood_flat_height = inch_to_mm(1 / 8)

        # Hole in reference plate accommodated something but I don't know what.
        self.reference_hole_diameter = 27

        # Distance between top and bottom holes. (3-hole has additional at center.)
        self.hole_distance_2 = 61
        self.hole_distance_3 = 76.6

        # Distance between screw mounting holes.
        self.screw_mount_hole_distance = 123
        self.screw_mount_diameter = 4.6
        pass

    def plate(self, chamfer_surround=0, chamfer_end=5):
        plate_quarter = (
            cq.Workplane("YZ")
            .line(self.plate_end_radius, 0)
            .line(0, self.plate_length / 2 - self.plate_end_radius)
            .tangentArcPoint(endpoint=(-self.plate_end_radius, self.plate_end_radius))
            .close()
            .extrude(self.plate_thickness)
        )

        plate_half = plate_quarter + plate_quarter.mirror("XZ")

        plate = plate_half + plate_half.mirror("XY")

        if chamfer_surround > 0:
            plate = plate.faces("<X").chamfer(chamfer_surround)

        if chamfer_end > 0:
            end_cut = (
                cq.Workplane("XZ")
                .line(0, self.plate_length / 2 - chamfer_end, forConstruction=True)
                .line(chamfer_end, chamfer_end)
                .line(-chamfer_end, 0)
                .close()
                .extrude(self.plate_width, both=True)
            )
            plate = plate - end_cut

        return plate

    def hood(self):
        hood_tube = (
            cq.Workplane("YZ")
            .circle(self.hood_outer_diameter / 2)
            .circle(self.hood_outer_diameter / 2 - self.hood_thickness)
            .extrude(self.hood_length_upper)
        )

        hood_intersect = (
            cq.Workplane("XZ")
            .lineTo(self.hood_length_lower, 0)
            .lineTo(
                self.hood_length_upper,
                self.hood_outer_diameter / 2 - self.hood_flat_height,
            )
            .line(0, self.hood_flat_height)
            .line(-self.hood_length_upper, 0)
            .close()
            .extrude(self.hood_outer_diameter, both=True)
        )

        hood = (
            hood_tube.intersect(hood_intersect)
            .edges("|X")
            .fillet(self.hood_thickness / 3)
        )

        return hood

    def reference_hole_cut(self):
        hole_cut = (
            cq.Workplane("YZ")
            .circle(self.reference_hole_diameter / 2 + self.print_margin)
            .extrude(self.plate_thickness)
        )

        return hole_cut

    def screw_mount_holes_cut(self):
        hole = (
            cq.Workplane("YZ")
            .circle(self.screw_mount_diameter / 2 + self.print_margin)
            .extrude(self.plate_thickness)
        )

        hole_offset = self.screw_mount_hole_distance / 2

        return hole.translate((0, 0, hole_offset)) + hole.translate(
            (0, 0, -hole_offset)
        )

    def face_plate_2(self, screw_holes=False):
        back_plate = self.plate()
        hole_cut = self.reference_hole_cut()
        hood_add = self.hood()
        offset = self.hole_distance_2 / 2

        face_plate = (
            back_plate
            - hole_cut.translate((0, 0, -offset))
            - hole_cut.translate((0, 0, offset))
            + hood_add.translate((0, 0, -offset))
            + hood_add.translate((0, 0, offset))
        )

        if screw_holes:
            face_plate = face_plate - self.screw_mount_holes_cut()

        return face_plate

    def face_plate_3(self, screw_holes=False):
        back_plate = self.plate()
        hole_cut = self.reference_hole_cut()
        hood_add = self.hood()
        offset = self.hole_distance_3 / 2

        face_plate = (
            back_plate
            - hole_cut
            - hole_cut.translate((0, 0, -offset))
            - hole_cut.translate((0, 0, offset))
            + hood_add
            + hood_add.translate((0, 0, -offset))
            + hood_add.translate((0, 0, offset))
        )

        if screw_holes:
            face_plate = face_plate - self.screw_mount_holes_cut()

        return face_plate


sh = signal_head()

show_object(
    sh.face_plate_3(screw_holes=True), options={"color": "aliceblue", "alpha": 0.25}
)
