---
layout: page
title: Part 8
permalink: /part8/
---

{% assign csv_url = '/notebooks/moma_artists.csv' | relative_url %}

## Part 8: Review session

Let's revisit four skills
from earlier parts — searching strings, converting strings to numbers,
sorting, and looking things up. Every example loads the `moma_artists.csv`  file with
`csv.DictReader` (from [Part 7](../part7/)):

```python
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)
```

### Searching strings: finding artists named Mary

`DisplayName` holds a full name, like `"Mary Cassatt"` or `"Pablo
Picasso"`, not a separate first and last name. To search by first name, we
first have to pull the first name out of the full one.

**Getting the first name with `.split()`.** `.split()` (from
[Part 2](../part2/)) breaks a string into a list wherever a space appears.
`"Mary Cassatt".split(" ")` becomes `["Mary", "Cassatt"]`, and `[0]` grabs
the first item — the first name:

```python
name = "Mary Cassatt"
first_name = name.split(" ")[0]

print(first_name)   # Mary
```

That's one artist. To check every artist in the dataset, put the same
idea inside the filter-and-append loop from [Part 5](../part5/): for each
artist, split `DisplayName` on the space, look at the first item, and
`.append()` the artist if it matches.

**Version 1: an exact match with `==`.**

```python
artists_named_mary = []

for artist in data:
    first_name = artist["DisplayName"].split(" ")[0]
    if first_name == "Mary":
        artists_named_mary.append(artist)

print(len(artists_named_mary))

for artist in artists_named_mary[:10]:
    print(artist["DisplayName"])
```

Which prints:

```text
33
Mary Bauermeister
Mary Callery
Mary Cassatt
Mary Ann Dorr
Mary Frank
Mary E. Frey
Mary Martin
Mary Miss
Mary Peck
Mary Petty
```

`==` (from [Part 1](../part1/)) only matches when the two strings are
*exactly* the same: same letters, same case, same length. `first_name ==
"Mary"` is `True` only when the first name is precisely `"Mary"`, nothing
more and nothing less.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

artists_named_mary = []

for artist in data:
    first_name = artist["DisplayName"].split(" ")[0]
    if first_name == "Mary":
        artists_named_mary.append(artist)

print(len(artists_named_mary))

for artist in artists_named_mary[:10]:
    print(artist["DisplayName"])
</script>

**Version 2: a "contains" match with `in`.** Swapping `==` for `in` (also
from [Part 1](../part1/) and used throughout [Part 2](../part2/)) changes
the question from "is the first name exactly `Mary`?" to "does the first
name have `Mary` inside it somewhere?":

```python
artists_named_mary = []

for artist in data:
    first_name = artist["DisplayName"].split(" ")[0]
    if "Mary" in first_name:
        artists_named_mary.append(artist)

print(len(artists_named_mary))
```

Which prints `34` — one more than the exact-match version. Printing the
full list shows why:

```python
for artist in artists_named_mary:
    print(artist["DisplayName"])
```

Somewhere in that list is `Maryan S. Maryan (Pinchas Burstein)`, whose
first name is `"Maryan"`, not `"Mary"`, but `"Mary"` *is* sitting inside
it, letters `M-a-r-y`, right at the start. `==` correctly excludes
`Maryan`, since the two strings aren't identical; `in` includes them,
since it only checks whether one string shows up inside another, not
whether they match completely. Neither version is "wrong" — which one you
want depends on whether a name like `Maryan` should count.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

artists_named_mary = []

for artist in data:
    first_name = artist["DisplayName"].split(" ")[0]
    if "Mary" in first_name:
        artists_named_mary.append(artist)

print(len(artists_named_mary))

for artist in artists_named_mary:
    print(artist["DisplayName"])
</script>

### Converting strings to numbers, step by step

We've filtered by birth year before (in [Part 7](../part7/)), but let's
slow down and look at exactly why the conversion step is necessary.

**Step 1: check the type.** Every value that comes out of a CSV row is a
string, even `BeginDate`, which looks like a number. `type()` (from
[Part 1](../part1/)) confirms it:

```python
first_row = data[0]

print(first_row["BeginDate"])         # '1930'
print(type(first_row["BeginDate"]))   # <class 'str'>
```

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

first_row = data[0]

print(first_row["BeginDate"])
print(type(first_row["BeginDate"]))
</script>

