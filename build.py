#!/usr/bin/env python3
"""
build.py — assembles the static pages from parts/.

Vercel does not run this. It exists so you only edit the header,
footer and <head> in one place instead of in eight files. Edit
anything in parts/, run `python3 build.py`, commit the result.

  parts/*.body.html   page content
  parts/_base.css     the original stylesheet
  parts/_depth.css    the 3D layer
  ->  *.html, styles.css
"""

import pathlib

ROOT = pathlib.Path(__file__).parent
PARTS = ROOT / "parts"

SITE = "https://genolytix.co.in"

# slug, nav label, <title>, meta description, eyebrow, h1, lead
PAGES = [
    {
        "slug": "work", "nav": "Our work",
        "title": "Our work — Netra eye care and AI drug discovery | Genolytix Technology",
        "desc": "Two programmes: Netra, an AI cataract screening and eye-care assistant for any phone, and end-to-end AI drug discovery from target identification to molecule generation.",
        "eyebrow": "Programmes", "h1": "Two programmes, one method",
        "lead": "Both start from the same place: a hard biological question, a lot of data, and models built to be checked rather than trusted.",
    },
    {
        "slug": "about", "nav": "About",
        "title": "About Genolytix — team, mission and approach | Genolytix Technology",
        "desc": "Genolytix is a computational research group working across biotechnology, healthcare, AI and data science, operating as a division of Suryon Enterprise LLP in Kolkata, India.",
        "eyebrow": "Who we are", "h1": "About Genolytix",
        "lead": "A computational research group working at the interface of biotechnology, healthcare, AI and data science — operating as a division of Suryon Enterprise LLP.",
    },
    {
        "slug": "services", "nav": "Services",
        "title": "Services — AI, bioinformatics and drug discovery support | Genolytix Technology",
        "desc": "Computational work for academic groups, biotech companies and healthcare organisations: machine learning for biology, drug discovery support, bioinformatics pipelines and healthcare analytics.",
        "eyebrow": "What we do for partners", "h1": "Services",
        "lead": "Alongside our own programmes, we take on computational work for academic groups, biotech companies and healthcare organisations.",
    },
    {
        "slug": "research", "nav": "Research",
        "title": "Research and publications | Genolytix Technology",
        "desc": "Peer-reviewed work on generative molecular design, single-cell target discovery, stochastic modelling of biological systems and epidemiology, plus collaborations, book chapters and patents.",
        "eyebrow": "Research & collaboration", "h1": "Research",
        "lead": "Peer-reviewed work on generative molecular design, single-cell target discovery, stochastic modelling of biological systems and epidemiology.",
    },
    {
        "slug": "news", "nav": "News",
        "title": "News and events | Genolytix Technology",
        "desc": "Workshops, talks, releases and programme milestones from Genolytix Technology, including our hands-on AI for drug discovery workshop.",
        "eyebrow": "News & events", "h1": "What's happening",
        "lead": "Workshops, talks, releases and milestones. Newest first.",
    },
    {
        "slug": "careers", "nav": "Join us", "body": "join", "cta": True,
        "title": "Careers — internships, ML and bioinformatics roles | Genolytix Technology",
        "desc": "Open roles at Genolytix: research interns in generative molecular design, ML engineers for medical imaging, bioinformatics analysts, and clinical and academic collaborators.",
        "eyebrow": "Join us", "h1": "Work with us",
        "lead": "We're small, which means whatever you take on is genuinely yours. Interns here ship things and appear on papers.",
    },
    {
        "slug": "contact", "nav": None,
        "title": "Contact Genolytix Technology",
        "desc": "Get in touch about a research collaboration, a drug discovery project, the Netra eye-care programme, a services enquiry or a job application.",
        "eyebrow": "Get in touch", "h1": "Contact",
        "lead": "A research problem, a dataset, a partnership, or an application — all welcome.",
    },
]

NAV = [(p["slug"], p["nav"], p.get("cta", False)) for p in PAGES if p["nav"]]


