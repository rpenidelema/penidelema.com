"""Builds the static pages of penidelema.com.

Every page shares one frame (corners, phone menu, scripts). Content lives in the
PAGES list below. Run `python3 tools/build.py` from the repository root, then
commit the generated .html files: GitHub Pages serves them as they are.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROOMS = [("making", "Making"), ("reading", "Reading"), ("looking", "Looking"),
         ("hosting", "Hosting"), ("journal", "Journal"), ("plus", "+")]
EMAIL = "rpenidelema@g.hmc.edu"

MARK = ('<svg class="mark" viewBox="0 0 44 60" aria-hidden="true">'
        '<path d="M12 54 V18" fill="none" stroke="#111214" stroke-width="3.4" stroke-linecap="round"/>'
        '<path d="M12 28 C 16 16, 26 12, 34 15" fill="none" stroke="#111214" stroke-width="3.4" stroke-linecap="round"/></svg>')

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
    <image id="photo" href="{p}assets/img/kreios.jpg" x="0" y="0" width="1600" height="900" preserveAspectRatio="xMidYMid slice" mask="url(#win)" opacity="0"/>
  </svg>
  <span class="skip caps quiet">Tap to skip</span>
</div>"""


# Preview gate: while the site is unfinished, visitors need a password.
# It is a curtain, not a lock: the pages are still public files.
# To open the site to everyone, set GATED = False and rebuild.
GATED = True
GATE_HEAD = """<meta name="robots" content="noindex, nofollow">
<script>(function(){var k;try{k=localStorage.getItem('pl-preview')}catch(e){}if(k!=='1')document.documentElement.classList.add('locked')})();</script>""" if GATED else ""
GATE = """<form class="gate" data-gate autocomplete="off">
  <a class="corner tl caps" href="{p}">""" + MARK + """Rodrigo Penide Lema</a>
  <div class="gate-in">
    <p class="t">In preparation.</p>
    <p class="quiet">The rooms are still being hung. If you were given a word, it opens here.</p>
    <label class="caps quiet" for="gate-pw">Password</label>
    <div class="gate-row"><input id="gate-pw" type="password" inputmode="numeric" autocomplete="off"><button type="submit" class="caps">Enter</button></div>
    <p class="gate-no caps quiet" aria-live="polite"></p>
  </div>
</form>""" if GATED else ""

def frame(path, title, body, room=None, where="", welcome=False, horizontal=False):
    depth = len([s for s in path.split("/") if s])
    p = "/" if path.endswith(".html") else "../" * depth
    menu = "".join(
        f'<a href="{p}{slug}/"{" aria-current=\"page\"" if slug == room else ""}>{name}</a>'
        for slug, name in ROOMS)
    overlay = "".join(f'<li><a href="{p}{slug}/">{name}</a></li>' for slug, name in ROOMS)
    extra = ""
    if horizontal:
        extra = f'<div class="corner br caps quiet" data-where>{where}</div>\n<div class="progress"><i></i></div>'
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="Rodrigo Penide Lema: engineering at Harvey Mudd, art history at Pomona.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Brygada+1918:ital,wght@0,400;0,500;1,400&display=swap">
<link rel="stylesheet" href="{p}assets/css/site.css">
{GATE_HEAD}
</head>
<body class="{'walk' if horizontal else 'reading'}">
{GATE.replace("{p}", p)}
<a class="corner tl caps" href="{p}">{MARK}Rodrigo Penide Lema</a>
<nav class="corner tr caps" aria-label="Rooms">{menu}<a href="{p}about/"{" aria-current=\"page\"" if room == "about" else ""}>About</a></nav>
<div class="corner bl caps langs"><a href="#" aria-current="true">EN</a><span class="quiet" title="Coming soon">ES</span><span class="quiet" title="Coming soon">GL</span></div>
{extra}
<button type="button" class="menu-btn caps" data-menu="open">Menu</button>
<div class="overlay" hidden>
  <div class="top"><a class="caps" href="{p}">Rodrigo Penide Lema</a><button type="button" class="caps" data-menu="close">Close</button></div>
  <ul>{overlay}<li><a class="quiet" href="{p}about/">About</a></li></ul>
  <div class="caps quiet">EN · ES · GL</div>
