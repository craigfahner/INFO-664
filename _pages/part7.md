---
layout: page
title: Part 7
permalink: /part7/
---

{% assign csv_url = '/notebooks/moma_artists.csv' | relative_url %}

## Part 7: Importing CSV data

### What a CSV file looks like

A **CSV** ("comma-separated values") file is a plain text file that stores
a table. Every line is one **row**, and the values (or **fields**) in each
row are separated by commas. The first row usually holds the column names,
called the **header**.

The examples in this part use [`moma_artists.csv`](../notebooks/moma_artists.csv),
a list of the artists in the Museum of Modern Art's collection. Here are
its first three lines, exactly as they appear in the file:

```text
ConstituentID,DisplayName,ArtistBio,Nationality,Gender,BeginDate,EndDate,Wiki QID,ULAN
1,Robert Arneson,"American, 1930–1992",American,male,1930,1992,,
2,Doroteo Arnaiz,"Spanish, born 1936",Spanish,male,1936,0,,
```

Two details are worth noticing before we write any code. The
`ArtistBio` field contains a comma of its own (`American, 1930–1992`), so
the file wraps it in double quotes to show that the comma is part of the
value and not a separator. And the last two fields on the first data row
are empty — that's what `,,` at the end of a line means.

*Running these examples on your own machine:* save `moma_artists.csv` in
the same folder as your notebook, and the file name alone
(`"moma_artists.csv"`) is enough for Python to find it. The interactive
editors on this page load the file for you.

### Importing a CSV and reading the first row

Python's built-in `csv` module knows how to read CSV files, including
tricky details like the quoted comma above. It isn't loaded automatically,
so we bring it in with `import`. The plan is to load the **entire file**
into a single variable up front, and then work with that variable, the same
way you would in a notebook:

```python
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    data = list(reader)

header = data[0]
first_row = data[1]

print(header)
print(first_row)
```

This is the most code we've seen so far in one go, so here it is piece by
piece:

- **`import csv`** makes the `csv` module's tools available, under the
  name `csv`. The reader we want is `csv.reader`.
- **`open("moma_artists.csv", "r", ...)`** opens the file and hands back a
  *file object*. Opening a file doesn't read anything yet; it just gets it
  ready. `"r"` and `encoding="utf-8"` are options we'll come back to
  below.
- **`with ... as file:`** runs the indented block below it while the file
  is open, and closes the file automatically when the block ends — even if
  something goes wrong inside. Like `for`, `if`, and `def`, it ends in a
  colon and its body is indented.
- **`csv.reader(file)`** wraps the file object in a *reader*. The reader
  splits each line into a list of fields, and hands them out one row at a
  time.
- **`list(reader)`** keeps asking the reader for rows until the file runs
  out, and collects them all into one list, which we store in `data`. A
  reader is used up once it has been read all the way through, so this is
  our one chance to grab everything. That's why the loading happens inside
  the `with` block, while the file is still open.
- **`data`** is an ordinary variable, so it's still there after the `with`
  block closes the file. Everything below this point works with `data`
  and never has to touch the file again.

Each row is a list of fields, and `data` is a list of those rows, a **list
of lists** (see [Part 3](../part3/)). That means we can pull out a row with
an index number, the same way as any other list item. Indexes start at
`0`, so `data[0]` is the first row in the file, which is the header of
column names, and `data[1]` is the first row of actual data. Printing them
gives:

```text
['ConstituentID', 'DisplayName', 'ArtistBio', 'Nationality', 'Gender', 'BeginDate', 'EndDate', 'Wiki QID', 'ULAN']
['1', 'Robert Arneson', 'American, 1930–1992', 'American', 'male', '1930', '1992', '', '']
```

Notice that `'American, 1930–1992'` came through as a single value: the
reader understood the quotes and kept the comma inside it.

From here on, most of the code blocks in the text assume `data` has been
loaded this way, and only show the new lines. The interactive editors repeat the
loading code at the top so that each one can run on its own.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    data = list(reader)

header = data[0]
first_row = data[1]

print(header)
print(first_row)
</script>

### A closer look at enumerate()

