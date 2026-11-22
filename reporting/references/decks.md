# Decks

Read this when the reader asked for slides, will present the material, or wants a brief to read as a deck. A deck is built from an HTML fragment of sections by [build-deck.py](../scripts/build-deck.py). The script wraps the fragment in reveal.js and highlight.js, which are vendored under [assets/deck](../assets/deck/VERSIONS.md), and can upload the result to [Postplan](postplan.md).

## Content

- Put an overview at the top of each vertical stack and the detail on the slides below it. A reader who only reads across the top row still gets the whole story.
- Write for the deck's reader, as [Briefs](briefs.md) describes for a reader outside the work.
- Reveal a slide's points one at a time only when the order of the argument matters.

## Source

- Give each slide or stack its own top-level `<section id="...">`, with an `<h2>`. The first section is the title slide: a `<p class="kicker">` line, an `<h1>`, one sentence, and status tags.
- Long material becomes a vertical stack: a `<section>` whose children are `<section>`s, one per sub-slide. Prefer that to shrinking text: one slide per module of an interface, per data shape, or per block of a table.
- A slide that cannot be split, such as a long table or code block, gets `class="scrollable"` and scrolls inside the frame.
- Code goes in `<pre><code class="language-ts">`, or another language name. highlight.js colours it.
- Inside sections, use only semantic HTML: `p`, `ul`, `ol`, `table` with `thead` and `tbody`, `pre`, `code`, `strong`, `em`. The deck provides the classes `muted`, `tag` (with `warn` and `err`), `two` for two columns, `check` for an acceptance box, and `kicker`.
- Leave out `<style>`, `<script>` and external resources. Embed images as data URLs, or link them from the [assets bucket](assets.md). Draw diagrams as inline SVG.

Keep the source fragment somewhere that outlives the container, not in `/tmp`: in `/workspace/briefings/<task>/` when that folder exists, otherwise beside the work it reports on. Record its path with the Postplan draft id. Later revisions are rebuilt from the source, not reconstructed from the published page.

## Build and publish

Run the build from a checkout of the repository the deck is about, with `--out` inside it. Postplan reads the repository from the Git checkout that contains the uploaded file. Check that the checkout's `origin` is the repository you expect.

```sh
python3 <skill-dir>/scripts/build-deck.py SOURCE.html \
  --title "Session storage spike" --out ./deck.html \
  --upload --description "Delivery brief: session storage spike"
```

- The first upload, without `--draft`, creates a draft and prints its URL and id. Record the id with the source path.
- Later rounds pass `--draft <id>` to update the same URL.
- `--scroll` builds one long scrolling page instead of paged slides.
- After uploading, run `postplan list` and check that the draft shows the expected repository. When it shows `no repo` or the wrong one, upload again from the right checkout.

## Check

- Look at every slide in a browser.
- No slide relies on colour alone: every tag carries text.
- Test names on a slide are the real test titles.
- `curl -s <url> | grep -c Reveal.initialize` prints `1`.
