"""Builds the static pages of penidelema.com.

Every page shares one frame (top bar, phone menu, footer, scripts). Content lives in the
PAGES list below; "{p}" in content is replaced with the relative path to the site root.
Run `python3 tools/build.py` from the repository root, then commit the generated .html
files: GitHub Pages serves them as they are.

Design: "the name as a monument" (art direction from the taste-skill, see
website/tools/taste-skill in the project files). The home page sets the name as large as a
quarry face, with a window between the two family names that shows the work. One serif
(Brygada 1918), five sizes, wall ground, ink, one navy accent. No thin rules, no shadows,
no small capitals.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROOMS = [("making", "Making"), ("reading", "Reading"), ("looking", "Looking"),
         ("hosting", "Hosting"), ("journal", "Journal"), ("plus", "+")]
EMAIL = "rpenidelema@g.hmc.edu"

MARK = ('<svg class="mark" viewBox="0 0 44 60" aria-hidden="true">'
        '<path d="M12 54 V18" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>'
        '<path d="M12 28 C 16 16, 26 12, 34 15" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg>')

ARROW = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 5l7 7-7 7" fill="none" '
         'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

WELCOME = """<div class="welcome" hidden aria-hidden="true">
  <svg viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">
    <defs>
      <mask id="win" maskUnits="userSpaceOnUse" x="0" y="0" width="1600" height="900">
        <rect width="1600" height="900" fill="black"/>
        <g id="win-g" transform="translate(800 450)">
          <path d="M-12 54 V-26" fill="none" stroke="white" stroke-width="14" stroke-linecap="round"/>
          <path d="M-12 -4 C 0 -34, 26 -44, 46 -36" fill="none" stroke="white" stroke-width="14" stroke-linecap="round"/>
        </g>
        <rect id="mfill" width="1600" height="900" fill="white" opacity="0"/>
      </mask>
    </defs>
    <rect width="1600" height="900" fill="#ffffff"/>
    <g id="ink-g" transform="translate(800 450)">
      <path id="s1" d="M-12 -4 C 0 -34, 26 -44, 46 -36" fill="none" stroke="#111214" stroke-width="7" stroke-linecap="round"/>
      <path id="s2" d="M-12 54 V-26" fill="none" stroke="#111214" stroke-width="7" stroke-linecap="round"/>
    </g>
    <image id="photo" href="{p}assets/img/quarry-window.jpg" x="0" y="0" width="1600" height="900" preserveAspectRatio="xMidYMid slice" mask="url(#win)" opacity="0"/>
  </svg>
  <span class="skip">Tap to skip</span>
</div>"""


def img(src, alt, w, h, cls="", lazy=True):
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{{p}}assets/img/{src}" alt="{alt}" width="{w}" height="{h}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async">')


def fig(cls, src, alt, w, h, caption, shutter=True, i=0):
    s = " shutter" if shutter else ""
    # Shutter images load eagerly: a clipped-shut frame never counts as "near the screen" for lazy loading.
    return (f'<figure class="{cls}"><div class="{s.strip()}" style="--i:{i}">{img(src, alt, w, h, lazy=not shutter)}</div>'
            f'<figcaption>{caption}</figcaption></figure>')


def bar(p, room):
    links = "".join(
        f'<a href="{p}{slug}/"{" aria-current=\"page\"" if slug == room else ""}>{name}</a>'
        for slug, name in ROOMS)
    return f"""<header class="bar">
  <a class="wordmark" href="{p}">{MARK}<span>Rodrigo Penide Lema</span></a>
  <nav class="rooms" aria-label="Rooms">{links}<a href="{p}about/"{" aria-current=\"page\"" if room == "about" else ""}>About</a></nav>
  <button type="button" class="menu-btn" data-menu="open" aria-expanded="false">Menu</button>
</header>"""


def foot(p):
    links = "".join(f'<a href="{p}{slug}/">{name}</a>' for slug, name in ROOMS)
    return f"""<footer class="foot">
  <nav aria-label="Rooms, again" data-reveal>{links}<a href="{p}about/">About</a><a href="mailto:{EMAIL}">{EMAIL}</a></nav>
  <p class="big" aria-hidden="true" data-reveal style="--i:1">Rodrigo Penide Lema</p>
  <div class="fine" data-reveal style="--i:2"><span>Engineering at Harvey Mudd, art history at Pomona.</span><span>English for now. Español and galego are on their way.</span><span>2026</span></div>
