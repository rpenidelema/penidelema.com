"""Builds the static pages of penidelema.com.

Every page shares one frame (the two top corners, the foot, scripts). Content lives in the
lists below; "{p}" in content is replaced with the relative path to the site root. Run
`python3 tools/build.py` from the repository root, then commit the generated .html files:
GitHub Pages serves them as they are.

Design: the site is laid out like /anarchitecture, an exhibition being planned.
White ground, black Arial at one small size, grey for numbers and what is secondary,
italic for titles. Nothing big, nothing bold. The name sits in the top-left corner, the
rooms in the top-right.

  Home         the signature alone in the middle of the screen, like the plan; below it,
               the checklist: every piece of work on the site, numbered.
  A room       its pictures hung in a row on a wall, above a floor line; below, its
               part of the checklist.
  A project    a wall label (title, date, place) and text on the left, pictures on the right.
  Photography  the gallery: one picture to a row, alternating sides, a caption beside it.

The line: Rodrigo's signature continues down every page as one thin pen stroke and stops
at the bottom edge. The page marks where it goes, and assets/js/site.js draws it:

  data-line="through"  pass behind this picture
  data-line="behind"   pass behind this whole block (a wall of pictures)
  data-line="avoid"    run down the emptier side of this block
  data-line-phone="…"  the same, on a phone only (it overrides data-line there)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROOMS = [("making", "Making"), ("reading", "Reading"), ("photography", "Photography"),
         ("leadership", "Leadership"), ("journal", "Journal"), ("plus", "+")]
ROOM_NAME = dict(ROOMS)
# Old addresses, kept so links already out in the world still arrive.
MOVED = {"looking": "photography", "hosting": "leadership"}
EMAIL = "rpenidelema@g.hmc.edu"


def img(src, alt, w, h, lazy=True):
    return (f'<img src="{{p}}assets/img/{src}" alt="{alt}" width="{w}" height="{h}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async">')


# ---------- The checklist: every piece of work on the site ----------
# (room, title, date, detail, link or None, picture for the room's wall or None)
WORK = [
    ("making", "Kreios Space", "2026", "Test hardware for plasma thrusters", "making/kreios/",
     ("kreios.jpg", "The Kreios Space test hall seen from above: two steel vacuum chambers and workbenches", 1800, 1350)),
    ("making", "The E80 robot", "2026", "A robot that floated and measured the sea", "making/e80/",
     ("e80-render.png", "A drawing of the E80 robot: a square PVC frame with an orange float and a blue electronics box", 614, 407)),
    ("making", "NorthStar", "2026–", "Sensing an electron beam", "making/northstar/",
     ("northstar.jpg", "The electron beam accelerator at NorthStar", 2000, 1333)),
    ("making", "A mine shaft winch", "2025", "Lowers a sensor payload 600 feet, on a $400 budget", None, None),
    ("making", "Alumni and students", "2025", "Human-centred design, with Pomona College", None, None),
    ("making", "People and animals", "2025", "Human-centred design, with The Salvation Army", None, None),
    ("reading", "The materials of a region", "2026–", "Bioregional research with Professor Jia Yi Gu", "reading/bioregional/",
     ("quarry-walk.jpg", "The residency group in hard hats and orange vests walking across a sand quarry", 1320, 977)),
    ("reading", "Anarchitecture", "2026", "Installation plan for the Benton Museum of Art", "anarchitecture/", None),
    ("reading", "An archive of voices", "2025–", "3,000 documents and 120 hours of interviews, with Professor Isabel Balseiro", None,
     ("stone-workshop.jpg", "A stone workshop: shelves of offcuts and tools under a coat of white dust", 1320, 1316)),
    ("reading", "Papers in art history", "soon", "Pomona College", None, None),
    ("photography", "Stone and earth", "2026", "Eight photographs, Provence", "photography/",
     ("quarry-window.jpg", "A limestone quarry seen through a gap between two cut walls", 1320, 1311)),
    ("leadership", "Class president", "2026–", "Harvey Mudd, Class of 2028", None, None),
    ("leadership", "Philanthropy", "2025–", "Director, Board of Trustees", None, None),
    ("leadership", "Mentoring", "2025–", "Fourteen new international students", None, None),
    ("leadership", "Student affairs", "2024–", "Representative to the Board of Trustees", None, None),
    ("leadership", "Volunteering", "2024–", "Mudders Making a Difference", None, None),
    ("plus", "Untitled (Lines)", "2026–", "A drawing everyone adds one line to", "plus/", None),
]
# Longer words for a room's own list, where there is room for them.
MORE = {
    "A mine shaft winch": "A collapsible winch that lowers a sensor payload more than 600 feet into a mine shaft, with gas sensors and live video.",
    "Alumni and students": "Designing better ways for alumni and students across the Claremont Colleges to meet.",
    "People and animals": "Asking how time with animals might support trust and purpose for people recovering from homelessness and addiction, in Orange County.",
    "Class president": "Elected by my classmates.",
    "Philanthropy": "Five fundraising campaigns designed for student initiatives and clubs, and a seat on the branding group for the College's major campaign.",
    "Mentoring": "A cohort of fourteen first-year students, one to one and in monthly gatherings.",
    "Student affairs": "The student voice on the Board's Student Affairs Committee.",
    "Volunteering": "Blood drives, tutoring at Claremont High School, and campaigns for local charities.",
}
NUM = {w[1]: i + 1 for i, w in enumerate(WORK)}


def entry(w, show_room=True, more=False):
    room, title, date, detail, href, _ = w
    head = f'<p class="n">{NUM[title]}</p>'
    if show_room:
        head += f'<p>{ROOM_NAME[room]}</p>'
    t = f'<p><i>{title}</i>, {date}</p><p>{detail}</p>'
    if more and title in MORE:
        t += f'<p class="more">{MORE[title]}</p>'
    inner = head + t
    if href:
        return f'<li><a href="{{p}}{href}">{inner}</a></li>'
    return f'<li>{inner}</li>'


def checklist(items, show_room=True, more=False, label="Checklist"):
    lis = "".join(entry(w, show_room, more) for w in items)
    return f'<section class="wrap list" aria-label="{label}" data-line="avoid"><ul>{lis}</ul></section>'


def wall(items):
    """The room's pictures, hung in a row at one height, above a floor line."""
    hung = []
    for w in items:
        room, title, date, detail, href, pic = w
        if not pic:
            continue
        src, alt, pw, ph = pic
        im = img(src, alt, pw, ph, lazy=False)
        cap = f'<figcaption><span class="n">{NUM[title]}</span> <i>{title}</i></figcaption>'
        body = f'<a href="{{p}}{href}">{im}{cap}</a>' if href else f'{im}{cap}'
        hung.append(f'<figure style="--r:{pw / ph:.3f}">{body}</figure>')
    if not hung:
        return ""
    return f'<section class="wallbox" aria-label="Pictures" data-line="behind"><div class="wall">{"".join(hung)}</div></section>'


