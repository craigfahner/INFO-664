---
layout: page
title: Part 11
permalink: /part11/
---

## Part 11: Web scraping

### What is web scraping?

In [Part 10](../part10/), we asked a server for data through an API, and it
answered with JSON that was organized for programs to read. An API is the
best way to get data when one exists. But many websites, including most
museum collection pages, have no API at all. What they do have is **web
pages**: documents written in **HTML** that a browser turns into the page you
see, with the headings, labels, and images laid out for a person to read.

**Web scraping** is writing a program to read those pages and pull out the
pieces we want, turning a page meant for people into structured data, like the
lists and dictionaries from [Part 3](../part3/). A scraper does by program
what you would do by hand when you copy the title, artist, and date off an
artwork's page into a spreadsheet, except it can do it for a thousand pages.

Scraping a page takes five steps, and the first four are the whole job for a
single page:

1. **Request** the page, with the `requests` library from Part 10.
2. **Parse** the HTML into a structure Python can search.
3. **Find** the elements that hold the data we want.
4. **Extract** the text (or the link, or the image address) from them.
5. **Repeat** for more pages, and **save** the results, as in Parts 9 and 10.

The tool for steps 2 to 4 is a library called BeautifulSoup.

### What is BeautifulSoup?

HTML is just text, a long string full of tags. Searching it with `.find()` and
`.split()` from [Part 2](../part2/), or even with regular expressions from
[Part 9](../part9/), gets painful quickly. **BeautifulSoup** is a Python
library that reads HTML and turns it into a tree of elements that we can
search by tag name, class, or position, the same way we looked things up in
nested dictionaries in Part 10.

It isn't part of Python, so it has to be installed. The package is named
`beautifulsoup4`, but we import it under its shorter name, `bs4`. If
`from bs4 import BeautifulSoup` gives a `ModuleNotFoundError` in a notebook,
run `%pip install beautifulsoup4` in a cell and try again. The editors on this
page already have it.

HTML is built out of the same pieces as the XML from the bonus section of
[Part 9](../part9/): **elements** wrapped in opening and closing **tags**, which
can contain text or other elements, and which can have **attributes** inside
the opening tag. Here is a simplified version of the kind of markup found on an
artwork page, stored in a string:

```python
from bs4 import BeautifulSoup

html = """
<html>
  <body>
    <h1>Adeline Ravoux</h1>
    <p class="artist">Vincent van Gogh</p>
    <p class="date">1890</p>
    <a href="/art/1958.31">Artwork page</a>
  </body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")
```

`BeautifulSoup(html, "html.parser")` reads the string and builds the tree. The
second argument names the parser to use, and `"html.parser"` is the one that
comes with Python. Everything after this point works on `soup`:

```python
title = soup.find("h1")
print(title)
print(title.get_text())
```

```text
<h1>Adeline Ravoux</h1>
Adeline Ravoux
```

- **`soup.find("h1")`** returns the **first** element with that tag name. It
  prints as the element itself, tags and all.
- **`.get_text()`** returns just the text inside the element, as a string.

