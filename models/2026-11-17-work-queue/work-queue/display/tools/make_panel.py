# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Generate the work-queue SCADE Display panel.

Run with the Python bundled in SCADE Display (it provides pyparsing):

  "<SCADE Display>/contrib/Python312/python.exe" display/tools/make_panel.py

Writes display/panel/: WorkQueuePanel.sgfx, card.ogfx, button.ogfx, cell.ogfx.
Everything there is generated: edit this script, not the files.

Screen: 1280 x 800, origin at the centre, Y up (SCADE Display convention).

Interaction is coordinate-agnostic. Every interactive item (queue card, job
button, drop zone, control button) carries its own rectangle active area; the
panel outputs, per item, whether the pointer is over it, plus the pointer press
and release events. The model never sees a coordinate: moving or resizing an
item here changes nothing in Swan. The pointer position stays local to the
panel, where it only places the dragged "ghost" card.

Links: the memory grid gets each slot's `next` link as a slot number plus a
`linked` flag; a Null link is drawn as a ground symbol, not as a number.
"""

import os
from pathlib import Path
import sys

HOME = Path(
    os.environ.get(
        "SCADE_DISPLAY_HOME", r"C:\Program Files\ANSYS Inc\v271\SCADE Display"
    )
)
sys.path.insert(0, str(HOME / "SCADE" / "APIs" / "Python" / "lib"))

from scade.model.display import (  # noqa: E402
    display as D,  # noqa: N812
    parsing as P,  # noqa: N812
)
from scade.model.display.xml import save_ogfx, save_sgfx  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "panel"
PANEL = "WorkQueuePanel"
WIDTH, HEIGHT = 1280, 800

# Item counts: must match the Swan side (View::CARDS, View::PAGE, Console::TOOLS,
# Console::ZONES, Console::CONTROLS). Positions are private to the panel.
CARDS, CELLS, TOOLS, ZONES, CONTROLS = 8, 64, 7, 2, 6
CARD_W, CARD_H, STEP = 120, 70, 132
BUTTON_W, BUTTON_H = 120, 40
CELL_W, CELL_H, GRID_COLS = 70, 44, 8
X0 = -560  # centre of the first item of every row

ROW_MACHINE = 335
ROW_CONTROLS = 270
ROW_TOOLS = 190
ROW_CARDS = 90
ROW_GRID = -30

# Colour table indices (default SCADE Display table).
BLACK, WHITE, LIGHT_GREY, GREY, DARK_GREY, DARKER_GREY = 1, 2, 4, 5, 6, 7
DARKER_RED, GREEN, YELLOW = 16, 41, 31
OP_COLORS = [
    51,
    21,
    41,
    61,
    71,
    11,
    31,
]  # Inspect Paint Pack Drill Rework SafetyCheck Production
OPERATIONS = ["Inspect", "Paint", "Pack", "Drill", "Rework", "Safety", "Production"]
CONTROL_LABELS = ["Pause", "Step", "Slow", "Normal", "Fast", "Fill"]
ZONE_LABELS = ["End", "Trash"]
ZONE_COLORS = [DARK_GREY, DARKER_RED]
FILL_COLOR = 74  # LIGHT FUSCHIA: a queue action, unlike the grey pacing buttons

# ---------------------------------------------------------------- helpers
_oid = [0]


def oid():
    """Return a new unique object identifier."""
    _oid[0] += 1
    return "7a5e0000-0000-4000-8000-%012d" % _oid[0]


def ty(s):
    """Parse a SCADE Display type."""
    return P.parse_type(s)


def ex(s):
    """Parse a SCADE Display expression."""
    return P.parse_expr(s)


def var(name, type_str, init):
    """Declare a variable."""
    return D.Variable(name=name, oid=oid(), type=ty(type_str), init=ex(init))


def mem(name, type_str, init, memory):
    """Declare a variable with or without memory."""
    return D.MemVariable(
        name=name, oid=oid(), type=ty(type_str), init=ex(init), memory=memory
    )


def chars(s, size):
    """Return `s` as a zero-padded list of `size` character codes."""
    codes = [ord(c) for c in s][: size - 1]
    return codes + [0] * (size - len(codes))


def char_list(s, size=16):
    """Return `s` as a character array literal."""
    return "[%s]" % ", ".join(str(c) for c in chars(s, size))


def array(values):
    """Return an array literal."""
    return "[%s]" % ", ".join(str(v) for v in values)


def rect(name, x0, y0, x1, y1, fill=-1, outline=-1, width=0):
    """Create a rectangle."""
    return D.Rectangle(
        name=name,
        oid=oid(),
        first_point=(float(x0), float(y0)),
        third_point=(float(x1), float(y1)),
        fill_color=fill,
        outline_color=outline,
        line_width=width,
    )


def label(name, s, x, y, font=0, color=WHITE, size=None, align=D.HorizAlignEnum.CENTER):
    """Create a text."""
    size = size or len(s) + 1
    t = D.Text(
        name=name,
        oid=oid(),
        position=(float(x), float(y)),
        value=chars(s, size),
        font=font,
        outline_color=color,
        horiz_align=align,
    )
    t.max_length.init = size
    return t


def bind(prop, expr):
    """Bind property `prop` to expression `expr`."""
    prop.expr = ex(expr)
    return prop


def int_text(name, x, y, expr, font=0, color=WHITE, digits=6):
    """Integer readout: a BiFont on a float value, all digits on the first font."""
    t = D.BiFont(
        name=name,
        oid=oid(),
        position=(float(x), float(y)),
        value=0.0,
        first_font=font,
        second_font=font,
        outline_color=color,
    )
    fmt = t.format
    fmt.integral_part.init = digits
    fmt.fractional_part.init = 0
    fmt.second_font_pos.init = 0
    fmt.leading_zeros.init = False
    fmt.display_sign.init = D.DisplaySignEnum.WHENNEGATIVE
    t.value.expr = ex(expr)
    return t


def area(name, w, h, inside):
    """Active area covering a w x h item centred on its origin; all pointers."""
    a = D.RectangleArea(
        name=name,
        oid=oid(),
        first_point=(-w / 2.0, h / 2.0),
        third_point=(w / 2.0, -h / 2.0),
        inside=ex(inside),
    )
    a.pointer_id.init = -1
    return a


def nplicator(name, file, origins, params, outputs=()):
    """Create one copy of `file` per origin.

    params: (name, element type, per-copy init values, source plug or None);
    outputs: (name, element type, target plug).
    """
    n = len(origins)
    np_ = D.NplicatorContainer(
        name=name,
        oid=oid(),
        file=file,
        nb_instances=n,
        inputs=[(p, ty("%s^%d" % (t, n))) for p, t, _, _ in params],
        outputs=[(p, ty("%s^%d" % (t, n))) for p, t, _ in outputs],
        origin=[(float(x), float(y)) for x, y in origins],
    )
    for prop, (_, _, inits, src) in zip(np_.input_parameters.parameters, params):
        values = inits if isinstance(inits, list) else [inits] * n
        assert len(values) == n, name
        prop.init = ex(array(values))
        if src is not None:
            prop.expr = ex(src)
    for prop, (_, _, dst) in zip(np_.output_parameters.output_parameters, outputs):
        prop.expr = ex(dst)
    return np_


def row(y, count, step=STEP, x0=X0):
    """Return the origins of `count` items in a row."""
    return [(x0 + i * step, y) for i in range(count)]


# ---------------------------------------------------------------- objects
def card_object():
    """Create a queue place.

    When `present`, a card coloured by operation with its name and slot. The
    active area is there even when the place is empty, so an empty place is a
    drop target too (the end of the queue).
    """
    w, h = CARD_W, CARD_H
    group = D.Container(name="group", oid=oid())
    obj = D.ReferenceObject(width=w + 8, height=h + 8, children=group)
    decl = obj.declaration
    decl.input.append(var("present", "bool", "true"))
    decl.input.append(var("color", "int32", str(OP_COLORS[1])))
    decl.input.append(var("edge", "int32", str(WHITE)))
    decl.input.append(var("slot", "float32", "0.0"))
    decl.input.append(var("name", "char^16", char_list("Paint")))
    decl.input.append(var("ink", "int32", str(BLACK)))
    decl.output.append(mem("hover", "bool", "false", True))
    items = group.children
    items.append(
        rect("place", -w / 2, h / 2, w / 2, -h / 2, outline=DARKER_GREY, width=0)
    )
    body = D.Container(name="card_body", oid=oid())
    bind(body.visible, "present")
    fill = rect(
        "fill", -w / 2, h / 2, w / 2, -h / 2, fill=OP_COLORS[1], outline=WHITE, width=2
    )
    bind(fill.fill_color, "color")
    bind(fill.outline_color, "edge")
    body.children.append(fill)
    name = label("op_name", "Paint", 0, 12, font=2, color=BLACK, size=16)
    bind(name.text_value, "name")
    bind(name.outline_color, "ink")
    body.children.append(name)
    slot_tag = label("slot_tag", "slot", -20, -18, font=0, color=BLACK)
    bind(slot_tag.outline_color, "ink")
    body.children.append(slot_tag)
    slot_value = int_text("slot_value", 22, -18, "slot", font=2, color=BLACK, digits=3)
    bind(slot_value.outline_color, "ink")
    body.children.append(slot_value)
    items.append(body)
    items.append(area("card_area", w, h, "hover"))
    return obj


def button_object():
    """Create a labelled button.

    Fill colour, label, `lit` frame; the active area reports `hover`.
    """
    w, h = BUTTON_W, BUTTON_H
    group = D.Container(name="group", oid=oid())
    obj = D.ReferenceObject(width=w + 8, height=h + 8, children=group)
    decl = obj.declaration
    decl.input.append(var("color", "int32", str(DARK_GREY)))
    decl.input.append(var("lit", "bool", "false"))
    decl.input.append(var("text", "char^16", char_list("Button")))
    decl.output.append(mem("hover", "bool", "false", True))
    items = group.children
    box = rect(
        "box", -w / 2, h / 2, w / 2, -h / 2, fill=DARK_GREY, outline=GREY, width=0
    )
    bind(box.fill_color, "color")
    items.append(box)
    frame = rect(
        "lit_frame",
        -w / 2 - 3,
        h / 2 + 3,
        w / 2 + 3,
        -h / 2 - 3,
        outline=YELLOW,
        width=2,
    )
    frame.visible.init = False
    bind(frame.visible, "lit")
    items.append(frame)
    text = label("label", "Button", 0, 0, font=2, color=BLACK, size=16)
    bind(text.text_value, "text")
    items.append(text)
    items.append(area("button_area", w, h, "hover"))
    return obj


def cell_object():
    """Create a memory slot.

    Grey when free, operation colour when used; version and next link. A slot
    that links nowhere (a Null reference) shows a ground symbol, not a number.
    Badges mark the queue head (H), tail (T) and free-list head (F); `mark` (a
    colour, -1 for none) outlines the slot when the model highlights it. The
    active area reports `hover`.
    """
    w, h = CELL_W, CELL_H
    group = D.Container(name="group", oid=oid())
    obj = D.ReferenceObject(width=w, height=h, children=group)
    decl = obj.declaration
    decl.input.append(var("color", "int32", str(DARKER_GREY)))
    decl.input.append(var("ink", "int32", str(WHITE)))
    decl.input.append(var("version", "float32", "0.0"))
    decl.input.append(var("next", "float32", "0.0"))
    decl.input.append(var("linked", "bool", "false"))
    decl.input.append(var("head", "bool", "false"))
    decl.input.append(var("tail", "bool", "false"))
    decl.input.append(var("free_head", "bool", "false"))
    decl.input.append(var("mark", "int32", "-1"))
    decl.output.append(mem("hover", "bool", "false", True))
    items = group.children
    box = rect(
        "box",
        -w / 2 + 2,
        h / 2 - 2,
        w / 2 - 2,
        -h / 2 + 2,
        fill=DARKER_GREY,
        outline=GREY,
        width=0,
    )
    bind(box.fill_color, "color")
    items.append(box)
    for item in [
        label("v_tag", "v", -26, 8, color=WHITE),
        int_text("version_value", 0, 8, "version", color=WHITE, digits=4),
        label("n_tag", ">", -26, -10, color=WHITE),
    ]:
        bind(item.outline_color, "ink")
        items.append(item)
    value = int_text("next_value", 0, -10, "next", color=WHITE, digits=3)
    bind(value.visible, "linked")
    bind(value.outline_color, "ink")
    items.append(value)
    # Null: an electrical ground, the usual drawing of a null pointer.
    ground = D.Container(name="null_link", oid=oid(), origin=(0.0, -10.0))
    ground.visible.init = True
    bind(ground.visible, "not linked")
    for name, half, y in [
        ("stem", 0, 5),
        ("ground_1", 9, -1),
        ("ground_2", 6, -4),
        ("ground_3", 3, -7),
    ]:
        points = [(0.0, 7.0), (0.0, -1.0)] if half == 0 else [(-half, y), (half, y)]
        stroke = D.Line(
            name=name, oid=oid(), points=points, outline_color=WHITE, line_width=0
        )
        bind(stroke.outline_color, "ink")
        ground.children.append(stroke)
    items.append(ground)
    # Role badges, top right corner: H (head) and T (tail) share a slot when the
    # queue holds one job, so T goes just below H.
    for name, letter, flag, color, y in [
        ("head_badge", "H", "head", GREEN, 10),
        ("tail_badge", "T", "tail", 21, -8),
        ("free_badge", "F", "free_head", LIGHT_GREY, 10),
    ]:
        badge = D.Container(name=name, oid=oid(), origin=(w / 2 - 11.0, float(y)))
        badge.visible.init = False
        bind(badge.visible, flag)
        badge.children.append(
            rect(name + "_box", -8, 9, 8, -9, fill=BLACK, outline=color, width=0)
        )
        badge.children.append(
            label(name + "_letter", letter, 0, 0, font=2, color=color)
        )
        items.append(badge)
    highlight = rect("highlight", -w / 2, h / 2, w / 2, -h / 2, outline=YELLOW, width=2)
    highlight.visible.init = False
    bind(highlight.visible, "mark >= 0")
    bind(highlight.outline_color, "mark")
    items.append(highlight)
    items.append(area("cell_area", w, h, "hover"))
    return obj


# ---------------------------------------------------------------- panel
def panel():
    """Create the panel specification."""
    layer = D.Layer(name="main_layer", oid=oid())
    spec = D.Specification(width=WIDTH, height=HEIGHT, layers=[layer])
    decl = layer.declaration
    zeros16 = char_list("")

    # Inputs, from the model. Design-time values give a meaningful snapshot.
    preview = [(5, 2), (4, 3), (1, 0), (2, 1)]  # (operation, slot) of 4 pending jobs
    shown = len(preview)
    inp = decl.input.append
    inp(
        var(
            "card_present",
            "bool^%d" % CARDS,
            array(["true" if i < shown else "false" for i in range(CARDS)]),
        )
    )
    inp(
        var(
            "card_color",
            "int32^%d" % CARDS,
            array(
                [OP_COLORS[preview[i][0]] if i < shown else GREY for i in range(CARDS)]
            ),
        )
    )
    inp(var("card_edge", "int32^%d" % CARDS, array([WHITE] * CARDS)))
    inp(
        var(
            "card_slot",
            "float32^%d" % CARDS,
            array(
                ["%d.0" % preview[i][1] if i < shown else "0.0" for i in range(CARDS)]
            ),
        )
    )
    inp(
        var(
            "card_name",
            "char^16^%d" % CARDS,
            array(
                [
                    char_list(OPERATIONS[preview[i][0]]) if i < shown else zeros16
                    for i in range(CARDS)
                ]
            ),
        )
    )
    cell_colors = [DARKER_GREY] * CELLS
    for op, slot in preview:
        cell_colors[slot] = OP_COLORS[op]
    inp(var("card_ink", "int32^%d" % CARDS, array([BLACK] * CARDS)))
    inp(var("cell_color", "int32^%d" % CELLS, array(cell_colors)))
    inp(var("cell_ink", "int32^%d" % CELLS, array([WHITE] * CELLS)))
    inp(var("cell_version", "float32^%d" % CELLS, array(["0.0"] * CELLS)))
    inp(var("cell_next", "float32^%d" % CELLS, array(["0.0"] * CELLS)))
    inp(var("cell_linked", "bool^%d" % CELLS, array(["false"] * CELLS)))
    inp(var("cell_head", "bool^%d" % CELLS, array(["false"] * CELLS)))
    inp(var("cell_tail", "bool^%d" % CELLS, array(["false"] * CELLS)))
    inp(var("cell_free_head", "bool^%d" % CELLS, array(["false"] * CELLS)))
    inp(var("cell_mark", "int32^%d" % CELLS, array([-1] * CELLS)))
    inp(var("running_color", "int32", str(OP_COLORS[0])))
    inp(var("running_progress", "float32", "0.4"))
    inp(var("running_name", "char^16", char_list("Inspect")))
    inp(var("remaining", "float32", "5.0"))
    inp(var("queue_length", "float32", "4.0"))
    inp(var("last_text", "char^48", char_list("Insert Drill before Pack", 48)))
    inp(var("status_text", "char^24", char_list("Accepted", 24)))
    inp(var("status_color", "int32", str(GREEN)))
    inp(var("tool_lit", "bool^%d" % TOOLS, array(["false"] * TOOLS)))
    inp(var("zone_lit", "bool^%d" % ZONES, array(["false"] * ZONES)))
    inp(
        var(
            "control_lit",
            "bool^%d" % CONTROLS,
            array(["true" if i == 3 else "false" for i in range(CONTROLS)]),
        )
    )
    inp(var("ghost_visible", "bool", "false"))
    inp(var("ghost_color", "int32", str(GREY)))
    inp(var("ghost_name", "char^16", zeros16))

    # Outputs, to the model: which item the pointer is over, and button events.
    # Hover flags keep their value between pointer moves (memory); press and
    # release are one-cycle events (no memory).
    out = decl.output.append
    out(mem("card_hover", "bool^%d" % CARDS, array(["false"] * CARDS), True))
    out(mem("tool_hover", "bool^%d" % TOOLS, array(["false"] * TOOLS), True))
    out(mem("zone_hover", "bool^%d" % ZONES, array(["false"] * ZONES), True))
    out(mem("control_hover", "bool^%d" % CONTROLS, array(["false"] * CONTROLS), True))
    out(mem("cell_hover", "bool^%d" % CELLS, array(["false"] * CELLS), True))
    out(mem("pressed", "bool", "false", False))
    out(mem("released", "bool", "false", False))
    # Pointer position as a ratio of the screen, local to the panel: it only
    # places the ghost.
    decl.local.append(mem("ghost_px", "float32", "0.5", True))
    decl.local.append(mem("ghost_py", "float32", "0.5", True))

    items = layer.children
    items.append(
        rect(
            "background",
            -WIDTH / 2,
            HEIGHT / 2,
            WIDTH / 2,
            -HEIGHT / 2,
            fill=BLACK,
            outline=-1,
        )
    )
    items.append(
        label(
            "title",
            "Live work queue",
            -WIDTH / 2 + 20,
            HEIGHT / 2 - 25,
            font=3,
            align=D.HorizAlignEnum.LEFT,
        )
    )

    # Machine: running job, progress, remaining cycles, pending count.
    y = ROW_MACHINE
    items.append(
        label("machine_title", "Machine", -620, y, font=2, align=D.HorizAlignEnum.LEFT)
    )
    x0, x1 = -500, -140
    items.append(
        rect(
            "machine_frame",
            x0,
            y + 15,
            x1,
            y - 15,
            fill=DARKER_GREY,
            outline=GREY,
            width=1,
        )
    )
    bar = D.TranslationContainer(
        name="machine_progress",
        oid=oid(),
        start_point=(float(x0 - x1), 0.0),
        end_point=(0.0, 0.0),
    )
    bar.start_translation_value.init = 0.0
    bar.end_translation_value.init = 1.0
    bind(bar.functional_translation_value, "running_progress")
    clip = D.ClipBox(
        name="machine_clip",
        oid=oid(),
        first_point=(float(x0), y + 15.0),
        third_point=(float(x1), y - 15.0),
    )
    fill = rect("machine_fill", x0, y + 14, x1, y - 14, fill=DARKER_GREY)
    bind(fill.fill_color, "running_color")
    bar.children.append(fill)
    progress = D.Container(name="machine_bar", oid=oid())
    progress.children.extend([clip, bar])
    items.append(progress)
    running = label(
        "running_label", "Inspect", (x0 + x1) / 2, y, font=2, color=WHITE, size=16
    )
    bind(running.text_value, "running_name")
    items.append(running)
    # Counters: label, then the number left-aligned after it, so a growing
    # number extends to the right, away from the label.
    for tag, text, x, expr in [
        ("remaining", "cycles left", -110, "remaining"),
        ("length", "pending", 90, "queue_length"),
    ]:
        items.append(label(tag + "_tag", text, x, y, align=D.HorizAlignEnum.LEFT))
        value = int_text(tag + "_value", x + 105, y, expr, font=2, digits=5)
        value.horiz_align.init = D.HorizAlignEnum.LEFT
        items.append(value)

    # Controls and last command status.
    # Pacing controls (Pause .. Fast), then a gap and Fill, which edits the
    # queue: it gets the job buttons' look (a colour) rather than grey.
    control_xy = row(ROW_CONTROLS, CONTROLS - 1) + [
        (X0 + (CONTROLS - 1) * STEP + 40, ROW_CONTROLS)
    ]
    items.append(
        label(
            "pace_title",
            "Machine pace",
            -620,
            ROW_CONTROLS + 35,
            font=2,
            align=D.HorizAlignEnum.LEFT,
        )
    )
    items.append(
        label(
            "fill_title",
            "Queue",
            control_xy[-1][0] - BUTTON_W / 2,
            ROW_CONTROLS + 35,
            font=2,
            align=D.HorizAlignEnum.LEFT,
        )
    )
    items.append(
        nplicator(
            "controls",
            "button.ogfx",
            control_xy,
            [
                ("color", "int32", [LIGHT_GREY] * (CONTROLS - 1) + [FILL_COLOR], None),
                ("lit", "bool", "false", "control_lit"),
                ("text", "char^16", [char_list(s) for s in CONTROL_LABELS], None),
            ],
            [("hover", "bool", "control_hover")],
        )
    )
    # Last command and its result, on their own line under the title.
    ys = HEIGHT / 2 - 25
    items.append(
        label(
            "last_tag",
            "Last command:",
            280,
            ys - 8,
            font=0,
            color=LIGHT_GREY,
            align=D.HorizAlignEnum.RIGHT,
        )
    )
    last = label(
        "last_text",
        "Insert Drill before Pack",
        290,
        ys + 6,
        font=2,
        color=WHITE,
        size=48,
        align=D.HorizAlignEnum.LEFT,
    )
    bind(last.text_value, "last_text")
    items.append(last)
    status = label(
        "status",
        "Accepted",
        290,
        ys - 16,
        font=2,
        color=GREEN,
        size=24,
        align=D.HorizAlignEnum.LEFT,
    )
    bind(status.text_value, "status_text")
    bind(status.outline_color, "status_color")
    items.append(status)

    # Job buttons: one per operation.
    items.append(
        label(
            "tools_title",
            "Jobs",
            -620,
            ROW_TOOLS + 35,
            font=2,
            align=D.HorizAlignEnum.LEFT,
        )
    )
    items.append(
        nplicator(
            "tools",
            "button.ogfx",
            row(ROW_TOOLS, TOOLS),
            [
                ("color", "int32", OP_COLORS, None),
                ("lit", "bool", "false", "tool_lit"),
                ("text", "char^16", [char_list(s) for s in OPERATIONS], None),
            ],
            [("hover", "bool", "tool_hover")],
        )
    )

    # Queue: one place per card, then the End and Trash drop zones.
    items.append(
        label(
            "queue_title",
            "Queue (logical order)",
            -620,
            ROW_CARDS + 50,
            font=2,
            align=D.HorizAlignEnum.LEFT,
        )
    )
    items.append(
        nplicator(
            "cards",
            "card.ogfx",
            row(ROW_CARDS, CARDS),
            [
                ("present", "bool", "false", "card_present"),
                ("color", "int32", GREY, "card_color"),
                ("edge", "int32", WHITE, "card_edge"),
                ("slot", "float32", "0.0", "card_slot"),
                ("name", "char^16", zeros16, "card_name"),
                ("ink", "int32", BLACK, "card_ink"),
            ],
            [("hover", "bool", "card_hover")],
        )
    )
    zx = X0 + CARDS * STEP + 4
    items.append(
        nplicator(
            "zones",
            "button.ogfx",
            [(zx, ROW_CARDS + 22), (zx, ROW_CARDS - 22)],
            [
                ("color", "int32", ZONE_COLORS, None),
                ("lit", "bool", "false", "zone_lit"),
                ("text", "char^16", [char_list(s) for s in ZONE_LABELS], None),
            ],
            [("hover", "bool", "zone_hover")],
        )
    )

    # Memory grid: slot i at row i / COLS, column i mod COLS.
    items.append(
        label(
            "memory_title",
            "Memory (physical slots)",
            -620,
            ROW_GRID + 35,
            font=2,
            align=D.HorizAlignEnum.LEFT,
        )
    )
    items.append(
        nplicator(
            "cells",
            "cell.ogfx",
            [
                (X0 + (i % GRID_COLS) * CELL_W, ROW_GRID - (i // GRID_COLS) * CELL_H)
                for i in range(CELLS)
            ],
            [
                ("color", "int32", DARKER_GREY, "cell_color"),
                ("ink", "int32", WHITE, "cell_ink"),
                ("version", "float32", "0.0", "cell_version"),
                ("next", "float32", "0.0", "cell_next"),
                ("linked", "bool", "false", "cell_linked"),
                ("head", "bool", "false", "cell_head"),
                ("tail", "bool", "false", "cell_tail"),
                ("free_head", "bool", "false", "cell_free_head"),
                ("mark", "int32", -1, "cell_mark"),
            ],
            [("hover", "bool", "cell_hover")],
        )
    )

    help_lines = [
        "Job button   click: append",
        "             drag onto a card: insert before it",
        "             drag onto Trash: cancel all of that kind",
        "Card         click: cancel",
        "             drag onto a card: move before it",
        "             drag onto End or an empty place: move last",
        "             drag onto Trash: cancel",
        "Pause / Step / speeds pace the machine.",
        "Fill queues one job of each kind.",
        "Memory: H head, T tail, F free-list head.",
        "Hover a slot or card: white = it, yellow = next,",
        "cyan = prev.",
        "Top right: the last command and its result.",
    ]
    for i, line in enumerate(help_lines):
        items.append(
            label(
                "help_%d" % i,
                line,
                20,
                ROW_GRID + 10 - 26 * i,
                font=4,
                color=LIGHT_GREY,
                align=D.HorizAlignEnum.LEFT,
            )
        )

    # Ghost card under the pointer while dragging (display only): a translucent
    # card with a yellow outline. Its position comes from a full-screen active
    # area, evaluated every cycle like the item hover flags; it never leaves the
    # panel. The area's width and height "percent" outputs are ratios in [0, 1]
    # measured from the lower-left corner (OGLX sglRectangleActiveAreaGet*Rate),
    # so the area is defined from that corner.
    tracker = D.RectangleArea(
        name="pointer_tracker",
        oid=oid(),
        first_point=(-WIDTH / 2.0, -HEIGHT / 2.0),
        third_point=(WIDTH / 2.0, HEIGHT / 2.0),
    )
    tracker.pointer_id.init = -1
    tracker.percent_width = D.OutputProp(ex("ghost_px"))
    tracker.percent_height = D.OutputProp(ex("ghost_py"))
    items.append(tracker)
    ghost = D.Container(name="ghost", oid=oid())
    ghost.visible.init = False
    bind(ghost.visible, "ghost_visible")
    bind(ghost.origin.x, "%.1f + ghost_px * %.1f" % (-WIDTH / 2.0, float(WIDTH)))
    bind(ghost.origin.y, "%.1f + ghost_py * %.1f" % (-HEIGHT / 2.0, float(HEIGHT)))
    g = rect(
        "ghost_box",
        -CARD_W / 2,
        CARD_H / 2,
        CARD_W / 2,
        -CARD_H / 2,
        fill=GREY,
        outline=YELLOW,
        width=2,
    )
    g.fill_opacity.init = 110
    bind(g.fill_color, "ghost_color")
    ghost.children.append(g)
    gname = label("ghost_label", "", 0, 0, font=2, color=WHITE, size=16)
    bind(gname.text_value, "ghost_name")
    ghost.children.append(gname)
    items.append(ghost)

    # Pointer buttons.
    listener = D.PointerEventListener(name="pointer", oid=oid())
    listener.relative.init = False
    listener.pressed = D.OutputProp(ex("pressed"))
    listener.released = D.OutputProp(ex("released"))
    items.append(listener)
    return spec


def main():
    """Write the panel and its objects to `OUT`."""
    OUT.mkdir(parents=True, exist_ok=True)
    save_ogfx(card_object(), str(OUT / "card.ogfx"))
    save_ogfx(button_object(), str(OUT / "button.ogfx"))
    save_ogfx(cell_object(), str(OUT / "cell.ogfx"))
    save_sgfx(panel(), str(OUT / (PANEL + ".sgfx")))
    print("written to", OUT)


if __name__ == "__main__":
    main()
