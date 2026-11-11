import build123d as bd
from bd_materials import metals
from cadgen import model, paint

def create_heat_sink_body(
    width: float = 40.0,
    depth: float = 40.0,
    height: float = 20.0,
    base_thickness: float = 4.0,
    fin_thickness: float = 1.2,
    fin_count: int = 11,
    margin: float = 1.0,
    clip_slot_width: float = 7.0,
    clip_slot_depth: float = 12.0,
):
    """Generates an extruded aluminum heat sink with vertical fins and a transverse clip slot."""
    fin_height = height - base_thickness
    span = width - 2 * margin - fin_thickness
    pitch = span / (fin_count - 1) if fin_count > 1 else 0
    fin_xs = [-span / 2 + i * pitch for i in range(fin_count)]

    # 1. Extrude 2D profile (base + vertical fins)
    with bd.BuildSketch(bd.Plane.XZ) as sketch:
        bd.Rectangle(width, base_thickness, align=(bd.Align.CENTER, bd.Align.MIN))
        for x in fin_xs:
            with bd.Locations((x, base_thickness)):
                bd.Rectangle(fin_thickness, fin_height, align=(bd.Align.CENTER, bd.Align.MIN))

    body = bd.extrude(sketch.sketch, amount=depth / 2, both=True)

    # 2. Cut transverse clip slot across the center along Y axis
    if clip_slot_width > 0 and clip_slot_depth > 0:
        slot_height = clip_slot_depth
        slot_z_min = base_thickness + fin_height - clip_slot_depth
        slot_box = bd.Box(
            width + 2.0,
            clip_slot_width,
            slot_height,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        slot_box = bd.Location((0, 0, slot_z_min)) * slot_box
        body = body - slot_box

    # 3. Add base corner edge chamfers/fillets for clean manufacturing finish
    try:
        edges_to_chamfer = body.edges().filter_by(bd.Axis.Z).filter_by(
            lambda e: abs(abs(e.center().X) - width / 2) < 1e-3 and abs(abs(e.center().Y) - depth / 2) < 1e-3
        )
        if edges_to_chamfer:
            body = bd.chamfer(edges_to_chamfer, length=0.8)
    except Exception:
        pass

    # Materials and Appearance (Anodized Aluminum)
    body.material = metals.aluminum()
    body.material.pbr = body.material.pbr.override(roughness=0.4, metalness=0.9)
    body.color = "#2A3439"  # Dark gunmetal / black anodized aluminum finish
    body.label = "aluminum_heat_sink"
    return body

@model
def heat_sink():
    """Standard 40x40x20mm heat sink for square semiconductor packages (e.g. BGA/SoC)."""
    return create_heat_sink_body(
        width=40.0, depth=40.0, height=20.0,
        base_thickness=4.0, fin_thickness=1.2, fin_count=11
    )

@model
def heat_sink_compact():
    """Compact 30x30x15mm heat sink for smaller semiconductor packages."""
    return create_heat_sink_body(
        width=30.0, depth=30.0, height=15.0,
        base_thickness=3.0, fin_thickness=1.0, fin_count=9,
        clip_slot_width=5.0, clip_slot_depth=8.0
    )

@model
def heat_sink_dense():
    """High-performance 50x50x25mm dense fin heat sink for high-power semiconductor packages."""
    return create_heat_sink_body(
        width=50.0, depth=50.0, height=25.0,
        base_thickness=5.0, fin_thickness=1.0, fin_count=15,
        clip_slot_width=8.0, clip_slot_depth=15.0
    )

@model
def semiconductor_cooling_assembly():
    """Assembly showing the aluminum heat sink mounted on a square semiconductor package with TIM layer."""
    hs = heat_sink().shape

    # Semiconductor Package (e.g. 35x35mm BGA package substrate + die)
    pkg_size = 35.0
    pkg_thickness = 2.2
    substrate = bd.Box(pkg_size, pkg_size, pkg_thickness, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX))
    substrate.color = "#0B3C5D"  # Greenish-blue FR4 substrate
    substrate.label = "ic_substrate"

    # Silicon Die / Heat Spreader in center (e.g. 15x15mm)
    die_size = 15.0
    die_thickness = 0.8
    die = bd.Box(die_size, die_size, die_thickness, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    die = bd.Location((0, 0, 0)) * die
    die.color = "#C0C0C0"  # Silver / metallic IHS
    die.label = "processor_die_ihs"

    # Thermal Interface Material (TIM) layer between die and heat sink bottom (0.15mm thick)
    tim_thickness = 0.15
    tim = bd.Box(die_size, die_size, tim_thickness, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    tim = bd.Location((0, 0, die_thickness)) * tim
    tim.color = "#708090"  # Gray thermal paste / pad
    tim.label = "tim_layer"

    # Heat sink positioned right above TIM (bottom of heat sink sits at Z = die_thickness + tim_thickness = 0.8 + 0.15 = 0.95 mm)
    hs_placed = bd.Location((0, 0, die_thickness + tim_thickness)) * hs
    hs_placed.label = "aluminum_heat_sink"

    # Combine into assembly compound
    assembly = bd.Compound(
        children=[substrate, die, tim, hs_placed],
        label="semiconductor_cooling_assembly"
    )
    return assembly

if __name__ == "__main__":
    heat_sink()
    heat_sink_compact()
    heat_sink_dense()
    semiconductor_cooling_assembly()
