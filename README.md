# myweb — personal homepage of Younghun Kim

Live at **https://andrewyounghunkim.github.io/myweb/**

Static, single-page, no build step and no dependencies. Open `index.html` in a
browser to see exactly what the deployed site looks like.

## Files

| Path | What it is |
|---|---|
| `index.html` | The homepage. **Single source of truth** — edit this. |
| `Profile.JPG` | Portrait shown in the masthead. |
| `CV.pdf` | Linked by the "Curriculum Vitae (PDF)" button. |
| `build.py` | Generates `dist/younghun-kim.html`, a one-file copy with the portrait and CV embedded as data URIs — for emailing or offline use. Not part of the deployed site. |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is instead of running Jekyll over them. |

`dist/` and `CV.docx` are gitignored: one is generated, the other is the
editable CV source that the site does not need.

## Publishing a change

```bash
git add -A && git commit -m "Update publications" && git push
```

Pages redeploys on push to `main`, usually within a minute. Then enable it once,
if it is not on yet: **Settings → Pages → Source: Deploy from a branch →
main / (root) → Save**.

## Updating content

- **New publication** — copy an existing `<li>` inside the matching
  `<ol class="pubs">` and bump the `[n]` in `.pubnum`. A new year gets its own
  `<p class="pubyear">` heading above a fresh `<ol class="pubs">`.
- **New award, degree, or news item** — copy a `.row` block inside the relevant
  `.dated`. In the News section the headline is a link, which is what gives it the
  ↗ marker; leave the `target="_blank" rel="noopener noreferrer"` attributes on it.
- **New tool** — add a `<span>` inside the relevant `.chips`.
- **Colors and fonts** — all of it lives in the `:root` custom properties at the
  top of the `<style>` block, with matching light/dark values. Change a token
  once and it propagates everywhere.
- **Replacing the CV** — drop the new `CV.pdf` in, same filename.

After any of those, run `python3 build.py` if you also keep the one-file copy
current.

## Notes

- The phone number from the CV is deliberately left off the public page; email is
  the only contact route. Add it back in the `.contact` block if you want it there.
- The masthead motif is drawn on a `<canvas>`: a skewed periodic lattice of nodes
  and linkers, the flat projection of a framework unit cell. It redraws on resize
  and on a light/dark switch, and honors `prefers-reduced-motion`.
- The page follows the visitor's light/dark system setting automatically.
- All asset links are relative, so the site works both at a repository subpath
  (`/myweb/`) and at a domain root if you ever move it.