</footer>"""


def frame(path, title, body, room=None, welcome=False, desc=None, home=False):
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Brygada+1918:ital,wght@0,400;0,500;1,400&display=swap">
<link rel="stylesheet" href="{p}assets/css/site.css">
</head>
<body>
{top}
<div class="overlay" hidden>
  <div class="top"><a href="{p}">Rodrigo Penide Lema</a><button type="button" data-menu="close">Close</button></div>
  <ul>{overlay}<li><a href="{p}about/">About</a></li></ul>
  <p class="small muted">English for now. Español and galego are on their way.</p>
</div>
{body.replace("{p}", p).replace("{bar}", bar(p, room))}
{foot(p)}
{WELCOME.replace("{p}", p) if welcome else ""}
<script src="{p}assets/js/site.js"></script>
</body>
</html>
"""
    out = ROOT / path / "index.html" if path else ROOT / "index.html"
    if path.endswith(".html"):
        out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


def facts(items, cls=""):
    lis = "".join(f'<li data-reveal style="--i:{i}"><b>{b}</b><span>{s}</span></li>' for i, (b, s) in enumerate(items))
    return f'<ul class="facts {cls}">{lis}</ul>'


def head(h1, lead, after=""):
    """The top of an inner page: title, one sentence, and whatever belongs to it (picture, facts)."""
    return f"""<section class="top">
<div class="head grid">
  <h1 data-reveal>{h1}</h1>
  <p class="lead" data-reveal style="--i:1">{lead}</p>
</div>
{after}
</section>"""


def article(h2, text, extra=""):
    return f"""<section class="article grid">
  <h2 data-reveal>{h2}</h2>
  <div class="text" data-reveal style="--i:1">{text}</div>
  {extra}
</section>"""


def nxt(label, href):
    return f'<nav class="next" aria-label="Next"><span>Next</span><a href="{{p}}{href}">{label}</a></nav>'


def poster_list(rows):
    out = []
    for i, (item, detail, href) in enumerate(rows):
        it = f'<a class="item" href="{{p}}{href}">{item}</a>' if href else f'<span class="item">{item}</span>'
        out.append(f'<li data-reveal style="--i:{i}">{it}<span class="detail">{detail}</span></li>')
    return "".join(out)


CONTACT = f"""<section class="contact" aria-labelledby="write">
  <div class="row"><h2 id="write">Write to me</h2></div>
  <div class="row"><a class="email" href="mailto:{EMAIL}">{EMAIL}</a></div>
  <div class="row"><span>Claremont, California</span></div>
  <div class="row greet-row"><span class="greet"><span>Hola</span><a class="go" href="mailto:{EMAIL}?subject=Hola%20Rodrigo" aria-label="Write an email to Rodrigo">{ARROW}</a></span></div>
</section>"""

PLUS = """<section class="plus grid" aria-labelledby="plus-h">
  <h2 id="plus-h" data-reveal>Add one line</h2>
  <div class="plus-frame" data-reveal><canvas tabindex="0" aria-label="A shared drawing. Draw one line with your finger or mouse, or press Enter to add one." aria-describedby="plus-how"></canvas></div>
  <div class="label" data-reveal style="--i:1">
    <p class="t">Untitled (Lines)</p>
    <p>2026–</p>
    <p>Rodrigo Penide Lema, with interventions by visitors from around the world</p>
    <p class="how" id="plus-how">One line each, drawn in one stroke. For now your line stays on your screen; soon every line will join the same drawing.</p>
    <p class="small" data-plus-status aria-live="polite"></p>
  </div>
</section>"""

PAGES = []

# ---------- Home ----------
WINDOW = ('<span class="win" aria-hidden="true">'
          + img("quarry-window.jpg", "", 1320, 1311, lazy=False)
          + img("kreios.jpg", "", 1800, 1350, lazy=False)
          + img("northstar.jpg", "", 2000, 1333, lazy=False)
          + img("clay.jpg", "", 1320, 1752, lazy=False)
          + '</span>')

