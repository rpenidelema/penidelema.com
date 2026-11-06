"""Builds the static pages of penidelema.com.

Every page shares one frame (top bar, phone menu, "Write to me", foot, scripts). Content
lives in the PAGES list below; "{p}" in content is replaced with the relative path to the
site root. Run `python3 tools/build.py` from the repository root, then commit the generated
.html files: GitHub Pages serves them as they are.

Design: "the line". Rodrigo's logo is a gesture drawn by hand. On the home page it draws
itself very large; on every other page it sits small in the corner. From its last stroke
the same line runs down the page: behind each picture, around the name of each room, down
the free side of every block of words, and at the end of the home page onto the paper of
the + drawing. The page marks where the line goes with data attributes, and
assets/js/site.js draws it:

  data-line="through"  pass behind this picture
  data-line="circle"   loop once around this word
  data-line="avoid"    run down the emptier side of this block
  data-line="end"      come down onto this sheet of paper and stop
  data-line="stop"     underline this word and stop
  data-line-phone="…"  the same, on a phone only (it overrides data-line there)

One look on purpose: navy ground, paper-white line and type, drawings on paper.
One serif (Brygada 1918), five sizes. No thin rules, no shadows, no small capitals.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROOMS = [("making", "Making"), ("reading", "Reading"), ("looking", "Looking"),
         ("hosting", "Hosting"), ("journal", "Journal"), ("plus", "+")]
EMAIL = "rpenidelema@g.hmc.edu"

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
         'aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>')


def img(src, alt, w, h, lazy=True):
    return (f'<img src="{{p}}assets/img/{src}" alt="{alt}" width="{w}" height="{h}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async">')


def shot(cls, src, alt, w, h, caption="", line="through", phone=None, i=0, lazy=True):
    """A picture the line can pass behind."""
    attrs = f' data-line="{line}"' if line else ""
    attrs += f' data-line-phone="{phone}"' if phone else ""
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure class="shot {cls}"{attrs} data-in style="--i:{i}">'
            f'{img(src, alt, w, h, lazy)}{cap}</figure>')


def words(cls, inner, line=None, phone="avoid", i=1):
    attrs = f' data-line="{line}"' if line else ""
    attrs += f' data-line-phone="{phone}"' if phone else ""
    return f'<div class="words {cls}"{attrs} data-in style="--i:{i}">{inner}</div>'


def go(label, href):
    return f'<a class="go" href="{{p}}{href}"><span>{label}</span>{ARROW}</a>'


def bar(p, room, hero=False):
    links = "".join(
        f'<li><a href="{p}{slug}/"{" aria-current=\"page\"" if slug == room else ""}'
        f'{" aria-label=\"Plus: a drawing everyone adds a line to\"" if slug == "plus" else ""}>{name}</a></li>'
        for slug, name in ROOMS)
    if hero:
        return f'<nav class="bar" aria-label="Rooms"><ul>{links}</ul></nav>'
    return f"""<header class="bar">
  <a class="home-name" href="{p}"><span class="mark-box" data-logo="mark" aria-hidden="true"></span><span>Rodrigo Penide Lema</span></a>
  <nav aria-label="Rooms"><ul class="rooms">{links}</ul></nav>
  <button type="button" class="menu-btn" data-menu="open" aria-expanded="false">Menu</button>
</header>"""


def write(p):
    return f"""<section class="wrap write" aria-labelledby="write">
  <h2 id="write">Write to me</h2>
  <div class="mail"><a href="mailto:{EMAIL}">{EMAIL}</a><button type="button" data-copy="{EMAIL}">Copy address</button></div>
</section>"""


def foot(p):
    links = "".join(f'<a href="{p}{slug}/">{name}</a>' for slug, name in ROOMS)
    return f"""<footer class="wrap foot">
  <span>Claremont, California</span>
  <nav aria-label="Rooms, again">{links}<a href="{p}about/">About</a></nav>
  <span>English for now. Español y galego, pronto.</span>
