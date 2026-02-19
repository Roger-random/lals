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
        self.tube_margin = 0.5

        # IBLS standard wheel gauge parameters for 7.5" gauge
        # http://ibls.org/mediawiki/index.php?title=IBLS_Wheel_Standard
        # Properly written CadQuery code should be able to accept
        # parameters for another gauge and generate an IBLS conforming
        # wheel profile. (This is not an immediate goal.)
        self.ibls_TG = inch_to_mm(7.5)  # Track Gauge
        self.ibls_T_min = inch_to_mm(0.75)  # Tire width
        self.ibls_W_max = inch_to_mm(0.156)  # Flange width
        self.ibls_F_max = inch_to_mm(0.187)  # Flange depth
        self.ibls_R_min = inch_to_mm(0.094)  # Contour radius
        self.ibls_R_max = inch_to_mm(0.125)
        self.ibls_r = inch_to_mm(0.062)  # Flange radius (typical)
        self.ibls_B = inch_to_mm(7.120)  # Back to back
        self.ibls_WG = inch_to_mm(7.44)  # Wheel gauge
        self.ibls_WC = inch_to_mm(7.281)  # Wheel check
        self.ibls_flange_taper_radians = math.radians(10)  # 10 degrees
        self.ibls_wheel_taper_radians = math.radians(2.5)  # 2.5 degrees

    def wheel(self, diameter: float, apply_fillet: bool = True):
        """
        Generate a wheel of the specified diameter that conforms to IBLS
        standard gauge requirements.

        :param self: class instance
        :param diameter: diameter of wheel in mm
        :type diameter: float
        """

        # Generate the core wheel flange shape
        wheel_flange_half = self.ibls_W_max / 2
        no_fillet_flange_distance = wheel_flange_half / math.tan(
            self.ibls_flange_taper_radians
        )
        wheel_flange = (
            cq.Workplane("XY")
            .lineTo(diameter / 2, 0)
            .line(no_fillet_flange_distance, wheel_flange_half)
            .line(-no_fillet_flange_distance, wheel_flange_half)
            .line(-diameter / 2, 0)
            .close()
            .revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(0, 1, 0))
        )

        # Generate the core wheel shape
        wheel_slope_distance = self.ibls_T_min * math.tan(self.ibls_wheel_taper_radians)
        wheel_core = (
            cq.Workplane("XY")
            .lineTo(diameter / 2, 0)
            .line(-wheel_slope_distance, -self.ibls_T_min)
            .lineTo(0, -self.ibls_T_min)
            .close()
            .revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(0, 1, 0))
        )

        # Assemble wheel
        wheel = wheel_flange + wheel_core

        if apply_fillet:
            # Apply fillet between wheel core and flange
            wheel = wheel.edges(sel.NearestToPointSelector((0, 0, 0))).fillet(
                radius=self.ibls_R_max
            )

            # Apply fillet to flange
            wheel = wheel.edges(
                sel.NearestToPointSelector((0, wheel_flange_half, 0))
            ).fillet(radius=self.ibls_r)

        return wheel

    def end_fit_test(self, flange_thickness=1.6, flange_height=10):
        """
        Minimalist plastic ring used to verify proper fit on tube with
        specified dimensions.
        """

        inner_flange = (
            cq.Workplane("XZ")
            .circle(radius=self.tube_diameter_inner / 2 - self.tube_margin)
            .circle(
                radius=self.tube_diameter_inner / 2
                - self.tube_margin
                - flange_thickness
            )
            .extrude(flange_height)
        )

        outer_flange = (
            cq.Workplane("XZ")
            .circle(
                radius=self.tube_diameter_outer / 2
                + self.tube_margin
                + flange_thickness
            )
            .circle(radius=self.tube_diameter_outer / 2 + self.tube_margin)
            .extrude(flange_height)
        )

        bottom_plate = (
            cq.Workplane("XZ")
            .circle(
                radius=self.tube_diameter_outer / 2
                + self.tube_margin
                + flange_thickness
            )
            .circle(radius=self.tube_diameter_inner / 2 - flange_height)
            .extrude(-flange_thickness)
        )
        return inner_flange + outer_flange + bottom_plate

    def endcap_wheel(self, diameter: float):
        base_wheel = self.wheel(diameter)

        tube_flange = self.end_fit_test(flange_thickness=3.6, flange_height=15).mirror(
            "XZ"
        )

        bearing_radius = 11
        bearing_subtract = (
            cq.Workplane("XZ")
            .transformed(offset=(0, 0, self.ibls_T_min))
            .circle(radius=bearing_radius + self.print_margin)
            .extrude(-7)
            .faces(">Y")
            .workplane()
            .circle(radius=bearing_radius + self.print_margin)
            .workplane(offset=bearing_radius / 2)
            .circle(radius=bearing_radius / 2)
            .loft()
        )

        sand_outlet_diameter = 4

        sand_funnel = (
            cq.Workplane("XY")
            .line(
                diameter / 2 - sand_outlet_diameter,
                -sand_outlet_diameter - self.ibls_R_max * 1.5,
            )
            .line(0, sand_outlet_diameter)
            .lineTo(
                self.tube_diameter_inner / 2 - self.tube_margin - 3.6, self.ibls_W_max
            )
            .line(0, 25 - self.ibls_W_max)
            .lineTo(0, 25)
            .close()
            .revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(0, 1, 0))
        )

        sand_outlet_count = 18
        sand_outlet_angle_degrees = 360 / sand_outlet_count
        sand_outlet = (
            cq.Workplane("XY")
            .transformed(
                offset=(
                    0,
                    -self.ibls_R_max * 1.5 - sand_outlet_diameter / 2,
                    diameter / 2 - sand_outlet_diameter,
                )
            )
            .circle(sand_outlet_diameter / 2)
            .extrude(diameter / 2)
        )
        outlet_reinforcement = (
            cq.Workplane("ZY")
            .line(
                diameter / 2 - sand_outlet_diameter,
                -sand_outlet_diameter - self.ibls_R_max * 1.5,
            )
            .line(0, sand_outlet_diameter)
            .lineTo(
                self.tube_diameter_inner / 2 - self.tube_margin - 3.6, self.ibls_W_max
            )
            .close()
            .extrude(sand_outlet_diameter / 2, both=True)
            .rotate((0, 0, 0), (0, 1, 0), sand_outlet_angle_degrees / 2)
        )
        sand_outlet_collection = sand_outlet
        outlet_reinforcement_collection = outlet_reinforcement
        for outlet_count in range(1, sand_outlet_count):
            sand_outlet_collection += sand_outlet.rotate(
                (0, 0, 0), (0, 1, 0), sand_outlet_angle_degrees * outlet_count
            )
            outlet_reinforcement_collection += outlet_reinforcement.rotate(
                (0, 0, 0), (0, 1, 0), sand_outlet_angle_degrees * outlet_count
            )

        endcap = (
            base_wheel
            + tube_flange
            - bearing_subtract
            - sand_funnel
            - sand_outlet_collection
            + outlet_reinforcement_collection
        )

        return endcap


tc = tube_core()

show_object(tc.endcap_wheel(inch_to_mm(5)), options={"color": "green", "alpha": 0.25})
