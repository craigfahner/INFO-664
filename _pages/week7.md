---
layout: page
title: Week 7
permalink: /week6/
---

## Week 7 activities


* [the Beautiful Soup Library!](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### Code Snippets for in-class demos

At various times today you'll need these code snippets! Keep them handy so you don't have to type out lengthy URLs etc:


**NYTimes API snippets!**

*Setting up API key and imports*:

```python
import requests
from getpass import getpass
from time import sleep

key = getpass("Paste your NYT API key: ")
```

*Making a query*:

```python
query = "migrant"

begin_date = "20260901"
end_date = "20260930"

url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&begin_date={begin_date}&end_date={end_date}&api-key={key}"
response = requests.get(url)
```

*Getting Paginated Results*:

```python
results = []

for page in range(0, 5):
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&begin_date={begin_date}&end_date={end_date}&page={page}&api-key={key}"
    response = requests.get(url)

    if response.ok:
        parsed = response.json()
        articles = parsed["response"]["docs"]
        results.append(articles)
    else:
        print("page", page, "failed with status code", response.status_code)

    sleep(12)
```

**Snippets for web scraping demo**:

*imports*:

```import csv
import json
import os # operating system library, let's us do things like making new folders
import requests
from time import sleep
from bs4 import BeautifulSoup # the scraping library!
```

*example html data*:

```
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

soup = BeautifulSoup(html, "html.parser")  # html.parser is the built-in parser that comes with python
```

*setting up a fetch function*:

```
headers = {"User-Agent": "INFO664-class-project (educational)"}   # you can call this whatever you want, it shows up on the scraped website's logs as who you are (ie not a Google/AI bot or web browser)

os.makedirs("scraped_pages", exist_ok=True)  # make a new folder to hold our scraped website HTML data. exist_ok = True means, if the directory already exists, do nothing and don't return an error

def fetch_page(url, filename):  # declaring a new function, which takes a URL to be scraped, and a destination filename, as arguments
    if os.path.exists(filename):  # check to see if file already exists, if so, don't download it from the web, load it instead
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()  # in this case, return provides the read file data, and escapes from the function, ignoring everything below

    response = requests.get(url, headers=headers) # grab the file, using our pre-defined headers as the header data

    if not response.ok: # if the response reports an error
        print(url, "failed with status code", response.status_code) # tell us why it failed
        return None # return a "None" object, since there's nothing usable in the response, and escape from this function
    with open(filename, "w",  encoding="utf-8") as file:
        file.write(response.text)

    sleep(10) # wait 10 seconds, since our robots.txt file asks for a 10 second Crawl-delay
    return response.text
```

### Homework:

## Week 7 Challenge A: Mapping the structure of a page

In Week 7, we worked out where the data lives on a Cleveland
Museum of Art page: we found the container that holds the facts, listed its
children, and worked out which parts were labeled rows and which were found
by position. In this challenge, you'll do the same thing for a **site you
choose**.

**The goal:** find the section of a page (typically a `<div>`, or sometimes a
`<table>`) that contains the data you care about, and use BeautifulSoup to
walk through its structure. What you hand in is a **map** of where each piece
of data is. You won't be extracting the data into a dictionary yet, we'll save that for next week!


### Before you start

- Read [Part 11](../part11/) up to the end of the section on examining a single
  item on the Cleveland Museum of Art site.

### Step 1: Pick a site

Choose a site, and work through these checks. Write down the answers, since
they're part of what you hand in:

| Question | How to check |
| --- | --- |
| What does `robots.txt` say? | Type `/robots.txt` after the site's main address in your browser. Are the pages you want allowed? What's the `Crawl-delay`? (How to read one is in [Part 11](../part11/).) |
| What do the terms of use say about automated access and reuse? | A one-line note is enough. |
| Is the data in the page's HTML? | Right-click the page, choose **View Page Source**, and search for a word from the data. If it's there, `requests` can see it. |

**Reading `robots.txt`:** find the `User-agent: *` section and compare the
address of your page (the part after the domain) with each `Disallow:` line. If
your page's address starts with the text on a `Disallow:` line, it's off limits.
Also write down the `Crawl-delay`, if there is one, and the date you checked.

**If a check fails:** if the site disallows the pages you want, or the page
fails the View Page Source test because it's built by JavaScript, you can
still use it for this challenge, but only in the way we do in this course:
**save the page by hand** in your browser (see Part 11), and mention in your
notes that you did. 

**Some sites to start from.** These sites' `robots.txt` files allowed ordinary
page requests when they were checked in October 2026, but sites change, so
check again. You still need to read each site's terms yourself.

You're encouraged to use the sites you researched last week, however, if those don't work, you may use a different one, or one of the following:

| Site | Why it's useful |
| --- | --- |
| A different artwork page on the Cleveland Museum of Art site (`clevelandart.org/art/<accession number>`) | Same layout as our lesson. The easiest choice. |
| A Wikipedia article about a painting (look for the box on the right) | The data is in a table (the `infobox`) instead of `<div>`s. Wikipedia asks scrapers to identify themselves, so use the `User-Agent` from Part 11. |
| `quotes.toscrape.com` or `books.toscrape.com` | Sites made for scraping practice. Each page has many repeated containers (one per quote, or one per book). |
| A course page in Pratt's catalog (`pratt-ug.catalog.prod.coursedog.com/courses/HMS101A`) | Fields are labeled with headings. The pages are large. |



### Step 2: Get the HTML once

Get the page's HTML into a file, and work from the file. There are two ways:

- **Fetch it once** with `requests`, using the honest `User-Agent` header from
  Part 11, and save `response.text` to a file.
- **Save it by hand** in your browser, if the site requires it.

```python
import requests

url = "https://SITE.com/the/page/you/want"
headers = {"User-Agent": "INFO664-class-project (educational)"}

response = requests.get(url, headers=headers)

with open("saved_page.html", "w", encoding="utf-8") as file:
    file.write(response.text)
```


Before moving on, **check the file**: open it in Jupyter Lab and see if there's data there. If it's missing, you saved an empty shell, and
you'll need to save it a different way.

### Step 3: Find the container in your browser

Open the page on the web, right-click on one of the facts you want, and choose
**Inspect**. In the Elements panel, look for the **smallest element that holds
all of the data you want**. A good container usually:

- has an `id`, or a recognizable tag like a `<table>`, and
- holds all of the facts, or is the one that's **repeated** on a list page
  (like the `<div>` for each quote).

Write down the container's tag, its `id` or class, and why you picked it.

### Step 4: Walk through it with BeautifulSoup

Here's a starting point. Replace the `CHANGE-ME` parts with your own
container:

```python
from bs4 import BeautifulSoup

with open("saved_page.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser")

container = soup.find(id="CHANGE-ME")        # or soup.find("table", class_="CHANGE-ME")
children = container.find_all(True, recursive=False)

print(len(children))

for i, child in enumerate(children):
    print(i, child.name, child.get("id"), "|", child.get_text(" ", strip=True)[:40])
    for j, grandchild in enumerate(child.find_all(True, recursive=False)):
        print("    ", j, grandchild.name, "|", grandchild.get_text(" ", strip=True)[:40])
```

This prints the container's **direct children**, and each child's own children,
indented underneath. Use it to answer these questions about *your* page:

- What are the container's direct children, and what does each one hold?
- Which children are **labeled rows** (a label, followed by a value), and which
  are identified only by their tag or their position?
- Inside a row, what kind of element holds the value: a link `<a>`, a `<span>`,
  a `<td>`, something else?
- Is any of the data **outside** the container, such as in the `<head>`?
- If the page has more than one of something, how many match, and which one
  do you want?

The tools from the lesson are all you need: `find()`, `find_all()`,
`recursive=False`, `.get_text(" ", strip=True)`, `.name`, `.get()`,
`find_parent()`, and `find_next_sibling()`. Print things often. If you're not
sure what an element is, print it.

### Step 5: Write up your map

In a markdown cell, make note of where different data points are located within the "soup". Aim for
at least five:

| Data | Tag / label | How I would find it | Stable or fragile? |
| --- | --- | --- | --- |
| *(example)* Medium | `<div>` labeled `Medium`, followed by an `<a>` | Find the label by its text, then its next sibling | Stable: it uses the label text |



### What to hand in

- The site's name and address, and your notes from the Step 1 checks
- Notes saying whether you fetched the page or saved it by hand
- Your notebook, with the traversal code and its output
- Your mapping in a Markdown cell

### When things go wrong

| What you see | What to try |
| --- | --- |
| Very little in the HTML, or the container is `None` | The page may be built by JavaScript. Go back to the View Page Source test, and check your saved file. |
| `find()` returns the wrong element | More than one element matches. Use a more specific search, or use `find_all()` and look at every match. |
| `AttributeError: 'NoneType' object has no attribute ...` | `find()` found nothing. Print the label or tag you searched for, and compare it with the page. Note that `string=` needs the text to match exactly. |
| Output scrolls forever | Slice the text (`[:40]`), and never print the whole `soup`. Print only the container. |
| Strange characters | Open the file with `encoding="utf-8"`. |
| An error status from the site (like `403`) | Don't try to work around it. Save the page by hand, or choose a different site. |

NOTE: I will be starting next class with some open time to work on this web-scraping task – if you encounter any problems, please come to class with your problems documented in comments in your notebook and we can work through them together!