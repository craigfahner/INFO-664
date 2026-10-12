---
layout: page
title: Week 7 Challenge B
permalink: /week7-challenge-b/
---

## Week 7 Challenge B: Extract the data and save it as JSON

[Challenge A](../week7-challenge-a/) ended with a **map**: you found the part of
a page that holds the data, and you worked out where each fact lives. In this
challenge, you'll use that map to **extract the data from the HTML**, collect it
into a list of dictionaries, and **save it as a JSON file**.

**Time:** about 60 minutes, on your own or in a pair.

**You'll need:** your site, your saved HTML, and your map from Challenge A. If
you want to switch sites, that's fine, but you'll need to do the Challenge A
checks for the new one first.

### Step 1: Design your record

Before writing any scraping code, decide what one record will look like. Pick
**6 to 8 facts** from your map, and sketch the dictionary you want by hand, as
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

Using your saved page and the map from Challenge A, write code that pulls
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
(from [Part 6](../part6/) and the end of Part 11):

```python
def scrape_page(html, url):
    soup = BeautifulSoup(html, "html.parser")

    # ... your extraction code ...

    return {
        "title": title,
        # ...
        "url": url,
    }
```

Test it: it should give you the same dictionary you built in Step 3.

### Step 5: Collect more than one record

Now build a **list of dictionaries**, with at least **3 records**. Which way you
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

# ... your loop, appending one dictionary per page or per container ...

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

### Step 7: Write up your data

In a markdown cell, add a small **data dictionary**, with one row for each key
in your records:

| Key | What it means | Where it comes from on the page | Problems I noticed |
| --- | --- | --- | --- |
| `title` | The item's name | The `<h1>` | None |

Then write a short paragraph (3 to 5 sentences) covering:

- Which values were **messy**, and what you did about them (or what you'd do
  with more time).
- What would **break** your function if the site changed.
- Whether the site had an **API or download** that would have been easier, and
  what scraping gave you that it wouldn't have (or didn't).

### What to hand in

- Your notebook, with your code and its output, running from top to bottom
- Your JSON file
- Your data dictionary table and your paragraph

**Before you share a file:** your JSON contains text copied from a site, so
check that site's terms of use for what you may reuse. Don't commit saved HTML
pages to the repository.

### Stretch

- **Clean one column.** Turn something like a year or a price into a real number
  (with `int()`, `float()`, or a regular expression), and handle the values
  that don't fit.
- **Use what you built.** Filter or sort your list with `sorted()` and a
  `lambda`, as in [Part 8](../part8/), and print the result.
- **Save a CSV copy** with `csv.DictWriter`, as in [Part 9](../part9/), and open
  it in a spreadsheet.
- **Add a second site** with the same keys, and save one combined file.

### When things go wrong

| What you see | What to try |
| --- | --- |
| `AttributeError: 'NoneType' object has no attribute ...` | `find()` found nothing on that page. Print what you searched for. If the fact is sometimes missing, check for `None` first. |
| Works on one page, fails on the next | The pages differ. Print the container's children for the failing page, and compare them with the first. This is why we look things up by label, not by position. |
| Values run together (`copy afterAnthony van Dyck`) | Use `get_text(" ", strip=True)` with the space separator. |
| `TypeError: Object of type ... is not JSON serializable` | Something in your dictionary is a BeautifulSoup element, not text. Use `.get_text()` to turn it into a string before you put it in the dictionary. |
| The JSON has `é`-style codes | Add `ensure_ascii=False` to `json.dump()`. |
| Two records are identical | Your loop might be appending the same dictionary each time. Check that the dictionary is built *inside* the loop. |

### How this will be assessed

| | What full marks looks like |
| --- | --- |
| Record design | 6 to 8 sensible keys, including `url` |
| Extraction | Each fact comes from its own tag, label, or attribute, and missing facts don't crash it |
| Function and loop | A function that works on every page, and a list of at least 3 records |
| JSON file | Valid, readable, and reloads to an equal list |
| Data dictionary and notes | Names messy values, fragile spots, and what the site's other options were |
