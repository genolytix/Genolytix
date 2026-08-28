# Genolytix Technology — website

Static site. Nine pages, no framework, no build step required to deploy.

## What's here

```
index.html          home — hero, proof strip, links into the rest
work.html           /work      the two programmes
about.html          /about     mission, approach, team
services.html       /services  partner services
research.html       /research  publications, collaborations, patents
news.html           /news      workshops, talks, milestones
careers.html        /careers   open roles
contact.html        /contact   address and enquiry form
404.html            shown for any unknown URL

styles.css          all styling
main.js             menu, card tilt, scroll reveal, contact form
lattice.js          the 3D molecular field behind the dark bands

vercel.json         clean URLs (/work, not /work.html)
sitemap.xml         list of pages for Google
robots.txt          points crawlers at the sitemap

build.py            optional, see below
parts/              optional, see below
```

## Deploying

1. Commit everything in this folder to the repository root, so `index.html`
   sits at the top level and not inside a subfolder.
2. In Vercel, the project needs no framework preset and no build command.
   Framework preset: **Other**. Output directory: leave empty.
3. `vercel.json` turns on clean URLs, so `/work` serves `work.html`.

### Still to add

These are referenced by the pages but not included here. Drop them in the
repository root:

- `logo.png` — the header logo, displayed at 169×46
- `favicon.ico`
- `apple-touch-icon.png`
- `og-cover.png` — 1200×630, used for link previews on LinkedIn, WhatsApp and X

Without `og-cover.png` shared links will show no image.

### Placeholder links

Search for `href="#"` before going live. The Google Scholar and LinkedIn links
on the about page and the LinkedIn link in the footer are still placeholders —
fill them in or delete those blocks.

## The contact form

Right now it opens the visitor's mail client with the message pre-filled. That
works, but it drops enquiries from anyone browsing without a configured mail
app. Two ways to make it a real form, both explained in a comment inside
`contact.html`:

- **Formspree** — free tier, no code. Set `action` and `method` on the form and
  delete the submit handler in `main.js`.
- **Vercel serverless** — add `api/contact.js` to the repo and post to
  `/api/contact`. Vercel picks up the `api/` folder with no configuration.

## Editing content

For a one-off change — a new publication, a new role, a date — just edit the
page's HTML directly. The pages are plain and readable.

The header, footer and `<head>` are repeated across all nine files, so a change
to the navigation means nine edits. `build.py` exists for that:

```
python3 build.py
```

It reads the page content from `parts/*.body.html` plus the layout in
`build.py` itself, and rewrites the HTML files, `styles.css` and `sitemap.xml`.
Edit `parts/`, run it, commit the result. Vercel never runs this — it only ever
serves the generated files. If you'd rather not use it, delete `build.py` and
`parts/` and edit the HTML by hand.

## Notes on the 3D

`lattice.js` draws a rotating molecular lattice: a point cloud in a 3D box,
projected through a perspective divide, with bonds between nodes that are
genuinely close in three dimensions. Depth drives node size, brightness and
bond opacity. It follows the pointer slightly, so the structure has an
orientation you can feel.

It runs on any element containing `<canvas class="fx3d">`. Two optional
attributes: `data-count` for the node count, `data-speed` for rotation rate.

The cards tilt in perspective under the pointer, with their content floating
above the card face and the shadow swinging opposite the tilt.

All of this is off for anyone with reduced motion enabled, and the tilt is off
on touch devices where there's no hover to reveal it. The lattice pauses when
scrolled out of view or when the tab is hidden, so it isn't burning battery in
a background tab.