</div>
{body.replace("{p}", p)}
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


def wall(where, art, label):
    return f'<div class="wall" data-where="{where}">{art}<div class="tomb">{label}</div></div>'


def empty(text):
    return f'<div class="empty-frame"><span class="caps quiet">{text}</span></div>'


def room(walls, hint=True):
    h = '<div class="hint caps quiet">Scroll to walk through</div>' if hint else ""
    return f'<main class="room"><div class="track">{"".join(walls)}</div>{h}</main>'


PLUS_WALL = wall("+", '<div class="plus-frame"><canvas aria-label="Shared drawing, add one line"></canvas></div>',
                 '<p class="t">Untitled (Lines)</p><p>2026–</p>'
                 '<p class="quiet">Rodrigo Penide Lema, with interventions by visitors from around the world</p>'
                 '<p class="note">Add one line before you leave.</p>')

KREIOS_WALL = wall("Making", '<img class="work" src="{p}assets/img/kreios.jpg" alt="The Kreios Space test hall seen from above: two steel vacuum chambers, workbenches and the company name on a concrete wall" width="1800" height="1350">',
                   '<p class="t">The test hall</p><p>Kreios Space, summer 2026</p>'
                   '<p class="quiet">Vacuum chambers, noble gases, machined aluminum</p>'
                   '<p class="note">I designed and machined a gas flow panel and sensor supports for these chambers. Most of the work is confidential, so the room is all you see.</p>'
                   '<a class="more caps" href="{p}making/kreios/">Read more</a>')

E80_WALL = wall("Making", '<img class="work small" src="{p}assets/img/e80-sketch.png" alt="Hand-drawn sketch of the E80 surface robot: a PVC frame with foam floats and a blue electronics box" width="740" height="330">',
                '<p class="t">A robot that floated</p><p>Baby Beach, Dana Point, spring 2026</p>'
                '<p class="quiet">PVC, pool noodles, polyethylene, aluminum, a Teensy, six motors</p>'
                '<p class="note">It followed its path and logged every reading. The thermometer agreed with the sea. The pH sensor read about 4, in water expected between 6 and 9.</p>'
                '<a class="more caps" href="{p}making/e80/">Read more</a>')

ARLES_WALL = wall("Reading", '<img class="work mid" src="{p}assets/img/arles.jpg" alt="The bioregional materials residency cohort standing in front of a limestone quarry wall in the sun" width="1600" height="1600">',
                  '<p class="t">Cohort, in a quarry</p><p>Atelier LUMA, Arles, summer 2026</p>'
                  '<p class="quiet">Limestone, people, a very bright day</p>'
                  '<p class="note">A residency on bioregional materials. It became the method I now use to map materials around Los Angeles with Professor Jia Yi Gu.</p>'
                  '<a class="more caps" href="{p}reading/bioregional/">Read more</a>')

PAGES = []

# Home
PAGES.append(dict(path="", title="Rodrigo Penide Lema", welcome=True, horizontal=True, where="Entrance", body=room([
    '<div class="wall title" data-where="Entrance"><div><h1>Rodrigo<br>Penide <em>Lema</em></h1>'
    '<p class="sub">Engineering at Harvey Mudd, art history at Pomona. A small exhibition of how things are made, and why they matter.</p></div></div>',
    KREIOS_WALL, E80_WALL, ARLES_WALL,
    wall("About", '<img class="work mid" src="{p}assets/img/portrait.jpg" alt="Rodrigo in a navy pinstripe shirt under an oak tree on campus" width="1200" height="1500">',
         '<p class="t">Portrait of the engineer as an art historian</p><p>Claremont, 2026</p>'
         '<p class="quiet">Spanish, Galician, Portuguese, English, French</p><a class="more caps" href="{p}about/">About</a>'),
    PLUS_WALL,
])))