HOME = """<section class="monument">
  {bar}
  <div class="says">
    <p>I study how things are made, and why they matter: engineering at Harvey Mudd, art history at Pomona.</p>
    <a class="button" href="#work">See the work """ + ARROW.replace('<svg ', '<svg width="20" height="20" ') + """</a>
  </div>
  <h1 class="name"><span class="sr">Rodrigo </span><span class="first">Penide</span>""" + WINDOW + """<span class="second">Lema</span></h1>
</section>

<section class="intro grid" aria-labelledby="one">
  <h2 id="one" data-reveal>One practice</h2>
  <p class="note" data-reveal style="--i:1">Two colleges across one street in Claremont. In one I learn to build things; in the other, to read them. Most of my work happens where the two meet.</p>
</section>
""" + facts([
    ("Harvey Mudd", "B.S. Engineering"),
    ("Pomona", "B.A. Art History"),
    ("2028", "Graduating class"),
    ("Five languages", "Spanish, Galician and Portuguese from home; English and French"),
]) + """
<div class="intro grid" style="padding-top:0">
  <p class="lead-in" data-reveal>A vacuum chamber, a robot at sea, a quarry in Provence, an archive of voices.</p>
  <figure><div class="shutter">""" + img("portrait.jpg", "Rodrigo in a navy pinstripe shirt under an oak tree on campus", 1200, 1500, lazy=False) + """</div></figure>
</div>

<section class="work grid" id="work" aria-labelledby="making-h">
  <h2 id="making-h" data-reveal>Making</h2>
  <p class="run" data-reveal style="--i:1"><a href="{p}making/kreios/">Plasma thruster test hardware at Kreios Space<span class="pic">""" + img("kreios.jpg", "", 1800, 1350) + """</span></a>, <a href="{p}making/e80/">a robot that floated at Dana Point<span class="pic">""" + img("e80-render.png", "", 614, 407) + """</span></a>, <a href="{p}making/northstar/">beam sensing at NorthStar<span class="pic">""" + img("northstar.jpg", "", 2000, 1333) + """</span></a>, <span class="n">a mine shaft winch, and design with people.</span></p>
</section>
<section class="work grid" style="padding-top:64px" aria-labelledby="reading-h">
  <h2 id="reading-h" data-reveal>Reading</h2>
  <p class="run" data-reveal style="--i:1"><a href="{p}reading/bioregional/">The materials of Los Angeles, with Jia Yi Gu<span class="pic">""" + img("clay.jpg", "", 1320, 1752) + """</span></a>, <span class="n">an archive of voices with Isabel Balseiro, and papers in art history.</span></p>
  <p class="count">Eight projects, 2024 to now.</p>
</section>

<section class="gallery grid" aria-labelledby="looking-h">
  <h2 id="looking-h" data-reveal>Looking</h2>
  """ + fig("g-a", "quarry-window.jpg", "A limestone quarry seen through a gap between two cut walls, with shrubs growing on the ledges", 1320, 1311, "A quarry, seen from inside another. Summer 2026.") + """
  """ + fig("g-b", "stone-saw.jpg", "A man feeds a block of limestone to a large circular saw inside a quarry hall", 1320, 738, "Cutting limestone into blocks.") + """
  """ + fig("g-c", "quarry-face.jpg", "Tall rooms cut into a pale quarry face, with pines along the top", 1320, 1299, "Rooms left behind by the stone that was taken.") + """
  """ + fig("g-d", "clay.jpg", "A hand holding a lump of pale clay over cracked dry ground", 1320, 1752, "Clay, picked up on site.") + """
  <p class="more" data-reveal><a class="link" href="{p}looking/">All the photographs</a></p>
</section>

<section class="poster grid" aria-labelledby="hosting-h">
  <h2 id="hosting-h" data-reveal>Hosting</h2>
  <ul>""" + "{HOSTING_ROWS}" + """</ul>
  <p class="more" data-reveal><a class="link" href="{p}hosting/">What each one involves</a></p>
</section>

""" + PLUS + "\n" + CONTACT

HOSTING_ROWS = [
    ("Class president", "Harvey Mudd, Class of 2028, since 2026", None),
    ("Philanthropy", "Director, Board of Trustees, since 2025", None),
    ("Mentoring", "Fourteen new international students, since 2025", None),
    ("Student affairs", "Representative to the Board, since 2024", None),
    ("Volunteering", "Mudders Making a Difference, since 2024", None),
]