# ---------- The frame ----------
def corner(p, title, home=False):
    links = "".join(
        f'<a href="{p}{slug}/"'
        f'{" aria-label=\"Plus: a drawing everyone adds a line to\"" if slug == "plus" else ""}>{name}</a>'
        for slug, name in ROOMS)
    if home:
        left = """<div class="corner hero-text"><h1>Rodrigo Penide Lema</h1><p class="g">Engineering at Harvey Mudd, art history at Pomona</p></div>"""
    else:
        left = f"""<a class="corner home-name" href="{p}"><span class="mark-box" data-logo="mark" aria-hidden="true"></span><span class="who"><span>Rodrigo Penide Lema</span><span>{title}</span></span></a>"""
    return f"""{left}
<nav class="corner-r rooms" aria-label="Rooms">{links}<a href="{p}about/">About</a></nav>
<button type="button" class="corner-r menu-btn" data-menu="open" aria-expanded="false">Index</button>"""


def foot(p):
    return f"""<footer class="wrap foot">
  <div class="mail"><a href="mailto:{EMAIL}">{EMAIL}</a><button type="button" data-copy="{EMAIL}">Copy</button></div>
  <span class="g">Claremont, California. English for now; español y galego, pronto.</span>
</footer>"""


def frame(path, title, body, room=None, home=False, label=None):
    depth = len([s for s in path.split("/") if s])
    p = "/" if path.endswith(".html") else "../" * depth
    overlay = "".join(f'<li><a href="{p}{slug}/">{name}</a></li>' for slug, name in ROOMS)
    desc = "Rodrigo Penide Lema: engineering at Harvey Mudd, art history at Pomona. Things made, and things read."
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#ffffff">
<link rel="stylesheet" href="{p}assets/css/site.css">
</head>
<body>
<div class="page{" page-" + room if room else ""}{" page-home" if home else ""}">
<svg class="line" aria-hidden="true"></svg>
<header>
{corner(p, label or title.split(" · ")[0], home)}
</header>
<main>
{body.replace("{p}", p)}
</main>
{foot(p)}
</div>
<div class="overlay" hidden>
  <div class="bar"><a href="{p}">Rodrigo Penide Lema</a><button type="button" data-menu="close">Close</button></div>
  <ul>{overlay}<li><a href="{p}about/">About</a></li></ul>