</footer>"""


def frame(path, title, body, room=None, desc=None, home=False):
    depth = len([s for s in path.split("/") if s])
    p = "/" if path.endswith(".html") else "../" * depth
    overlay = "".join(f'<li><a href="{p}{slug}/">{name}</a></li>' for slug, name in ROOMS)
    desc = desc or "Rodrigo Penide Lema: engineering at Harvey Mudd, art history at Pomona. Things made, and things read."
    top = "" if home else bar(p, room)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#1c2a66">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Brygada+1918:ital,wght@0,400;0,500;1,400&display=swap">
<link rel="stylesheet" href="{p}assets/css/site.css">
</head>
<body>
<div class="page{" page-" + room if room else ""}">
<svg class="line" aria-hidden="true"></svg>
{('<div class="wrap">' + top + '</div>') if top else ""}
<main>
{body.replace("{p}", p).replace("{bar}", bar(p, room, hero=True))}
</main>
{write(p)}
{foot(p)}
</div>
<div class="overlay" hidden>
  <div class="top"><a href="{p}">Rodrigo Penide Lema</a><button type="button" class="menu-btn" data-menu="close">Close</button></div>
  <ul>{overlay}<li><a href="{p}about/">About</a></li></ul>
  <p>English for now. Español y galego, pronto.</p>
</div>
<script src="{p}assets/js/site.js"></script>
</body>
</html>
"""
    out = ROOT / path / "index.html" if path else ROOT / "index.html"
    if path.endswith(".html"):
        out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


def top(h1, lead="", room=False):
    """The top of an inner page. A room's name gets the loop; a longer title, the line runs beside."""
    if room:
        return f"""<section class="wrap top room v-left" aria-label="{h1}">
  <h1><span data-line="circle">{h1}</span></h1>
  {f'<p class="lead" data-line="avoid" data-in>{lead}</p>' if lead else ""}
</section>"""
    return f"""<section class="wrap top">
  <div class="grid" data-line="avoid" data-side="left"><h1 data-in>{h1}</h1>{f'<p class="lead" data-in style="--i:1">{lead}</p>' if lead else ""}</div>
</section>"""


def facts(items):
    lis = "".join(f'<li data-in style="--i:{i}"><b>{b}</b><span>{s}</span></li>' for i, (b, s) in enumerate(items))
    return f'<section class="wrap row grid"><ul class="facts big text-col" data-line="avoid">{lis}</ul></section>'


def text(inner, h2=""):
    head = f"<h2>{h2}</h2>" if h2 else ""
    return f'<section class="wrap row grid"><div class="text text-col" data-line="avoid" data-in>{head}{inner}</div></section>'


def pics(*figs):
    cls = {2: "two", 3: "three"}.get(len(figs), "")
    return f'<section class="wrap row"><div class="pics {cls}">{"".join(figs)}</div></section>'


def hero_pic(src, alt, w, h, caption):
    return f'<section class="wrap row grid">{shot("R7", src, alt, w, h, caption, lazy=False)}</section>'


def nxt(label, href, line="stop"):
    attr = f' data-line="{line}"' if line else ""
    return f'<nav class="wrap next" aria-label="Next"><span>Next</span><a href="{{p}}{href}"{attr}>{label}</a></nav>'


def roles(rows, cls="L7"):
    lis = []
    for i, (item, detail, more) in enumerate(rows):
        m = f"<p>{more}</p>" if more else ""
        lis.append(f'<li data-in style="--i:{i % 3}"><b>{item}</b><span>{detail}</span>{m}</li>')
    return f'<div class="list {cls}" data-line="avoid"><ul>{"".join(lis)}</ul></div>'


PLUS = """<section class="wrap plus grid" id="plus" aria-label="Plus: a drawing everyone adds one line to">
  <div class="sheet" data-line="end">
    <canvas tabindex="0" aria-label="A shared drawing. Drag to add your line, or press Enter." aria-describedby="plus-how"></canvas>
    <div class="label">
      <b>Untitled (Lines), 2026–</b>
      <span>Rodrigo Penide Lema, with interventions by visitors from around the world.</span>
      <span id="plus-how">One line each, in one stroke. For now your line stays on your screen; soon every line will join the same drawing.</span>
      <output aria-live="polite" data-plus-status>The line above is mine. Add one of yours.</output>
    </div>
  </div>
</section>"""

PAGES = []

