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

    def endcap_wheel_and_ring(self, diameter: float):
        """
        Generate a wheel that caps the end of the tube and dispenses sand

        :param self: Instance
        :param diameter: Diameter of wheel
        :type diameter: float
        """

        # Experiment: try a squared-off flange to see if it has better ability
        # to stay on track.

        # Build on top of the base wheel generator
        base_wheel = self.wheel(diameter, apply_fillet=False)

        # Clip with cylinder of larger radius
        base_wheel_intersect = (
            cq.Workplane("XZ")
            .circle(radius=diameter / 2 + inch_to_mm(1 / 4))
            .extrude(self.ibls_T_min * 2, both=True)
        )

        base_wheel = base_wheel.intersect(base_wheel_intersect)

        # Cut a hole for a commodity 608 bearing
        bearing_radius = 11  # 608 bearing diameter of 22mm
        bearing_thickness = 7  # 608 bearing thickness 7mm
        bearing_subtract = (
            cq.Workplane("XZ")
            .transformed(offset=(0, 0, self.ibls_T_min))
            .circle(radius=bearing_radius + self.print_margin / 2)
            .extrude(-bearing_thickness)
            .faces(">Y")
            .workplane()
            .circle(radius=bearing_radius + self.print_margin / 2)
            .workplane(offset=bearing_radius / 2)
            .circle(radius=bearing_radius / 2)
            .loft()
        )

        # Crush ribs help grip the bearing
        crush_rib_radius = 3
        crush_rib_height = 0.2
        crush_rib = (
            cq.Workplane("XZ")
            .transformed(
                offset=(
                    bearing_radius + crush_rib_radius - crush_rib_height,
                    0,
                    self.ibls_T_min,
                )
            )
            .circle(radius=crush_rib_radius)
            .extrude(-bearing_thickness)
            .faces("<Y")
            .chamfer(crush_rib_height)
        )

        crush_ribs = (
            crush_rib
            + crush_rib.rotate((0, 0, 0), (0, 1, 0), 120)
            + crush_rib.rotate((0, 0, 0), (0, 1, 0), 240)
        )

        bearing_subtract = bearing_subtract - crush_ribs

        # Supporting wall around bearing hole
        bearing_wall = 4
        bearing_add = (
            cq.Workplane("XZ")
            .transformed(offset=(0, 0, self.ibls_T_min))
            .circle(radius=bearing_radius + bearing_wall)
            .extrude(-bearing_thickness)
            .faces(">Y")
            .workplane()
            .circle(radius=bearing_radius + bearing_wall)
            .workplane(offset=bearing_radius / 2 + bearing_wall)
            .circle(radius=bearing_radius / 2 + bearing_wall)
            .loft()
        )

        # Parameters for sand dispensing outlet holes
        sand_outlet_diameter = 2
        sand_outlet_thickness = 1.6
        funnel_inner_edge = -sand_outlet_diameter - self.ibls_R_max * 1.5

        # Groove around perimeter of wheel that keeps the dispensing holes
        # a little bit away from the (likely damp) surface hopefully keeping
        # them from getting mudded up. This groove will also hold a clip that
        # keeps sand inside until we're ready to start sanding.
        perimeter_groove_depth = 2.5
        ring_base_thickness = 4
        perimeter_groove_subtract = (
            cq.Workplane("XY")
            .lineTo(
                diameter / 2,
                funnel_inner_edge - perimeter_groove_depth,
                forConstruction=True,
            )
            .line(-perimeter_groove_depth, perimeter_groove_depth)
            .line(0, sand_outlet_diameter)
            .line(perimeter_groove_depth, perimeter_groove_depth)
            .line(ring_base_thickness, 0)
            .line(0, -sand_outlet_diameter - perimeter_groove_depth * 2)
            .close()
            .revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(0, 1, 0))
        )

        # Cut shape that funnels sand out to outlet holes
        sand_funnel = (
            cq.Workplane("XY")
            .lineTo(0, funnel_inner_edge)
            .lineTo(
                diameter / 2
                - sand_outlet_thickness
                - sand_outlet_diameter * 3
                - perimeter_groove_depth,
                funnel_inner_edge,
            )
            .line(sand_outlet_diameter, -sand_outlet_diameter)
            .line(sand_outlet_diameter, 0)
            .lineTo(
                diameter / 2 - sand_outlet_thickness - perimeter_groove_depth,
                funnel_inner_edge,
            )
            .line(0, sand_outlet_diameter)
            .lineTo(self.tube_diameter_inner / 2 - self.tube_margin, self.ibls_W_max)
            .line(0, 25 - self.ibls_W_max)
            .lineTo(0, 25)
            .close()
            .revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(0, 1, 0))
        )

        # Cutting sand outlet holes
        sand_outlet_count = 18
        sand_outlet_angle_degrees = 360 / sand_outlet_count
        sand_outlet = (
            cq.Workplane("XY")
            .transformed(
                offset=(
                    0,
                    -self.ibls_R_max * 1.5 - sand_outlet_diameter / 2,
                    0,
                )
            )
            .circle(sand_outlet_diameter / 2)
            .extrude(diameter)
        )

        # Cutting these holes and the funnel leading up to them severely
        # weakens wheel structure. The inner reinforcement ribs add structural
        # strength and also hooks to inner tube diameter. Each rib is placed
        # halfway between two holes
        reinforcement_inner_height = 15
        reinforcement_chamfer = 2.4
        reinforcement_thickness_half = 1.2
        reinforcement_overlap = (
            diameter / 2 - self.tube_diameter_inner / 2
        ) / 2 - perimeter_groove_depth
        outlet_reinforcement = (
            cq.Workplane("ZY")
            .lineTo(0, funnel_inner_edge - sand_outlet_diameter, forConstruction=True)
            .lineTo(
                self.tube_diameter_inner / 2 + reinforcement_overlap,
                funnel_inner_edge - sand_outlet_diameter,
            )
            .lineTo(
                self.tube_diameter_inner / 2 + reinforcement_overlap,
                0,
            )
            .lineTo(self.tube_diameter_inner / 2 - self.tube_margin, self.ibls_W_max)
            .line(0, reinforcement_inner_height)
            .line(-reinforcement_chamfer, reinforcement_chamfer)
            .line(-reinforcement_chamfer, 0)
            .lineTo(
                self.tube_diameter_inner * 0.3,
                -self.ibls_R_max * 1.5 - sand_outlet_diameter,
            )
            .close()
            .extrude(reinforcement_thickness_half, both=True)
            .rotate((0, 0, 0), (0, 1, 0), sand_outlet_angle_degrees / 2)
        )

        # Repeat outlet holes and reinforcement ribs all around
        sand_outlet_collection = sand_outlet
        outlet_reinforcement_collection = outlet_reinforcement
        for outlet_count in range(1, sand_outlet_count):
            sand_outlet_collection += sand_outlet.rotate(
                (0, 0, 0), (0, 1, 0), sand_outlet_angle_degrees * outlet_count
            )
            outlet_reinforcement_collection += outlet_reinforcement.rotate(
                (0, 0, 0), (0, 1, 0), sand_outlet_angle_degrees * outlet_count
            )

        # Rib reinforcement grips the inner tube surface, the cone grips the
        # outer tube surface.
        cone_outer_height = reinforcement_inner_height
        cone_thickness_inner = reinforcement_thickness_half * 2
        cone_chamfer = reinforcement_thickness_half / 2
        tube_outer_cone = (
            cq.Workplane("ZY")
            .lineTo(
                self.tube_diameter_outer / 2 + self.tube_margin,
                self.ibls_W_max,
                forConstruction=True,
            )
            .line(0, cone_outer_height - cone_chamfer)
            .line(cone_chamfer, cone_chamfer)
            .line(cone_thickness_inner - cone_chamfer, 0)
            .line(cone_thickness_inner, -cone_outer_height)
            .close()
            .revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(0, 1, 0))
        )

        # Put it all together for an endcap wheel
        endcap = (
            base_wheel
            - perimeter_groove_subtract
            - sand_funnel
            - sand_outlet_collection
            + outlet_reinforcement_collection
            + tube_outer_cone
            + bearing_add
            - bearing_subtract
        )

        # Using the perimeter groove subtract shape, build a matching ring to
        # close dispensing holes until ready to sand.
        ring_lip_start_radius = diameter / 2
        ring_lip_depth = 12
        ring_lip_outer = 5
        ring_lip_inner = 3
        ring_lip_thickness = -sand_outlet_diameter - perimeter_groove_depth * 2
        ring_offset_z = -funnel_inner_edge + perimeter_groove_depth
        ring_lip_half = (
            cq.Workplane("XZ")
            .transformed(offset=(0, 0, ring_offset_z))
            .lineTo(0, ring_lip_start_radius, forConstruction=True)
            .line(ring_lip_inner, 0)
            .line(ring_lip_outer - ring_lip_inner, ring_lip_depth)
            .lineTo(0, ring_lip_start_radius + ring_lip_depth)
            .close()
            .extrude(ring_lip_thickness)
        )
        ring_lip = ring_lip_half + ring_lip_half.mirror("YZ")
        ring_slot_width_half = 0.5
        ring_slot_subtract = (
            cq.Workplane("XZ")
            .line(ring_slot_width_half, 0)
            .line(0, diameter)
            .line(-ring_slot_width_half * 2, 0)
            .line(0, -diameter)
            .close()
            .extrude(diameter, both=True)
        )

        ring = perimeter_groove_subtract + ring_lip - ring_slot_subtract

        return (endcap, ring)

    def endcap_shim(self, thickness):
        """
        The tube was purposely cut a little bit too short for endcap_wheel()
        to reach target gauge width. Better a little bit too short than too
        long because we can shim short. This method generates a shim of
        specified thickness to help reach 7.5" gauge width.

        :param self: Class instance
        :param thickness: thickness of desired shim in millimeters
        """
        shim = (
            cq.Workplane("XZ")
            .transformed(offset=(0, 0, -self.ibls_W_max))
            .circle(radius=self.tube_diameter_outer / 2 - self.tube_margin)
            .circle(radius=self.tube_diameter_inner / 2 + self.tube_margin)
            .extrude(-thickness)
        )

        return shim

    def axle_to_cross_beam(self):
        """
        Cross beam is an aluminum extrusion. This shape connects cross beam to
        wheel axle.

        :param self: Class instance
        """
        wheel_center_to_beam_center = 90
        extrusion_size = 20
        extrusion_wrap_thickness = 9
        axle_diameter = 8
        connector_width = 20
        connector_thickness = 15

        # Round end of connector that will wrap around 8mm axle
        axle_round = (
            cq.Workplane("XZ")
            .transformed(offset=(0, 0, self.ibls_T_min))
            .circle(radius=connector_width / 2)
            .extrude(connector_thickness)
            .faces("<Y")
            .workplane()
            .circle(radius=axle_diameter / 2 + 3)
            .extrude(2)
        )

        # Cut hole for metal axle
        axle_subtract = (
            cq.Workplane("XZ")
            .circle(radius=axle_diameter / 2 + self.print_margin)
            .extrude(100)
        )

        axle_subtract_rib = (
            cq.Workplane("XZ")
            .transformed(
                offset=(0, axle_diameter / 2 + 2 - self.print_margin, self.ibls_T_min)
            )
            .circle(radius=2)
            .extrude(connector_thickness)
        )

        axle_subtract = (
            axle_subtract
            - axle_subtract_rib
            - axle_subtract_rib.rotate((0, 0, 0), (0, 1, 0), 120)
            - axle_subtract_rib.rotate((0, 0, 0), (0, 1, 0), 240)
        )

        # Portion of connector that wraps around extrusion beam
        extrusion_wrap = (
            cq.Workplane("XZ")
            .transformed(offset=(0, wheel_center_to_beam_center, self.ibls_T_min))
            .rect(
                extrusion_size + extrusion_wrap_thickness * 2,
                extrusion_size + extrusion_wrap_thickness * 2,
            )
            .extrude(connector_thickness)
            .edges("|Y")
            .fillet(extrusion_wrap_thickness / 3)
        )

        # Cut a hole for extrusion fastener
        extrusion_fastener_subtract = (
            cq.Workplane("XY")
            .transformed(
                offset=(
                    0,
                    -self.ibls_T_min - connector_thickness / 2,
                    wheel_center_to_beam_center,
                )
            )
            .circle(radius=2.5 + self.print_margin)
            .extrude(20)
        )

        # Cut a hole for extrusion beam profile
        extrusion_subtract = (
            cq.Workplane("XZ")
            .transformed(offset=(0, wheel_center_to_beam_center, self.ibls_T_min))
            .rect(
                extrusion_size + self.print_margin,
                extrusion_size + self.print_margin,
            )
            .extrude(connector_thickness)
            .edges("|Y")
            .fillet(0.5)
        )

        # Simple box that connects axle support to beam support
        connector_body = (
            cq.Workplane("XZ")
            .transformed(offset=(0, 0, self.ibls_T_min))
            .line(connector_width / 2, 0)
            .line(0, wheel_center_to_beam_center)
            .line(-connector_width, 0)
            .line(0, -wheel_center_to_beam_center)
            .close()
            .extrude(connector_thickness)
        )

        # Put it all together!
        connector = (
            (
                (
                    (axle_round + extrusion_wrap + connector_body)
                    .edges("|Y")
                    .fillet(extrusion_wrap_thickness / 2)
                )
                - axle_subtract
                - extrusion_subtract
            )
            .faces("|Z")
            .chamfer(1)
        ) - extrusion_fastener_subtract

        return connector

    def beam_to_handle(self):
        """
        Printed connector to install handle on cross beam

        :param self: Class instance
        """
        wheel_center_to_beam_center = 90
        connector_thickness = 30
        handle_diameter = 18
        handle_recess = 50
        handle_crush_rib_radius = 2
        handle_crush_rib_height = self.print_margin * 2

        extrusion_size = 20
        extrusion_wrap_thickness = 7.5

        # Portion of connector that wraps around extrusion beam
        extrusion_wrap = (
            cq.Workplane("XZ")
            .transformed(offset=(0, wheel_center_to_beam_center, 0))
            .rect(
                extrusion_size + extrusion_wrap_thickness * 2,
                extrusion_size + extrusion_wrap_thickness * 2,
            )
            .extrude(-connector_thickness)
            .edges("|Y")
            .fillet(extrusion_wrap_thickness / 3)
        )

        # Cut a hole for extrusion beam profile
        extrusion_subtract = (
            cq.Workplane("XZ")
            .transformed(offset=(0, wheel_center_to_beam_center, 0))
            .rect(
                extrusion_size + self.print_margin,
                extrusion_size + self.print_margin,
            )
            .extrude(-connector_thickness)
            .edges("|Y")
            .fillet(0.5)
        )

        # Cut a hole for extrusion fastener
        extrusion_fastener_subtract = (
            cq.Workplane("YZ")
            .transformed(
                offset=(connector_thickness / 2, wheel_center_to_beam_center, 0)
            )
            .circle(radius=2.5 + self.print_margin)
            .extrude(extrusion_size, both=True)
        )

        # Portion that wrapes around handle
        handle_wrap = (
            cq.Workplane("XY")
            .transformed(
                offset=(
                    0,
                    connector_thickness / 2,
                    wheel_center_to_beam_center
                    + extrusion_size / 2
                    + extrusion_wrap_thickness,
                )
            )
            .polygon(8, diameter=connector_thickness, circumscribed=True)
            .extrude(handle_recess)
        )

        # Cut hole for handle
        handle_subtract = (
            cq.Workplane("XY")
            .transformed(
                offset=(
                    0,
                    connector_thickness / 2,
                    wheel_center_to_beam_center + extrusion_size / 2,
                )
            )
            .circle(radius=handle_diameter / 2)
            .extrude(handle_recess + extrusion_wrap_thickness)
        )

        # Crush rib to help hold handle in place
        handle_rib = (
            cq.Workplane("XY")
            .transformed(
                offset=(
                    0,
                    connector_thickness / 2
                    - handle_diameter / 2
                    - handle_crush_rib_radius
                    + handle_crush_rib_height,
                    wheel_center_to_beam_center + extrusion_size / 2,
                )
            )
            .circle(radius=handle_crush_rib_radius)
            .extrude(handle_recess + extrusion_wrap_thickness)
        )

        # Account for rib in handle hole
        handle_subtract = (
            handle_subtract
            - handle_rib
            - handle_rib.rotate(
                (0, connector_thickness / 2, 0), (0, connector_thickness / 2, 1), 120
            )
            - handle_rib.rotate(
                (0, connector_thickness / 2, 0), (0, connector_thickness / 2, 1), 240
            )
        )

        connector = (
            extrusion_wrap
            + handle_wrap
            - handle_subtract
            - extrusion_subtract
            - extrusion_fastener_subtract
        )

        return connector

    def twist_plug_and_hole(
        self, funnel_radius=inch_to_mm(0.5), plug_height=inch_to_mm(0.5), step_unit=2
    ):
        """
        An insert-and-twist plug and the hole that can be used to subtract
        from where we want the plug.
        """
        steps_needed = 5
        if plug_height < step_unit * steps_needed:
            raise ValueError(
                f"Plug height {plug_height} is too short to accommodate {steps_needed} steps of {step_unit} each"
            )

        tab_width = step_unit * 4
        plug_outer = (
            cq.Workplane("XY")
            .line(funnel_radius, 0)
            .line(step_unit * 2, step_unit * 2)
            .line(0, step_unit)
            .line(-step_unit, step_unit)
            .lineTo(funnel_radius + step_unit, plug_height)
            .lineTo(0, plug_height)
            .close()
            .revolve(360, (0, 0, 0), (0, 1, 0))
        )

        plug_inner = (
            cq.Workplane("XY")
            .line(funnel_radius, 0)
            .line(step_unit, step_unit)
            .lineTo(funnel_radius + step_unit, plug_height)
            .lineTo(0, plug_height)
            .close()
            .revolve(360, (0, 0, 0), (0, 1, 0))
        ) + (
            cq.Workplane("XZ")
            .rect((funnel_radius + step_unit * 2) * 2, tab_width)
            .extrude(-plug_height)
        )

        handle_oversize = funnel_radius * 2
        handle_subtract = (
            cq.Workplane("ZY")
            .lineTo(tab_width / 2, step_unit * 4, forConstruction=True)
            .line(handle_oversize, 0)
            .line(0, handle_oversize)
            .line(-handle_oversize, 0)
            .line(0, -handle_oversize)
            .close()
            .extrude(funnel_radius * 2, both=True)
            .edges("|X")
            .fillet(step_unit / 2)
        )

        plug = (
            (
                plug_outer.intersect(plug_inner)
                - handle_subtract
                - handle_subtract.mirror("XY")
            )
            .faces(">Y")
            .fillet(step_unit / 4)
        )

        return plug


tc = tube_core()

(wheel, ring) = tc.endcap_wheel_and_ring(inch_to_mm(5))

# show_object(wheel, options={"color": "green", "alpha": 0.25})
# show_object(ring, options={"color": "purple", "alpha": 0.25})
# show_object(tc.endcap_shim(inch_to_mm(0.15)), options={"color": "blue", "alpha": 0.25})
# show_object(tc.axle_to_cross_beam(), options={"color": "yellow", "alpha": 0.25})
# show_object(tc.beam_to_handle(), options={"color": "red", "alpha": 0.25})

plug = tc.twist_plug_and_hole()

show_object(plug, options={"color": "aliceblue", "alpha": 0.25})

blank_cylinder = cq.Workplane("XZ").circle(radius=inch_to_mm(1)).extrude(inch_to_mm(1))
show_object(blank_cylinder, options={"color": "purple", "alpha": 0.25})
