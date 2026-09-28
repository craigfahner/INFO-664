---
layout: page
title: Part 8 Solution
permalink: /part8_solution/
---

{% assign csv_url = '/notebooks/moma_artists.csv' | relative_url %}

## Part 8 solution: the ten most common birth years

This walks through one way to solve the [challenge at the bottom of
Part 8](../part8/#code-challenge-the-ten-most-common-birth-years): count how
many artists share each `BeginDate`, and print the 10 most common years.
Every tool used here was already covered somewhere in the course — nothing
new shows up in this write-up.

As always, we start by loading the whole file with `csv.DictReader` (from
[Part 7](../part7/)):

```python
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)
```

### Step 1: count how many artists share each birth year

We build an empty dictionary, then loop over every artist. For each one,
we need to know whether we've already started counting their birth year:
if we have, add `1` to the running count; if we haven't, this is the
first artist for that year, so start it at `1`.

That's a plain `if` / `else` (from [Part 5](../part5/)), and checking
whether a key already exists in a dictionary uses the same `in` operator
that checks whether a value is already in a list or a string (from
[Part 1](../part1/)) — `year in year_counts` asks "is `year` one of the
keys in `year_counts` already?":

```python
year_counts = {}

for artist in data:
    year = artist["BeginDate"]
    if year in year_counts:
        year_counts[year] = year_counts[year] + 1
    else:
        year_counts[year] = 1
```

Reading it alongside the loop: the first time we see, say, `"1942"`,
`"1942" in year_counts` is `False`, so `year_counts["1942"] = 1` creates
that key (the same "assigning to a new key" behavior from
[Part 3](../part3/)). The next time we come across an artist born in
1942, `"1942" in year_counts` is now `True`, so we take the existing
count, `year_counts["1942"]`, add `1` to it, and assign it right back to
the same key — updating it instead of creating it. By the end of the
loop, `year_counts` has one entry per distinct `BeginDate`, mapping it to
how many artists share it.

*By the way:* you'll sometimes see this same idea written as
`year_counts[year] = year_counts.get(year, 0) + 1`, using
`.get()` with a default (from Part 3) instead of a separate `if` / `else`.
It does exactly the same thing in one line — `.get(year, 0)` returns the
existing count, or `0` if the key isn't there yet — but the `if` / `else`
version above says the same thing more explicitly, and doesn't need
anything beyond what's already been covered.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

year_counts = {}

for artist in data:
    year = artist["BeginDate"]
    if year in year_counts:
        year_counts[year] = year_counts[year] + 1
    else:
        year_counts[year] = 1

print(len(year_counts))
print(year_counts["1942"])
</script>

### Step 2: sort the years by count

`sorted()` (used throughout [Part 3](../part3/) and earlier in
[Part 8](../part8/)) can take a dictionary directly, same as it takes a
list — you just get its **keys** back, in sorted order. Here, that means
`sorted(year_counts)` would hand back every distinct `BeginDate`, sorted
alphabetically as text. That's not what we want; we want them sorted by
*how many artists share that year*, which means we still need a `key`.

This is the same `sorted()` / `key=lambda` breakdown from earlier in
[Part 8](../part8/), just with a different lookup inside the `lambda`.
Before, we sorted a list of artist dictionaries by pulling out one field:
`key=lambda artist: int(artist["BeginDate"])`. This time we're sorting a
list of *years* (the keys of `year_counts`), and for each one we want to
look up its count in `year_counts`:

```python
sorted_years = sorted(year_counts, key=lambda year: year_counts[year], reverse=True)

print(sorted_years[0])   # the single most common year
```

`lambda year: year_counts[year]` reads as "for each year, look up its
count in `year_counts`." `sorted()` uses that count to decide the order,
but `sorted_years` itself only comes back with the years — the counts
were just used for comparing, the same way `int(artist["BeginDate"])`
was only used for comparing back when we sorted artists directly.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

year_counts = {}

for artist in data:
    year = artist["BeginDate"]
    if year in year_counts:
        year_counts[year] = year_counts[year] + 1
    else:
        year_counts[year] = 1

sorted_years = sorted(year_counts, key=lambda year: year_counts[year], reverse=True)

print(sorted_years[0])
print(len(sorted_years))
</script>

### Step 3: print the top 10, with their counts

`reverse=True` (from [Part 3](../part3/)) sorts largest-to-smallest
instead of the default smallest-to-largest, so `sorted_years[0]` is
already the most common year. Slicing with `[:10]` (from
[Part 2](../part2/) and [Part 7](../part7/)) keeps just the first 10.
Since `sorted_years` only holds the years themselves, we look each one
back up in `year_counts` to print its count alongside it:

```python
for year in sorted_years[:10]:
    print(year, year_counts[year])
```

Which prints:

```text
0 3515
1942 195
1938 193
1940 185
1943 184
1941 180
1937 179
1946 176
1944 169
1947 164
```

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

year_counts = {}

for artist in data:
    year = artist["BeginDate"]
    if year in year_counts:
        year_counts[year] = year_counts[year] + 1
    else:
        year_counts[year] = 1

sorted_years = sorted(year_counts, key=lambda year: year_counts[year], reverse=True)

for year in sorted_years[:10]:
    print(year, year_counts[year])
</script>

### A familiar gotcha: "0" is not a birth year

Look closely at that output: `0` is on top, with `3515` artists — more than
18 times the runner-up. We've run into this before, in
[Part 7](../part7/) and again in [Part 8](../part8/)'s sorting section:
`0` means "unknown" in this dataset, not "born in year zero." It isn't a
real birth year at all, just a stand-in for missing data, and it's common
enough that it swamps the real results.

The fix is the filter pattern used everywhere in this course: build a list
that leaves out artists with an unknown `BeginDate`, *before* counting:

```python
known_birth_years = []

for artist in data:
    if artist["BeginDate"] != "0":
        known_birth_years.append(artist)
```

### Putting it all together

Run the same two steps as before, but starting from `known_birth_years`
instead of `data`:

```python
year_counts = {}

for artist in known_birth_years:
    year = artist["BeginDate"]
    if year in year_counts:
        year_counts[year] = year_counts[year] + 1
    else:
        year_counts[year] = 1

sorted_years = sorted(year_counts, key=lambda year: year_counts[year], reverse=True)

for year in sorted_years[:10]:
    print(year, year_counts[year])
```

Which prints:

```text
1942 195
1938 193
1940 185
1943 184
1941 180
1937 179
1946 176
1944 169
1947 164
1936 163
```

That's a believable answer: the ten years right around 1936–1947 —
unsurprising, since MoMA's collection leans heavily on 20th-century
artists who were likely to have been in their 20s to 40s, a common age
range for exhibited and collected work, during the middle of the century.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

known_birth_years = []

for artist in data:
    if artist["BeginDate"] != "0":
        known_birth_years.append(artist)

year_counts = {}

for artist in known_birth_years:
    year = artist["BeginDate"]
    if year in year_counts:
        year_counts[year] = year_counts[year] + 1
    else:
        year_counts[year] = 1

sorted_years = sorted(year_counts, key=lambda year: year_counts[year], reverse=True)

for year in sorted_years[:10]:
    print(year, year_counts[year])
</script>

If your own solution got the same 10 years (with or without noticing the
`"0"` issue on your own), that's the exercise working as intended — the
gotcha is the whole point, not a footnote. Real datasets almost always
have a value like this hiding somewhere, and the only way to catch it is
to look closely at your first, unfiltered result instead of trusting it.