# ---------- Home ----------
HOSTING_ROWS = [
    ("Class president", "Harvey Mudd, Class of 2028, since 2026", None),
    ("Philanthropy", "Director, Board of Trustees, since 2025", None),
    ("Mentoring", "Fourteen new international students, since 2025", None),
    ("Student affairs", "Representative to the Board, since 2024", None),
    ("Volunteering", "Mudders Making a Difference, since 2024", None),
]


def verb(word, href, side="v-left"):
    return (f'<div class="verb {side}"><h2 id="{href}-h"><a href="{{p}}{href}/">'
            f'<span data-line="circle">{word}</span></a></h2></div>')


HOME = """<header class="hero wrap">
  {bar}
  <div class="logo-box" data-logo="hero" aria-hidden="true"></div>
  <div class="hero-text" data-line-phone="avoid">
    <h1>Rodrigo<br>Penide Lema</h1>
    <p>I study how things are made, and why they matter: engineering at Harvey Mudd, art history at Pomona.</p>
  </div>
</header>

<section class="wrap row intro grid" aria-label="About">
  """ + words("L mid", """<p>Two colleges across one street in Claremont. In one I learn to build things; in the other, to read them.</p>
    <ul class="facts"><li>B.S. Engineering, Harvey Mudd</li><li>B.A. Art History, Pomona</li><li>Class of 2028, five languages</li></ul>
    """ + go("About me", "about/"), i=0) + """
  """ + shot("R4", "portrait.jpg", "Rodrigo in a navy pinstripe shirt under an oak tree on campus", 1200, 1500, i=1, lazy=False) + """
</section>

<section class="wrap" aria-labelledby="making-h">
  """ + verb("Making", "making") + """
  <div class="row grid">
    """ + shot("R6", "kreios.jpg", "The Kreios Space test hall seen from above: two steel vacuum chambers and workbenches", 1800, 1350) + """
    """ + words("W-L end", "<h3>Kreios Space</h3><p>Test hardware for plasma thrusters. The work is under NDA, so its page is mostly words.</p>" + go("Read about it", "making/kreios/")) + """
  </div>
  <div class="row grid">
    """ + shot("L sheet-pic", "e80-render.png", "A drawing of the E80 robot: a square PVC frame with an orange float and a blue electronics box", 614, 407) + """
    """ + words("R mid", "<h3>The E80 robot</h3><p>A robot that floated at Dana Point and measured the sea: 17.86 °C, turbidity under 0.6 NTU.</p>" + go("Read about it", "making/e80/")) + """
  </div>
  <div class="row grid">
    """ + shot("R7", "northstar.jpg", "The electron beam accelerator at NorthStar, where the sensing system will sit", 2000, 1333) + """
    """ + words("W-L", "<h3>NorthStar</h3><p>Sensing an electron beam, on the accelerator itself. Ongoing.</p>" + go("Read about it", "making/northstar/")) + """
  </div>
</section>

<section class="wrap" aria-labelledby="reading-h">
  """ + verb("Reading", "reading", "v-right") + """
  <div class="row grid">
    """ + shot("L4", "clay.jpg", "A hand holding a lump of pale clay over cracked dry ground", 1320, 1752) + """
    """ + words("R mid", "<h3>The materials of Los Angeles</h3><p>Bioregional research with Professor Jia Yi Gu: where a region's clay, stone and timber come from, and who works them.</p>" + go("Read about it", "reading/bioregional/")) + """
  </div>
  <div class="row grid">
    """ + words("R", "<h3>An archive of voices</h3><p>With Professor Isabel Balseiro. And papers in art history, on how things are looked at.</p>", line="avoid", i=0) + """
  </div>
</section>

<section class="wrap" aria-labelledby="looking-h">
  """ + verb("Looking", "looking") + """
  <div class="row grid">
    """ + shot("R", "quarry-window.jpg", "A limestone quarry seen through a gap between two cut walls, with shrubs on the ledges", 1320, 1311) + """
    """ + words("W-L end", "<p class=\"plain\">A quarry, seen from inside another. Provence, summer 2026.</p>") + """
  </div>
  <div class="row grid">
    """ + shot("L6", "stone-saw.jpg", "A man feeds a block of limestone to a large circular saw inside a quarry hall", 1320, 738) + """
    """ + words("W-R end", "<p class=\"plain\">Cutting limestone into blocks.</p>") + """
  </div>
  <div class="row grid">
    """ + shot("R4", "quarry-face.jpg", "Tall rooms cut into a pale quarry face, with pines along the top", 1320, 1299) + """
    """ + words("W-L mid", "<p class=\"plain\">Rooms left behind by the stone that was taken.</p>" + go("All the photographs", "looking/")) + """
  </div>
</section>

<section class="wrap" aria-labelledby="hosting-h">
  """ + verb("Hosting", "hosting", "v-right") + """
  <div class="row grid roles">""" + roles(HOSTING_ROWS, "L6") + """</div>
</section>

""" + PLUS