**Step 2: see what goes wrong without converting.** Python won't compare a
string and a number with `>`. Trying it raises a `TypeError` and stops the
program:

```python
first_row["BeginDate"] > 1990
```

```text
TypeError: '>' not supported between instances of 'str' and 'int'
```

This is the same kind of error [Part 3](../part3/) ran into trying to use
a `list` as a dictionary key — Python refusing to combine two things that
don't work together, rather than silently guessing what we meant.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

first_row = data[0]

print(first_row["BeginDate"] > 1990)
</script>

Run that one and read the error at the bottom of the output — that's what
a `TypeError` looks like, and it's worth getting used to reading them.

**Step 3: convert with `int()`.** `int()` (from
[Part 1](../part1/)) takes a string made of digits and returns the
equivalent whole number:

```python
birth_year_text = first_row["BeginDate"]   # '1930', a str
birth_year = int(birth_year_text)          # 1930, an int

print(type(birth_year))   # <class 'int'>
print(birth_year > 1990)  # False
```

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

first_row = data[0]

birth_year_text = first_row["BeginDate"]
birth_year = int(birth_year_text)

print(type(birth_year))
print(birth_year > 1990)
</script>

**Step 4: do the conversion inside the filter loop.** Once we know why the
conversion is needed, the rest is the same filter-and-append pattern as
the Mary examples above — except this time the condition converts
`BeginDate` to a number before comparing it, all in one line:

```python
recent_artists = []

for artist in data:
    if int(artist["BeginDate"]) > 1990:
        recent_artists.append(artist)

print(len(recent_artists))
```

Which prints `211`. `int(artist["BeginDate"])` runs fresh for every artist
as the loop reaches them — there's no separate step where we convert the
whole column at once, we just convert each value right before comparing
it.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

recent_artists = []

for artist in data:
    if int(artist["BeginDate"]) > 1990:
        recent_artists.append(artist)

print(len(recent_artists))
</script>

### Sorting a list by a key: ordering by birth year

[Part 3](../part3/) introduced `sorted()` with `key=lambda ...` on a small
list of bird sightings. Let's break that syntax down piece by piece and
apply it to the full artist dataset.

```python
sorted_by_birth = sorted(data, key=lambda artist: int(artist["BeginDate"]))
```

Reading it from the outside in:

- **`sorted(data, ...)`** — `sorted()` takes a list and returns a **new**,
  reordered list. Like the filters above, it doesn't change `data`
  itself.
- **`key=...`** — `sorted()` doesn't know what "order" means for a list of
  dictionaries; a dictionary doesn't have a built-in order the way numbers
  do. `key` tells it what to compare instead: a small helper that
  `sorted()` runs on *every* item in the list, using whatever that helper
  returns as the thing to sort by.
- **`lambda artist: int(artist["BeginDate"])`** — this is the helper
  itself. A `lambda` is a small, unnamed function, written inline instead
  of with `def` (from [Part 6](../part6/)). `lambda artist: ...` says "for
  each item, call it `artist`, and return..."; `int(artist["BeginDate"])`
  is what gets returned — the artist's birth year, converted to a number
  just like in the previous section. So the whole expression means: "sort
  `data`, and for each artist, sort by their birth year as a number."

Running it:

```python
sorted_by_birth = sorted(data, key=lambda artist: int(artist["BeginDate"]))

for artist in sorted_by_birth[:5]:
    print(artist["DisplayName"], "-", artist["BeginDate"])
```

Which prints:

```text
Artko - 0
Isidora Aschheim - 0
Atelier Eggers - 0
A.A.P. - 0
Norman Ackroyd - 0
```

That's not very useful — remember from [Part 7](../part7/) that `0` means
"unknown" in this dataset, so every artist with an unrecorded birth year
sorts to the very front, ahead of anyone with a real, known date. Real
data rarely sorts cleanly on the first try.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

sorted_by_birth = sorted(data, key=lambda artist: int(artist["BeginDate"]))

for artist in sorted_by_birth[:5]:
    print(artist["DisplayName"], "-", artist["BeginDate"])
</script>

**Filtering before sorting.** The fix is the filter pattern again: build a
list that only keeps artists with a known birth year, *then* sort that
list:

```python
known_birth_years = []

for artist in data:
    if artist["BeginDate"] != "0":
        known_birth_years.append(artist)

sorted_by_birth = sorted(known_birth_years, key=lambda artist: int(artist["BeginDate"]))

for artist in sorted_by_birth[:5]:
    print(artist["DisplayName"], "-", artist["BeginDate"])
```