# Making
PAGES.append(dict(path="making", title="Making · Rodrigo Penide Lema", room="making", horizontal=True, where="Making", body=room([
    '<div class="wall title" data-where="Making"><div><h1><em>Making</em></h1><p class="sub">Things built, tested, and designed for people.</p></div></div>',
    KREIOS_WALL, E80_WALL,
    wall("Making", empty("Photograph to come"), '<p class="t">Sensing an electron beam</p><p>NorthStar, 2026–</p><p class="quiet">Sensors, a particle accelerator, FLUKA</p><p class="note">An autonomous sensing system inside a particle accelerator.</p>'),
    wall("Making", empty("Photograph to come"), '<p class="t">A winch for a mine shaft</p><p>2025</p><p class="quiet">Motorized winch, gas sensors, live video</p><p class="note">A collapsible winch that lowers a sensor payload more than 600 feet, on a $400 budget.</p>'),
    wall("Making", empty("Photograph to come"), '<p class="t">Alumni and students</p><p>With Pomona College</p><p class="quiet">Human-centered design</p><p class="note">Designing meaningful connection between alumni and students across the Claremont Colleges.</p>'),
    wall("Making", empty("Work in progress"), '<p class="t">People and animals</p><p>With The Salvation Army, Orange County, 2026–</p><p class="quiet">Human-centered design</p><p class="note">How connection with animals might support well-being, trust and purpose for people recovering from homelessness and addiction.</p>'),
])))

# Reading
PAGES.append(dict(path="reading", title="Reading · Rodrigo Penide Lema", room="reading", horizontal=True, where="Reading", body=room([
    '<div class="wall title" data-where="Reading"><div><h1><em>Reading</em></h1><p class="sub">Materials, archives and images, read closely.</p></div></div>',
    ARLES_WALL,
    wall("Reading", empty("Image to come"), '<p class="t">An archive of voices</p><p>With Professor Isabel Balseiro, 2025–</p><p class="quiet">3,000 documents, 120 hours of interviews</p><p class="note">Research in comparative literature: building and keeping an archive of documents and recorded interviews.</p>'),
    wall("Reading", empty("Papers to come"), '<p class="t">Papers in art history</p><p>Pomona College</p><p class="quiet">Essays, with short abstracts</p>'),
])))

# Looking
PAGES.append(dict(path="looking", title="Looking · Rodrigo Penide Lema", room="looking", horizontal=True, where="Looking", body=room([
    '<div class="wall title" data-where="Looking"><div><h1><em>Looking</em></h1><p class="sub">Photographs.</p></div></div>',
    wall("Looking", empty("The first series hangs here soon"), '<p class="t">Untitled series</p><p>2026</p>'),
], hint=False)))

# +
PAGES.append(dict(path="plus", title="+ · Rodrigo Penide Lema", room="plus", horizontal=True, where="+", body=room([
    '<div class="wall title" data-where="+"><div><h1>Add <em>one line</em></h1><p class="sub">Every visitor adds a single line to one shared drawing.</p></div></div>',
    PLUS_WALL,
], hint=False)))

# Kreios
PAGES.append(dict(path="making/kreios", title="Kreios Space · Rodrigo Penide Lema", room="making", body="""<main class="read">
  <div class="label"><span class="t">The test hall</span><span>Kreios Space, summer 2026</span><span class="quiet">Assembly, integration and test intern</span></div>
  <div class="body">
    <h1>Test hardware for plasma thrusters</h1>
    <p class="lead">I spent the summer inside a vacuum-chamber test facility, designing and machining what it was missing.</p>
    <p>I built a control panel for the flow of three noble gases, and supports for three sensing systems inside the chamber. Between builds I ran impedance tests and diagnosed plasma across thrust setups.</p>
    <p>I also started documenting the tests that, until then, had gone unrecorded.</p>
    <figure><img src="{p}assets/img/kreios.jpg" alt="The Kreios Space test hall seen from above" width="1800" height="1350"><figcaption>The test hall, seen from above.</figcaption></figure>
  </div>
  <aside><p>Much of this work is confidential under a NATO agreement, so this page is told mostly in words.</p></aside>
  <div class="next caps"><a href="{p}making/">Back to Making</a><a href="{p}making/e80/">Next: A robot that floated</a></div>
</main>"""))