PAGES.append(dict(path="", title="Rodrigo Penide Lema", welcome=True, home=True,
                  body=HOME.replace("{HOSTING_ROWS}", poster_list(HOSTING_ROWS))))

# ---------- Making ----------
PAGES.append(dict(path="making", title="Making · Rodrigo Penide Lema", room="making", body=head(
    "Making", "Things built, tested, and designed for people.") + """
<section class="poster grid" aria-label="Projects">
  <ul>""" + poster_list([
    ("Kreios Space", "Test hardware for plasma thrusters, 2026", "making/kreios/"),
    ("The E80 robot", "Water sensing at Dana Point, 2026", "making/e80/"),
    ("NorthStar", "Sensing an electron beam, 2026 to now", "making/northstar/"),
    ("A mine shaft winch", "A sensor payload lowered 600 feet, 2025", None),
    ("Alumni and students", "Human-centred design, with Pomona College", None),
    ("People and animals", "Human-centred design, with The Salvation Army", None),
]) + """</ul>
  <div class="pair">
    """ + fig("", "kreios.jpg", "The Kreios Space test hall seen from above: two steel vacuum chambers and workbenches", 1800, 1350, "The test hall at Kreios Space.") + """
    """ + fig("", "e80-render.png", "A drawing of the E80 robot: a square PVC frame with an orange float and a blue electronics box", 614, 407, "The E80 robot, drawn before it was built.", i=1) + """
  </div>
</section>
<section class="article grid">
  <h2 data-reveal>Still to be written up</h2>
  <div class="text" data-reveal style="--i:1">
    <p>A collapsible winch that lowers a sensor payload more than 600 feet into a mine shaft, with gas sensors and live video, on a $400 budget.</p>
    <p>With Pomona College, designing better ways for alumni and students across the Claremont Colleges to meet.</p>
    <p>With The Salvation Army in Orange County, asking how time with animals might support trust and purpose for people recovering from homelessness and addiction.</p>
  </div>
</section>"""))

# ---------- Kreios ----------
PAGES.append(dict(path="making/kreios", title="Kreios Space · Rodrigo Penide Lema", room="making", body=head(
    "Test hardware for plasma thrusters",
    "I spent the summer of 2026 inside a vacuum-chamber test facility, designing and machining what it was missing.", """
<figure class="hero-pic"><div class="shutter">""" + img("kreios.jpg", "The Kreios Space test hall seen from above: two steel vacuum chambers, workbenches and the company name on a concrete wall", 1800, 1350, lazy=False) + """</div><figcaption>The test hall, seen from above.</figcaption></figure>
""" + facts([
    ("Kreios Space", "Assembly, integration and test intern, summer 2026"),
    ("Three noble gases", "Through a flow-control panel I designed and machined"),
    ("Three sensing systems", "Mounted inside the chamber on supports I built"),
    ("Mostly words", "The work is confidential under a NATO agreement"),
], "inner")) + article("The work", """
    <p>I built a control panel for the flow of three noble gases, and supports for three sensing systems inside the chamber. Between builds I ran impedance tests and diagnosed plasma across thrust setups.</p>
    <p>I also started documenting the tests that, until then, had gone unrecorded.</p>
    <p>Much of this work is confidential, so this page is told mostly in words, and the room is all you see.</p>""") + nxt("A robot that floated", "making/e80/")))