</div>
<script src="{p}assets/js/site.js"></script>
</body>
</html>
"""
    if room and not home:
        html = html.replace(f'<a href="{p}{room}/"', f'<a href="{p}{room}/" aria-current="page"', 1)
    out = ROOT / path / "index.html" if path else ROOT / "index.html"
    if path.endswith(".html"):
        out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


# ---------- Building blocks ----------
def label(title, lines, intro=""):
    """A wall label: the title in italics, then the facts, one to a line, then the text."""
    ls = "".join(f"<p>{l}</p>" for l in lines)
    i = f'<div class="intro">{intro}</div>' if intro else ""
    return f'<div class="tomb"><p><i>{title}</i></p>{ls}{i}</div>'


def fig(src, alt, w, h, caption="", lazy=True, cls=""):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="shot {cls}" data-line="through">{img(src, alt, w, h, lazy)}{cap}</figure>'


def part(text, *figs, first=False):
    """One part of a project: words on the left, its pictures on the right."""
    return (f'<section class="wrap part{" first" if first else ""}">'
            f'<div class="words" data-line="avoid">{text}</div>'
            f'<div class="pics">{"".join(figs)}</div></section>')


def h(t):
    return f'<h2>{t}</h2>'


G = '<span class="g">{}</span>'.format

PAGES = []

# ---------- Home ----------
HOME = """<section class="hero" aria-label="Signature">
  <div class="logo-box" data-logo="hero" aria-hidden="true"></div>