# E80
PAGES.append(dict(path="making/e80", title="A robot that floated · Rodrigo Penide Lema", room="making", body="""<main class="read">
  <div class="label"><span class="t">A robot that floated</span><span>Baby Beach, Dana Point, spring 2026</span><span class="quiet">Engineering 80, Harvey Mudd</span><span class="quiet">PVC, pool noodles, polyethylene, aluminum, a Teensy, six motors</span></div>
  <div class="body">
    <h1>A robot that floated, and two sensors that lied</h1>
    <p class="lead">We built a surface robot to measure the water at five points of Baby Beach in Dana Point, near a sewage outlet, and asked whether temperature, pH and turbidity changed from place to place.</p>
    <p>The frame was a cube of PVC pipe wrapped in foam pool noodles, with a curved polyethylene top plate and a sealed electronics box in the middle. Underneath, about 15 centimeters below the surface, hung a thermistor, a pH probe and an infrared turbidity sensor in an aluminum bracket modified so water could flow straight through it.</p>
    <figure><img src="{p}assets/img/e80-sketch.png" alt="Sketch of the robot: a PVC frame with foam floats and a blue electronics box" width="740" height="330"><figcaption>The frame, and how the floats were cut to fit it.</figcaption></figure>
    <h2>What happened at the beach</h2>
    <p>The robot did everything we asked of it. It floated, followed its programmed path, stopped at each of the five locations, and logged data while its motors were off.</p>
    <p>The thermistor agreed with the sea: about 17.8 to 18.2 °C. The other two did not. The pH sensor read about 4, in water expected between 6 and 9, and the turbidity sensor read under 0.5 NTU where the water measured about 13.</p>
    <h2>What I learned</h2>
    <p>The sensors were not dead. They had been calibrated in the lab, never in saltwater, and the sea is not the lab. The robot worked. The lesson was about calibration: test the whole sensor, mounted, in the conditions it will actually meet.</p>
  </div>
  <aside><p>Draft written from my final report. More photographs to come.</p></aside>
  <div class="next caps"><a href="{p}making/">Back to Making</a><a href="{p}making/kreios/">Next: The test hall</a></div>
</main>"""))

# Bioregional
PAGES.append(dict(path="reading/bioregional", title="Bioregional materials · Rodrigo Penide Lema", room="reading", body="""<main class="read">
  <div class="label"><span class="t">Cohort, in a quarry</span><span>Atelier LUMA, Arles, summer 2026</span><span class="quiet">Biofabrique LA, with Professor Jia Yi Gu, 2026–</span></div>
  <div class="body">
    <h1>The materials that grow and are made around Los Angeles</h1>
    <p class="lead">I spent the summer of 2026 in a residency on bioregional materials at Atelier LUMA in Arles.</p>
    <p>Back in California, I adapted that work into a method for mapping the material streams, suppliers and craftspeople of Southern California, to find where building and design could source locally.</p>
    <p>I do this as the founding student researcher of Biofabrique LA, working with faculty from Harvey Mudd, MIT, USC and SCI-Arc, and with researchers at Atelier LUMA.</p>
    <figure><img src="{p}assets/img/arles.jpg" alt="The residency cohort in front of a limestone quarry wall" width="1600" height="1600"><figcaption>The residency cohort, Arles.</figcaption></figure>
  </div>
  <aside><p>Draft written from my CV. More to come.</p></aside>
  <div class="next caps"><a href="{p}reading/">Back to Reading</a><a href="{p}making/e80/">Next: A robot that floated</a></div>
</main>"""))