# ---------- E80 ----------
PAGES.append(dict(path="making/e80", title="A robot that floated · Rodrigo Penide Lema", room="making", body=head(
    "A robot that floated",
    "We built a surface robot to measure the sea at five points of a beach in Dana Point. Two of its three sensors got the water wrong.", """
<div class="band">
  <div class="grid">
    <div class="inside" data-reveal><p>A floating PVC frame, six motors, and three sensors hanging under the surface.</p></div>
    """ + fig("", "e80-render.png", "A drawing of the robot: a square PVC frame with an orange float, a blue electronics box on top and motors at the corners", 614, 407, "The robot, as drawn before it was built.") + """
  </div>
</div>
""" + facts([
    ("Five locations", "Baby Beach, Dana Point, spring 2026"),
    ("Six motors", "Forward, back and sideways, in a grid at each site"),
    ("Three sensors", "Temperature, pH and turbidity, about 15 cm down"),
    ("Four of us", "With Emily Bersin, Anna Chen and TJ Kidd"),
], "inner")) + article("The robot", """
    <p>The frame was a floating box of PVC pipe, with an upper platform and a lower mesh, so the sensing structure stayed under water while the robot stayed afloat. The waterproof electronics box sat in the middle of the top platform, to spread the weight evenly and keep the cables short.</p>
    <p>The turbidity sensor pointed down through the platform inside a length of PVC pipe, with its opening facing the direction of travel so fresh water kept flowing past it.</p>""",
    '<div class="duo">' + fig("", "e80-frame.png", "A drawing of the PVC frame from above, with its floats cut to fit", 587, 425, "The frame and its floats.")
    + fig("", "e80-sketch.png", "A hand sketch of the robot from the side", 740, 330, "An early sketch.", i=1) + '</div>') + article("The circuits", """
    <p>Each sensor needed its own amplifier to turn a tiny signal into something the Teensy could read: an inverting offset amplifier with a buffer for the thermistor, a non-inverting pair for the pH probe, and for turbidity a 555 timer pulsing an infrared diode, read by a photodiode through a transimpedance amplifier.</p>""",
    '<div class="duo">' + fig("on-white", "e80-thermistor.jpg", "Circuit diagram of the thermistor amplifier", 1260, 680, "Temperature: the thermistor circuit.")
    + fig("on-white", "e80-turbidity-circuit.jpg", "Circuit diagram of the turbidity photodiode amplifier", 1280, 610, "Turbidity: the photodiode circuit.", i=1) + '</div>') + article("What the sea said", """
    <p>The robot did everything we asked of it. It floated, followed its path, stopped at each location and logged every sample.</p>
    <p>The thermistor agreed with the sea: an average of 17.86 °C, less than half a degree from the 18.2 °C we measured by hand. The other two did not. The pH sensor read three to four points low, and the turbidity sensor read between 0.28 and 0.54 NTU, where a classmate's sample of the same water measured 13.3.</p>""",
    '<div class="trio">' + fig("on-white", "e80-temperature.jpg", "Graph of temperature at five locations, flat near 17.9 degrees", 1372, 818, "Temperature at the five locations.")
    + fig("on-white", "e80-ph.jpg", "Graph of pH at five locations, far below the expected line", 1377, 818, "pH, against the expected value.", i=1)
    + fig("on-white", "e80-turbidity.jpg", "Graph of turbidity at five locations, all below 0.6", 1389, 818, "Turbidity at the five locations.", i=2) + '</div>') + article("What I learned", """
    <p>The sensors were not broken. They had been calibrated in fresh water, and the sea is not fresh water: salt changes how a thermistor and a pH probe behave, and our turbidity amplifier had so much gain that it saw almost nothing at all.</p>
    <p>The robot worked. The lesson was about calibration: test the whole sensor, mounted, in the water it will actually meet.</p>
    <p class="small muted">Engineering 80, Harvey Mudd, spring 2026. Thanks to Professors Helms, Mohanty, Sinopoli and Yang, to Lynn and Xavier, and to Angie Zhou and Spencer Michaelson for sharing their measurements of the water.</p>""") + nxt("Sensing an electron beam", "making/northstar/")))

# ---------- NorthStar ----------
PAGES.append(dict(path="making/northstar", title="NorthStar · Rodrigo Penide Lema", room="making", body=head(
    "Sensing an electron beam",
    "At NorthStar I am helping design the system that senses the beam of an electron accelerator.", """
<figure class="hero-pic"><div class="shutter">""" + img("northstar.jpg", "A particle accelerator on its delivery day: a large ring of dark magnets wrapped in blue and red tubing, pressure gauges in front, a worker bending down beside it", 2000, 1333, lazy=False) + """</div><figcaption>The accelerator our system is designed for, on the day it arrived. Photograph: NorthStar.</figcaption></figure>
""" + facts([
    ("NorthStar", "2026 to now"),
    ("An electron beam", "Inside a particle accelerator"),
    ("Simulated first", "Modelled in FLUKA before it is built"),
], "inner")) + article("The work", """
    <p>We are designing a sensing system that works inside the accelerator itself, where the beam runs. Before anything is built, we model how it will behave in FLUKA, a code for simulating particles passing through matter.</p>
    <p>The project is under way; more here as it can be shared.</p>""") + nxt("Test hardware for plasma thrusters", "making/kreios/")))

