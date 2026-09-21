---
layout: page
title: Part 7 Challenge
permalink: /part7-challenge/
---

{% assign csv_url = '/notebooks/moma_artists.csv' | relative_url %}

## Part 7 challenge: counting artists by gender

In [Part 7](../part7/) we loaded [`moma_artists.csv`](../notebooks/moma_artists.csv)
with `csv.DictReader` and filtered it down to a smaller list. This time,
we'll filter the **whole dataset** and count what's left.

### The challenge

1. Load the whole CSV as a list of dictionaries.
2. Filter the list so it only keeps artists with a **non-empty** `Gender`
   field. This removes most of the studios and companies, which don't have
   a gender recorded.
3. Count how many of the remaining artists are `male`, `female`,
   `non-binary`, or **other** (anything else that was recorded), and store
   each count in its own variable.
4. Use f-strings to print a sentence for each count, like:

   > There are 10000 male artists in the MoMA collection.
   > There are 2494 female artists in the MoMA collection.

Give it a try before scrolling down. Here's an editor with the loading code
already filled in:

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

# your code here
</script>

### Step 1: filter out the empty genders

This is the same filter-and-append pattern from [Part 5](../part5/) and
Part 7. We loop over every artist in `data`, and only `.append()` the ones
whose `Gender` isn't an empty string (`""`):

```python
artists_with_gender = []

for artist in data:
    if artist["Gender"] != "":
        artists_with_gender.append(artist)

print(len(data))
print(len(artists_with_gender))
```

Which prints:

```text
15763
12501
```

`!=` means "not equal to" (see [Part 1](../part1/)). Out of 15,763 rows,
3,262 have a blank `Gender`, so we're left with 12,501.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

artists_with_gender = []

for artist in data:
    if artist["Gender"] != "":
        artists_with_gender.append(artist)

print(len(data))
print(len(artists_with_gender))
</script>

### Step 2: sort the artists into four groups

Now we loop over the filtered list and decide which group each artist
belongs to. An `if` / `elif` / `else` chain (see [Part 5](../part5/)) is a
good fit, because every artist should land in **exactly one** group:

```python
male_artists = []
female_artists = []
non_binary_artists = []
other_artists = []

for artist in artists_with_gender:
    gender = artist["Gender"]
    if gender == "male":
        male_artists.append(artist)
    elif gender == "female":
        female_artists.append(artist)
    elif gender == "non-binary":
        non_binary_artists.append(artist)
    else:
        other_artists.append(artist)
```

Notice that we use `==` here, and not the `"male" in gender` check from
Part 7. That check would be a mistake for counting: `"male" in "female"`
is `True`, so every female artist would be counted as male too. When we need
each artist to fall into just one group, we match the whole value exactly.
The final `else` catches everything left over, which is what makes the
"other" group work. We don't need to list every unusual value ourselves.

Then we dump the size of each group into a variable with `len()`:

```python
male_count = len(male_artists)
female_count = len(female_artists)
non_binary_count = len(non_binary_artists)
other_count = len(other_artists)
```

It's a good idea to check that we haven't lost anyone. The four counts
should add up to the number of artists we started with:

```python
print(male_count + female_count + non_binary_count + other_count == len(artists_with_gender))   # True
```

And since the "other" group is small, we can print it to see exactly what
ended up in it:

```python
for artist in other_artists:
    print(artist["DisplayName"], "-", artist["Gender"])
```

Which prints:

```text
Anton Prinner - male (trans? ftm?)
A.K. Burns - gender non-conforming
Evelyn Taocheng Wang - transgender woman
Tadáskía - female (transwoman)
```

These are free-text values that don't exactly match `"male"`, `"female"`,
or `"non-binary"`, so they fall through to the `else`.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

artists_with_gender = []

for artist in data:
    if artist["Gender"] != "":
        artists_with_gender.append(artist)

male_artists = []
female_artists = []
non_binary_artists = []
other_artists = []

for artist in artists_with_gender:
    gender = artist["Gender"]
    if gender == "male":
        male_artists.append(artist)
    elif gender == "female":
        female_artists.append(artist)
    elif gender == "non-binary":
        non_binary_artists.append(artist)
    else:
        other_artists.append(artist)

male_count = len(male_artists)
female_count = len(female_artists)
non_binary_count = len(non_binary_artists)
other_count = len(other_artists)

print(male_count + female_count + non_binary_count + other_count == len(artists_with_gender))

for artist in other_artists:
    print(artist["DisplayName"], "-", artist["Gender"])
</script>

### Step 3: print the results with f-strings

With the counts stored in variables, the last step is to build each
sentence with an f-string (see [Part 2](../part2/)). Anything inside curly
braces is replaced by that variable's value:

```python
print(f"There are {male_count} male artists in the MoMA collection.")
print(f"There are {female_count} female artists in the MoMA collection.")
print(f"There are {non_binary_count} non-binary artists in the MoMA collection.")
print(f"There are {other_count} artists with another gender recorded in the MoMA collection.")
```

Which prints:

```text
There are 10000 male artists in the MoMA collection.
There are 2494 female artists in the MoMA collection.
There are 3 non-binary artists in the MoMA collection.
There are 4 artists with another gender recorded in the MoMA collection.
```

Here's everything together:

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

artists_with_gender = []

for artist in data:
    if artist["Gender"] != "":
        artists_with_gender.append(artist)

male_artists = []
female_artists = []
non_binary_artists = []
other_artists = []

for artist in artists_with_gender:
    gender = artist["Gender"]
    if gender == "male":
        male_artists.append(artist)
    elif gender == "female":
        female_artists.append(artist)
    elif gender == "non-binary":
        non_binary_artists.append(artist)
    else:
        other_artists.append(artist)

male_count = len(male_artists)
female_count = len(female_artists)
non_binary_count = len(non_binary_artists)
other_count = len(other_artists)

print(f"There are {male_count} male artists in the MoMA collection.")
print(f"There are {female_count} female artists in the MoMA collection.")
print(f"There are {non_binary_count} non-binary artists in the MoMA collection.")
print(f"There are {other_count} artists with another gender recorded in the MoMA collection.")
</script>

### Things to think about

- **What is this a count of?** Some of the `male` and `female` rows are
  still firms, not individuals (`interware SARL` has `male` recorded, as we
  saw in Part 7), and 3,262 rows have no gender at all. Some of those are
  people whose gender just wasn't recorded. Be careful how you word a claim
  like "there are 10000 male artists" when you write about a dataset like
  this.
- **Whose categories are these?** The four groups we counted come from how
  MoMA recorded the data, and we chose to collapse the free-text entries
  into a single "other" bucket. A different choice about where to draw those
  lines would give different counts.
- **Going further:** add a line that prints each group as a percentage of
  `len(artists_with_gender)`, or format the big numbers with commas using
  `{male_count:,}` inside the f-string, or repeat the count for another
  column, like `Nationality`.
