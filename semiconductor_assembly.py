import build123d as bd
from bd_materials import metals
from cadgen import model, paint

@model
def semiconductor_die():
    """15 mm x 15 mm x 0.7 mm Silicon Die dissipating 150W continuous thermal power."""
    die = bd.Box(15.0, 15.0, 0.7, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    die.material = metals.aluminum()
    die.material.pbr = die.material.pbr.override(roughness=0.2, metalness=0.1)
    die.color = "#3B7A57"  # Deep silicon green/grey
    die.label = "silicon_die_150w_15x15x0.7mm"
    return die

@model
def tim_layer_paste():
    """Ultra-thin 0.05 mm silicone thermal paste TIM layer."""
    tim = bd.Box(15.0, 15.0, 0.05, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    tim.material = metals.aluminum()
    tim.color = "#708090"  # Slate grey silicone paste
    tim.label = "tim_silicone_paste_0.05mm"
    return tim

@model
def tim_layer_solder():
    """Ultra-thin 0.05 mm sintered silver / AuSn eutectic solder TIM layer."""
    tim = bd.Box(15.0, 15.0, 0.05, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    tim.material = metals.silver()
    tim.material.pbr = tim.material.pbr.override(roughness=0.1, metalness=0.95)
    tim.color = "#E0E0E0"  # Bright metallic sintered silver / gold-tin
    tim.label = "tim_sintered_silver_solder_0.05mm"
    return tim

@model
def heat_sink_conventional():
    """50mm x 50mm x 25mm Heat Sink with conventional extruded parallel fins."""
    width, depth, height, base_thickness = 50.0, 50.0, 25.0, 3.0
    fin_height = height - base_thickness
    fin_count = 13
    fin_thickness = 1.2
    margin = 2.0
    span = width - 2 * margin - fin_thickness
    pitch = span / (fin_count - 1)
    fin_xs = [-span / 2 + i * pitch for i in range(fin_count)]

    with bd.BuildSketch(bd.Plane.XZ) as sketch:
        bd.Rectangle(width, base_thickness, align=(bd.Align.CENTER, bd.Align.MIN))
        for x in fin_xs:
            with bd.Locations((x, base_thickness)):
                bd.Rectangle(fin_thickness, fin_height, align=(bd.Align.CENTER, bd.Align.MIN))

    body = bd.extrude(sketch.sketch, amount=depth / 2, both=True)
    body.material = metals.copper()
    body.material.pbr = body.material.pbr.override(roughness=0.3, metalness=0.9)
    body.color = "#B87333"  # Copper
    body.label = "heat_sink_conventional_extruded_50x50x25mm"
    return body

@model
def heat_sink_generative_microchannel():
    """50mm x 50mm x 25mm Heat Sink with generative / branched microchannel and pin-fin array geometries."""
    width, depth, height, base_thickness = 50.0, 50.0, 25.0, 3.0
    fin_height = height - base_thickness
    base = bd.Box(width, depth, base_thickness, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    
    pin_radius = 0.8
    pin_height = fin_height
    import math
    rings = [8.0, 16.0, 22.0]
    counts = [6, 12, 18]
    
    with bd.BuildPart() as p:
        bd.add(base)
        with bd.Locations((0, 0, base_thickness)):
            bd.Cylinder(radius=5.0, height=pin_height, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            for r, count in zip(rings, counts):
                for i in range(count):
                    angle = 2 * math.pi * i / count
                    x = r * math.cos(angle)
                    y = r * math.sin(angle)
                    with bd.Locations((x, y, 0)):
                        bd.Cylinder(radius=pin_radius, height=pin_height, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))

    body = p.part
    body.material = metals.copper()
    body.material.pbr = body.material.pbr.override(roughness=0.25, metalness=0.95)
    body.color = "#DAA520"  # Golden copper / sintered microchannel
    body.label = "heat_sink_generative_branched_microchannel_50x50x25mm"
    return body

@model
def semiconductor_assembly_conventional():
    """Complete 3-layer assembly: Die (15x15x0.7) + Silicone Paste TIM (0.05mm) + Conventional Heat Sink."""
    die = semiconductor_die().shape
    tim = tim_layer_paste().shape
    hs = heat_sink_conventional().shape

    tim_placed = bd.Location((0, 0, 0.7)) * tim
    hs_placed = bd.Location((0, 0, 0.75)) * hs

    assembly = bd.Compound(
        children=[die, tim_placed, hs_placed],
        label="semiconductor_assembly_conventional_variant"
    )
    return assembly

@model
def semiconductor_assembly_generative():
    """Complete 3-layer assembly: Die (15x15x0.7) + Sintered Silver Solder TIM (0.05mm) + Generative Microchannel Heat Sink."""
    die = semiconductor_die().shape
    tim = tim_layer_solder().shape
    hs = heat_sink_generative_microchannel().shape

    tim_placed = bd.Location((0, 0, 0.7)) * tim
    hs_placed = bd.Location((0, 0, 0.75)) * hs

    assembly = bd.Compound(
        children=[die, tim_placed, hs_placed],
        label="semiconductor_assembly_generative_variant"
    )
    return assembly

if __name__ == "__main__":
    semiconductor_die()
    tim_layer_paste()
    tim_layer_solder()
    heat_sink_conventional()
    heat_sink_generative_microchannel()
    semiconductor_assembly_conventional()
    semiconductor_assembly_generative()