# ---------- Reading ----------
PAGES.append(dict(path="reading", title="Reading · Rodrigo Penide Lema", room="reading", body=head(
    "Reading", "Materials, archives and images, read closely.") + """
<section class="poster grid" aria-label="Research">
  <ul>""" + poster_list([
    ("Bioregional materials", "With Professor Jia Yi Gu, 2026 to now", "reading/bioregional/"),
    ("An archive of voices", "With Professor Isabel Balseiro, 2025 to now", None),
    ("Papers in art history", "Pomona College, coming soon", None),
]) + """</ul>
  <div class="pair">
    """ + fig("", "quarry-walk.jpg", "The residency group in hard hats and orange vests walking across a sand quarry", 1320, 977, "Walking a quarry with the residency, summer 2026.") + """
    """ + fig("", "stone-workshop.jpg", "A stone workshop: shelves of offcuts and tools under a coat of white dust", 1320, 1316, "A stone workshop.", i=1) + """
  </div>
</section>
<section class="article grid">
  <h2 data-reveal>An archive of voices</h2>
  <div class="text" data-reveal style="--i:1">
    <p>Research in comparative literature with Professor Isabel Balseiro: building and keeping an archive of some 3,000 documents and 120 hours of recorded interviews.</p>
  </div>
</section>"""))

# ---------- Bioregional ----------
PAGES.append(dict(path="reading/bioregional", title="Bioregional materials · Rodrigo Penide Lema", room="reading", body=head(
    "The materials of a region",
    "What grows and is made around Los Angeles, and who makes it: a method I brought back from a residency in France.", """
<figure class="hero-pic"><div class="shutter">""" + img("quarry-walk.jpg", "The residency group in hard hats and orange vests walking across a sand quarry", 1320, 977, lazy=False) + """</div><figcaption>Walking a quarry with the residency, summer 2026.</figcaption></figure>
""" + facts([
    ("Atelier LUMA", "A residency on bioregional materials, Arles, summer 2026"),
    ("Biofabrique LA", "Founding student researcher"),
    ("Jia Yi Gu", "The professor I do this research with"),
    ("Four schools", "Harvey Mudd, MIT, USC and SCI-Arc"),
], "inner")) + article("The method", """
    <p>I spent the summer of 2026 in a residency on bioregional materials at Atelier LUMA in Arles: stone, earth and clay, the people who quarry and shape them, and the distances between them.</p>
    <p>Back in California, I adapted that work into a method for mapping the material streams, suppliers and craftspeople of Southern California, to find where building and design could source locally.</p>
    <p>I do this as the founding student researcher of Biofabrique LA, with faculty from Harvey Mudd, MIT, USC and SCI-Arc, and with researchers at Atelier LUMA.</p>""",
    '<div class="duo">' + fig("", "clay.jpg", "A hand holding a lump of pale clay over cracked dry ground", 1320, 1752, "Clay, picked up on site.")
    + fig("", "stone-saw.jpg", "A man feeds a block of limestone to a large circular saw", 1320, 738, "Cutting limestone into blocks.", i=1) + '</div>') + nxt("A robot that floated", "making/e80/")))

# ---------- Looking ----------
PAGES.append(dict(path="looking", title="Looking · Rodrigo Penide Lema", room="looking", body=head(
    "Looking", "Photographs from a residency on stone and earth in Provence, summer 2026.") + """
<section class="gallery grid" aria-label="Photographs" style="padding-top:clamp(56px,7vw,104px)">
  """ + fig("g-a", "quarry-window.jpg", "A limestone quarry seen through a gap between two cut walls", 1320, 1311, "A quarry, seen from inside another.") + """
  """ + fig("g-b", "stone-saw.jpg", "A man feeds a block of limestone to a large circular saw inside a quarry hall", 1320, 738, "Cutting limestone into blocks.") + """
  """ + fig("g-c", "quarry-face.jpg", "Tall rooms cut into a pale quarry face, with pines along the top", 1320, 1299, "Rooms left behind by the stone that was taken.") + """
  """ + fig("g-d", "clay.jpg", "A hand holding a lump of pale clay over cracked dry ground", 1320, 1752, "Clay, picked up on site.") + """
  """ + fig("g-a2", "quarry-inside.jpg", "Inside a quarry: cut walls, and a floor of white rubble and dust", 1320, 1311, "Inside, the floor is rubble and dust.") + """
  """ + fig("g-b2", "quarry-walk.jpg", "The residency group in hard hats and orange vests walking across a sand quarry", 1320, 977, "Walking a working quarry.") + """
  """ + fig("g-c2", "stone-workshop.jpg", "A stone workshop: shelves of offcuts and tools under a coat of white dust", 1320, 1316, "A stone workshop.") + """
  """ + fig("g-d2", "arles.jpg", "The residency cohort standing in front of a limestone quarry wall in the sun", 1600, 1600, "The cohort, Arles.") + """
</section>"""))