# Hosting
PAGES.append(dict(path="hosting", title="Hosting · Rodrigo Penide Lema", room="hosting", body="""<main class="read">
  <div class="label"><span class="t">Hosting</span><span class="quiet">Making room for other people</span></div>
  <div class="body">
    <h1>Hosting</h1>
    <ul class="roles">
      <li><span class="caps quiet">2026 – now</span><div><h2>Class President <span>· Harvey Mudd, Class of 2028</span></h2><ul><li>Elected by my peers</li></ul></div></li>
      <li><span class="caps quiet">2025 – now</span><div><h2>Director of Philanthropy <span>· Board of Trustees, Advancement Committee</span></h2><ul><li>Designed five fundraising campaigns for student initiatives and clubs</li><li>Branding working group for the College's major fundraising campaign</li></ul></div></li>
      <li><span class="caps quiet">2025 – now</span><div><h2>Mentor <span>· New International Students and Scholars</span></h2><ul><li>A cohort of 14 first-year students, one to one and in monthly gatherings</li></ul></div></li>
      <li><span class="caps quiet">2024 – now</span><div><h2>Student Representative <span>· Board of Trustees, Student Affairs Committee</span></h2></div></li>
      <li><span class="caps quiet">2024 – now</span><div><h2>Leadership <span>· Mudders Making a Difference</span></h2><ul><li>Blood drives, tutoring at Claremont High School, and campaigns for local charities</li></ul></div></li>
    </ul>
  </div>
  <aside></aside>
</main>"""))

# Journal
PAGES.append(dict(path="journal", title="Journal · Rodrigo Penide Lema", room="journal", body="""<main class="read">
  <div class="label"><span class="t">Journal</span><span class="quiet">Notes, newest first</span></div>
  <div class="body"><h1>Journal</h1><p class="lead quiet">The first entry is on its way.</p></div>
  <aside></aside>
</main>"""))

# About
PAGES.append(dict(path="about", title="About · Rodrigo Penide Lema", room="about", body=f"""<main class="read">
  <div class="label"><img src="{{p}}assets/img/portrait.jpg" alt="Rodrigo in a navy pinstripe shirt under an oak tree on campus" width="1200" height="1500"></div>
  <div class="body">
    <h1>Engineering at Harvey Mudd, art history at Pomona.</h1>
    <p class="lead">I study how things are made, and why they matter.</p>
    <p>Most of my work happens where those two questions meet: in a vacuum chamber, in an archive of interviews, in a map of the materials that grow and are made around Los Angeles.</p>
    <h2>Study</h2>
    <p>B.S. Engineering, Harvey Mudd College. B.A. Art History, Pomona College. Class of 2028.</p>
    <h2>Languages</h2>
    <p>Spanish, Galician and Portuguese, natively. English and French.</p>
    <h2>Honors</h2>
    <p>Randal Lewis Fellow in Innovation and Entrepreneurship. Emerging Leader Award, Harvey Mudd, 2025 and 2026.</p>
    <h2>Write to me</h2>
    <div class="copy-row"><span class="em" id="email">{EMAIL}</span><button type="button" class="caps" data-copy="email">Copy email</button></div>
  </div>
  <aside><p>Draft bio, to be rewritten in my voice.</p></aside>
</main>"""))

# 404
PAGES.append(dict(path="404.html", title="Not found · Rodrigo Penide Lema", body="""<main class="read">
  <div class="label"></div>
  <div class="body"><h1>This room is empty.</h1><p class="lead"><a href="/" style="border-bottom:1px solid var(--stone-2)">Back to the entrance</a></p></div>
  <aside></aside>
</main>"""))

if __name__ == "__main__":
    for page in PAGES:
        frame(page["path"], page["title"], page["body"], page.get("room"), page.get("where", ""),
              page.get("welcome", False), page.get("horizontal", False))
    print(f"Built {len(PAGES)} pages")
