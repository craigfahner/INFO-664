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
so we bring it in with `import`:

```python
import csv

with open("moma_artists.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    first_row = next(reader)

print(header)
print(first_row)
```

This is the most code we've seen so far in one go, so here it is piece by
piece:

- **`import csv`** makes the `csv` module's tools available, under the
  name `csv`. The reader we want is `csv.reader`.
- **`open("moma_artists.csv", ...)`** opens the file and hands back a
  *file object*. Opening a file doesn't read anything yet; it just gets it
  ready. `newline=""` and `encoding="utf-8"` are options we'll come back
  to below.
- **`with ... as file:`** runs the indented block below it while the file
  is open, and closes the file automatically when the block ends — even if
  something goes wrong inside. Like `for`, `if`, and `def`, it ends in a
  colon and its body is indented.
- **`csv.reader(file)`** wraps the file object in a *reader*. The reader
  splits each line into a list of fields.
- **`next(reader)`** asks the reader for one row. The first call returns
  the first line of the file (the header). Calling it again picks up where
  it left off, so the second call returns the first row of actual data.
  That's why `header` and `first_row` end up holding different rows.

Each row comes back as a list, so everything from
[Part 3](../part3/) applies. Printing them gives:

```text
['ConstituentID', 'DisplayName', 'ArtistBio', 'Nationality', 'Gender', 'BeginDate', 'EndDate', 'Wiki QID', 'ULAN']
['1', 'Robert Arneson', 'American, 1930–1992', 'American', 'male', '1930', '1992', '', '']
```

Notice that `'American, 1930–1992'` came through as a single value: the
reader understood the quotes and kept the comma inside it.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    first_row = next(reader)

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
import csv

with open("moma_artists.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    first_row = next(reader)

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

with open("moma_artists.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    first_row = next(reader)

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
| `newline=""` | Turns off Python's own newline translation so the `csv` module can handle line endings itself. Without it, a quoted field that contains a line break (common in long museum descriptions) can be split into the wrong rows. The `csv` documentation recommends always including it. |
| `encoding="utf-8"` | Says how the bytes in the file map to characters. If you leave it out, Python uses your operating system's default, which differs between machines (often not UTF-8 on Windows). |

Encoding is the one that quietly corrupts cultural data, because names and
places are full of characters outside plain English text — the `–` in
`1930–1992`, the `ü` in `Jüri Arrak`. If you pick the wrong encoding you
either get a `UnicodeDecodeError` or, worse, no error but garbled text.
Here's the same first row read as `latin-1`, an older encoding that
assigns a different character to every byte:

```python
import csv

with open("moma_artists.csv", newline="", encoding="latin-1") as file:
    reader = csv.reader(file)
    header = next(reader)
    first_row = next(reader)

print(first_row)
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

with open("moma_artists.csv", newline="", encoding="latin-1") as file:
    reader = csv.reader(file)
    header = next(reader)
    first_row = next(reader)

print(first_row)
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

You pass them after the file object, by name. Here are a few of them
doing their work on the first row of `moma_artists.csv`.

**`delimiter`.** If the delimiter doesn't match the file, the reader can't
find any field boundaries and returns each line as one long string. The
file uses commas, so asking for semicolons gets us nothing useful:

```python
import csv

with open("moma_artists.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=";")
    header = next(reader)

print(header)
# ['ConstituentID,DisplayName,ArtistBio,Nationality,Gender,BeginDate,EndDate,Wiki QID,ULAN']
print(len(header))   # 1
```

A one-item list where you expected nine columns is the classic sign of the
wrong delimiter.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=";")
    header = next(reader)

print(header)
print(len(header))
</script>

**`quoting`.** With `csv.QUOTE_NONE` the reader stops treating quote
characters as special, so the comma inside the artist's bio is treated as
a separator like any other. The bio gets split in two, its quote marks
stay attached, and the row grows from nine fields to ten:

```python
import csv

with open("moma_artists.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file, quoting=csv.QUOTE_NONE)
    header = next(reader)
    first_row = next(reader)

print(first_row)
# ['1', 'Robert Arneson', '"American', ' 1930–1992"', 'American', 'male', '1930', '1992', '', '']
print(len(first_row))   # 10
```

This is exactly the problem that quoting exists to solve, and it's why you
should almost never split CSV lines by hand with `.split(",")` (as in
[Part 2](../part2/)) once your data has commas in it.

<script type="py-editor" config='{"files": {"{{ csv_url }}": "./moma_artists.csv"}}'>
import csv

with open("moma_artists.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file, quoting=csv.QUOTE_NONE)
    header = next(reader)
    first_row = next(reader)

print(first_row)
print(len(first_row))
</script>

**`delimiter` and `skipinitialspace` on text that isn't in a file.**
`csv.reader` doesn't actually need a file. It accepts anything that hands
it one line of text at a time, including a plain list of strings. That
makes it easy to test an option on a small sample before pointing it at a
big file:

```python
import csv

lines = ["1, Robert Arneson, American"]

print(next(csv.reader(lines)))
# ['1', ' Robert Arneson', ' American']

print(next(csv.reader(lines, skipinitialspace=True)))
# ['1', 'Robert Arneson', 'American']

pipe_lines = ["1|Robert Arneson|American"]

print(next(csv.reader(pipe_lines, delimiter="|")))
# ['1', 'Robert Arneson', 'American']
```

By default the leading space after each comma stays attached to the value;
`skipinitialspace=True` trims it. The pipe example shows `delimiter`
working properly, on a line that really is separated by `|`.

<script type="py-editor">
import csv

lines = ["1, Robert Arneson, American"]

print(next(csv.reader(lines)))
print(next(csv.reader(lines, skipinitialspace=True)))

pipe_lines = ["1|Robert Arneson|American"]

print(next(csv.reader(pipe_lines, delimiter="|")))
</script>

The reader object also keeps track of where it is: after the two `next()`
calls in our first example, `reader.line_num` would be `2`. That number
comes in handy for error messages ("problem on line 5,412") once we start
looping through the whole file.