# ---------- Hosting ----------
PAGES.append(dict(path="hosting", title="Hosting · Rodrigo Penide Lema", room="hosting", body=head(
    "Hosting", "Making room for other people: the roles I have been trusted with.") + """
<section class="poster grid" aria-label="Roles">
  <ul>
    <li data-reveal><span class="item">Class president</span><span class="detail">Harvey Mudd, Class of 2028, since 2026</span><p class="say roles-say">Elected by my classmates.</p></li>
    <li data-reveal><span class="item">Philanthropy</span><span class="detail">Director, Board of Trustees, since 2025</span><p class="say roles-say">Five fundraising campaigns designed for student initiatives and clubs, and a seat on the branding group for the College's major campaign.</p></li>
    <li data-reveal><span class="item">Mentoring</span><span class="detail">New International Students and Scholars, since 2025</span><p class="say roles-say">A cohort of fourteen first-year students, one to one and in monthly gatherings.</p></li>
    <li data-reveal><span class="item">Student affairs</span><span class="detail">Representative to the Board of Trustees, since 2024</span><p class="say roles-say">The student voice on the Board's Student Affairs Committee.</p></li>
    <li data-reveal><span class="item">Volunteering</span><span class="detail">Mudders Making a Difference, since 2024</span><p class="say roles-say">Blood drives, tutoring at Claremont High School, and campaigns for local charities.</p></li>
  </ul>
</section>"""))

# ---------- Journal ----------
PAGES.append(dict(path="journal", title="Journal · Rodrigo Penide Lema", room="journal", body=head(
    "Journal", "Notes, newest first. The first entry is on its way.")))

# ---------- + ----------
PAGES.append(dict(path="plus", title="+ · Rodrigo Penide Lema", room="plus", body=head(
    "One shared drawing", "Every visitor adds a single line.") + PLUS))

# ---------- About ----------
PAGES.append(dict(path="about", title="About · Rodrigo Penide Lema", room="about", body="""<section class="about grid">
  <figure data-reveal>""" + img("portrait.jpg", "Rodrigo in a navy pinstripe shirt under an oak tree on campus", 1200, 1500, lazy=False) + """</figure>
  <div class="text">
    <h1 data-reveal>Rodrigo Penide Lema</h1>
    <p class="lead" data-reveal style="--i:1">I study how things are made, and why they matter.</p>
    <p data-reveal style="--i:2">Most of my work happens where those two questions meet: in a vacuum chamber, in an archive of interviews, in a map of the materials that grow and are made around Los Angeles.</p>
    <h2 data-reveal>Study</h2>
    <p data-reveal style="--i:1">B.S. Engineering, Harvey Mudd College. B.A. Art History, Pomona College. Class of 2028.</p>
    <h2 data-reveal>Languages</h2>
    <p data-reveal style="--i:1">Spanish, Galician and Portuguese, natively. English and French.</p>
    <h2 data-reveal>Honours</h2>
    <p data-reveal style="--i:1">Randal Lewis Fellow in Innovation and Entrepreneurship. Emerging Leader Award, Harvey Mudd, 2025 and 2026.</p>
  </div>
</section>
""" + CONTACT))

# ---------- 404 ----------
PAGES.append(dict(path="404.html", title="Not found · Rodrigo Penide Lema", body=head(
    "This room is empty", '<a class="link" href="/">Back to the entrance</a>')))

if __name__ == "__main__":
    for page in PAGES:
        frame(page["path"], page["title"], page["body"], page.get("room"),
              page.get("welcome", False), home=page.get("home", False))
    print(f"Built {len(PAGES)} pages")