PAGES.append(dict(path="", title="Rodrigo Penide Lema", home=True, body=HOME))

# ---------- Making ----------
PAGES.append(dict(path="making", title="Making · Rodrigo Penide Lema", room="making", body=top(
    "Making", "Things built, tested, and designed for people.", room=True) + """
<section class="wrap" aria-label="Projects">
  <div class="row grid">
    """ + shot("R6", "kreios.jpg", "The Kreios Space test hall seen from above: two steel vacuum chambers and workbenches", 1800, 1350, lazy=False) + """
    """ + words("W-L end", "<h2>Kreios Space</h2><p>Test hardware for plasma thrusters, summer 2026.</p>" + go("Read about it", "making/kreios/")) + """
  </div>
  <div class="row grid">
    """ + shot("L sheet-pic", "e80-render.png", "A drawing of the E80 robot: a square PVC frame with an orange float and a blue electronics box", 614, 407) + """
    """ + words("R mid", "<h2>The E80 robot</h2><p>Water sensing at Dana Point, spring 2026.</p>" + go("Read about it", "making/e80/")) + """
  </div>
  <div class="row grid">
    """ + shot("R7", "northstar.jpg", "The electron beam accelerator at NorthStar", 2000, 1333) + """
    """ + words("W-L", "<h2>NorthStar</h2><p>Sensing an electron beam, 2026 to now.</p>" + go("Read about it", "making/northstar/")) + """
  </div>
  <div class="row grid roles">""" + roles([
    ("A mine shaft winch", "2025", "A collapsible winch that lowers a sensor payload more than 600 feet into a mine shaft, with gas sensors and live video, on a $400 budget."),
    ("Alumni and students", "Human-centred design, with Pomona College", "Designing better ways for alumni and students across the Claremont Colleges to meet."),
    ("People and animals", "Human-centred design, with The Salvation Army", "Asking how time with animals might support trust and purpose for people recovering from homelessness and addiction, in Orange County."),
]) + """</div>
</section>
""" + nxt("Reading", "reading/")))

# ---------- Kreios ----------
PAGES.append(dict(path="making/kreios", title="Kreios Space · Rodrigo Penide Lema", room="making", body=top(
    "Test hardware for plasma thrusters",
    "I spent the summer of 2026 inside a vacuum-chamber test facility, designing and machining what it was missing.")
    + hero_pic("kreios.jpg", "The Kreios Space test hall seen from above: two steel vacuum chambers, workbenches and the company name on a concrete wall", 1800, 1350, "The test hall, seen from above.")
    + facts([
        ("Kreios Space", "Assembly, integration and test intern, summer 2026"),
        ("Three noble gases", "Through a flow-control panel I designed and machined"),
        ("Three sensing systems", "Mounted inside the chamber on supports I built"),
        ("Mostly words", "The work is confidential under a NATO agreement"),
    ]) + text("""
    <p>I built a control panel for the flow of three noble gases, and supports for three sensing systems inside the chamber. Between builds I ran impedance tests and diagnosed plasma across thrust setups.</p>
    <p>I also started documenting the tests that, until then, had gone unrecorded.</p>
    <p>Much of this work is confidential, so this page is told mostly in words, and the room is all you see.</p>""", "The work")
    + nxt("A robot that floated", "making/e80/")))