</section>
""" + checklist(WORK)
PAGES.append(dict(path="", title="Rodrigo Penide Lema", home=True, body=HOME))


def room_page(slug, intro):
    items = [w for w in WORK if w[0] == slug]
    body = (f'<section class="wrap room-intro" data-line="avoid"><p class="g">{intro}</p></section>'
            + wall(items) + checklist(items, show_room=False, more=True, label=ROOM_NAME[slug]))
    PAGES.append(dict(path=slug, title=f"{ROOM_NAME[slug]} · Rodrigo Penide Lema", room=slug, body=body))


room_page("making", "Things built, tested, and designed for people.")
room_page("reading", "Materials, archives and images, read closely.")
room_page("leadership", "Making room for other people: the roles I have been trusted with.")

# ---------- Kreios ----------
PAGES.append(dict(path="making/kreios", title="Kreios Space · Rodrigo Penide Lema", room="making", label="Kreios Space", body=
    part(label("Test hardware for plasma thrusters", ["Kreios Space, summer 2026", "Assembly, integration and test intern", G("Under a NATO confidentiality agreement")],
               """<p>I spent the summer of 2026 inside a vacuum-chamber test facility, designing and machining what it was missing.</p>
    <p>I built a control panel for the flow of three noble gases, and supports for three sensing systems inside the chamber. Between builds I ran impedance tests and diagnosed plasma across thrust setups.</p>
    <p>I also started documenting the tests that, until then, had gone unrecorded.</p>
    <p>Much of this work is confidential, so this page is told mostly in words, and the room is all you see.</p>"""),
         fig("kreios.jpg", "The Kreios Space test hall seen from above: two steel vacuum chambers, workbenches and the company name on a concrete wall", 1800, 1350, "The test hall, seen from above.", lazy=False), first=True)))

# ---------- E80 ----------
PAGES.append(dict(path="making/e80", title="A robot that floated · Rodrigo Penide Lema", room="making", label="The E80 robot", body=
    part(label("A robot that floated", ["Engineering 80, Harvey Mudd, spring 2026", "Baby Beach, Dana Point", G("With Emily Bersin, Anna Chen and TJ Kidd")],
               "<p>We built a surface robot to measure the sea at five points of a beach in Dana Point: six motors, and three sensors about 15 cm down. Two of the three sensors got the water wrong.</p>"),
         fig("e80-render.png", "A drawing of the robot: a square PVC frame with an orange float, a blue electronics box on top and motors at the corners", 614, 407, "The robot, as drawn before it was built.", lazy=False, cls="sheet-pic"), first=True)
    + part(h("The robot") + """
    <p>The frame was a floating box of PVC pipe, with an upper platform and a lower mesh, so the sensing structure stayed under water while the robot stayed afloat. The waterproof electronics box sat in the middle of the top platform, to spread the weight evenly and keep the cables short.</p>
    <p>The turbidity sensor pointed down through the platform inside a length of PVC pipe, with its opening facing the direction of travel so fresh water kept flowing past it.</p>""",
           fig("e80-frame.png", "A drawing of the PVC frame from above, with its floats cut to fit", 587, 425, "The frame and its floats.", cls="sheet-pic"),
           fig("e80-sketch.png", "A hand sketch of the robot from the side", 740, 330, "An early sketch.", cls="sheet-pic"))
    + part(h("The circuits") + """
    <p>Each sensor needed its own amplifier to turn a tiny signal into something the Teensy could read: an inverting offset amplifier with a buffer for the thermistor, a non-inverting pair for the pH probe, and for turbidity a 555 timer pulsing an infrared diode, read by a photodiode through a transimpedance amplifier.</p>""",
           fig("e80-thermistor.jpg", "Circuit diagram of the thermistor amplifier", 1260, 680, "Temperature: the thermistor circuit."),
           fig("e80-turbidity-circuit.jpg", "Circuit diagram of the turbidity photodiode amplifier", 1280, 610, "Turbidity: the photodiode circuit."))
    + part(h("What the sea said") + """
    <p>The robot did everything we asked of it. It floated, followed its path, stopped at each location and logged every sample.</p>
    <p>The thermistor agreed with the sea: an average of 17.86 °C, less than half a degree from the 18.2 °C we measured by hand. The other two did not. The pH sensor read three to four points low, and the turbidity sensor read between 0.28 and 0.54 NTU, where a classmate's sample of the same water measured 13.3.</p>""",
           fig("e80-temperature.jpg", "Graph of temperature at five locations, flat near 17.9 degrees", 1372, 818, "Temperature at the five locations."),
           fig("e80-ph.jpg", "Graph of pH at five locations, far below the expected line", 1377, 818, "pH, against the expected value."),
           fig("e80-turbidity.jpg", "Graph of turbidity at five locations, all below 0.6", 1389, 818, "Turbidity at the five locations."))
    + part(h("What I learned") + """
    <p>The sensors were not broken. They had been calibrated in fresh water, and the sea is not fresh water: salt changes how a thermistor and a pH probe behave, and our turbidity amplifier had so much gain that it saw almost nothing at all.</p>
    <p>The robot worked. The lesson was about calibration: test the whole sensor, mounted, in the water it will actually meet.</p>
    <p class="g">Thanks to Professors Helms, Mohanty, Sinopoli and Yang, to Lynn and Xavier, and to Angie Zhou and Spencer Michaelson for sharing their measurements of the water.</p>""")))

