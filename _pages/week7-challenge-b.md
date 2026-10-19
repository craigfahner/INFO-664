---
layout: page
title: Week 7 Challenge B
permalink: /week7-challenge-b/
---

## Week 7 Challenge B: Extract the data and save it as JSON

### Step 1: Design your record

Before writing any scraping code, decide what one record/entry will look like. Pick
a relevant set of "facts" to record (at least 3) from your map, and sketch the dictionary you want by hand, as
we did at the start of the Cleveland example in [Part 11](../part11/):

```python
{
    "title": "...",
    "artist": "...",
    "year": "...",
    "url": "...",
}
```

- Use short, lowercase key names, with underscores in place of spaces.
- Include a `"url"` key, so each record points back to the page it came from.
- Choose facts that are on *every* page of your site, plus at most one or two
  that are sometimes missing.

### Step 2: Extract each fact from one page

Using your saved page and the map from last week, write code that pulls
**each fact into its own variable**, one at a time. Print each variable as you
go, so you can see it work before moving on. These are the techniques from the
lesson, and each fact will probably use one of them:

| Where the fact lives | Technique |
| --- | --- |
| In a tag of its own, such as a heading | `container.find("h3").get_text(strip=True)` |
| In a row with a label | Find the label by its text, then `find_next_sibling()` (or the `<td>` beside a `<th>`) |
| Next to something you can find, with no label | `find_parent()` and `find_next_sibling()` |
| In an attribute, like a link's address | `element["href"]` or `element.get("href")` |
| In the page's `<head>` | `soup.find("meta", property="og:image")["content"]` |

Two things to handle as you go:

- **Missing facts.** If a page doesn't have a fact, `find()` returns `None`, and
  calling a method on `None` raises an error. Check for `None` first, as the
  `get_row_value()` function did in the lesson, or look the fact up in a
  dictionary with `.get()`, which returns `None` if the key isn't there.
- **Tidying the text.** `get_text(strip=True)` removes extra whitespace. A
  `" "` separator, as in `get_text(" ", strip=True)`, keeps separate pieces of
  text from running together. `.strip("()")` removes characters from the ends,
  and a regular expression from [Part 9](../part9/) can pull a piece out of a
  longer string. Try the options and see which gives the cleanest result.

### Step 3: Build one dictionary

Put your variables together into the dictionary you sketched, and print it with
a loop:

```python
record = {
    "title": title,
    "artist": artist,
    # ... the rest of your keys ...
    "url": url,
}

for key, value in record.items():
    print(key, "=", value)
```

Check each value against the page itself. Is anything `None` that shouldn't
be? Is anything truncated, doubled, or strangely spaced?

### Step 4: Turn it into a function

Wrap your code in a function, so that it can be run on any page. It should take
the page's HTML and its address as arguments, and **return** the dictionary
(from [Part 6](../part6/) and the end of [Part 11](../part11/

```python
def scrape_page(html, url):
    soup = BeautifulSoup(html, "html.parser")

    # ... your exrtraction code that converts elements into a dictionary ...

    return {
        "title": title,
        # ...
        "url": url,
    }
```

Test it: it should give you the same dictionary you built in Step 3.

### Step 5: Collect more than one record (optional)

If your dataset allows it, make **list of dictionaries**, with at least **3 records**. Which way you
do it depends on your site:

- **Separate pages for each item** (an artwork, a course, an article). Collect
  at least three addresses by hand into a `urls` list. Then loop over the list,
  call your function on each page's HTML, and `.append()` each result. Use
  saved copies of the pages if you've been given them. If you fetch pages
  yourself, check `response.ok`, send your honest `User-Agent`, and use
  `sleep()` for the site's `Crawl-delay` (or a few seconds, if it doesn't give
  one).
- **One page with many items** (like the quotes or books practice sites). Use
  `find_all()` to get every container, loop over them, and build one dictionary
  from each container.

Either way, the result is a list:

```python
records = []

# ... your loop with the extraction function developed in the previous step... appending one dictionary per page or per container ...

print(len(records))
```

### Step 6: Save it as JSON

Write the list to a file with `json.dump()`, as in the last section of
Part 11:

```python
import json

with open("my_data.json", "w", encoding="utf-8") as file:
    json.dump(records, file, indent=4, ensure_ascii=False)
```

Then **check your file**:

1. Open `my_data.json` in a text editor. Is it readable? Do the accented
   characters and dashes look right?
2. Read it back with `json.load()`, and check that `len()` is what you expect
   and that `loaded == records` is `True`.
3. Look at one record in the loaded data, and compare it with the page one more
   time.