Before we use it on the CSV data, let's look at what `enumerate()` does
on its own. It takes a collection (a list, a tuple, a string, anything you
could loop over) and pairs every item with its position:

```python
x = ('apple', 'banana', 'cherry')
y = enumerate(x)

print(list(y))  # print as list so it is readable, rather than as an "enumerate object"
```

Which prints:

```text
[(0, 'apple'), (1, 'banana'), (2, 'cherry')]
```

The result is a list of **tuples** (from [Part 3](../part3/)), and each
tuple holds two things: the item's position first, then the item itself.
The positions are the same **indexes** we use when we write `x[0]`, so
they start counting at `0`, not `1`.

The `list(y)` in the example is there for a reason. `enumerate()` doesn't
hand back a list, it hands back an *enumerate object*, which produces its
pairs one at a time as something asks for them. If we printed `y` directly
we'd see something like `<enumerate object at 0x10511e6b0>` instead of
the pairs. Wrapping it in `list()` asks for all of the pairs at once so we
can read them. Like the CSV reader above, an enumerate object is used up as
it's read, so a second `list(y)` on the same `y` would come back empty.

<script type="py-editor">
x = ('apple', 'banana', 'cherry')
y = enumerate(x)

print(y)
print(list(y))
</script>

Most of the time we don't build a list at all. We hand `enumerate()`
straight to a `for` loop (from [Part 4](../part4/)), which asks for one
pair per pass. Since each pair is a tuple of two values, the loop can
unpack it into two variables in one go, `index` and `fruit` here:

```python
x = ('apple', 'banana', 'cherry')

for index, fruit in enumerate(x):
    print(index, fruit)
```

Which prints:

```text
0 apple
1 banana
2 cherry
```

On the first pass `index` is `0` and `fruit` is `'apple'`; on the second,
`1` and `'banana'`; and so on until the collection runs out. The variable
names are up to you (`index, fruit` could just as well be `i, item`), but
the order isn't: the position always comes first and the item second.

<script type="py-editor">
x = ('apple', 'banana', 'cherry')

for index, fruit in enumerate(x):
    print(index, fruit)
</script>

If you'd rather count from `1` (for a numbered list, say), `enumerate()`
takes an optional `start` value:

```python
x = ('apple', 'banana', 'cherry')

print(list(enumerate(x, start=1)))
# [(1, 'apple'), (2, 'banana'), (3, 'cherry')]
```

<script type="py-editor">
x = ('apple', 'banana', 'cherry')

print(list(enumerate(x, start=1)))
</script>

### Pulling values out of the row

Since `first_row` is a list, we can index into it to get a single value,
and `header` tells us which column each position belongs to. That's a
good fit for `enumerate()`: looping over `header` gives us each column
name along with its position, and that same position is the index of the
matching value in `first_row`. Column `0` is `ConstituentID`, and the
value at `first_row[0]` is its data; column `1` is `DisplayName`, whose
data is at `first_row[1]`; and so on across the row:

```python
header = data[0]
first_row = data[1]

print(first_row[1])   # Robert Arneson

for index, column_name in enumerate(header):
    print(column_name, "=", first_row[index])

birth_year = first_row[5]
print(type(birth_year))   # <class 'str'>
print(int(birth_year) + 1)
```

The `for index, column_name in enumerate(header)` loop works just like
the fruit example: on each pass `index` is the column's position and
`column_name` is its name from the header. `first_row[index]` then grabs
the value sitting at that same position in the data row, so the loop
prints one `name = value` line per column.

Every field comes back as a **string**, even ones that look like numbers.
`first_row[5]` is `'1930'`, not `1930`, so `birth_year + 1` would fail
with a `TypeError` until we convert it with `int()` (see the
[type conversion functions in Part 1](../part1/)). Empty fields come back
as empty strings (`''`), not as a special "missing" value — worth
remembering when we start cleaning data.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    data = list(reader)

header = data[0]
first_row = data[1]

print(first_row[1])

for index, column_name in enumerate(header):
    print(column_name, "=", first_row[index])

birth_year = first_row[5]
print(type(birth_year))
print(int(birth_year) + 1)
</script>