# ---------- E80 ----------
PAGES.append(dict(path="making/e80", title="A robot that floated · Rodrigo Penide Lema", room="making", body=top(
    "A robot that floated",
    "We built a surface robot to measure the sea at five points of a beach in Dana Point. Two of its three sensors got the water wrong.")
    + hero_pic("e80-render.png", "A drawing of the robot: a square PVC frame with an orange float, a blue electronics box on top and motors at the corners", 614, 407, "The robot, as drawn before it was built.").replace('class="shot R7"', 'class="shot R6 sheet-pic"')
    + facts([
        ("Five locations", "Baby Beach, Dana Point, spring 2026"),
        ("Six motors", "Forward, back and sideways, in a grid at each site"),
        ("Three sensors", "Temperature, pH and turbidity, about 15 cm down"),
        ("Four of us", "With Emily Bersin, Anna Chen and TJ Kidd"),
    ]) + text("""
    <p>The frame was a floating box of PVC pipe, with an upper platform and a lower mesh, so the sensing structure stayed under water while the robot stayed afloat. The waterproof electronics box sat in the middle of the top platform, to spread the weight evenly and keep the cables short.</p>
    <p>The turbidity sensor pointed down through the platform inside a length of PVC pipe, with its opening facing the direction of travel so fresh water kept flowing past it.</p>""", "The robot")
    + pics(shot("sheet-pic", "e80-frame.png", "A drawing of the PVC frame from above, with its floats cut to fit", 587, 425, "The frame and its floats."),
           shot("sheet-pic", "e80-sketch.png", "A hand sketch of the robot from the side", 740, 330, "An early sketch.", line=None, i=1))
    + text("""
    <p>Each sensor needed its own amplifier to turn a tiny signal into something the Teensy could read: an inverting offset amplifier with a buffer for the thermistor, a non-inverting pair for the pH probe, and for turbidity a 555 timer pulsing an infrared diode, read by a photodiode through a transimpedance amplifier.</p>""", "The circuits")
    + pics(shot("", "e80-thermistor.jpg", "Circuit diagram of the thermistor amplifier", 1260, 680, "Temperature: the thermistor circuit."),
           shot("", "e80-turbidity-circuit.jpg", "Circuit diagram of the turbidity photodiode amplifier", 1280, 610, "Turbidity: the photodiode circuit.", line=None, i=1))
    + text("""
    <p>The robot did everything we asked of it. It floated, followed its path, stopped at each location and logged every sample.</p>
    <p>The thermistor agreed with the sea: an average of 17.86 °C, less than half a degree from the 18.2 °C we measured by hand. The other two did not. The pH sensor read three to four points low, and the turbidity sensor read between 0.28 and 0.54 NTU, where a classmate's sample of the same water measured 13.3.</p>""", "What the sea said")
    + pics(shot("", "e80-temperature.jpg", "Graph of temperature at five locations, flat near 17.9 degrees", 1372, 818, "Temperature at the five locations.", line=None),
           shot("", "e80-ph.jpg", "Graph of pH at five locations, far below the expected line", 1377, 818, "pH, against the expected value.", i=1),
           shot("", "e80-turbidity.jpg", "Graph of turbidity at five locations, all below 0.6", 1389, 818, "Turbidity at the five locations.", line=None, i=2))
    + text("""
    <p>The sensors were not broken. They had been calibrated in fresh water, and the sea is not fresh water: salt changes how a thermistor and a pH probe behave, and our turbidity amplifier had so much gain that it saw almost nothing at all.</p>
    <p>The robot worked. The lesson was about calibration: test the whole sensor, mounted, in the water it will actually meet.</p>
    <p class="small">Engineering 80, Harvey Mudd, spring 2026. Thanks to Professors Helms, Mohanty, Sinopoli and Yang, to Lynn and Xavier, and to Angie Zhou and Spencer Michaelson for sharing their measurements of the water.</p>""", "What I learned")
    + nxt("Sensing an electron beam", "making/northstar/")))

# ---------- NorthStar ----------
PAGES.append(dict(path="making/northstar", title="NorthStar · Rodrigo Penide Lema", room="making", body=top(
    "Sensing an electron beam",
    "At NorthStar I am helping design the system that senses the beam of an electron accelerator.")
    + hero_pic("northstar.jpg", "A particle accelerator on its delivery day: a large ring of dark magnets wrapped in blue and red tubing, pressure gauges in front, a worker bending down beside it", 2000, 1333, "The accelerator our system is designed for, on the day it arrived. Photograph: NorthStar.")
    + facts([
        ("NorthStar", "2026 to now"),
        ("An electron beam", "Inside a particle accelerator"),
        ("Simulated first", "Modelled in FLUKA before it is built"),
    ]) + text("""
    <p>We are designing a sensing system that works inside the accelerator itself, where the beam runs. Before anything is built, we model how it will behave in FLUKA, a code for simulating particles passing through matter.</p>
    <p>The project is under way; more here as it can be shared.</p>""", "The work")
    + nxt("Test hardware for plasma thrusters", "making/kreios/")))

