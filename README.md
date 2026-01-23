# My Adventures at Los Angeles Live Steamers

Source for site posted at
[https://roger-random.github.io/lals/](https://roger-random.github.io/lals/)

---

### Primary objective

Track my activities, plans, and progress against those
plans surrounding scale model railroading at
[Los Angeles Live Steamers Railroad Museum](https://lalsrm.org/)

### Secondary objective

Learn how to use static-site generators that can take my simple markup text
and spits out a website with all the modern web buzzwords like using a mobile
friendly responsive layout scheme.

Currently using
[Hugo](https://gohugo.io/)
which consumes my written words in the
[```content```](./content/)
subdirectory and spits out all generated content to the
[```public```](./public/)
subdirectory which is then hosted by
[GitHub Pages](https://docs.github.com/en/pages)
and accessible at
[https://roger-random.github.io/lals/](https://roger-random.github.io/lals/)

One of the first customizations I did after completing Hugo Quickstart is to
look for another theme as the
[Anake](https://github.com/theNewDynamic/gohugo-theme-ananke)
theme used in the tutorial was not to my liking. After browsing a few
documentation-focused themes I decided
[Hugo Book](https://github.com/alex-shpak/hugo-book)
looked interesting for the following reasons:

* Higher text density and less whitespace than other themes.
* Index bar of all pages on the left
* Text search
* Mermaid charts

### Room for improvement

Hosting this on GitHub Pages is a bit odd. For one thing, this setup means
that all the images are duplicated. My original in ```contents``` and a copy
in ```public```. This feels like a mistake. I'm probably not doing something
I should be doing to be more efficient. Until I figure it out, I chalk it up
to just being part of learning Hugo.
