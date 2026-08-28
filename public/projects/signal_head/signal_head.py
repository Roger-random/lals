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
    """
    3D-printed shapes to solve various problems relating to signals heads for
    traffic control on the train track layout for Los Angeles Live Steamers.
    Filament material must account for the harsh hot SoCal sunshine:
    * PLA will quickly deform and is pretty hopeless.
    * PETG is sufficient for experimentation but will only last a few months.
    * ASA (or some new hotness) for long-term deployment.
    """

    def __init__(self):
        # Extra margin for 3D printed parts to fit.
        self.print_margin = 0.2

        # Back plate dictating exterior profile of the signal head.
        self.plate_width = inch_to_mm(3)
        self.plate_length = inch_to_mm(8)
        self.plate_thickness = inch_to_mm(3 / 16)
        self.plate_end_radius = self.plate_width / 2

        # Dwarf plate that extends barely beyond the enclosure
        self.plate_dwarf_width = 46
        self.plate_dwarf_length = 137
        self.plate_dwarf_end_radius = self.plate_dwarf_width / 2

        # Hood that shades a single light
        self.hood_outer_diameter = inch_to_mm(1.5)
        self.hood_thickness = inch_to_mm(3 / 16)
        self.hood_length_upper = inch_to_mm(1.25)
        self.hood_flat_height = inch_to_mm(1 / 8)
        self.hood_length_lower = (
            self.hood_length_upper
            - self.hood_outer_diameter / 2
            + self.hood_flat_height
        )

        # Hole in reference plate accommodated something but I don't know what.
        self.reference_hole_diameter = 27

        # Distance between top and bottom holes. (3-hole has additional at center.)
        self.hole_distance_2 = inch_to_mm(2.5)
        self.hole_distance_3 = inch_to_mm(3)

        # Distance between screw mounting holes.
        self.screw_mount_hole_distance = 125
        self.screw_mount_hole_vertical_offset = 3.75
        self.screw_mount_diameter = (
            6  # Generously sized to accommodate enclosure variation
        )

        # "20mm" diameter acrylic lens dimensions rounded up 0.5mm for a bit of
        # wiggle room lining up with LED behind.
        self.lens_diameter_lip = 20.5
        self.lens_diameter_flat = 18
        self.lens_thickness = 10
        self.lens_mount_wall_thickness = 4
        self.lens_mount_lip_thickness = 2
        self.lens_mount_wall_chamfer = 2.5

        # Hold things together with zip-ties. If this idea works out I can then
        # justify spending time to design a better system.
        self.zip_tie_slot_width = 3
        self.zip_tie_slot_length = 7
        self.lens_pcb_width = 25
        self.fitting_width = inch_to_mm(2)

        # Dimensions for accommodating side marker lights
        self.side_marker_ring_radius_top = 18.7 / 2
        self.side_marker_ring_radius_bottom = 19 / 2
        self.side_marker_ring_thickness = 4.8

        self.side_marker_barrel_radius_outer = 29 / 2
        self.side_marker_barrel_thickness = 2.4
        self.side_marker_barrel_radius_inner = (
            self.side_marker_barrel_radius_outer - self.side_marker_barrel_thickness
        )
        self.side_marker_barrel_height = 15
        self.side_marker_barrel_taper_angle_radians = math.radians(55)
        self.side_marker_barrel_taper_height = (
            self.side_marker_barrel_radius_inner - self.side_marker_ring_radius_bottom
        ) / math.tan(self.side_marker_barrel_taper_angle_radians)
        self.side_marker_barrel_taper_start = (
            self.side_marker_barrel_height
            - self.side_marker_ring_thickness
            - self.side_marker_barrel_taper_height
        )
        self.side_marker_barrel_fillet = 0.5

    def plate(self, chamfer_surround: float = 0, chamfer_end: float = 0):
        """
        Returns plain back plate upon which all other signal head features are built.
        Optional chamfer all around by setting chamfer_surround to nonzero size in mm.
        Optional cut chamfer at top end by setting chamfer_end to nonzero size in mm.
        """
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
            plate = plate.faces().chamfer(chamfer_surround)

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

    def plate_dwarf(self):
        """
        Smaller back plate for dwarf signals that extend only a bit outside of
        the enclosure.
        """
        plate_quarter = (
            cq.Workplane("YZ")
            .line(self.plate_dwarf_end_radius, 0)
            .line(0, self.plate_dwarf_length / 2 - self.plate_dwarf_end_radius)
            .tangentArcPoint(
                endpoint=(-self.plate_dwarf_end_radius, self.plate_dwarf_end_radius)
            )
            .close()
            .extrude(self.plate_thickness)
        )

        plate_half = plate_quarter + plate_quarter.mirror("XZ")

        plate = plate_half + plate_half.mirror("XY")

        return plate

    def hood(self):
        """
        A hood sits over a light to provide minimal shade to help light visibility.
        Dimensions copied from reference 3D printed version, which looks a little
        different from the metal ones already on site.
        """
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

    def hood_2(self):
        """
        Now that I have an actual existing metal hood on hand, I will try to
        copy majority of its curvature. Intended to be a directly replacement
        to hood() so they can be swapped around as desired.
        """
        hood_2_outer_diameter = 44
        hood_2_thickness = 5
        hood_2_length = 36
        hood_2_outer_radius = hood_2_outer_diameter / 2
        hood_2_taper_degrees = 2
        hood_2_taper_radians = math.radians(hood_2_taper_degrees)
        hood_2_taper_radius = math.atan(hood_2_taper_radians) * hood_2_length
        hood_2_bottom_taper_degrees = 5
        hood_2_bottom_taper_length = hood_2_length / 2
        hood_2_bottom_taper_radians = math.radians(hood_2_bottom_taper_degrees)
        hood_2_bottom_taper_rise = (
            math.atan(hood_2_bottom_taper_radians) * hood_2_bottom_taper_length
        )

        hood_tube_outer = (
            cq.Workplane("YZ")
            .circle(hood_2_outer_radius)
            .workplane(hood_2_length)
            .circle(hood_2_outer_radius - hood_2_taper_radius)
            .loft()
        )

        hood_tube_inner = (
            cq.Workplane("YZ")
            .circle(hood_2_outer_radius - hood_2_thickness)
            .workplane(hood_2_length)
            .circle(hood_2_outer_radius - hood_2_thickness + hood_2_taper_radius)
            .loft()
        )

        hood_tube_intersect = (
            cq.Workplane("XZ")
            .lineTo(hood_2_bottom_taper_length, hood_2_bottom_taper_rise)
            .tangentArcPoint(
                (
                    hood_2_length,
                    hood_2_outer_radius - hood_2_thickness + hood_2_taper_radius,
                ),
                relative=False,
            )
            .lineTo(hood_2_length, hood_2_outer_radius)
            .lineTo(0, hood_2_outer_radius)
            .close()
            .extrude(hood_2_outer_diameter, both=True)
        )

        hood = (hood_tube_outer - hood_tube_inner).intersect(hood_tube_intersect)

        return hood

    def reference_hole_cut(self):
        """
        Object to use to subtract for cutting a hole for one of the lights.
        Dimension copied from reference 3D printed object, not sure what this
        hole is supposed to fit.
        """
        hole_cut = (
            cq.Workplane("YZ")
            .circle(self.reference_hole_diameter / 2 + self.print_margin)
            .extrude(self.plate_thickness)
        )

        return hole_cut

    def screw_mount_holes_cut(self):
        """
        A two-part object for cutting mounting screw holes.
        """
        hole = (
            cq.Workplane("YZ")
            .circle(self.screw_mount_diameter / 2 + self.print_margin)
            .extrude(inch_to_mm(3))
        )

        hole_offset = self.screw_mount_hole_distance / 2

        return hole.translate((0, 0, hole_offset)) + hole.translate(
            (0, 0, -hole_offset)
        )

    def zip_tie_slot(self, distance):
        """
        Two-part object for two symmetric zip 'distance' from vertical center
        """
        offset = distance / 2 + self.zip_tie_slot_width / 2
        slot_cut = (
            cq.Workplane("YZ")
            .rect(xLen=self.zip_tie_slot_width, yLen=self.zip_tie_slot_length)
            .extrude(self.plate_thickness)
        )

        ties_cut = slot_cut.translate((0, offset, 0)) + slot_cut.translate(
            (0, -offset, 0)
        )

        return ties_cut

    def zip_ties_cut(self):
        """
        Cut slots for zip ties.
        """

        pcb_slots = self.zip_tie_slot(self.lens_pcb_width)
        body_slots = self.zip_tie_slot(self.fitting_width)

        return pcb_slots + body_slots

    def lens_mount_add(self):
        """
        Volume to be added for mounting a 20mm acrylic lens, then subtracted
        by counterpart cut shape.
        """
        add = (
            cq.Workplane("YZ")
            .circle(radius=self.lens_diameter_lip / 2 + self.lens_mount_wall_thickness)
            .extrude(self.lens_thickness + self.lens_mount_lip_thickness)
            .faces(">X")
            .chamfer(self.lens_mount_wall_chamfer)
        )

        return add

    def lens_mount_cut(self):
        """
        After adding volume of counterpart add shape, subtract this cut shape.
        """
        cut_main = (
            cq.Workplane("YZ")
            .circle(radius=self.lens_diameter_lip / 2 + self.print_margin)
            .extrude(self.lens_thickness)
        )

        cut_leave_lip = (
            cq.Workplane("YZ")
            .circle(radius=self.lens_diameter_flat / 2 + self.print_margin)
            .extrude(self.lens_thickness * 2)
        )

        cut_base_flare = (
            cq.Workplane("YZ")
            .circle(
                radius=self.lens_diameter_lip / 2
                + self.print_margin
                + self.lens_mount_wall_chamfer
            )
            .workplane(offset=self.lens_mount_wall_chamfer)
            .circle(radius=self.lens_diameter_lip / 2 + self.print_margin)
            .loft()
            .faces(">X")
            .workplane()
            .circle(radius=self.lens_diameter_lip / 2 + self.print_margin)
            .extrude(self.lens_thickness - self.lens_mount_wall_chamfer)
            .faces(">X")
            .workplane()
            .circle(radius=self.lens_diameter_lip / 2 + self.print_margin)
            .workplane(offset=self.lens_mount_lip_thickness)
            .circle(
                radius=self.lens_diameter_lip / 2
                + self.print_margin
                - self.lens_mount_lip_thickness
            )
            .loft()
        )

        cut = cut_base_flare

        return cut

    def face_plate(self, lights):
        """
        Generate a face plate for number of lights as per 'lights' param
        Screw mounting holes optional. (Defaults to none.)
        """
        face_plate = self.plate(chamfer_surround=0, chamfer_end=0)
        mount_add = self.side_marker_barrel_outer()
        hole_cut = self.side_marker_barrel_inner()
        hood_add = self.hood_2()

        if lights == 3:
            offset = self.hole_distance_3 / 2
            face_plate = (
                face_plate
                + mount_add.translate((0, 0, -self.screw_mount_hole_vertical_offset))
                + mount_add.translate(
                    (0, 0, -self.screw_mount_hole_vertical_offset - offset)
                )
                + mount_add.translate(
                    (0, 0, -self.screw_mount_hole_vertical_offset + offset)
                )
                - hole_cut.translate((0, 0, -self.screw_mount_hole_vertical_offset))
                - hole_cut.translate(
                    (0, 0, -self.screw_mount_hole_vertical_offset - offset)
                )
                - hole_cut.translate(
                    (0, 0, -self.screw_mount_hole_vertical_offset + offset)
                )
                + hood_add.translate((0, 0, -self.screw_mount_hole_vertical_offset))
                + hood_add.translate(
                    (0, 0, -self.screw_mount_hole_vertical_offset - offset)
                )
                + hood_add.translate(
                    (0, 0, -self.screw_mount_hole_vertical_offset + offset)
                )
            )
        elif lights == 2:
            offset = self.hole_distance_2 / 2

            face_plate = (
                face_plate
                + mount_add.translate((0, 0, -offset))
                + mount_add.translate((0, 0, offset))
                - hole_cut.translate((0, 0, -offset))
                - hole_cut.translate((0, 0, offset))
                + hood_add.translate((0, 0, -offset))
                + hood_add.translate((0, 0, offset))
            )
        elif lights == 1:
            face_plate = face_plate + mount_add - hole_cut + hood_add
            pass
        else:
            raise ValueError(
                f"Not yet able to generate face plate for {lights} lights."
            )

        face_plate = face_plate - self.screw_mount_holes_cut()

        return face_plate

    def dwarf(self):
        """
        Dwarf signal faceplate using side marker LED modules.
        """
        plate_base = self.plate_dwarf()
        hood_add = self.hood_2()
        hole_cut = self.side_marker_barrel_inner()
        mount_add = self.side_marker_barrel_outer()

        offset = self.hole_distance_2 / 2

        face_plate = (
            plate_base
            + mount_add.translate((0, 0, -offset))
            + mount_add.translate((0, 0, offset))
            - hole_cut.translate((0, 0, -offset))
            - hole_cut.translate((0, 0, offset))
            + hood_add.translate((0, 0, -offset))
            + hood_add.translate((0, 0, offset))
        )

        face_plate = face_plate - self.screw_mount_holes_cut()

        return face_plate

    def side_marker_fit_test(self):
        """
        Small object to fit a commodity vehicle side marker light module.

        Firsthand experience found the modules aren't as uniform across
        manufacturers as I had hoped. While it is possible there's a hole
        size where they'll all fit (loosely or tightly) I'm going to treat
        them as different sizes.
        """

        ring_radius = 15
        hole_height = 10

        radius_g = 19 / 2
        radius_ry = 18.7 / 2
        height_g = 4.8
        height_ry = 5.3

        fit_test_plate = cq.Workplane("XY").rect(xLen=110, yLen=40).extrude(3)
        fit_test_plate = fit_test_plate.edges("|Z").fillet(10)

        ring_g = cq.Workplane("XY").circle(radius=ring_radius).extrude(height_g)
        hole_g = cq.Workplane("XY").circle(radius=radius_g).extrude(hole_height)

        ring_ry = cq.Workplane("XY").circle(radius=ring_radius).extrude(height_ry)
        hole_ry = cq.Workplane("XY").circle(radius=radius_ry).extrude(hole_height)

        fit_test_plate = (
            fit_test_plate
            + ring_g.translate((-35, 0, 0))
            + ring_ry
            + ring_ry.translate((35, 0, 0))
            - hole_g.translate((-35, 0, 0))
            - hole_ry
            - hole_ry.translate((35, 0, 0))
        )

        return fit_test_plate

    def side_marker_barrel_outer(self):
        """
        A barrel shape to accommodate side marker LED modules. Used to build
        the outer volume, follow by subtraction of matchining inner shape.
        """
        return (
            cq.Workplane("YZ")
            .circle(radius=self.side_marker_barrel_radius_outer)
            .extrude(self.side_marker_barrel_height)
            .faces(">X")
            .fillet(self.side_marker_barrel_fillet)
        )

    def side_marker_barrel_inner(self):
        """
        Shape for cutting a cavity to accommodate side marker LED modules out
        of the matching outer shape.
        """
        return (
            cq.Workplane("YZ")
            .circle(radius=self.side_marker_barrel_radius_inner)
            .extrude(self.side_marker_barrel_taper_start)
            .faces(">X")
            .workplane()
            .circle(radius=self.side_marker_barrel_radius_inner)
            .workplane(self.side_marker_barrel_taper_height)
            .circle(radius=self.side_marker_ring_radius_bottom)
            .loft()
            .faces(">X")
            .workplane()
            .circle(radius=self.side_marker_ring_radius_bottom)
            .workplane(self.side_marker_ring_thickness)
            .circle(radius=self.side_marker_ring_radius_top)
            .loft()
        )

    def side_marker_test_ring(self):
        """
        The commodity side marker LED modules vary more than I had thought
        they would. This is the (futile?) search for a design that can fit all
        of them. It takes advantage of the fact they all have a rubber surround
        for some dimensional tolerance. It may not be a perfect fit for all of
        the different vendors, but maybe I can find a point where they can all
        fit snugly enough for our purposes.
        """
        barrel_outer = self.side_marker_barrel_outer()

        barrel_inner = self.side_marker_barrel_inner()

        marker_housing = barrel_outer - barrel_inner

        return marker_housing

    def absolute_sign(self):
        """
        Some of the absolute signs are in very bad shape. This is an effort to
        create 3D-printed replacements.
        """
        width = inch_to_mm(4)
        height = inch_to_mm(4)
        thickness = inch_to_mm(1 / 8)
        fillet = inch_to_mm(0.25)
        hole_spacing = inch_to_mm(3 + 1 / 16)
        hole_diameter = inch_to_mm(5 / 32)

        back = (
            cq.Workplane("XY")
            .rect(xLen=width, yLen=height)
            .extrude(thickness)
            .edges("|Z")
            .fillet(fillet)
            .edges()
            .chamfer(0.6)
        )

        hole = cq.Workplane("XY").circle(radius=hole_diameter / 2).extrude(thickness)

        text = (
            cq.Workplane("XY")
            .transformed(offset=(0, inch_to_mm(0.2)))
            .text(txt="A", fontsize=110, distance=thickness + 1, font="Arial Black")
        )

        sign = (
            back
            - hole.translate((hole_spacing / 2, 0, 0))
            - hole.translate((-hole_spacing / 2, 0, 0))
            + text
        )

        return sign

    def type_v_face_plate(self):
        """
        The "type V" or "V style" signal consists of three separate lights on a
        large circular faceplate located on the same circular radius about the
        center but 120 degrees apart. Green is to the upper left, yellow upper
        right, and red is directly below center. At the moment there is no plan
        on how to upgrade these automotive-style bulb sockets to newer LED
        types so I'm experimenting with commodity vehicle side marker LEDs.
        """
        plate_radius = inch_to_mm(8) / 2
        plate_thickness = inch_to_mm(1 / 8)
        mounting_hole_offset_h = inch_to_mm(6) / 2
        mounting_hole_offset_v = inch_to_mm(4 + 1 / 8) / 2
        mounting_hole_radius = inch_to_mm(3 / 16) / 2
        mounting_hole_bevel_radius = inch_to_mm(3 / 8) / 2
        mounting_hole_bevel_height = mounting_hole_bevel_radius - mounting_hole_radius
        placement_radius = inch_to_mm(4 + 1 / 4) / 2

        placement_offset_v = math.cos(math.radians(60)) * placement_radius
        placement_offset_h = math.sin(math.radians(60)) * placement_radius

        hole_radius = 19 / 2

        plate = cq.Workplane("YZ").circle(plate_radius).extrude(plate_thickness)

        hole_cut = cq.Workplane("YZ").circle(hole_radius).extrude(20)

        ring_radius = 15
        height_g = 4.8
        height_ry = 5.3

        ring_g = cq.Workplane("YZ").circle(radius=ring_radius).extrude(height_g)
        ring_ry = cq.Workplane("YZ").circle(radius=ring_radius).extrude(height_ry)

        hood = self.hood_2()

        translate_g = (0, -placement_offset_h, placement_offset_v)
        translate_y = (0, placement_offset_h, placement_offset_v)
        translate_r = (0, 0, -placement_radius)

        mounting_hole = (
            cq.Workplane("YZ")
            .circle(mounting_hole_radius)
            .extrude(plate_thickness - mounting_hole_bevel_height)
            .faces(">X")
            .workplane()
            .circle(mounting_hole_radius)
            .workplane(mounting_hole_bevel_height)
            .circle(mounting_hole_bevel_radius)
            .loft()
        )

        face_plate = (
            plate
            + ring_g.translate(translate_g)
            + ring_ry.translate(translate_y)
            + ring_ry.translate(translate_r)
            + hood.translate(translate_g)
            + hood.translate(translate_y)
            + hood.translate(translate_r)
            - hole_cut.translate(translate_g)
            - hole_cut.translate(translate_y)
            - hole_cut.translate(translate_r)
            - mounting_hole.translate(
                (0, mounting_hole_offset_h, mounting_hole_offset_v)
            )
            - mounting_hole.translate(
                (0, -mounting_hole_offset_h, mounting_hole_offset_v)
            )
            - mounting_hole.translate(
                (0, mounting_hole_offset_h, -mounting_hole_offset_v)
            )
            - mounting_hole.translate(
                (0, -mounting_hole_offset_h, -mounting_hole_offset_v)
            )
        )

        return face_plate

    def dome_searchlight(self):
        """
        Found a RGB status indicator light that is intended to be a more
        compact all-in-one version of a vertical stack light. However,
        if we turn it sideways, it might work for a searchlight-type
        signal. This is the 3D-printed back plate to give it the right
        shape to look like it belong. The back side is flat until I figure
        out how it'll be mounted on the pillar.
        """
        back_plate_radius = inch_to_mm(6) / 2
        back_plate_thickness = inch_to_mm(3 / 16)
        through_hole_radius = 32 / 2
        body_clearance_radius = 51 / 2

        back_plate = (
            cq.Workplane("YZ")
            .circle(back_plate_radius)
            .circle(body_clearance_radius)
            .extrude(back_plate_thickness)
        )

        # Can either protrude or be a recess depending on aesthetic preferences
        dome_area = (
            cq.Workplane("YZ")
            .circle(body_clearance_radius)
            .circle(through_hole_radius)
            .extrude(back_plate_thickness)
        )

        hood = (
            self.hood_2()
        )  # .val().scale(1.6) # VSCode really doesn't like the 1.6X scale. Not sure why?

        searchlight = back_plate + dome_area + hood

        return searchlight


sh = signal_head()

show_object(sh.dwarf(), options={"color": "green", "alpha": 0.25})