# ---------- Reading ----------
PAGES.append(dict(path="reading", title="Reading · Rodrigo Penide Lema", room="reading", body=top(
    "Reading", "Materials, archives and images, read closely.", room=True) + """
<section class="wrap" aria-label="Research">
  <div class="row grid">
    """ + shot("R6", "quarry-walk.jpg", "The residency group in hard hats and orange vests walking across a sand quarry", 1320, 977, lazy=False) + """
    """ + words("W-L end", "<h2>The materials of a region</h2><p>Bioregional research with Professor Jia Yi Gu, 2026 to now.</p>" + go("Read about it", "reading/bioregional/")) + """
  </div>
  <div class="row grid">
    """ + shot("L4", "stone-workshop.jpg", "A stone workshop: shelves of offcuts and tools under a coat of white dust", 1320, 1316) + """
    """ + words("R mid", "<h2>An archive of voices</h2><p>Research in comparative literature with Professor Isabel Balseiro: building and keeping an archive of some 3,000 documents and 120 hours of recorded interviews. 2025 to now.</p>") + """
  </div>
  <div class="row grid">
    """ + words("R", "<h2>Papers in art history</h2><p>Pomona College. The first ones will be here soon.</p>", line="avoid", i=0) + """
  </div>
</section>
""" + nxt("Looking", "looking/")))

# ---------- Bioregional ----------
PAGES.append(dict(path="reading/bioregional", title="Bioregional materials · Rodrigo Penide Lema", room="reading", body=top(
    "The materials of a region",
    "What grows and is made around Los Angeles, and who makes it: a method I brought back from a residency in France.")
    + hero_pic("quarry-walk.jpg", "The residency group in hard hats and orange vests walking across a sand quarry", 1320, 977, "Walking a quarry with the residency, summer 2026.")
    + facts([
        ("Atelier LUMA", "A residency on bioregional materials, Arles, summer 2026"),
        ("Biofabrique LA", "Founding student researcher"),
        ("Jia Yi Gu", "The professor I do this research with"),
        ("Four schools", "Harvey Mudd, MIT, USC and SCI-Arc"),
    ]) + text("""
    <p>I spent the summer of 2026 in a residency on bioregional materials at Atelier LUMA in Arles: stone, earth and clay, the people who quarry and shape them, and the distances between them.</p>
    <p>Back in California, I adapted that work into a method for mapping the material streams, suppliers and craftspeople of Southern California, to find where building and design could source locally.</p>
    <p>I do this as the founding student researcher of Biofabrique LA, with faculty from Harvey Mudd, MIT, USC and SCI-Arc, and with researchers at Atelier LUMA.</p>""", "The method")
    + pics(shot("", "clay.jpg", "A hand holding a lump of pale clay over cracked dry ground", 1320, 1752, "Clay, picked up on site."),
           shot("", "stone-saw.jpg", "A man feeds a block of limestone to a large circular saw", 1320, 738, "Cutting limestone into blocks.", line=None, i=1))
    + nxt("A robot that floated", "making/e80/")))