### Options for open()

Two options on `open()` matter for every CSV you read:

| Option | What it does |
| --- | --- |
| `"r"` | The **mode**: how the file is opened. `"r"` means *read* (text), and it's what `open()` does by default if you leave the mode out. Other modes include `"w"` (write a new file, replacing any existing one) and `"a"` (append to the end of one). |
| `encoding="utf-8"` | Says how the bytes in the file map to characters. If you leave it out, Python uses your operating system's default, which differs between machines (often not UTF-8 on Windows). |

Encoding is the one that quietly corrupts cultural data, because names and
places are full of characters outside plain English text — the `–` in
`1930–1992`, the `ü` in `Jüri Arrak`. If you pick the wrong encoding you
either get a `UnicodeDecodeError` or, worse, no error but garbled text.
Here's the same first row of data (`data[1]`) read as `latin-1`, an older encoding that
assigns a different character to every byte:

```python
import csv

with open("moma_artists.csv", "r", encoding="latin-1") as file:
    reader = csv.reader(file)
    data = list(reader)

print(data[1])
# [..., 'American, 1930â\x80\x931992', ...]
```

The en dash was saved as three bytes, and `latin-1` reads each of those
bytes as its own character (the `\x80` and `\x93` are two of them, shown
as escape codes because they have no visible form). UTF-8 is by far the most common encoding for
CSV files, so it's the sensible default to try first. When it fails or
gives garbage, the file's source (or an error message) usually says what
was used instead — `"utf-8-sig"` for files exported from Excel with a
byte-order mark, or `"latin-1"` and `"cp1252"` for older exports.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="latin-1") as file:
    reader = csv.reader(file)
    data = list(reader)

print(data[1])
</script>

Try changing `"latin-1"` back to `"utf-8"` and running it again, then
try `"ascii"` to see the error you get when the file contains a character
the encoding doesn't know.

### Options for csv.reader()

`csv.reader(file)` uses sensible defaults, but it accepts a number of
keyword options for files that don't follow the standard layout. These are
the ones you'll see most often:

| Option | Default | What it does |
| --- | --- | --- |
| `delimiter` | `","` | The single character that separates fields. Use `"\t"` for tab-separated files, `";"` (common in European exports), or any other single character. |
| `quotechar` | `'"'` | The character that wraps a field containing the delimiter or a line break. |
| `quoting` | `csv.QUOTE_MINIMAL` | How quote characters are interpreted. `csv.QUOTE_NONE` ignores quoting entirely; `csv.QUOTE_NONNUMERIC` converts every unquoted field to a `float`. |
| `skipinitialspace` | `False` | If `True`, ignores spaces directly after a delimiter, for files written as `a, b, c`. |
| `doublequote` | `True` | Whether a doubled quote inside a quoted field (`""`) stands for one literal quote character. |
| `escapechar` | `None` | A character that marks the next character as literal, for files that escape with a backslash instead of doubling quotes. |
| `strict` | `False` | If `True`, raises a `csv.Error` on badly formatted input instead of guessing. |
| `dialect` | `"excel"` | A named bundle of all of the options above. `"excel-tab"` and `"unix"` are also built in. |


### Reading the whole file and picking a random row