To find an element by its **class** attribute, add `class_`. (It has the
underscore because `class` is already a reserved word in Python, which is why
we can't use it as a name.) To find *every* match instead of just the first,
use `find_all()`, which returns a list that we can loop over, like the
filtering loops from earlier parts:

```python
artist = soup.find("p", class_="artist")
print(artist.get_text())

for paragraph in soup.find_all("p"):
    print(paragraph.get_text())
```

```text
Vincent van Gogh
Vincent van Gogh
1890
```

An element's attributes work like dictionary keys. The link's address is the
`href` attribute, so:

```python
link = soup.find("a")
print(link["href"])        # /art/1958.31
print(link.get("href"))    # /art/1958.31
```

Square brackets raise a `KeyError` if the attribute is missing, and `.get()`
returns `None` instead, which is the same difference as in
[Part 3](../part3/).

<script type="py-editor" config='{"packages": ["beautifulsoup4"]}'>
from bs4 import BeautifulSoup

html = """
<html>
  <body>
    <h1>Adeline Ravoux</h1>
    <p class="artist">Vincent van Gogh</p>
    <p class="date">1890</p>
    <a href="/art/1958.31">Artwork page</a>
  </body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")

title = soup.find("h1")
print(title)
print(title.get_text())

artist = soup.find("p", class_="artist")
print(artist.get_text())

for paragraph in soup.find_all("p"):
    print(paragraph.get_text())

link = soup.find("a")
print(link["href"])
print(link.get("href"))
</script>

Those few methods are most of what we need: `find()`, `find_all()`,
`.get_text()`, and attribute lookups. The harder part of scraping is working
out *which* element on a real page holds the data we want, which comes up in
the next sections. But before we write a scraper for any real site, we have to
decide whether we're allowed to.

### Finding a website that can be scraped

Not every site is a good candidate, and some that technically could be
scraped shouldn't be. Before choosing a site, work through these questions:

| Question | How to check |
| --- | --- |
| Is there an API or a data download? | Look for "open access", "API", or "data" in the site's menus and footer, or search for `<museum name> open access data`. If one exists, use it. It's more reliable, and it's what the site's owners prefer you to do. |
| Does the site allow automated access? | Read its `robots.txt` file (see below). |
| Do the terms of use allow it? | Read the site's "Terms of Use" or "Terms and Conditions" page, usually linked in the footer, and look for anything about automated access, scraping, or reuse of content. |
| What is the content's license? | Open-access collections often say so right on the page. Otherwise, images and text may be copyrighted, even if they're easy to download. |
| Is the data actually in the page's HTML? | Open the page, right-click, choose **View Page Source**, and search (Cmd/Ctrl+F) for a word from the data you want. If it's there, `requests` can see it. If not, the page loads its content with JavaScript after it opens, and `requests` will only get an empty shell. |
| Does the data include personal information? | Be careful with anything about private individuals, even if it's publicly visible. |

The "View Page Source" test is worth getting in the habit of. Right-clicking
and choosing **Inspect** shows the page *after* the browser has run its
JavaScript, and **View Page Source** shows what the server originally sent,
which is all that `requests` will get.

### What is robots.txt?

Almost every website has a file at the same address: its domain followed by
`/robots.txt`. For example, `https://www.clevelandart.org/robots.txt`. It's
plain text, and it's where the site's owners say which parts of the site
automated programs ("robots", also called crawlers or bots) may visit, and how
fast. **To read one, type `/robots.txt` after a site's main address in your
browser.** Try it with the Cleveland address above. Here is what it said in
October 2026:

```text
# *
User-agent: *
Crawl-delay: 10
Disallow: /membership
Disallow: /orders
Disallow: /api
Disallow: /errors
Disallow: /404
Disallow: /500

# Host
Host: https://www.clevelandart.org

# Sitemaps
Sitemap: https://www.clevelandart.org/sitemap.xml
```

Lines starting with `#` are comments. The rest are **directives**:

| Directive | Meaning |
| --- | --- |
| `User-agent:` | Which robots the rules below apply to. `*` means all of them. |
| `Disallow:` | A path that robots should **not** request. `Disallow: /membership` rules out any address that starts with `/membership`. |
| `Allow:` | An exception to a `Disallow`. |
| `Crawl-delay:` | How many seconds to wait between requests. |
| `Sitemap:` | The address of a list of the site's pages, which can be a useful list of pages to visit. |

Anything that isn't disallowed is allowed. Cleveland's file doesn't rule out
its artwork pages (addresses starting with `/art/`), so they're fine to
request, as long as we wait 10 seconds between requests. Compare that with the
collection database of the Milwaukee Art Museum, whose whole file is:

```text
User-agent: *
Disallow: /
```

`Disallow: /` blocks every path on the site, so that site asks robots not to
visit it at all. A site's owners can change these rules at any time, and in
recent years many have tightened them, partly in response to large-scale
crawlers collecting data to train AI systems. A class exercise gets caught by
the same rules, so it's worth reading them every time.

**How to read one.** Open the file in your browser, and then:

1. **If you get a "not found" page,** the site hasn't published any rules, so
   check its terms of use instead.
2. **Find the group that covers you.** `User-agent: *` means all robots, and
   that's the group that applies to a script like ours.
3. **Compare your page's address with each `Disallow:` line.** Take the part of
   the address after the domain, such as `/art/1958.31`. If it *starts with* the
   path on a `Disallow:` line, that page is off limits. `/membership/join` is
   blocked by `Disallow: /membership`, but `/art/1958.31` doesn't start with any
   of Cleveland's `Disallow:` paths, so it's allowed. A `Disallow:` with nothing
   after it blocks nothing.
4. **Look for an `Allow:` line**, which makes an exception to a `Disallow:`.
5. **Note the `Crawl-delay:`**, if there is one. That's how many seconds to wait
   between requests.
6. **Write down what you found,** including the date, since the rules can change.

**`robots.txt` isn't a lock.** Nothing stops a program from ignoring it. It's a
published request from the site's owners, and respecting it is the
expected behavior. Ignoring it can get your IP address blocked, break the
site's terms of use, and cause real trouble for you. It also matters because a
scraper that sends requests too quickly can slow a site down for everyone else.

### Identifying yourself, and going slowly

Two more habits make a scraper a good citizen:

- **Identify yourself.** By default, `requests` announces itself as
  `python-requests`, and some sites refuse that outright. (The Frick
  Collection's website answered it with an error and an empty page.) We can
  send our own `User-Agent` header instead, with a name that says honestly who
  and what we are:

  ```python
  headers = {"User-Agent": "INFO664-class-project (educational)"}
  response = requests.get(url, headers=headers)
  ```

  This is about being upfront, not about disguise. The point is to say who is
  asking, not to pretend to be a browser.
- **Wait between requests.** Use the `sleep()` function from
  [Part 10](../part10/) and respect any `Crawl-delay`. Cleveland asks for 10
  seconds, so a loop over several pages should have `sleep(10)` at the end of
  each pass.

For a site that allows it, a good pattern is to **fetch a page once, save it to
a file, and do all your experimenting on the saved copy.** Working out which
element holds what takes many tries, and this way each try doesn't send
another request to the museum's server:

```python
import requests
from time import sleep

url = "https://www.clevelandart.org/art/1958.31"
headers = {"User-Agent": "INFO664-class-project (educational)"}

response = requests.get(url, headers=headers)

with open("cma_1958_31.html", "w", encoding="utf-8") as file:
    file.write(response.text)

sleep(10)
```

`response.text` is the page's HTML as one long string, and the `with open(...)`
code is the same writing pattern from [Part 9](../part9/). Reading the saved
file back in and handing it to BeautifulSoup is the reverse:

```python
from bs4 import BeautifulSoup

with open("cma_1958_31.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser")
```

From here on, `soup` works the same whether the HTML came from a live request
or a saved file.

### What to do if robots.txt doesn't allow access

Sometimes the site you want says no. That might be a `Disallow` rule covering
the pages you need, or a blanket `Disallow: /` like the Milwaukee Art
Museum's. Here are the options, roughly in the order to try them:

1. **Look for an API or open data.** A site that blocks crawlers often
   publishes the same data a better way.
2. **Ask.** A short email to the museum's digital or collections team, saying
   it's a class project, sometimes gets you a data file or permission in
   writing. If you get permission, keep the reply.
3. **Choose a different site.** There are plenty of good sources, and there's
   no prize for picking the hardest one.
4. **Save the pages by hand.** The rest of this section covers it.

**In this course, saving pages by hand is the only workaround we use, and only
for practice in class.** The reasoning is that `robots.txt` is aimed at
*automated* requests. Opening a page in your own browser and saving it is
ordinary human use. BeautifulSoup can then parse the saved file on your own
computer with no request to the site at all. Save a handful of pages that way,
not hundreds. If you save more and more pages with a script or an automated
browser, you're back to crawling the site, just in a roundabout way.

Equally important is what we **don't** do, even in class:

- Disguising a program as a browser by faking its `User-Agent`.
- Getting around "are you a robot?" pages, challenge screens, or login walls,
  including with automated browsers.
- Using hidden search keys or internal addresses found in a site's code to
  query its servers directly.
- Ignoring a `Disallow` rule because nothing technically stops us.

**How to save a page.** In your browser, open the page and use File → Save
Page As (Cmd/Ctrl+S). What you choose in the format menu matters. (The exact
names vary a little between browsers; these are Chrome's.)

- **"Webpage, HTML only"** saves exactly what the server sent, the same as
  `response.text` and "View Page Source". It's fine for pages whose data is
  in the source.
- **"Webpage, Complete"** saves the page as the browser has built it,
  including anything its JavaScript added, plus a folder of images and
  scripts. Use it for pages that fail the View Page Source test above.
- **Copying from developer tools** gets the same built page: open
  **Inspect**, go to the **Elements** tab, right-click the `<html>` element at
  the top, choose **Copy → Copy outerHTML**, and paste it into a text editor.
  Save it with a name ending in `.html`.

Whichever way you save it, **check the file before parsing it.** Open it in a
text editor and search for a word from the data you want. If it's missing, you
saved the empty shell, and need to try a different option.

A few housekeeping rules:

- **Use a consistent name** for each file, such as `pratt_HMS101A.html`, so a
  later loop can find them all.
- **Keep the saved pages in one folder** next to your notebook.
- **Don't commit them to GitHub.** A copy of a page from a site that forbids
  crawling may carry copyright, and a public repository would redistribute it.
  Add the folder to a `.gitignore` file.
- **Open them with `encoding="utf-8"`**, as with every other text file in this
  course.

Everything after this step is the same no matter where the HTML came from:
open the file, parse it into `soup`, find the elements, and extract the data.

### Examining a single item: an artwork page on the Cleveland site

The Cleveland Museum of Art's `robots.txt` allows its artwork pages, so that's
the site we'll scrape. Before writing any code that extracts data, we need to
understand how a page is built, because the whole job is finding where each
piece of data lives in the HTML. We'll work with one artwork, Vincent van
Gogh's portrait *Adeline Ravoux*, at:

```text
https://www.clevelandart.org/art/1958.31
```

Look at that address. The end of it, `1958.31`, is the work's **accession
number**, the museum's own identifier for it. Every artwork has its own, and
its page address is built from it. For example, `/art/1916.1039` is another
painting. That pattern is what will let us move from one page to the next
later on.

**Decide what you want.** Open the page in your browser and read it like a
data collector. We'll aim to end up with a dictionary like this, with one
value for each of the facts the page shows:

```python
{
    "title": "Adeline Ravoux",
    "artist": "Vincent van Gogh",
    "date": "1890",
    "culture": "Netherlands",
    "medium": "oil on fabric",
    "measurements": "Framed: 72.5 x 73.5 x 8.5 cm (28 9/16 x 28 15/16 x 3 3/8 in.); Unframed: 50.2 x 50.5 cm (19 3/4 x 19 7/8 in.)",
    "credit_line": "Bequest of Leonard C. Hanna Jr.",
    "accession_number": "1958.31",
    "location": "222 Impressionism & Post-Impressionism",
}
```

#### Looking at the HTML in your browser

Your browser's **developer tools** show a page's structure. Right-click on the
artwork's title and choose **Inspect** (in Safari, first turn on the Develop
menu in its settings). A panel opens with the **Elements** tab, showing the
page's HTML as a tree of nested elements, the same kind of tree as the XML
from [Part 9](../part9/):

- **Hover** over an element in the tree, and the browser highlights the
  matching part of the page. Hover over the highlighted parts of the page, and
  the panel shows you the elements behind them.
- **Click the small triangles** to open and close an element's children.
- **Search** the tree with Cmd/Ctrl+F, for example for `Medium`.

Then run the test from earlier in this part: right-click the page, choose
**View Page Source**, and search for `oil on fabric`. It's there, so the data
is in the HTML the server sends, and `requests` will see it too.

#### Looking at the HTML with BeautifulSoup

Now the same page in code. These examples use the saved copy of the page,
`cma_1958_31.html`, from the section on saving a page earlier in this part:

```python
from bs4 import BeautifulSoup

with open("cma_1958_31.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser")
```

An HTML page has two main parts: a `<head>`, which holds information *about*
the page, and a `<body>`, which holds what you see. Start with the head:

```python
print(soup.title.get_text())
print(soup.find("meta", property="og:title")["content"])
```

```text
Adeline Ravoux | Cleveland Museum of Art
Adeline Ravoux | Cleveland Museum of Art
```

`soup.title` is a shortcut for the first `<title>` element, which is the text on
the browser tab. The `<meta>` tag with `property="og:title"` is information
the site provides for search engines and for the preview that appears when
someone shares the link. Both hold the title, but with the museum's name added
to the end.

Now the first heading in the body:

```python
print(soup.find("h1").get_text())
```

```text
Artwork Page for Adeline Ravoux
```

That doesn't match anything on the screen. The page's `<h1>` has the class
`sr-only`, which means it's for screen readers only and hidden from view. This
is a good thing to remember: **what's in the HTML isn't always what's on the
screen**, and the reverse can be true as well.

#### The details container

The facts about the artwork are all inside one element with an `id`, a unique
name that only one element on the page can have. That makes it the easiest
kind of element to find:

```python
box = soup.find(id="artwork-details-container")
```

Elements nested inside another one are its **children**. We can list the
container's children with `find_all()`. Passing `True` means "any tag at all",
and `recursive=False` limits it to the *direct* children, not the children's
children:

```python
children = box.find_all(True, recursive=False)

print(len(children))

for index, child in enumerate(children):
    print(index, child.name, "|", child.get_text(" ", strip=True)[:60])
```

```text
14
0 h2 | Details / Information for Adeline Ravoux
1 div | Adeline Ravoux
2 div | 1890
3 div | Vincent van Gogh (Dutch, 1853–1890)
4 div | Culture Netherlands
5 div | Medium oil on fabric
6 div | Measurements Framed: 72.5 x 73.5 x 8.5 cm (28 9/16 x 28 15/16 x 3
7 div | Credit Line Bequest of Leonard C. Hanna Jr. 1958.31
8 div | Public Domain You can copy, modify, and distribute this work, all
9 div | Location 222 Impressionism & Post-Impressionism
10 div | ArtLens App Share Download Print
11 div | ? Did You Know? Adeline Ravoux, at age 13, was not pleased with her po
12 div | Description In May 1890, Vincent van Gogh arrived in Auvers, a small t
13 div | Videos Artist Biography Provenance Citations Exhibition History Cite t
```

Two things in that code deserve a closer look.

**`enumerate()`** (from [Part 7](../part7/)). A `for` loop normally gives us one
thing per pass: the next `child`. Here we also want each child's *position* in
the list, so that we can talk about "child 5". `enumerate()` takes a list and
hands back **pairs**, each one a position followed by the item at that
position. Here it is on a short list:

```python
tags = ["h2", "div", "div"]

print(list(enumerate(tags)))
```

```text
[(0, 'h2'), (1, 'div'), (2, 'div')]
```

(The `list()` is only there so that we can see the pairs. `enumerate()` really
makes them one at a time, as the loop asks for them.) The positions start at
`0`, like list indexes. In our loop, `for index, child in enumerate(children):`
**unpacks** each pair into two variables. On the first pass, `index` is `0` and
`child` is the `<h2>`. On the second, `index` is `1` and `child` is the first
`<div>`, and so on to the end of the list.

Without `enumerate()`, we'd have to keep the count ourselves:

```python
index = 0

for child in children:
    print(index, child.name)
    index += 1
```

That gives the same numbers, but with extra bookkeeping, and it's an easy line to
forget. (`enumerate(children, start=1)` would count from `1` instead, but we
want `0` here, because it matches the positions we use to pick a child out of
the list, as in `children[5]` below.)

**`strip=True`** removes extra whitespace around each piece of text.

The output is the page's structure laid out as a list, and almost every fact we
want is in it:

- **Children `1`, `2`, and `3`** hold the title, the date, and the artist.
  They have no labels. We can tell them apart by what they contain: the title
  is in an `<h3>`, and the artist is in an `<h4>`.
- **Children `4` to `7`, and `9`**, are **label and value rows**: a label like
  `Medium`, followed by its value.

Look inside one of the rows, such as the `Medium` row:

```python
row = children[5]

for part in row.find_all(True, recursive=False):
    print(part.name, "|", part.get_text(strip=True))
```

```text
div | Medium
a | oil on fabric
```

Every row has a label in a `<div>` and a value after it. The value might be a
link (`<a>`), a `<span>`, or another `<div>`. The `Credit Line` row is a bit
different: its value is a `<div>` holding a link to the credit (`Bequest of
Leonard C. Hanna Jr.`) *and* a separate `<span>` with the accession number
(`1958.31`). So the accession number is found in two places: the page's
address, and the Credit Line row.

Here is where each piece of data lives:

| Data | Where to find it |
| --- | --- |
| Title | The `<h3>` in child 1 of the container (also in `<title>` and the `og:title` meta tag, with the museum name added) |
| Date | Child 2, a `<div>` with just the date |
| Artist | The `<a>` inside the `<h4>` in child 3. The artist's nationality and years are in a `<span>` next to it |
| Culture, Medium, Measurements, Location | A row whose label `<div>` says `Culture`, `Medium`, and so on, followed by its value |
| Credit line | The `<a>` in the `Credit Line` row |
| Accession number | The `<span>` after the credit line link, and the end of the page's address |
| License | The `Public Domain` notice, child 8 |

The editor below has a trimmed copy of the real markup for the container, with
the styling details removed, so you can try these methods without a network
request. It stops after the `Location` row, so it has 10 children where the full
page has 14. Try printing the artist's name, or the text of the `Measurements`
row:

<script type="py-editor" config='{"packages": ["beautifulsoup4"]}'>
from bs4 import BeautifulSoup

html = """
<div id="artwork-details-container">
 <h2>Details / Information for Adeline Ravoux</h2>
 <div><h3 data-testid="heading" id="adeline-ravoux">Adeline Ravoux</h3></div>
 <div>1890</div>
 <div>
  <div><div><h4 data-testid="heading"><span>
   <a href="/art/collection/search?artists=Vincent%20van%20Gogh"><span>Vincent van Gogh</span></a>
  </span></h4></div>
  <span>(Dutch, 1853–1890)</span></div>
 </div>
 <div><div>Culture</div><a href="/art/collection/search?culture=Netherlands">Netherlands</a></div>
 <div><div>Medium</div><a href="/art/collection/search?medium=oil%20on%20fabric">oil on fabric</a></div>
 <div><div>Measurements</div><span>Framed: 72.5 x 73.5 x 8.5 cm (28 9/16 x 28 15/16 x 3 3/8 in.); Unframed: 50.2 x 50.5 cm (19 3/4 x 19 7/8 in.)</span></div>
 <div><div>Credit Line</div><div>
  <a href="/art/collection/search?credit=Bequest%20of%20Leonard%20C.%20Hanna%20Jr.">Bequest of Leonard C. Hanna Jr.</a>
  <span> 1958.31</span></div></div>
 <div><div><svg><title>Public Domain</title></svg></div>
  <div>You can copy, modify, and distribute this work, all without asking permission.</div></div>
 <div><div>Location</div><span>
  <a href="/art/collection/search?gallery=222%20Impressionism%20%26%20Post-Impressionism">222 Impressionism &amp; Post-Impressionism</a>
 </span></div>
</div>
"""

soup = BeautifulSoup(html, "html.parser")
box = soup.find(id="artwork-details-container")
children = box.find_all(True, recursive=False)

print(len(children))

for index, child in enumerate(children):
    print(index, child.name, "|", child.get_text(" ", strip=True)[:60])

print()

row = children[5]

for part in row.find_all(True, recursive=False):
    print(part.name, "|", part.get_text(strip=True))
</script>

#### Which parts of the markup can we rely on?

A scraper breaks when the page changes, so it matters what we hang it on. Some
parts of a page are stable, and some are accidents:

| What to rely on | Why |
| --- | --- |
| An `id`, like `artwork-details-container` | An `id` is meant to identify one element, and the page's own code often uses it, so it tends to stay put. |
| Tag names, like `h3` and `h4` | The page's headings are structural. |
| **Label text**, like the word `Medium` | The labels are what a person reads, so they change rarely. Finding a row by its label survives other rows being added or removed. |
| **Position**, like "child 5" | Risky. A work with no `Culture` row would shift every row after it by one. |
| **Class names**, like `font-bold mb-1` | Avoid. On this site they look like styling shorthand (bold, margin, and so on), not meaning, and the site's developers can change them any time without it affecting what you see. |

For these reasons, in the next section we'll find the container by its `id`
and each row by its label, not by position and class names. When you look at
other works on the site, expect rows to differ. Try opening another artwork,
like `https://www.clevelandart.org/art/1916.1039`, in your browser, inspect its
details container, and compare it with this one. Which rows are the same, and
which aren't?

#### Optional: the JSON in the page

There's one more thing hiding in this page. Near the bottom of the HTML is a
`<script>` element with the `id` `__NEXT_DATA__`, and inside it is a block of
**JSON**, the format from [Parts 9 and 10](../part9/). The site's software
uses that data to build the page, and it's sent along with it. Since it's JSON,
we can read it with the `json` module. (`json.loads()`, with an *s*, converts a
*string* into Python data, the way `json.load()` does for a file.)

```python
import json

script = soup.find("script", id="__NEXT_DATA__")
data = json.loads(script.string)

record = data["props"]["pageProps"]["artworkData"]

print(len(record))
print(record["title"], record["creation_date"], record["technique"])
print(record["accession_number"], record["share_license_status"])
```

```text
77
Adeline Ravoux 1890 oil on fabric
1958.31 CC0
```

The record has 77 keys, including everything we found in the visible rows,
plus `culture` (a list), `creators` (a list of dictionaries), `department`,
`current_location`, and `share_license_status`, which says `CC0`, the
museum's open-access license. The nesting here is the same kind we explored in
the NYT API example: dictionaries inside dictionaries, so we get at a value by
writing out the path to it.

This is tidy, but it comes with a catch. The structure of that JSON belongs to
the site's own software, and nobody promises it will stay the same. Many sites
have no embedded JSON at all, so the skills that carry over to them are the
ones for reading the HTML tags. **In this lesson, we'll stay with the HTML
tags**, and leave the JSON as something to notice whenever you inspect a page's
source.

Now that we know where everything is, the next step is to write code that
extracts it.

### Scraping the artwork page

Now we'll pull each fact out of the page's HTML tags and collect them into
the dictionary we planned. These examples start from the saved page and the
details container we found in the last section:

```python
from bs4 import BeautifulSoup

with open("cma_1958_31.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser")

box = soup.find(id="artwork-details-container")
```

#### The title, artist, and date

The title and artist have tags of their own: the title is the container's
`<h3>`, and the artist is its `<h4>`. We find each one and take its text:

```python
title = box.find("h3").get_text(strip=True)
artist = box.find("h4").get_text(" ", strip=True)

print(title)
print(artist)
```

```text
Adeline Ravoux
Vincent van Gogh
```

(The `" "` in the artist's `get_text()` tells it to put a space between
separate pieces of text inside the element. We don't need it for this
artwork, but some works have more than one piece of text in their artist
element, and without the space they'd run together. You'll see an example
below.)

The date is trickier, because it has no label and no tag of its own. It's a
plain `<div>` sitting right after the title. That means we need to find it by
its **position in the tree**, relative to something we can find. Two more
terms describe where elements sit:

- An element's **parent** is the element that contains it. The `<h3>`'s parent
  is the `<div>` that wraps it.
- **Siblings** are elements at the same level, side by side inside the same
  parent. The date `<div>` is the title `<div>`'s next sibling.

So we find the `<h3>`, go up to its parent `<div>` with `find_parent()`, and
then across to the next sibling `<div>` with `find_next_sibling()`:

```python
title_block = box.find("h3").find_parent("div")
date = title_block.find_next_sibling("div").get_text(strip=True)

print(date)
```

```text
1890
```

This is the most fragile lookup we'll write, since it depends on the date
staying right after the title. When a page gives you labels, use them. When it
doesn't, a lookup relative to a landmark like this is the next best thing.

#### The labeled rows

For `Culture`, `Medium`, `Measurements`, and `Location`, we use the labels.
`find()` can search for an element by its text with `string=`, so
`box.find("div", string="Medium")` means "the `<div>` whose text is exactly
`Medium`". That's the label. The value is the label's next sibling:

```python
label = box.find("div", string="Medium")
value = label.find_next_sibling()

print(value.get_text(" ", strip=True))
```

```text
oil on fabric
```

We'll want to do this five times, so it's worth writing a function (from
[Part 6](../part6/)) instead of repeating the lines. The function has to handle
one more thing: a work might not *have* a row, such as a `Culture`. In that
case `find()` returns `None`, and calling `.find_next_sibling()` on `None`
would raise an error. So the function checks for `None` first and returns it
instead:

```python
def get_row_value(box, label_text):
    label = box.find("div", string=label_text)
    if label is None:
        return None
    return label.find_next_sibling()

def get_row_text(box, label_text):
    value = get_row_value(box, label_text)
    if value is None:
        return None
    return value.get_text(" ", strip=True)
```

`get_row_value()` returns the value *element* (or `None`), and
`get_row_text()` builds on it to return just its text. Now each row is one
line:

```python
culture = get_row_text(box, "Culture")
medium = get_row_text(box, "Medium")
measurements = get_row_text(box, "Measurements")
location = get_row_text(box, "Location")

print(culture)
print(medium)
print(measurements)
print(location)
```

```text
Netherlands
oil on fabric
Framed: 72.5 x 73.5 x 8.5 cm (28 9/16 x 28 15/16 x 3 3/8 in.); Unframed: 50.2 x 50.5 cm (19 3/4 x 19 7/8 in.)
222 Impressionism & Post-Impressionism
```

#### The credit line and accession number

The `Credit Line` row is different. Its value isn't one piece of text. It's a
`<div>` holding a link (the credit) *and* a `<span>` (the accession number).
So we get the value element with `get_row_value()`, and then look inside it:

```python
credit = get_row_value(box, "Credit Line")

credit_line = credit.find("a").get_text(strip=True)
accession_number = credit.find("span").get_text(strip=True)

print(credit_line)
print(accession_number)
```

```text
Bequest of Leonard C. Hanna Jr.
1958.31
```

#### The rest of the relevant data

The nine facts above are the core of the record. The page has a few more
that are worth keeping in a dataset: a short biography line for the artist, the
license, the description, the address of the image, and the page's own address.
Each of them comes from tags we haven't used yet.

**The artist's biography.** The nationality and years, like
`(Dutch, 1853–1890)`, sit in a `<span>` right next to the artist's name. It's
a sibling of the `<div>` that wraps the `<h4>`, so we go up from the `<h4>`
and across, as we did for the date. Then `.strip("()")` removes the
parentheses from both ends of the text, using the `strip()` method from
[Part 2](../part2/) with the characters to remove:

```python
artist_block = box.find("h4").find_parent("div")
bio_text = artist_block.find_next_sibling("span").get_text(strip=True)
artist_bio = bio_text.strip("()")

print(artist_bio)
```

```text
Dutch, 1853–1890
```

**The license.** The `Public Domain` notice has an icon, and the words are in
the icon's `<svg>` image, as a `<title>` element inside it. We find the
`<svg>`, then the `<title>` inside that:

```python
license_text = box.find("svg").find("title").get_text(strip=True)

print(license_text)
```

```text
Public Domain
```

(We call the variable `license_text` because `license` is the name of a
function that already exists in Python.)

**The description.** This one is laid out differently from the rows above. Its
label is an `<h3>` heading, not a `<div>`, and the value is the `<span>`
after it. So the search names `h3`:

```python
description_label = box.find("h3", string="Description")
description = description_label.find_next_sibling("span").get_text(" ", strip=True)

print(description[:80])
```

```text
In May 1890, Vincent van Gogh arrived in Auvers, a small town north of Paris, wh
```

(The slice `[:80]` keeps the first 80 characters. The full description runs
to a few sentences.) Labels aren't always in the same kind of tag, which is
why it pays to look at the structure first.

**The image address.** The page's main image isn't in the details container.
Its address is in the `<head>`, in the same kind of `<meta>` tag we used for
the title, with the property `og:image`. The address is in the tag's `content`
attribute, which we read like a dictionary key:

```python
image_url = soup.find("meta", property="og:image")["content"]

print(image_url[:60])
```

```text
https://piction.clevelandart.org/cma/ump.di?e=DBA3E21E7303FB
```

We're only saving the *address* of the image, not downloading the image itself.
(For this work the page says the image is public domain, but the license can
differ from one work to the next, so check before downloading images.)

**The page's own address.** The page doesn't say what its address is, but we
know it, because it's the address we asked for. Keeping it in the record lets
us get back to the page later:

```python
url = "https://www.clevelandart.org/art/1958.31"
```

#### Putting it all in a dictionary

Now everything we want is in a variable, and we can assemble the whole record:

```python
artwork = {
    "title": title,
    "artist": artist,
    "artist_bio": artist_bio,
    "date": date,
    "culture": culture,
    "medium": medium,
    "measurements": measurements,
    "credit_line": credit_line,
    "accession_number": accession_number,
    "location": location,
    "license": license_text,
    "description": description,
    "image_url": image_url,
    "url": url,
}

for key, value in artwork.items():
    print(key, "=", value)
```

```text
title = Adeline Ravoux
artist = Vincent van Gogh
artist_bio = Dutch, 1853–1890
date = 1890
culture = Netherlands
medium = oil on fabric
measurements = Framed: 72.5 x 73.5 x 8.5 cm (28 9/16 x 28 15/16 x 3 3/8 in.); Unframed: 50.2 x 50.5 cm (19 3/4 x 19 7/8 in.)
credit_line = Bequest of Leonard C. Hanna Jr.
accession_number = 1958.31
location = 222 Impressionism & Post-Impressionism
license = Public Domain
description = In May 1890, Vincent van Gogh arrived in Auvers, a small town north of Paris, ...
image_url = https://piction.clevelandart.org/cma/ump.di?e=DBA3E21E7303FB54FA88AA7F4C77DAD98BD...
url = https://www.clevelandart.org/art/1958.31
```

(The description and the image address are shortened with `...` here. Yours
will print in full.) That's one artwork, scraped from its HTML tags into a
dictionary with 14 keys, in the same shape as the dictionaries from our earlier
CSV and JSON lessons. The editor below runs all of the steps on a trimmed copy
of the page's markup. Try changing a label, such as `"Medium"` to
`"Measurements"`, or asking for a label that isn't on the page, like
`"Provenance"`, to see the `None` come back:

<script type="py-editor" config='{"packages": ["beautifulsoup4"]}'>
from bs4 import BeautifulSoup

html = """
<html>
<head>
 <meta property="og:image" content="https://piction.clevelandart.org/cma/ump.di?e=DBA3E21E7303FB54FA88AA7F4C77DAD98BD491FB080247C617896105276440B3&s=24247294&se=116628280&v=0&f=1958.31_w.jpg">
</head>
<body>
<div id="artwork-details-container">
 <h2>Details / Information for Adeline Ravoux</h2>
 <div><h3 data-testid="heading" id="adeline-ravoux">Adeline Ravoux</h3></div>
 <div>1890</div>
 <div>
  <div><div><h4 data-testid="heading"><span>
   <a href="/art/collection/search?artists=Vincent%20van%20Gogh"><span>Vincent van Gogh</span></a>
  </span></h4></div>
  <span>(Dutch, 1853–1890)</span></div>
 </div>
 <div><div>Culture</div><a href="/art/collection/search?culture=Netherlands">Netherlands</a></div>
 <div><div>Medium</div><a href="/art/collection/search?medium=oil%20on%20fabric">oil on fabric</a></div>
 <div><div>Measurements</div><span>Framed: 72.5 x 73.5 x 8.5 cm (28 9/16 x 28 15/16 x 3 3/8 in.); Unframed: 50.2 x 50.5 cm (19 3/4 x 19 7/8 in.)</span></div>
 <div><div>Credit Line</div><div>
  <a href="/art/collection/search?credit=Bequest%20of%20Leonard%20C.%20Hanna%20Jr.">Bequest of Leonard C. Hanna Jr.</a>
  <span> 1958.31</span></div></div>
 <div><div><svg><title>Public Domain</title></svg></div>
  <div>You can copy, modify, and distribute this work, all without asking permission.</div></div>
 <div><div>Location</div><span>
  <a href="/art/collection/search?gallery=222%20Impressionism%20%26%20Post-Impressionism">222 Impressionism &amp; Post-Impressionism</a>
 </span></div>
 <div><h3>Description</h3><span>In May 1890, Vincent van Gogh arrived in Auvers, a small town north of Paris, where he rented a room at the inn of Arthur Ravoux. This portrait, completed during the last months of the artist’s life, depicts Ravoux’s 13-year-old daughter, Adeline.</span></div>
</div>
</body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")
box = soup.find(id="artwork-details-container")
url = "https://www.clevelandart.org/art/1958.31"


def get_row_value(box, label_text):
    label = box.find("div", string=label_text)
    if label is None:
        return None
    return label.find_next_sibling()


def get_row_text(box, label_text):
    value = get_row_value(box, label_text)
    if value is None:
        return None
    return value.get_text(" ", strip=True)


title = box.find("h3").get_text(strip=True)
artist = box.find("h4").get_text(" ", strip=True)

artist_block = box.find("h4").find_parent("div")
bio_text = artist_block.find_next_sibling("span").get_text(strip=True)
artist_bio = bio_text.strip("()")

title_block = box.find("h3").find_parent("div")
date = title_block.find_next_sibling("div").get_text(strip=True)

culture = get_row_text(box, "Culture")
medium = get_row_text(box, "Medium")
measurements = get_row_text(box, "Measurements")
location = get_row_text(box, "Location")

credit = get_row_value(box, "Credit Line")
credit_line = credit.find("a").get_text(strip=True)
accession_number = credit.find("span").get_text(strip=True)

license_text = box.find("svg").find("title").get_text(strip=True)

description_label = box.find("h3", string="Description")
description = description_label.find_next_sibling("span").get_text(" ", strip=True)

image_url = soup.find("meta", property="og:image")["content"]

artwork = {
    "title": title,
    "artist": artist,
    "artist_bio": artist_bio,
    "date": date,
    "culture": culture,
    "medium": medium,
    "measurements": measurements,
    "credit_line": credit_line,
    "accession_number": accession_number,
    "location": location,
    "license": license_text,
    "description": description,
    "image_url": image_url,
    "url": url,
}

for key, value in artwork.items():
    print(key, "=", value)

print(get_row_text(box, "Provenance"))
</script>

The markup in that editor is a trimmed copy of the real page. The description
is cut down to its first two sentences, and the page's other sections, such as
the navigation and footer, are left out.

#### The same code on a different page

Because the code looks for labels, it should work on other artwork pages too.
Here's what the same steps produce for `/art/1916.1039`, a portrait of
Charles I, if you save its page and run them on it (with the long values
shortened again):

```text
title = Portrait of Charles I (1600–1649)
artist = copy after Anthony van Dyck
artist_bio = Flemish, 1599–1641
date = 1600s or later
culture = Flanders
medium = oil on canvas
measurements = Framed: 153.7 x 130.2 x 105.4 cm (60 1/2 x 51 1/4 x 41 1/2 in.); Unframed: 116.8 x 96.3 cm (46 x 37 15/16 in.)
credit_line = Gift of Mr. and Mrs. J. H. Wade
accession_number = 1916.1039
location = Not on view
license = Public Domain
description = This is a fragment of a copy of van Dyck's portrait of 1632. Originally a double...
image_url = https://piction.clevelandart.org/cma/ump.di?e=2FF4BAFCE94CA0AEBB797846F258D508E2...
url = https://www.clevelandart.org/art/1916.1039
```

The structure was the same, so the code worked, but the *values* show how messy
real data is:

- **The artist** is `copy after Anthony van Dyck`. In the HTML, `copy after`
  and the artist's name are separate pieces of text. That's why we gave
  `get_text()` a `" "` separator: without it, the result would be
  `copy afterAnthony van Dyck`.
- **The date** is `1600s or later`, not a year. We'd need to clean it up
  before using it as a number, perhaps with a regular expression from
  [Part 9](../part9/).
- **The location** is `Not on view`, because this work isn't in a gallery
  right now.

Scraping is only half the job. The data you get is only as tidy as the page it
came from.

We now have the code to turn one artwork page into one dictionary. The next
step is to repeat it for many pages, and collect the dictionaries in a list.

### Scraping several artworks

One artwork is a record. To make a *dataset*, we need to repeat the steps for
many works and collect the results. We'll scrape the works by Vincent van Gogh
in the Cleveland Museum of Art's collection, in four steps:

1. Make a list of the pages' addresses.
2. Turn the single-page code from the last section into a function.
3. Loop over the list, scraping each page.
4. Collect the dictionaries in a list.

#### Collecting the URLs

First, we need the addresses. The collection search page lists an artist's
works, but it builds its results with JavaScript after the page opens, so
`requests` would get an empty page, the same problem we met with the "View
Page Source" test. A person using a browser sees the list just fine, so this
step is one we do by hand, as a person deciding which pages to study:

1. Open one of the artist's artwork pages, such as
   `https://www.clevelandart.org/art/1958.31`, and click the artist's name,
   *Vincent van Gogh*. This opens the collection search, showing his works.
2. Open each work and copy its address from the browser's address bar. The
   address always ends with the work's accession number, so you can also copy
   just the accession numbers and add them to
   `https://www.clevelandart.org/art/`.
3. Paste the addresses into a Python list, one string per address.

At the time of writing, the collection has five works by Van Gogh:

```python
urls = [
    "https://www.clevelandart.org/art/1958.31",
    "https://www.clevelandart.org/art/1947.209",
    "https://www.clevelandart.org/art/1958.32",
    "https://www.clevelandart.org/art/1958.30",
    "https://www.clevelandart.org/art/1948.303",
]
```

It's worth pasting each address into your browser to check it before running
anything. A typo means a `404` error, the status code from
[Part 10](../part10/), and that's much easier to catch now than after the loop
has run.

#### Turning the scraper into a function

The code from the last section does one page. We'll wrap it in a function, from
[Part 6](../part6/), so we can call it once per page. The function takes the
page's HTML text and its address as **arguments**, and **returns** the
dictionary. Taking the HTML as an argument matters: the function doesn't care
whether the HTML came from a live request or from a saved file, which we'll use
in a moment.

It uses the two helper functions from the last section, `get_row_value()` and
`get_row_text()`, so those need to be defined in your notebook above this one.
The rest is the same code as before, one step after another:

```python
def scrape_artwork(html, url):
    soup = BeautifulSoup(html, "html.parser")
    box = soup.find(id="artwork-details-container")

    title = box.find("h3").get_text(strip=True)
    artist = box.find("h4").get_text(" ", strip=True)

    artist_block = box.find("h4").find_parent("div")
    bio_text = artist_block.find_next_sibling("span").get_text(strip=True)
    artist_bio = bio_text.strip("()")

    title_block = box.find("h3").find_parent("div")
    date = title_block.find_next_sibling("div").get_text(strip=True)

    culture = get_row_text(box, "Culture")
    medium = get_row_text(box, "Medium")
    measurements = get_row_text(box, "Measurements")
    location = get_row_text(box, "Location")

    credit = get_row_value(box, "Credit Line")
    credit_line = credit.find("a").get_text(strip=True)
    accession_number = credit.find("span").get_text(strip=True)

    license_text = box.find("svg").find("title").get_text(strip=True)

    description_label = box.find("h3", string="Description")
    description = description_label.find_next_sibling("span").get_text(" ", strip=True)

    image_url = soup.find("meta", property="og:image")["content"]

    return {
        "title": title,
        "artist": artist,
        "artist_bio": artist_bio,
        "date": date,
        "culture": culture,
        "medium": medium,
        "measurements": measurements,
        "credit_line": credit_line,
        "accession_number": accession_number,
        "location": location,
        "license": license_text,
        "description": description,
        "image_url": image_url,
        "url": url,
    }
```

The `return` ends the function by sending back the finished dictionary. Calling
`scrape_artwork(html, url)` with a page's HTML gives us that page's record.

#### Looping over the URLs

Now we go through the list. For each address, the loop requests the page,
checks that it worked, calls the function on the page's HTML, and **appends**
the resulting dictionary to a list, the same `.append()` pattern from
[Part 3](../part3/):

```python
import requests
from time import sleep

headers = {"User-Agent": "INFO664-class-project (educational)"}

artworks = []

for url in urls:
    response = requests.get(url, headers=headers)

    if response.ok:
        artwork = scrape_artwork(response.text, url)
        artworks.append(artwork)
    else:
        print(url, "failed with status code", response.status_code)

    sleep(10)
```

- **`headers`** is the honest `User-Agent` from earlier in this part.
- **`response.ok`** is the success check from Part 10. If a request fails, the
  loop prints the address and the status code, and moves on to the next one,
  so one bad address doesn't stop the whole run.
- **`response.text`** is the page's HTML as a string, which is exactly what
  `scrape_artwork()` wants as its first argument.
- **`sleep(10)`** is the 10-second pause that Cleveland's `robots.txt` asks
  for. Five pages take about a minute.

**A note on running this in class.** If everyone runs this loop at the same
moment, the museum's server receives all those requests at once, far faster than
the 10 seconds it asks for. So in class we'll take turns, or work from saved
copies of the pages. Because `scrape_artwork()` takes the HTML as an argument,
the saved-copy version only changes where the HTML comes from. Say you've
saved each page in your notebook's folder as, for example,
`cma_1958_31.html`. Then the loop reads the files instead of making requests,
and doesn't need `sleep()`:

```python
artworks = []

for url in urls:
    accession = url.split("/")[-1]
    filename = "cma_" + accession.replace(".", "_") + ".html"

    with open(filename, "r", encoding="utf-8") as file:
        artworks.append(scrape_artwork(file.read(), url))
```

`url.split("/")[-1]` (from [Part 2](../part2/)) takes the last piece of the
address, the accession number, and `.replace(".", "_")` turns it into the
form used in the file name.

#### The dictionary list

When the loop finishes, `artworks` is a list of dictionaries, one per work:

```python
print(len(artworks))

for artwork in artworks:
    print(artwork["accession_number"], "|", artwork["title"], "|", artwork["date"], "|", artwork["medium"])
```

```text
5
1958.31 | Adeline Ravoux | 1890 | oil on fabric
1947.209 | The Large Plane Trees (Road Menders at Saint-Rémy) | 1889 | oil on fabric
1958.32 | Two Poplars in the Alpilles near Saint-Rémy | 1889 | oil on fabric
1958.30 | Landscape with Wheelbarrow | 1883 | watercolor and opaque watercolor with black chalk on cream paper
1948.303 | Dr. Gachet | 1890 | Etching and drypoint, enhanced with black ink on laid paper
```

That's the same shape as the `data` list from `csv.DictReader` in
[Part 7](../part7/): a list of dictionaries with the same keys, which means
everything we did with those applies here too. For instance, the filter loop
from [Part 5](../part5/), using `in` from [Part 2](../part2/), picks out the
works made in oil:

```python
oil_paintings = []

for artwork in artworks:
    if "oil" in artwork["medium"]:
        oil_paintings.append(artwork)

for artwork in oil_paintings:
    print(artwork["title"])
```

```text
Adeline Ravoux
The Large Plane Trees (Road Menders at Saint-Rémy)
Two Poplars in the Alpilles near Saint-Rémy
```

The run also turned up differences between the works, which our label-based
code coped with:

- **The drawing has an extra row.** *Landscape with Wheelbarrow* has a
  `Support` row that the other works don't. Because we look rows up by label,
  an extra row doesn't disturb anything. We just don't collect it.
- **The location varies.** Two of the works say `Not on view`, two say
  `222 Impressionism & Post-Impressionism`, and the fifth says it is on loan,
  with dates (`On view at Fondation Louis Vuitton, Paris, Oct 9, 2026 - Mar 8,
  2027`). A column like this needs cleaning before it can be counted or mapped.
- **The mediums vary widely**, from `oil on fabric` to `Etching and drypoint,
  enhanced with black ink on laid paper`.
- **The code is only as good as the page.** If the museum redesigns its pages,
  `scrape_artwork()` will most likely stop with an `AttributeError`, from
  calling a method on `None`. That's the signal to inspect the new page and
  update the code.

The editor below runs the same function and loop on two works, using trimmed
copies of their pages in place of live requests. The `saved_pages` dictionary
stands in for the web: it looks up each address and returns that page's HTML.
Try adding a `print()` of one whole dictionary, or filtering for the works
dated `1890`:

<script type="py-editor" config='{"packages": ["beautifulsoup4"]}'>
from bs4 import BeautifulSoup

page_adeline = """
<html>
<head><meta property="og:image" content="https://piction.clevelandart.org/cma/ump.di?e=DBA3E21E7303FB54FA88AA7F4C77DAD98BD491FB080247C617896105276440B3&s=24247294&se=116628280&v=0&f=1958.31_w.jpg"></head>
<body>
<div id="artwork-details-container">
 <h2>Details / Information for Adeline Ravoux</h2>
 <div><h3 data-testid="heading" id="adeline-ravoux">Adeline Ravoux</h3></div>
 <div>1890</div>
 <div>
  <div><div><h4 data-testid="heading"><span>
   <a href="/art/collection/search?artists=Vincent%20van%20Gogh"><span>Vincent van Gogh</span></a>
  </span></h4></div>
  <span>(Dutch, 1853–1890)</span></div>
 </div>
 <div><div>Culture</div><a href="/art/collection/search?culture=Netherlands">Netherlands</a></div>
 <div><div>Medium</div><a href="/art/collection/search?medium=oil%20on%20fabric">oil on fabric</a></div>
 <div><div>Measurements</div><span>Framed: 72.5 x 73.5 x 8.5 cm (28 9/16 x 28 15/16 x 3 3/8 in.); Unframed: 50.2 x 50.5 cm (19 3/4 x 19 7/8 in.)</span></div>
 <div><div>Credit Line</div><div>
  <a href="/art/collection/search?credit=Bequest%20of%20Leonard%20C.%20Hanna%20Jr.">Bequest of Leonard C. Hanna Jr.</a>
  <span> 1958.31</span></div></div>
 <div><div><svg><title>Public Domain</title></svg></div>
  <div>You can copy, modify, and distribute this work, all without asking permission.</div></div>
 <div><div>Location</div><span>
  <a href="/art/collection/search?gallery=222%20Impressionism%20%26%20Post-Impressionism">222 Impressionism &amp; Post-Impressionism</a>
 </span></div>
 <div><h3>Description</h3><span>In May 1890, Vincent van Gogh arrived in Auvers, a small town north of Paris, where he rented a room at the inn of Arthur Ravoux. This portrait, completed during the last months of the artist’s life, depicts Ravoux’s 13-year-old daughter, Adeline.</span></div>
</div>
</body>
</html>
"""

page_gachet = """
<html>
<head><meta property="og:image" content="https://piction.clevelandart.org/cma/ump.di?e=ED80E9485DC95300FBDCDE8A6F4CECF327C16F80A5BC205243994608C9849820&s=24247294&se=399313166&v=3&f=1948.303_w.jpg"></head>
<body>
<div id="artwork-details-container">
 <h2>Details / Information for Dr. Gachet</h2>
 <div><h3 data-testid="heading" id="dr-gachet">Dr. Gachet</h3></div>
 <div>1890</div>
 <div>
  <div><div><h4 data-testid="heading"><span>
   <a href="/art/collection/search?artists=Vincent%20van%20Gogh"><span>Vincent van Gogh</span></a>
  </span></h4></div>
  <span>(Dutch, 1853–1890)</span></div>
 </div>
 <div><div>Culture</div><a href="/art/collection/search?culture=Netherlands">Netherlands</a></div>
 <div><div>Medium</div><a href="/art/collection/search?medium=Etching">Etching and drypoint, enhanced with black ink on laid paper</a></div>
 <div><div>Measurements</div><span>18.1 x 15.2 cm (7 1/8 x 6 in.)</span></div>
 <div><div>Credit Line</div><div>
  <a href="/art/collection/search?credit=Dudley%20P.%20Allen%20Fund">Dudley P. Allen Fund</a>
  <span> 1948.303</span></div></div>
 <div><div><svg><title>Public Domain</title></svg></div>
  <div>You can copy, modify, and distribute this work, all without asking permission.</div></div>
 <div><div>Location</div><span>
  <a href="/art/collection/search?gallery=Not%20on%20view">Not on view</a>
 </span></div>
 <div><h3>Description</h3><span>This portrait of Dr. Paul Gachet, made just two months before the artist’s death, is the only etching that Vincent van Gogh created.</span></div>
</div>
</body>
</html>
"""

saved_pages = {
    "https://www.clevelandart.org/art/1958.31": page_adeline,
    "https://www.clevelandart.org/art/1948.303": page_gachet,
}

urls = list(saved_pages.keys())


def get_row_value(box, label_text):
    label = box.find("div", string=label_text)
    if label is None:
        return None
    return label.find_next_sibling()


def get_row_text(box, label_text):
    value = get_row_value(box, label_text)
    if value is None:
        return None
    return value.get_text(" ", strip=True)


def scrape_artwork(html, url):
    soup = BeautifulSoup(html, "html.parser")
    box = soup.find(id="artwork-details-container")

    title = box.find("h3").get_text(strip=True)
    artist = box.find("h4").get_text(" ", strip=True)

    artist_block = box.find("h4").find_parent("div")
    bio_text = artist_block.find_next_sibling("span").get_text(strip=True)
    artist_bio = bio_text.strip("()")

    title_block = box.find("h3").find_parent("div")
    date = title_block.find_next_sibling("div").get_text(strip=True)

    culture = get_row_text(box, "Culture")
    medium = get_row_text(box, "Medium")
    measurements = get_row_text(box, "Measurements")
    location = get_row_text(box, "Location")

    credit = get_row_value(box, "Credit Line")
    credit_line = credit.find("a").get_text(strip=True)
    accession_number = credit.find("span").get_text(strip=True)

    license_text = box.find("svg").find("title").get_text(strip=True)

    description_label = box.find("h3", string="Description")
    description = description_label.find_next_sibling("span").get_text(" ", strip=True)

    image_url = soup.find("meta", property="og:image")["content"]

    return {
        "title": title,
        "artist": artist,
        "artist_bio": artist_bio,
        "date": date,
        "culture": culture,
        "medium": medium,
        "measurements": measurements,
        "credit_line": credit_line,
        "accession_number": accession_number,
        "location": location,
        "license": license_text,
        "description": description,
        "image_url": image_url,
        "url": url,
    }


artworks = []

for url in urls:
    html = saved_pages[url]
    artwork = scrape_artwork(html, url)
    artworks.append(artwork)

print(len(artworks))

for artwork in artworks:
    print(artwork["accession_number"], "|", artwork["title"], "|", artwork["date"], "|", artwork["medium"])
</script>

The pattern here (a list of inputs, a function that does the work for one, and a
loop that collects the results into a list) is what turns a scraper into a
dataset builder. The last step is to save the list to a file. We'll do it two
ways: as a CSV, and as JSON.

#### Saving the list as a CSV

`artworks` only exists while the notebook is running. To keep the dataset, we
write it to a file. We'll start with a **CSV**, the format from
[Part 7](../part7/) that opens in any spreadsheet. This is the same process as
the "Saving a CSV file" section of [Part 9](../part9/): a list of dictionaries
goes into a `csv.DictWriter`.

```python
import csv

with open("van_gogh_artworks.csv", "w", encoding="utf-8") as file:
    writer = csv.DictWriter(file, artworks[0].keys())
    writer.writeheader()
    writer.writerows(artworks)
```

It works the same way as it did in Part 9:

- **`"w"`** opens the file for writing, and replaces it if it already exists.
- **`artworks[0].keys()`** gives the column names: the keys of the first
  dictionary, in order. Our 14 keys become 14 columns.
- **`writer.writeheader()`** writes the column names as the first line.
- **`writer.writerows(artworks)`** writes one line for each dictionary.

This is where building the dictionaries with a function pays off. Every
dictionary that `scrape_artwork()` returns has the same 14 keys, so they all fit
the same columns. A dictionary with an extra key would make `DictWriter` stop
with a `ValueError`.

The new file, `van_gogh_artworks.csv`, appears next to your notebook. It's about
5 KB, with one header line and five rows. Here is the header:

```text
title,artist,artist_bio,date,culture,medium,measurements,credit_line,accession_number,location,license,description,image_url,url
```

Some of our values contain commas, like `Dutch, 1853–1890` in `artist_bio`,
the long descriptions, and the medium `Etching and drypoint, enhanced with black
ink on laid paper`. The writer puts quotation marks around those, the same way
the `ArtistBio` values were quoted in the MoMA file in Part 7, so the commas
inside a value aren't mistaken for the commas between columns.

**Checking the file.** Reading it back with `csv.DictReader`, as in Part 7, is a
good test:

```python
with open("van_gogh_artworks.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    loaded = list(reader)

print(len(loaded))
print(loaded[0]["title"])
print(loaded[4]["medium"])
print(loaded == artworks)
```

```text
5
Adeline Ravoux
Etching and drypoint, enhanced with black ink on laid paper
True
```

The comma in the medium survived, and `loaded == artworks` is `True`. That
comparison only holds because everything we scraped is already text. A CSV file
stores **everything as text**, so a number would come back as a string, and
there's no way to write `None`. A value of `None` is written as an empty cell,
and read back as an empty string, `''`, which is a difference from JSON. The
editor below shows it:

<script type="py-editor">
import csv

artworks = [
    {
        "title": "Adeline Ravoux",
        "artist": "Vincent van Gogh",
        "artist_bio": "Dutch, 1853–1890",
        "date": "1890",
        "medium": "oil on fabric",
        "culture": "Netherlands",
    },
    {
        "title": "Dr. Gachet",
        "artist": "Vincent van Gogh",
        "artist_bio": "Dutch, 1853–1890",
        "date": "1890",
        "medium": "Etching and drypoint, enhanced with black ink on laid paper",
        "culture": "Netherlands",
    },
]

artworks[1]["culture"] = None   # pretend this work's page had no Culture row

with open("demo_artworks.csv", "w", encoding="utf-8") as file:
    writer = csv.DictWriter(file, artworks[0].keys())
    writer.writeheader()
    writer.writerows(artworks)

with open("demo_artworks.csv", "r", encoding="utf-8") as file:
    print(file.read())

with open("demo_artworks.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    loaded = list(reader)

print(loaded[1]["medium"])
print(repr(loaded[1]["culture"]))
print(loaded == artworks)
</script>

The last line prints `False` this time, because the `None` in `artworks` came
back as `''`.

Two notes about opening the file in a spreadsheet. If accented letters or dashes
look wrong in Excel, try `encoding="utf-8-sig"` when writing the file, which adds a
marker that tells Excel it's UTF-8. And if you're on Windows and blank lines
show up between the rows, add `newline=""` to `open()`, as mentioned in
[Part 9](../part9/).

#### Saving the list as JSON

A CSV is one way to keep the dataset. **JSON** is another, and it's a good fit
for a list of dictionaries: that's exactly the shape JSON describes, so the file
is a faithful copy of what's in memory. It also keeps things that a CSV can't,
like nested lists and dictionaries, and the difference between a missing value
(`null`) and an empty string. And it's the format most web data uses.

In [Part 9](../part9/), `json.load()` read a JSON file into Python. Its
counterpart for writing is `json.dump()`:

```python
import json

with open("van_gogh_artworks.json", "w", encoding="utf-8") as file:
    json.dump(artworks, file, indent=4, ensure_ascii=False)
```

- **`open(..., "w", ...)`** is the write mode from [Part 7](../part7/). It
  creates the file, or **replaces** it if it already exists.
- **`json.dump(artworks, file, ...)`** converts the Python data into JSON text
  and writes it to the file. Note the order: `json.dump()` takes the data first
  and the file second, while `csv.DictWriter()` takes the file first.
- **`indent=4`** spreads the output over many lines, with each level of nesting
  indented four spaces, so a person can read the file. Leave it out and the
  whole list is written as a single long line, which is smaller but unreadable.
- **`ensure_ascii=False`** keeps accented letters and dashes as they are. By
  default, `json` writes any character outside plain English text as an
  escape code. Compare the two with `json.dumps()` (with an *s*, which makes a
  *string* instead of writing a file):

  ```python
  title = artworks[1]["title"]

  print(json.dumps(title))
  print(json.dumps(title, ensure_ascii=False))
  ```

  ```text
  "The Large Plane Trees (Road Menders at Saint-R\u00e9my)"
  "The Large Plane Trees (Road Menders at Saint-Rémy)"
  ```

  Both are valid JSON, and a program reading either one gets the same text
  back. But the second is far easier to read, especially for the
  `–` in a date range like `1853–1890`.

The new file, `van_gogh_artworks.json`, appears next to your notebook. It's
about 7 KB, 81 lines. This is the start of it, with the long values shortened
(the file has them in full):

```text
[
    {
        "title": "Adeline Ravoux",
        "artist": "Vincent van Gogh",
        "artist_bio": "Dutch, 1853–1890",
        "date": "1890",
        "culture": "Netherlands",
        "medium": "oil on fabric",
        "measurements": "Framed: 72.5 x 73.5 x 8.5 cm (28 9/16 x 28 15/16 x 3 3/8 in.); Unframed: 50...",
        "credit_line": "Bequest of Leonard C. Hanna Jr.",
        "accession_number": "1958.31",
        "location": "222 Impressionism & Post-Impressionism",
        "license": "Public Domain",
        "description": "In May 1890, Vincent van Gogh arrived in Auvers, a small town north of Paris...",
        "image_url": "https://piction.clevelandart.org/cma/ump.di?e=DBA3E21E7303FB54FA88AA7F4C77DAD9...",
        "url": "https://www.clevelandart.org/art/1958.31"
    },
    {
        "title": "The Large Plane Trees (Road Menders at Saint-Rémy)",
        "artist": "Vincent van Gogh",
```

Python's types become JSON's in a predictable way: a list becomes an array in
square brackets, a dictionary becomes an object in curly braces, strings stay
strings, and `None` becomes `null`. That last one matters here: if a work's
page had no `Culture` row, `get_row_text()` returned `None`, and the file would
have `"culture": null` for that work.

**Checking the file.** Reading it back with `json.load()` is a good test that
it was written correctly, and it's also how you'd load the dataset in any
later notebook:

```python
with open("van_gogh_artworks.json", "r", encoding="utf-8") as file:
    loaded = json.load(file)

print(type(loaded))
print(len(loaded))
print(loaded[0]["title"])
print(loaded == artworks)
```

```text
<class 'list'>
5
Adeline Ravoux
True
```

We get back a list of 5 dictionaries, and `loaded == artworks` is `True`: the
data that came out of the file is identical to what went in. The editor below
shows the same steps on two of the works, using a smaller set of keys. It also
sets one value to `None` so that you can see it become `null`:

<script type="py-editor">
import json

artworks = [
    {
        "title": "Adeline Ravoux",
        "artist": "Vincent van Gogh",
        "artist_bio": "Dutch, 1853–1890",
        "date": "1890",
        "culture": "Netherlands",
    },
    {
        "title": "The Large Plane Trees (Road Menders at Saint-Rémy)",
        "artist": "Vincent van Gogh",
        "artist_bio": "Dutch, 1853–1890",
        "date": "1889",
        "culture": "Netherlands",
    },
]

artworks[1]["culture"] = None   # pretend this work's page had no Culture row

with open("demo_artworks.json", "w", encoding="utf-8") as file:
    json.dump(artworks, file, indent=4, ensure_ascii=False)

with open("demo_artworks.json", "r", encoding="utf-8") as file:
    loaded = json.load(file)

print(len(loaded))
print(loaded == artworks)
print()

print(json.dumps(artworks[1]["title"]))
print(json.dumps(artworks[1]["title"], ensure_ascii=False))
print()

with open("demo_artworks.json", "r", encoding="utf-8") as file:
    print(file.read())
</script>

Try removing `indent=4` or `ensure_ascii=False` from the `json.dump()` call and
running it again, to see what the file looks like without them.

A word on what the file contains. It holds text and addresses copied from the
museum's pages. That's fine to keep for our class work, but before you share or
publish a dataset like this, check the museum's terms of use for what you may
reuse. The `license` field is there to help with that, but it's no substitute
for reading the terms.

That's the whole pipeline. We checked that scraping was allowed, looked at how
a page is built, wrote code to pull one artwork out of its HTML tags, turned
that into a function and ran it on a list of pages, and saved the list of
dictionaries as a CSV and as JSON.