def head(title, desc, canonical, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{SITE}{canonical}" />
  <meta name="theme-color" content="#0A2540" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Genolytix Technology" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{SITE}{canonical}" />
  <meta property="og:image" content="{SITE}/og-cover.png" />
  <meta name="twitter:card" content="summary_large_image" />

  <link rel="icon" href="favicon.ico" sizes="any" />
  <link rel="apple-touch-icon" href="apple-touch-icon.png" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Spline+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap"
    rel="stylesheet" />

  <link rel="stylesheet" href="styles.css" />
{extra}</head>
"""


def header(active):
    links = []
    for slug, label, cta in NAV:
        cls = "navlink nav-cta" if cta else "navlink"
        current = ' aria-current="page"' if slug == active else ""
        links.append(f'      <a class="{cls}" href="/{slug}"{current}>{label}</a>')
    links = "\n".join(links)
    return f"""
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header>
    <a class="brand" href="/" aria-label="Genolytix Technology — home">
      <img src="logo.svg" alt="Genolytix Technology" width="161" height="46" />
    </a>

    <button class="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="nav">&#9776;</button>

    <nav id="nav">
{links}
    </nav>
  </header>

  <main id="main">
"""


FOOTER = """
  </main>

  <footer>
    <div class="footer-grid">
      <div>
        <h4>Genolytix Technology</h4>
        <p style="margin-bottom:12px;">AI for drug discovery and accessible healthcare. A division of Suryon
          Enterprise LLP, Kolkata, India.</p>
        <p><a href="mailto:customer_service@genolytix.co.in">customer_service@genolytix.co.in</a></p>
      </div>
      <div>
        <h4>Explore</h4>
        <a href="/work">Our work</a>
        <a href="/about">About &amp; team</a>
        <a href="/services">Services</a>
        <a href="/research">Research</a>
      </div>
      <div>
        <h4>Connect</h4>
        <a href="/news">News &amp; events</a>
        <a href="/careers">Join us</a>
        <a href="/contact">Contact</a>
        <!-- Add your real profile here -->
        <a href="#" rel="noopener">LinkedIn</a>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; <span id="year">2026</span> Genolytix Technology &mdash; a division of Suryon Enterprise LLP
    </div>
  </footer>

  <script src="lattice.js" defer></script>
  <script src="main.js" defer></script>
</body>

</html>
"""

ORG_JSONLD = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Genolytix Technology",
    "alternateName": "Genolytix",
    "url": "https://genolytix.co.in/",
    "logo": "https://genolytix.co.in/logo.png",
    "email": "customer_service@genolytix.co.in",
    "parentOrganization": { "@type": "Organization", "name": "Suryon Enterprise LLP" },
    "description": "AI and computational solutions for drug discovery and healthcare, including generative molecular design and AI-assisted eye-care screening.",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Suryon Enterprise LLP, D-9/15, EKT Phase-IV",
      "addressLocality": "Kolkata",
      "postalCode": "700107",
      "addressCountry": "IN"
    },
    "founder": [
      { "@type": "Person", "name": "Bhaswar Ghosh", "jobTitle": "Founder & CEO" },
      { "@type": "Person", "name": "Soham Choudhuri", "jobTitle": "Co-founder & AI Officer" }
    ],
    "knowsAbout": ["AI drug discovery", "Generative peptide design", "Bioinformatics", "Medical imaging AI", "Computational biology"]
  }
  </script>
"""

HOME_BODY = """
    <!-- ================= HERO ================= -->
    <section class="hero">
      <canvas class="fx3d" aria-hidden="true"></canvas>
      <div class="hero-inner">
        <span class="eyebrow">AI &middot; Drug discovery &middot; Accessible healthcare</span>
        <h1>AI Solutions for <span class="accent">Healthcare &amp; Biotechnology</span></h1>
        <p class="sub">Transforming biological data into scientific intelligence &mdash; from computational
          design to clinical analytics. From AI-driven drug discovery to accessible eye-care screening, we
          build the models that turn hard biology into decisions people can act on.</p>
        <div class="hero-actions">
          <a class="btn" href="/work">See what we're building</a>
          <a class="btn ghost on-dark" href="/research">Read our research</a>
        </div>
      </div>
    </section>

    <div class="proof">
      <div class="proof-inner">
        <div class="metric">
          <span class="num">15+</span>
          <span class="label">Peer-reviewed papers</span>
        </div>
        <div class="metric">
          <span class="num">7</span>
          <span class="label">Global collaborations</span>
        </div>
        <div class="metric">
          <span class="num">1</span>
          <span class="label">Patent filed (IPO)</span>
        </div>
        <div class="metric">
          <span class="num">2</span>
          <span class="label">Active programmes</span>
        </div>
      </div>
    </div>

    <!-- ================= WHAT'S HERE ================= -->
    <section class="explore">
      <p class="section-kicker">Where to start</p>
      <h2 class="section-title">What's on this site</h2>
      <p class="lead">Four ways in, depending on why you came.</p>

      <div class="grid">
        <a class="explore-card" href="/work">
          <span class="step">PROGRAMMES</span>
          <h3>What we're building</h3>
          <p>Netra, an eye-care assistant that screens for cataract from a phone photo, and our end-to-end
            drug discovery chain from target to molecule.</p>
          <span class="more">See the programmes &rarr;</span>
        </a>

        <a class="explore-card" href="/research">
          <span class="step">PUBLICATIONS</span>
          <h3>The method, published</h3>
          <p>Peer-reviewed work in <em>J. Chem. Inf. Model.</em>, <em>Scientific Reports</em>,
            <em>Nature Communications</em> and <em>Physical Biology</em>.</p>
          <span class="more">Read the papers &rarr;</span>
        </a>

        <a class="explore-card" href="/services">
          <span class="step">FOR PARTNERS</span>
          <h3>Work we take on</h3>
          <p>Bioinformatics pipelines, generative molecular design, healthcare analytics and scientific
            consulting for academic and industry teams.</p>
          <span class="more">See services &rarr;</span>
        </a>

        <a class="explore-card" href="/careers">
          <span class="step">OPEN ROLES</span>
          <h3>Join the group</h3>
          <p>Research interns, ML engineers, bioinformatics analysts, and clinical partners who can help
            validate Netra.</p>
          <span class="more">See open positions &rarr;</span>
        </a>
      </div>
    </section>
"""


def build():
    # ---- stylesheet ----
    css = (PARTS / "_base.css").read_text(encoding="utf-8")
    depth = (PARTS / "_depth.css").read_text(encoding="utf-8")
    (ROOT / "styles.css").write_text(css.rstrip() + "\n" + depth, encoding="utf-8")

    # ---- home ----
    (ROOT / "index.html").write_text(
        head(
            "Genolytix Technology — AI for Drug Discovery &amp; Accessible Eye Care",
            "Genolytix Technology builds AI for biology and healthcare: end-to-end drug discovery from "
            "target identification to molecule generation, and an AI cataract screening app that gives "
            "people in India free access to eye-care guidance.",
            "/",
            ORG_JSONLD,
        ) + header("") + HOME_BODY + FOOTER,
        encoding="utf-8",
    )

    # ---- interior pages ----
    for p in PAGES:
        body = (PARTS / f"{p.get('body', p['slug'])}.body.html").read_text(encoding="utf-8")

        if p["slug"] == "contact":
            # The contact panel is already a dark block, so it carries the
            # lattice itself rather than sitting under a second dark band.
            content = f"""
    <section class="section contact">
      <canvas class="fx3d" data-count="26" data-speed="0.7" aria-hidden="true"></canvas>
      <p class="section-kicker">{p['eyebrow']}</p>
      <h1 class="section-title">{p['h1']}</h1>
      <p class="lead">{p['lead']}</p>
{body}
    </section>
"""
        else:
            content = f"""
    <section class="page-hero">
      <canvas class="fx3d" data-count="34" data-speed="0.8" aria-hidden="true"></canvas>
      <div class="page-hero-inner">
        <p class="eyebrow">{p['eyebrow']}</p>
        <h1>{p['h1']}</h1>
        <p class="page-lead">{p['lead']}</p>
      </div>
    </section>

    <section class="section">
{body}
    </section>
"""

        (ROOT / f"{p['slug']}.html").write_text(
            head(p["title"], p["desc"], "/" + p["slug"])
            + header(p["slug"])
            + content
            + FOOTER,
            encoding="utf-8",
        )

    # ---- 404 ----
    (ROOT / "404.html").write_text(
        head("Page not found | Genolytix Technology",
             "That page does not exist. Browse our programmes, research and services instead.",
             "/404")
        + header("")
        + """
    <section class="page-hero">
      <canvas class="fx3d" data-count="30" data-speed="0.6" aria-hidden="true"></canvas>
      <div class="page-hero-inner">
        <p class="eyebrow">404</p>
        <h1>That page isn't here</h1>
        <p class="page-lead">The link may be out of date. Everything on the site is one click away below.</p>
        <div class="hero-actions" style="justify-content:flex-start;margin-top:26px;">
          <a class="btn" href="/">Go to the home page</a>
          <a class="btn ghost on-dark" href="/contact">Tell us what you were looking for</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="grid">
        <a class="explore-card" href="/work"><span class="step">PROGRAMMES</span><h3>Our work</h3>
          <p>Netra eye-care screening and end-to-end AI drug discovery.</p></a>
        <a class="explore-card" href="/research"><span class="step">PUBLICATIONS</span><h3>Research</h3>
          <p>Peer-reviewed papers, collaborations and patents.</p></a>
        <a class="explore-card" href="/services"><span class="step">FOR PARTNERS</span><h3>Services</h3>
          <p>Computational work for academic and industry teams.</p></a>
        <a class="explore-card" href="/careers"><span class="step">OPEN ROLES</span><h3>Join us</h3>
          <p>Internships, engineering roles and collaborations.</p></a>
      </div>
    </section>
"""
        + FOOTER,
        encoding="utf-8",
    )

    # ---- sitemap ----
    urls = ["/"] + ["/" + p["slug"] for p in PAGES]
    entries = "\n".join(
        f"  <url><loc>{SITE}{u}</loc><changefreq>monthly</changefreq></url>" for u in urls
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n</urlset>\n",
        encoding="utf-8",
    )

    print("built:", ", ".join(["index.html"] + [p["slug"] + ".html" for p in PAGES]))


if __name__ == "__main__":
    build()