The examples above loaded the whole file into `data` with `list(reader)`.
This one does the same thing, but first takes the header off with
`next(reader)`, which asks the reader for a single row (the next one it
hasn't handed out yet) and returns it. Everything left over then goes into
`rows`, so `rows` holds just the artists: a **list of lists** (see
[Part 3](../part3/)), one inner list per artist.

Once we have that list, picking a random row is the same trick as the
bonus example in [Part 3](../part3/). `random.randint(a, b)` gives back a
random whole number from `a` up to *and including* `b`, so we ask for a
number between `0` and `len(rows) - 1` (the last valid index) and use it
to pull one row out of `rows`:

```python
import csv
import random

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    rows = list(reader)

print(len(rows))   # how many artists are in the file

random_index = random.randint(0, len(rows) - 1)
random_row = rows[random_index]

print("Row", random_index)
for index, column_name in enumerate(header):
    print(column_name, "=", random_row[index])
```

Some things to notice in this one:

- **`rows = list(reader)`** reads everything left in the file. Because
  `header = next(reader)` already used up the first line, `rows` doesn't
  include the header, so `rows[0]` is the first *artist*, not the column
  names.
- **The data lives on after the `with` block.** The file is closed
  automatically once the indented block ends, but `header` and `rows` are
  ordinary variables that hold copies of the data, so we can keep using
  them below. That's why all the reading happens inside the `with` and all
  the picking and printing happens outside of it.
- **`len(rows) - 1`** matters because `randint` includes its upper bound
  and list indexes start at `0`. Asking for `randint(0, len(rows))` would
  occasionally produce an index one past the end of the list and raise an
  `IndexError`.
- **The loop is the one from earlier.** `enumerate(header)` supplies each
  column name and its position, and `random_row[index]` supplies the
  matching value. Run it a few times: some artists have a full set of
  values, while others have empty `Wiki QID` and `ULAN` fields, or a
  `BeginDate` or `EndDate` of `0`, which in this file means "unknown or
  still living."

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv
import random

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    rows = list(reader)

print(len(rows))

random_index = random.randint(0, len(rows) - 1)
random_row = rows[random_index]

print("Row", random_index)
for index, column_name in enumerate(header):
    print(column_name, "=", random_row[index])
</script>

Press the run button again to get a different artist each time.

`random.choice()` is a shortcut for the two lines that pick the row. It
takes any list and returns one random item from it, with no index math
needed:

```python
random_row = random.choice(rows)
```

### Reading rows as dictionaries with DictReader

`csv.reader` gives us each row as a list, so we have to remember which
position belongs to which column: `first_row[5]` is the birth year, but
nothing in the code says so. `csv.DictReader` solves this. It reads the
header row for us and uses those column names as **keys**, so every row
comes back as a **dictionary** (see [Part 3](../part3/)) instead of a list.

Here is the same idea as our first example, with two differences. We use
`csv.DictReader` in place of `csv.reader`, and this time we'll look at the
**last** item in the list instead of the first:

```python
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

last_row = data[-1]

print(last_row)

for key, value in last_row.items():
    print(key, "=", value)
```

Which prints:

```text
{'ConstituentID': '140918', 'DisplayName': 'John Wallace', 'ArtistBio': 'American, 1929 – 2011', 'Nationality': 'American', 'Gender': 'male', 'BeginDate': '1929', 'EndDate': '2011', 'Wiki QID': '', 'ULAN': ''}
ConstituentID = 140918
DisplayName = John Wallace
ArtistBio = American, 1929 – 2011
Nationality = American
Gender = male
BeginDate = 1929
EndDate = 2011
Wiki QID = 
ULAN = 
```

What's different from the `csv.reader` version:

- **`csv.DictReader(file)`** takes the same file object as `csv.reader`,
  and `list(reader)` collects the rows the same way. It also accepts the
  same options (`delimiter`, `quotechar`, and so on), plus a `fieldnames`
  option for supplying your own column names when a file has no header row.
- **The header is no longer part of the data.** `DictReader` uses the first
  line of the file as the keys, so it isn't returned as a row. That means
  `data[0]` is the first artist, and there is no separate `header` variable
  to keep track of.
- **`data[-1]` is the last item.** A negative index counts backwards from
  the end of the list, so `-1` is the last item, `-2` is the second to
  last, and so on (as in [Part 3](../part3/)). It's handy here because we
  don't need to know how many rows the file has.
- **`.items()`** gives every key in a dictionary along with its value, as
  a `(key, value)` pair. It works just like `enumerate()`, which paired
  each item with its position: the `for` loop unpacks each pair into two
  variables, here `key` and `value`. So we get a `name = value` line for
  every column without needing `header` or index numbers at all.
- **Values are still strings.** `'1929'` is text, not a number, just like
  with `csv.reader`.

The biggest benefit is that we can now ask for a value by column name.
`last_row["DisplayName"]` is much easier to read than `last_row[1]`, and it
keeps working even if the columns are reordered:

```python
print(last_row["DisplayName"])   # John Wallace
print(last_row["Wiki QID"])      # (empty: this artist has no Wiki QID)
```

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

last_row = data[-1]

print(last_row)

for key, value in last_row.items():
    print(key, "=", value)

print(last_row["DisplayName"])
print(last_row["Wiki QID"])
</script>

### Filtering by nationality

Since every row is a dictionary, we can check a single column of every
artist without counting positions. This uses the filtering pattern from
[Part 5](../part5/): loop over the list, use an `if` to test each item,
and `.append()` the ones that pass onto a new list. Here we keep only the
artists whose `Nationality` is `"Swedish"`:

```python
swedish_artists = []

for artist in data:
    if artist["Nationality"] == "Swedish":
        swedish_artists.append(artist)

print(len(swedish_artists))

for artist in swedish_artists[:10]:
    print(artist["DisplayName"], "-", artist["ArtistBio"])
```

Which prints:

```text
131
Folke Arstrom - Swedish, 1907–1997
Göran Åslin - Swedish, born 1940
Erik Gunnar Asplund - Swedish, 1885–1940
Monika Andersson - Swedish, born 1957
Olof Backman - Swedish, born 1899
Olle Baertling - Swedish, 1911–1981
Hagbard Elis Bergh - Swedish, 1881–1954
Håkan Bergkvist - Swedish, born 1946
Bengt Böckman - Swedish, born 1936
Carl-Arne Breger - Swedish, born 1923
```

A few things to notice:

- **The column is `Nationality`, not a birth country.** This file doesn't
  have a birth country column. The value we're matching is the nationality
  MoMA has recorded, which is `"Swedish"` and not `"Sweden"`, and it can
  differ from where someone was actually born. (Some `ArtistBio` values do
  mention a birthplace, like `"American, born Germany"`, but not in a
  consistent format we can filter on directly.) Some artists have no
  nationality at all, so their value is an empty string, and they won't
  match.
- **`==` has to match exactly**, including capital letters, so
  `"swedish"` wouldn't match `"Swedish"`.
- **`swedish_artists[:10]`** is a slice of the list (as in
  [Part 2](../part2/), slicing works on lists just like it does on
  strings), giving just the first 10 items. That keeps the output short.
  Remove `[:10]` to print all of them, and `len(swedish_artists)` above
  tells you how many there are in total.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

swedish_artists = []

for artist in data:
    if artist["Nationality"] == "Swedish":
        swedish_artists.append(artist)

print(len(swedish_artists))

for artist in swedish_artists[:10]:
    print(artist["DisplayName"], "-", artist["ArtistBio"])
</script>

Try changing `"Swedish"` to another nationality, like `"Finnish"` or
`"Japanese"`, and running it again.

### Filtering by birth year

Filtering on a number works the same way, with one extra step. Every
value from the CSV is a string, and Python can't compare a string like
`"1993"` to the number `1990`: it raises a `TypeError`. We convert the
`BeginDate` with `int()` first (see
[Part 1](../part1/)), then compare it with `>`:

```python
recent_artists = []

for artist in data:
    if int(artist["BeginDate"]) > 1990:
        recent_artists.append(artist)

print(len(recent_artists))

for artist in recent_artists[:10]:
    print(artist["DisplayName"], "-", artist["BeginDate"])
```

Which prints:

```text
211
K2 Design Studio - 1993
Cyan - 1992
Studio Boot - 1992
Una - 1992
interware SARL - 2000
IDEO - 1991
Acordis Industrial Fibers, The Netherlands - 1999
SHoP Architects PC - 1996
Pandora Design - 1998
Micro Compact Car Smart GmbH, Renningen, Germany, and Hambach, France - 1994
```

- **`int(artist["BeginDate"])`** does the conversion for each artist as the
  loop reaches them. It works here because every `BeginDate` in this file
  is made of digits. If a column had blanks, `int("")` would raise a
  `ValueError`, and we'd need to check for that first.
- **Artists with a `BeginDate` of `0` are left out automatically.** In
  this file `0` means "unknown," and `0 > 1990` is `False`, so those rows
  never get added.
- **Not everyone in the results is a person.** The MoMA collection also
  includes design studios, architecture firms, and companies, and for
  those `BeginDate` holds the year the group was founded. That's why so
  many of the results are firms and studios and not individuals. We'll
  filter those out next.

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

for artist in recent_artists[:10]:
    print(artist["DisplayName"], "-", artist["BeginDate"])
</script>

Try changing the year, or change `>` to `<` to see the artists born
before it. (Watch out for those `0` values, which would now all match!)

### Filtering the filtered list: only people

Our list of recent artists is full of studios and companies. The `Gender`
column gives us a way to filter most of them out, since a group doesn't
have a gender recorded, and its value is an empty string. We already have
the list `recent_artists`, so we can filter that list further to make a
new one, `recent_people`. The new loop keeps an artist only if their
`Gender` contains `"male"`, `"female"`, or `"non-binary"`:

```python
recent_people = []

for artist in recent_artists:
    gender = artist["Gender"]
    if "male" in gender or "female" in gender or "non-binary" in gender:
        recent_people.append(artist)

print(len(recent_people))

for artist in recent_people:
    print(artist["DisplayName"], "-", artist["BeginDate"], "-", artist["Gender"])
```

Which prints:

```text
23
interware SARL - 2000 - male
Max Weisel - 1991 - male
Zack Khalil - 1991 - male
Lucy Jones - 1991 - female
Yara Said - 1991 - female
Farah Al Qasimi - 1991 - female
Kahlil Robert Irving - 1992 - male
Louis Fratino - 1993 - male
Nora Turato - 1991 - female
Tyler Mitchell - 1995 - male
Jibbe van Schie - 1998 - male
Aria Dean - 1993 - female
Tadáskía - 1993 - female (transwoman)
Ji Jiawei - 1994 - male
Liu Liyuan - 1997 - female
Yuan Ruizhe - 1997 - female
Ye Zichen - 1996 - male
Arinjoy Sen - 1996 - male
Silvia Rosi - 1992 - female
Gabriel Fontana - 1993 - male
Luther Konadu - 1991 - male
Adam Vosburgh - 1994 - male
César Béjar - 1992 - male
```

Out of 211 recent artists, only 23 are left. Some things to notice:

- **The loop is over `recent_artists`, not `data`.** Each filter produces
  a new list that we can feed into the next one, so the two conditions
  (born after 1990, then has a gender) are applied one after the other.
- **`in` works on strings too.** `"male" in gender` asks whether the text
  `"male"` appears anywhere inside `gender` (see
  [Part 2](../part2/)), and `or` (from [Part 5](../part5/)) means only one
  of the three checks has to be `True`. An empty string contains none of
  them, which is how the groups get left out.
- **Why "contains" instead of `==`?** The `Gender` column isn't limited to
  three tidy values: it also includes free-text entries like
  `"female (transwoman)"`, which an exact match on `"female"` would miss.
  Checking whether the value *contains* the word catches it.
- **The `"female"` check is redundant.** The letters `male` appear inside
  `female`, so `"male" in "female"` is `True`, and the first check already
  catches everyone the second one does. We keep it in the code so it says
  what we mean, but it's a good example of how substring matching can
  surprise you. Try deleting it and running the code again to see that the
  result doesn't change.
- **The filter isn't perfect.** `interware SARL` is a company, but it has
  `male` recorded as its gender, so it slipped through. And the reverse
  also happens: an artist with no gender recorded, like `Dana Kavelina`,
  gets left out even though they're a person. A blank value tells us the
  gender wasn't recorded, and that's not always because it's a group.
  When you filter real cultural data, expect to double check the results
  by hand.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)

recent_artists = []

for artist in data:
    if int(artist["BeginDate"]) > 1990:
        recent_artists.append(artist)

recent_people = []

for artist in recent_artists:
    gender = artist["Gender"]
    if "male" in gender or "female" in gender or "non-binary" in gender:
        recent_people.append(artist)

print(len(recent_people))

for artist in recent_people:
    print(artist["DisplayName"], "-", artist["BeginDate"], "-", artist["Gender"])
</script>