# ---------- NorthStar ----------
PAGES.append(dict(path="making/northstar", title="NorthStar · Rodrigo Penide Lema", room="making", label="NorthStar", body=
    part(label("Sensing an electron beam", ["NorthStar, 2026 to now", "Inside a particle accelerator", G("Modelled in FLUKA before it is built")],
               """<p>At NorthStar I am helping design the system that senses the beam of an electron accelerator.</p>
    <p>It works inside the accelerator itself, where the beam runs. Before anything is built, we model how it will behave in FLUKA, a code for simulating particles passing through matter.</p>
    <p>The project is under way; more here as it can be shared.</p>"""),
         fig("northstar.jpg", "A particle accelerator on its delivery day: a large ring of dark magnets wrapped in blue and red tubing, pressure gauges in front, a worker bending down beside it", 2000, 1333, "The accelerator our system is designed for, on the day it arrived. Photograph: NorthStar.", lazy=False), first=True)))

# ---------- Bioregional ----------
PAGES.append(dict(path="reading/bioregional", title="Bioregional materials · Rodrigo Penide Lema", room="reading", label="The materials of a region", body=
    part(label("The materials of a region", ["Atelier LUMA, Arles, summer 2026", "Biofabrique LA, founding student researcher", G("With Professor Jia Yi Gu")],
               """<p>What grows and is made around Los Angeles, and who makes it: a method I brought back from a residency in France.</p>
    <p>I spent the summer of 2026 in a residency on bioregional materials at Atelier LUMA in Arles: stone, earth and clay, the people who quarry and shape them, and the distances between them.</p>
    <p>Back in California, I adapted that work into a method for mapping the material streams, suppliers and craftspeople of Southern California, to find where building and design could source locally.</p>
    <p>I do this as the founding student researcher of Biofabrique LA, with faculty from Harvey Mudd, MIT, USC and SCI-Arc, and with researchers at Atelier LUMA.</p>"""),
         fig("quarry-walk.jpg", "The residency group in hard hats and orange vests walking across a sand quarry", 1320, 977, "Walking a quarry with the residency, summer 2026.", lazy=False),
         fig("clay.jpg", "A hand holding a lump of pale clay over cracked dry ground", 1320, 1752, "Clay, picked up on site.", cls="narrow"),
         fig("stone-saw.jpg", "A man feeds a block of limestone to a large circular saw", 1320, 738, "Cutting limestone into blocks."), first=True)))

# ---------- Photography: the gallery ----------
LOOK = [
    ("quarry-window.jpg", "A limestone quarry seen through a gap between two cut walls", 1320, 1311, "A quarry, seen from inside another."),
    ("stone-saw.jpg", "A man feeds a block of limestone to a large circular saw inside a quarry hall", 1320, 738, "Cutting limestone into blocks."),
    ("quarry-face.jpg", "Tall rooms cut into a pale quarry face, with pines along the top", 1320, 1299, "Rooms left behind by the stone that was taken."),
    ("clay.jpg", "A hand holding a lump of pale clay over cracked dry ground", 1320, 1752, "Clay, picked up on site."),
    ("quarry-inside.jpg", "Inside a quarry: cut walls, and a floor of white rubble and dust", 1320, 1311, "Inside, the floor is rubble and dust."),
    ("quarry-walk.jpg", "The residency group in hard hats and orange vests walking across a sand quarry", 1320, 977, "Walking a working quarry."),
    ("stone-workshop.jpg", "A stone workshop: shelves of offcuts and tools under a coat of white dust", 1320, 1316, "A stone workshop."),
    ("arles.jpg", "The residency cohort standing in front of a limestone quarry wall in the sun", 1600, 1600, "The cohort, Arles."),
]
GALLERY = ('<section class="wrap room-intro" data-line="avoid"><p><i>Stone and earth</i>, 2026</p><p class="g">Photographs from a residency on stone and earth in Provence.</p></section>'
           '<section class="wrap gallery" aria-label="Photographs">' + "".join(
               f'<figure class="g-row {"r" if k % 2 == 0 else "l"}"><div class="g-pic" data-line="through">{img(src, alt, w, h, lazy=k > 1)}</div>'
               f'<figcaption><span class="n">{k + 1}</span><br>{cap}</figcaption></figure>'
               for k, (src, alt, w, h, cap) in enumerate(LOOK)) + "</section>")