# ---------- Looking ----------
LOOK = [
    ("R", "W-L end", "quarry-window.jpg", "A limestone quarry seen through a gap between two cut walls", 1320, 1311, "A quarry, seen from inside another."),
    ("L6", "W-R end", "stone-saw.jpg", "A man feeds a block of limestone to a large circular saw inside a quarry hall", 1320, 738, "Cutting limestone into blocks."),
    ("R4", "W-L mid", "quarry-face.jpg", "Tall rooms cut into a pale quarry face, with pines along the top", 1320, 1299, "Rooms left behind by the stone that was taken."),
    ("L4", "R end", "clay.jpg", "A hand holding a lump of pale clay over cracked dry ground", 1320, 1752, "Clay, picked up on site."),
    ("R6", "W-L end", "quarry-inside.jpg", "Inside a quarry: cut walls, and a floor of white rubble and dust", 1320, 1311, "Inside, the floor is rubble and dust."),
    ("L6", "W-R end", "quarry-walk.jpg", "The residency group in hard hats and orange vests walking across a sand quarry", 1320, 977, "Walking a working quarry."),
    ("R4", "W-L mid", "stone-workshop.jpg", "A stone workshop: shelves of offcuts and tools under a coat of white dust", 1320, 1316, "A stone workshop."),
    ("L6", "W-R end", "arles.jpg", "The residency cohort standing in front of a limestone quarry wall in the sun", 1600, 1600, "The cohort, Arles."),
]
PAGES.append(dict(path="looking", title="Looking · Rodrigo Penide Lema", room="looking", body=top(
    "Looking", "Photographs from a residency on stone and earth in Provence, summer 2026.", room=True)
    + '<section class="wrap" aria-label="Photographs">' + "".join(
        f'<div class="row grid">{shot(sc, src, alt, w, h, lazy=k > 1)}{words(wc, f"<p class=\"plain\">{cap}</p>")}</div>'
        for k, (sc, wc, src, alt, w, h, cap) in enumerate(LOOK)) + "</section>"
    + nxt("Hosting", "hosting/")))

# ---------- Hosting ----------
PAGES.append(dict(path="hosting", title="Hosting · Rodrigo Penide Lema", room="hosting", body=top(
    "Hosting", "Making room for other people: the roles I have been trusted with.", room=True)
    + '<section class="wrap"><div class="row grid roles">' + roles([
        ("Class president", "Harvey Mudd, Class of 2028, since 2026", "Elected by my classmates."),
        ("Philanthropy", "Director, Board of Trustees, since 2025", "Five fundraising campaigns designed for student initiatives and clubs, and a seat on the branding group for the College's major campaign."),
        ("Mentoring", "New International Students and Scholars, since 2025", "A cohort of fourteen first-year students, one to one and in monthly gatherings."),
        ("Student affairs", "Representative to the Board of Trustees, since 2024", "The student voice on the Board's Student Affairs Committee."),
        ("Volunteering", "Mudders Making a Difference, since 2024", "Blood drives, tutoring at Claremont High School, and campaigns for local charities."),
    ]) + "</div></section>"
    + nxt("Journal", "journal/")))

# ---------- Journal ----------
PAGES.append(dict(path="journal", title="Journal · Rodrigo Penide Lema", room="journal", body=top(
    "Journal", "Notes, newest first. The first entry is on its way.", room=True)
    + nxt("Add a line to the drawing", "plus/")))

# ---------- + ----------
PAGES.append(dict(path="plus", title="+ · Rodrigo Penide Lema", room="plus", body=top(
    "One shared drawing", "Every visitor adds a single line to it.") + PLUS))

# ---------- About ----------
PAGES.append(dict(path="about", title="About · Rodrigo Penide Lema", room="about", body=top(
    "Rodrigo Penide Lema", "I study how things are made, and why they matter.") + """
<section class="wrap row grid">
  """ + shot("R4", "portrait.jpg", "Rodrigo in a navy pinstripe shirt under an oak tree on campus", 1200, 1500, lazy=False) + """
  """ + words("W-L mid", "<p class=\"plain\">Most of my work happens where those two questions meet: in a vacuum chamber, in an archive of interviews, in a map of the materials that grow and are made around Los Angeles.</p>") + """
</section>
""" + text("""
    <h2>Study</h2><p>B.S. Engineering, Harvey Mudd College. B.A. Art History, Pomona College. Class of 2028.</p>
    <h2>Languages</h2><p>Spanish, Galician and Portuguese, natively. English and French.</p>
    <h2>Honours</h2><p>Randal Lewis Fellow in Innovation and Entrepreneurship. Emerging Leader Award, Harvey Mudd, 2025 and 2026.</p>""")
    + nxt("Making", "making/")))

# ---------- 404 ----------
PAGES.append(dict(path="404.html", title="Not found · Rodrigo Penide Lema", body=top(
    "This page is not here", "The line goes on somewhere else.") + nxt("Back to the beginning", "")))

if __name__ == "__main__":
    for page in PAGES:
        frame(page["path"], page["title"], page["body"], page.get("room"), home=page.get("home", False))
    print(f"Built {len(PAGES)} pages")