Which prints:

```text
St. Francis of Assisi - 1181
Josiah Wedgwood - 1730
J.A. Henckels, Solingen, Germany - 1731
Francisco de Goya - 1746
Thomas Bewick - 1753
```

That's the earliest-born artists (or, in a few cases, organizations) in
the collection. Add `reverse=True` (from [Part 3](../part3/)) to flip the
order and see the most recently born instead:

```python
sorted_by_birth = sorted(known_birth_years, key=lambda artist: int(artist["BeginDate"]), reverse=True)

for artist in sorted_by_birth[:5]:
    print(artist["DisplayName"], "-", artist["BeginDate"])
```

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

known_birth_years = []

for artist in data:
    if artist["BeginDate"] != "0":
        known_birth_years.append(artist)

sorted_by_birth = sorted(known_birth_years, key=lambda artist: int(artist["BeginDate"]))

for artist in sorted_by_birth[:5]:
    print(artist["DisplayName"], "-", artist["BeginDate"])

sorted_by_birth_desc = sorted(known_birth_years, key=lambda artist: int(artist["BeginDate"]), reverse=True)

for artist in sorted_by_birth_desc[:5]:
    print(artist["DisplayName"], "-", artist["BeginDate"])
</script>

### Looking up one artist in a list of dictionaries

Last, a simple but common task: given a name, find that one artist's row
and use it. This uses only the filter-and-append pattern from earlier in
this part — nothing new.

```python
matches = []

for artist in data:
    if artist["DisplayName"] == "Pablo Picasso":
        matches.append(artist)

picasso = matches[0]

print(picasso)
```

`matches` will only ever hold one artist in this dataset (nobody else
shares that exact name), so `matches[0]` — the first, and only, item —
gets us the row we're after. `picasso` is now a single dictionary, just
like `first_row` earlier in this part.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

matches = []

for artist in data:
    if artist["DisplayName"] == "Pablo Picasso":
        matches.append(artist)

picasso = matches[0]

print(picasso)
</script>

**Building a bio with an f-string.** Now that we have `picasso` as a
single dictionary, we can pull out each field with `["key"]` (as in
[Part 3](../part3/)) and drop them into an f-string (from
[Part 2](../part2/)) to build a sentence out of the raw data:

```python
bio = f"{picasso['DisplayName']} was a {picasso['Nationality']} artist, born in {picasso['BeginDate']} and died in {picasso['EndDate']}."


print(bio)
```

Which prints:

```text
Pablo Picasso was a Spanish artist, born in 1881 and died in 1973.
```

Splitting the f-string across several lines with parentheses is just a
readability choice — Python joins adjacent string literals automatically,
so `("a" "b")` is the same as `"ab"`. Every `{ }` still works exactly the
same as a single-line f-string; there's just more room to see each piece.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

matches = []

for artist in data:
    if artist["DisplayName"] == "Pablo Picasso":
        matches.append(artist)

picasso = matches[0]

bio = f"{picasso['DisplayName']} was a {picasso['Nationality']} artist, born in {picasso['BeginDate']} and died in {picasso['EndDate']}."

print(bio)
</script>

Try changing `"Pablo Picasso"` to another `DisplayName` from the dataset
and running it again — the same four lines work for any artist in the
file. (If the name isn't in the dataset, `matches` comes back empty, and
`matches[0]` raises an `IndexError` — there's nothing at index `0` of an
empty list.)

### Code challenge: the ten most common birth years

MoMA's artists were born across hundreds of years. Which birth years
show up the most often in the collection?

Write code that:

1. Loads the whole dataset (you know how to do this already).
2. Builds a dictionary that counts how many artists share each
   `BeginDate` value — one key per year, one count per key.
3. Sorts that dictionary by count, largest first, and keeps just the top
   **10**.
4. Prints each of those years next to its count.

Everything you need has already been covered somewhere in this course.
For step 2, think about the `if` / `else` and `in` patterns from
[Part 5](../part5/) and [Part 1](../part1/) — for each artist, is their
birth year already a key in your dictionary or not? For step 3, `sorted()`
takes a `lambda` key, the same way it did earlier in this part — it just
doesn't have to be sorting a list of dictionaries. 

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

# your code here
</script>