PAGES.append(dict(path="photography", title="Photography · Rodrigo Penide Lema", room="photography", body=GALLERY))

# ---------- Journal ----------
PAGES.append(dict(path="journal", title="Journal · Rodrigo Penide Lema", room="journal", body=
    '<section class="wrap room-intro" data-line="avoid"><p class="g">Notes, newest first. The first entry is on its way.</p></section>'))

# ---------- + ----------
PLUS = """<section class="wrap plus" aria-label="Plus: a drawing everyone adds one line to">
  <div class="sheet" data-line="through">
    <canvas tabindex="0" aria-label="A shared drawing. Drag to add your line, or press Enter." aria-describedby="plus-how"></canvas>
  </div>
  <div class="tomb">
    <p><i>Untitled (Lines)</i>, 2026–</p>
    <p>Rodrigo Penide Lema, with interventions by visitors from around the world</p>
    <p class="g" id="plus-how">One line each, in one stroke. For now your line stays on your screen; soon every line will join the same drawing.</p>
    <output aria-live="polite" data-plus-status>The line on the paper is mine. Add one of yours.</output>
  </div>
</section>"""
PAGES.append(dict(path="plus", title="+ · Rodrigo Penide Lema", room="plus", label="Untitled (Lines)", body=PLUS))

# ---------- About ----------
PAGES.append(dict(path="about", title="About · Rodrigo Penide Lema", room="about", label="About", body=
    part(label("Rodrigo Penide Lema", ["B.S. Engineering, Harvey Mudd College", "B.A. Art History, Pomona College", "Class of 2028"],
               """<p>I study how things are made, and why they matter.</p>
    <p>Most of my work happens where those two questions meet: in a vacuum chamber, in an archive of interviews, in a map of the materials that grow and are made around Los Angeles.</p>
    <p><span class="g">Languages</span><br>Spanish, Galician and Portuguese, natively. English and French.</p>
    <p><span class="g">Honours</span><br>Randal Lewis Fellow in Innovation and Entrepreneurship. Emerging Leader Award, Harvey Mudd, 2025 and 2026.</p>"""),
         fig("portrait.jpg", "Rodrigo in a navy pinstripe shirt under an oak tree on campus", 1200, 1500, lazy=False, cls="narrow"), first=True)))

# ---------- 404 ----------
PAGES.append(dict(path="404.html", title="Not found · Rodrigo Penide Lema", label="Not found", body=
    '<section class="wrap room-intro" data-line="avoid"><p class="g">This page is not here. <a href="{p}">Back to the beginning</a>.</p></section>'))


def moved(old, new):
    """A page that has changed address: send the visitor on, at once."""
    out = ROOT / old / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved · Rodrigo Penide Lema</title>
<meta http-equiv="refresh" content="0; url=../{new}/">
<link rel="canonical" href="https://penidelema.com/{new}/">
<meta name="robots" content="noindex">
<style>body{{margin:24px;background:#fff;color:#000;font:13px/1.4 Arial,"Helvetica Neue",Helvetica,sans-serif}}</style>
</head>
<body><p>This page is now at <a href="../{new}/">{new}</a>.</p></body>
</html>
""")


if __name__ == "__main__":
    for page in PAGES:
        frame(page["path"], page["title"], page["body"], page.get("room"), home=page.get("home", False), label=page.get("label"))
    for old, new in MOVED.items():
        moved(old, new)
    print(f"Built {len(PAGES)} pages and {len(MOVED)} redirects")
