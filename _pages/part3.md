---
layout: page
title: Part 3
permalink: /part3/
---

## Part 3: Collections

### Lists

A list is an ordered collection of values, written with square brackets
and commas: `[value1, value2, ...]`. We already ran into lists back in
[Part 2](../part2/) as the result of `.split()` — a list is that same
type, just built directly instead of coming from splitting a string.

A list can hold strings, numbers, or even other lists:

```python
birds = ["Robin", "Sparrow", "Blue Jay", "Cardinal", "Crow",
         "Finch", "Owl", "Hawk", "Hummingbird", "Woodpecker"]

leap_years = [2000, 2004, 2008, 2012, 2016, 2020, 2024]

bands = [
    ["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"],
    ["Mick Jagger", "Keith Richards", "Charlie Watts", "Ronnie Wood", "Bill Wyman"],
    ["John Phillips", "Michelle Phillips", "Cass Elliot", "Denny Doherty"],
]

print(birds)
print(leap_years)
print(bands)
```

`birds` is a list of `str`, `leap_years` is a list of `int`, and `bands`
is a **list of lists** — each item in `bands` is itself a whole list (The
Beatles, then The Rolling Stones, then The Mamas & the Papas).

<script type="py-editor">
birds = ["Robin", "Sparrow", "Blue Jay", "Cardinal", "Crow",
         "Finch", "Owl", "Hawk", "Hummingbird", "Woodpecker"]

leap_years = [2000, 2004, 2008, 2012, 2016, 2020, 2024]

bands = [
    ["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"],
    ["Mick Jagger", "Keith Richards", "Charlie Watts", "Ronnie Wood", "Bill Wyman"],
    ["John Phillips", "Michelle Phillips", "Cass Elliot", "Denny Doherty"],
]

print(birds)
print(leap_years)
print(bands)
</script>

### Indexing into a list of lists

Grabbing a value out of `birds` or `leap_years` is just `[index]`, the
same as indexing a string. `bands` needs one extra step, since each item
in `bands` is itself a list — the first `[ ]` picks which band, and the
second `[ ]` picks which member of that band:

```python
band_member = bands[0][1]   # 2nd member of the 1st band -- "Paul McCartney"
leap_year = leap_years[3]   # 4th leap year in the list -- 2012
bird = birds[4]             # 5th bird in the list -- "Crow"

sentence = f"{band_member} was born in {leap_year} and their favorite bird is {bird}"
print(sentence)
```

<script type="py-editor">
birds = ["Robin", "Sparrow", "Blue Jay", "Cardinal", "Crow",
         "Finch", "Owl", "Hawk", "Hummingbird", "Woodpecker"]

leap_years = [2000, 2004, 2008, 2012, 2016, 2020, 2024]

bands = [
    ["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"],
    ["Mick Jagger", "Keith Richards", "Charlie Watts", "Ronnie Wood", "Bill Wyman"],
    ["John Phillips", "Michelle Phillips", "Cass Elliot", "Denny Doherty"],
]

band_member = bands[0][1]
leap_year = leap_years[3]
bird = birds[4]

sentence = f"{band_member} was born in {leap_year} and their favorite bird is {bird}"
print(sentence)
</script>

### Searching for a value in a list

You can use the `in` operator, as we did with strings, to find an item in a list:

```
albums = ["Abbey Road", "Revolver", "Let It Be"]
"Revolver" in albums  # True
```

You can also use the `index` method to back-search for the index-position of a given item:

`albums.index("Revolver")  # 1`



### Changing a value in a list

Unlike strings — where every method we've used (`.upper()`, `.replace()`,
`.strip()`, ...) hands back a brand-new string — lists are **mutable**:
you can change an item in place with `[index] = new_value`, no new list
required. Assigning to `bands[1][3]` reaches into the Rolling Stones list
(`bands[1]`) and replaces its 4th member (`[3]`), swapping "Ronnie Wood"
for original member "Brian Jones":

```python
print(bands[1])   # before

bands[1][3] = "Brian Jones"

print(bands[1])   # after
```

<script type="py-editor">
bands = [
    ["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"],
    ["Mick Jagger", "Keith Richards", "Charlie Watts", "Ronnie Wood", "Bill Wyman"],
    ["John Phillips", "Michelle Phillips", "Cass Elliot", "Denny Doherty"],
]

print(bands[1])

bands[1][3] = "Brian Jones"

print(bands[1])
</script>

### Adding an item to a list

`.append()` adds a new item to the **end** of a list, growing it by one —
another way lists can change after they're created:

```python
birds = ["Robin", "Sparrow", "Blue Jay", "Cardinal", "Crow",
         "Finch", "Owl", "Hawk", "Hummingbird", "Woodpecker"]

birds.append("Cockatoo")

print(birds)
```

<script type="py-editor">
birds = ["Robin", "Sparrow", "Blue Jay", "Cardinal", "Crow",
         "Finch", "Owl", "Hawk", "Hummingbird", "Woodpecker"]

birds.append("Cockatoo")

print(birds)
</script>

### List operations: min, max, len, average, and sort

A handful of built-in functions work on any list of numbers:

```python
temperatures = [72, 68, 95, 61, 80, 77, 55, 90, 83, 64]

print(min(temperatures))   # smallest value
print(max(temperatures))   # largest value
print(len(temperatures))   # how many items are in the list

average = sum(temperatures) / len(temperatures)
print(average)
```

There's no built-in `average()` function, but `sum()` adds up every value
in the list, and dividing that by `len()` (the count of values) gives the
average.

`.sort()` puts the list in order — from smallest to largest by default —
and, like the list changes from earlier in this section, it does this
**in place** rather than returning a new list:

```python
temperatures.sort()
print(temperatures)
```

<script type="py-editor">
temperatures = [72, 68, 95, 61, 80, 77, 55, 90, 83, 64]

print(min(temperatures))
print(max(temperatures))
print(len(temperatures))

average = sum(temperatures) / len(temperatures)
print(average)

temperatures.sort()
print(temperatures)
</script>

`.sort` can also  order things in reverse, using the `reverse=True` argument:

`temperatures.sort(reverse=True)`

### More list methods

Starting from a daily routine, here's a walkthrough of six more list
methods, each one changing the list a little further:

```python
daily_routine = ["wake up", "eat breakfast", "go to work", "eat lunch",
                  "go home", "exercise", "eat dinner", "watch tv"]

# append() -- add a new item to the end
daily_routine.append("go to sleep")
print(daily_routine)

# insert(index, item) -- add an item at a specific position, shifting
# everything else at and after that position to the right. "eat breakfast"
# is at index 1, so inserting at index 2 puts "walk the dog" right after it.
daily_routine.insert(2, "walk the dog")
print(daily_routine)

# remove(value) -- remove the first item that matches the given value
daily_routine.remove("exercise")
print(daily_routine)

# pop(index) -- remove an item by index and return it; .index() finds
# "watch tv"'s current position first, since earlier steps shifted it
popped_task = daily_routine.pop(daily_routine.index("watch tv"))
print(popped_task)
print(daily_routine)

# reverse() -- flip the order of the whole list, in place
daily_routine.reverse()
print(daily_routine)

# clear() -- remove everything, leaving an empty list
daily_routine.clear()
print(daily_routine)
```

<script type="py-editor">
daily_routine = ["wake up", "eat breakfast", "go to work", "eat lunch",
                  "go home", "exercise", "eat dinner", "watch tv"]

daily_routine.append("go to sleep")
print(daily_routine)

daily_routine.insert(2, "walk the dog")
print(daily_routine)

daily_routine.remove("exercise")
print(daily_routine)

popped_task = daily_routine.pop(daily_routine.index("watch tv"))
print(popped_task)
print(daily_routine)

daily_routine.reverse()
print(daily_routine)

daily_routine.clear()
print(daily_routine)
</script>

### Dictionaries

A list looks things up by **position** — `birds[2]` only makes sense if
you remember that index `2` happens to be the third bird. A dictionary
instead looks things up by **label**: it's a collection of `key: value`
pairs, written with curly braces, where each value is retrieved by name
rather than by position. That makes a dictionary a natural fit for
describing one real-world thing with several named attributes.

Here are the first three Beatles albums (UK releases), each one a
dictionary with the same four keys — `album_title`, `release_date`,
`running_time`, and `tracks` (itself a list, since an album has many
tracks):

```python
beatles_albums = [
    {
        "album_title": "Please Please Me",
        "release_date": "22 March 1963",
        "running_time": "31:59",
        "tracks": ["I Saw Her Standing There", "Misery", "Anna (Go to Him)",
                   "Chains", "Boys", "Ask Me Why", "Please Please Me",
                   "Love Me Do", "P.S. I Love You", "Baby It's You",
                   "Do You Want to Know a Secret", "A Taste of Honey",
                   "There's a Place", "Twist and Shout"],
    },
    {
        "album_title": "With the Beatles",
        "release_date": "22 November 1963",
        "running_time": "33:07",
        "tracks": ["It Won't Be Long", "All I've Got to Do", "All My Loving",
                   "Don't Bother Me", "Little Child", "Till There Was You",
                   "Please Mister Postman", "Roll Over Beethoven", "Hold Me Tight",
                   "You Really Got a Hold on Me", "I Wanna Be Your Man",
                   "Devil in Her Heart", "Not a Second Time",
                   "Money (That's What I Want)"],
    },
    {
        "album_title": "A Hard Day's Night",
        "release_date": "10 July 1964",
        "running_time": "30:09",
        "tracks": ["A Hard Day's Night", "I Should Have Known Better", "If I Fell",
                   "I'm Happy Just to Dance with You", "And I Love Her", "Tell Me Why",
                   "Can't Buy Me Love", "Any Time at All", "I'll Cry Instead",
                   "Things We Said Today", "When I Get Home", "You Can't Do That",
                   "I'll Be Back"],
    },
]

first_album = beatles_albums[0]
print(first_album["album_title"])
print(first_album["release_date"])
print(first_album["running_time"])
print(first_album["tracks"])
```

`beatles_albums` is a list (indexed `[0]`, `[1]`, `[2]` — one per album),
and each item inside it is a dictionary (indexed by key, like
`["album_title"]`) — a list and a dictionary working together.

<script type="py-editor">
beatles_albums = [
    {
        "album_title": "Please Please Me",
        "release_date": "22 March 1963",
        "running_time": "31:59",
        "tracks": ["I Saw Her Standing There", "Misery", "Anna (Go to Him)",
                   "Chains", "Boys", "Ask Me Why", "Please Please Me",
                   "Love Me Do", "P.S. I Love You", "Baby It's You",
                   "Do You Want to Know a Secret", "A Taste of Honey",
                   "There's a Place", "Twist and Shout"],
    },
    {
        "album_title": "With the Beatles",
        "release_date": "22 November 1963",
        "running_time": "33:07",
        "tracks": ["It Won't Be Long", "All I've Got to Do", "All My Loving",
                   "Don't Bother Me", "Little Child", "Till There Was You",
                   "Please Mister Postman", "Roll Over Beethoven", "Hold Me Tight",
                   "You Really Got a Hold on Me", "I Wanna Be Your Man",
                   "Devil in Her Heart", "Not a Second Time",
                   "Money (That's What I Want)"],
    },
    {
        "album_title": "A Hard Day's Night",
        "release_date": "10 July 1964",
        "running_time": "30:09",
        "tracks": ["A Hard Day's Night", "I Should Have Known Better", "If I Fell",
                   "I'm Happy Just to Dance with You", "And I Love Her", "Tell Me Why",
                   "Can't Buy Me Love", "Any Time at All", "I'll Cry Instead",
                   "Things We Said Today", "When I Get Home", "You Can't Do That",
                   "I'll Be Back"],
    },
]

first_album = beatles_albums[0]
print(first_album["album_title"])
print(first_album["release_date"])
print(first_album["running_time"])
print(first_album["tracks"])
</script>

### Converting a dictionary value from a string to seconds

`running_time` is stored as a string, `"31:59"` — the same
minutes-and-seconds format from the song length example back in
[Part 2](../part2/). The same conversion applies here: split on `:`,
convert each half to an `int`, then combine them:

```python
running_time = beatles_albums[0]["running_time"]   # "31:59"

minutes_str, seconds_str = running_time.split(":")
total_seconds = int(minutes_str) * 60 + int(seconds_str)

print(total_seconds)   # 1919
```

<script type="py-editor">
beatles_albums = [
    {
        "album_title": "Please Please Me",
        "release_date": "22 March 1963",
        "running_time": "31:59",
        "tracks": ["I Saw Her Standing There", "Misery"],
    },
]

running_time = beatles_albums[0]["running_time"]

minutes_str, seconds_str = running_time.split(":")
total_seconds = int(minutes_str) * 60 + int(seconds_str)

print(total_seconds)
</script>

### Adding a new key to a dictionary

Assigning to `dictionary["some_key"] = value` adds a new key/value pair if
that key doesn't already exist — the same "created (or updated)"
assignment behavior from [Part 1's Variables section](../part1/), just
applied to a dictionary key instead of a plain variable name. Here, each
album gets a new `running_time_in_seconds` key, using the same
string-to-seconds conversion as before:

```python
minutes_str, seconds_str = beatles_albums[0]["running_time"].split(":")
beatles_albums[0]["running_time_in_seconds"] = int(minutes_str) * 60 + int(seconds_str)

minutes_str, seconds_str = beatles_albums[1]["running_time"].split(":")
beatles_albums[1]["running_time_in_seconds"] = int(minutes_str) * 60 + int(seconds_str)

minutes_str, seconds_str = beatles_albums[2]["running_time"].split(":")
beatles_albums[2]["running_time_in_seconds"] = int(minutes_str) * 60 + int(seconds_str)

print(beatles_albums[0])
print(beatles_albums[1])
print(beatles_albums[2])
```

<script type="py-editor">
beatles_albums = [
    {
        "album_title": "Please Please Me",
        "release_date": "22 March 1963",
        "running_time": "31:59",
        "tracks": ["I Saw Her Standing There", "Misery", "Anna (Go to Him)",
                   "Chains", "Boys", "Ask Me Why", "Please Please Me",
                   "Love Me Do", "P.S. I Love You", "Baby It's You",
                   "Do You Want to Know a Secret", "A Taste of Honey",
                   "There's a Place", "Twist and Shout"],
    },
    {
        "album_title": "With the Beatles",
        "release_date": "22 November 1963",
        "running_time": "33:07",
        "tracks": ["It Won't Be Long", "All I've Got to Do", "All My Loving",
                   "Don't Bother Me", "Little Child", "Till There Was You",
                   "Please Mister Postman", "Roll Over Beethoven", "Hold Me Tight",
                   "You Really Got a Hold on Me", "I Wanna Be Your Man",
                   "Devil in Her Heart", "Not a Second Time",
                   "Money (That's What I Want)"],
    },
    {
        "album_title": "A Hard Day's Night",
        "release_date": "10 July 1964",
        "running_time": "30:09",
        "tracks": ["A Hard Day's Night", "I Should Have Known Better", "If I Fell",
                   "I'm Happy Just to Dance with You", "And I Love Her", "Tell Me Why",
                   "Can't Buy Me Love", "Any Time at All", "I'll Cry Instead",
                   "Things We Said Today", "When I Get Home", "You Can't Do That",
                   "I'll Be Back"],
    },
]

minutes_str, seconds_str = beatles_albums[0]["running_time"].split(":")
beatles_albums[0]["running_time_in_seconds"] = int(minutes_str) * 60 + int(seconds_str)

minutes_str, seconds_str = beatles_albums[1]["running_time"].split(":")
beatles_albums[1]["running_time_in_seconds"] = int(minutes_str) * 60 + int(seconds_str)

minutes_str, seconds_str = beatles_albums[2]["running_time"].split(":")
beatles_albums[2]["running_time_in_seconds"] = int(minutes_str) * 60 + int(seconds_str)

print(beatles_albums[0])
print(beatles_albums[1])
print(beatles_albums[2])
</script>

### Safely accessing a dictionary value with get()

`beatles_albums[0]["producer"]` would raise a `KeyError` if `"producer"`
isn't a key in that dictionary — there's no key by that name in any album
here. `.get(key, default)` checks for the key and returns its value if
found, or the `default` you provide if it isn't, instead of crashing:

```python
first_album = beatles_albums[0]

print(first_album.get("producer", "Unknown"))       # "Unknown" -- no "producer" key
print(first_album.get("album_title", "Unknown"))     # "Please Please Me" -- key exists

print(first_album["producer"])   # KeyError: 'producer'
```

<script type="py-editor">
first_album = {
    "album_title": "Please Please Me",
    "release_date": "22 March 1963",
    "running_time": "31:59",
}

print(first_album.get("producer", "Unknown"))
print(first_album.get("album_title", "Unknown"))

print(first_album["producer"])
</script>

### Tuples

Before using one as a dictionary key, it's worth introducing the tuple
itself: a tuple is an ordered collection of values, just like a list, but
written with parentheses `( )` instead of square brackets. The important
difference is that a tuple is **immutable** — once created, it can't be
changed. Indexing works the same as it does on a list:

```python
coordinates = (40.7128, -74.0060)

print(coordinates)
print(coordinates[0])   # indexing works just like a list -- 40.7128

coordinates[0] = 0
# TypeError: 'tuple' object does not support item assignment
```

<script type="py-editor">
coordinates = (40.7128, -74.0060)

print(coordinates)
print(coordinates[0])

coordinates[0] = 0
</script>

That immutability is exactly why a tuple — unlike a list — is allowed as
a dictionary key, which is what the next example relies on.

### What can be used as a dictionary key?

A dictionary key has to be **immutable** — a type of value that can't be
changed after it's created. `str`, `int`, `float`, and `tuple` all work
fine as keys (that's why every key so far has been a string):

```python
mixed_keys = {}
mixed_keys[1] = "an int key"
mixed_keys["one"] = "a string key"
mixed_keys[(1, 2)] = "a tuple key"

print(mixed_keys)
```

Lists (and dictionaries) are **mutable**, so Python won't allow them as
keys — a key has to stay the same forever so Python can reliably find it
again later:

```python
mixed_keys[[1, 2]] = "a list key"
# TypeError: unhashable type: 'list'
```

<script type="py-editor">
mixed_keys = {}
mixed_keys[1] = "an int key"
mixed_keys["one"] = "a string key"
mixed_keys[(1, 2)] = "a tuple key"

print(mixed_keys)

mixed_keys[[1, 2]] = "a list key"
</script>

### Sorting a list of dictionaries

Let's look at a new dataset, exploring a common task when dealing with datasets: sorting by quantities.

Say a birder finishes a walk through Central Park having recorded every
bird they spotted, from the first one seen to the last. Each observation
is a dictionary with four keys (`common_name`, `scientific_name`,
`location`, and `count`), and the list holds them in observation order -
so index `0` is the first bird, and the last index is the most recent:

```python
central_park_birds = [
    {
        "common_name": "Blue Jay",
        "scientific_name": "Cyanocitta cristata",
        "location": "The Ramble",
        "count": 2,
    },
    {
        "common_name": "Northern Cardinal",
        "scientific_name": "Cardinalis cardinalis",
        "location": "The Ramble",
        "count": 1,
    },
    {
        "common_name": "American Robin",
        "scientific_name": "Turdus migratorius",
        "location": "Great Lawn",
        "count": 12,
    },
    {
        "common_name": "Red-tailed Hawk",
        "scientific_name": "Buteo jamaicensis",
        "location": "Belvedere Castle",
        "count": 1,
    },
    {
        "common_name": "Mallard",
        "scientific_name": "Anas platyrhynchos",
        "location": "The Lake",
        "count": 7,
    },
]

print(central_park_birds)
```

<script type="py-editor">
central_park_birds = [
    {
        "common_name": "Blue Jay",
        "scientific_name": "Cyanocitta cristata",
        "location": "The Ramble",
        "count": 2,
    },
    {
        "common_name": "Northern Cardinal",
        "scientific_name": "Cardinalis cardinalis",
        "location": "The Ramble",
        "count": 1,
    },
    {
        "common_name": "American Robin",
        "scientific_name": "Turdus migratorius",
        "location": "Great Lawn",
        "count": 12,
    },
    {
        "common_name": "Red-tailed Hawk",
        "scientific_name": "Buteo jamaicensis",
        "location": "Belvedere Castle",
        "count": 1,
    },
    {
        "common_name": "Mallard",
        "scientific_name": "Anas platyrhynchos",
        "location": "The Lake",
        "count": 7,
    },
]

print(central_park_birds)
</script>

Observation order isn't the only order that matters, though. Maybe what
matters most is which birds showed up in the largest numbers. To reorder
the list by `count`, use `sorted()`. Unlike `.sort()` (from earlier in
this part, which rearranges a list **in place**), `sorted()` returns a
brand-new list and leaves `central_park_birds` itself untouched.

There's one catch: `sorted()` can't tell, on its own, which value inside
each dictionary to compare. The `key` argument tells it what to sort by —
you hand it a small helper that receives one item and returns the value to
use. `key=lambda bird: bird["count"]` reads as "for each bird (a
dictionary), sort by its `count`." (A `lambda` is just a short, unnamed
function that, in this case, extracts the "count" field from the dataset – we will be exploring custom functions next week.)

```python
sorted_birds = sorted(central_park_birds, key=lambda bird: bird["count"])

print(sorted_birds)
```

<script type="py-editor">
central_park_birds = [
    {
        "common_name": "Blue Jay",
        "scientific_name": "Cyanocitta cristata",
        "location": "The Ramble",
        "count": 2,
    },
    {
        "common_name": "Northern Cardinal",
        "scientific_name": "Cardinalis cardinalis",
        "location": "The Ramble",
        "count": 1,
    },
    {
        "common_name": "American Robin",
        "scientific_name": "Turdus migratorius",
        "location": "Great Lawn",
        "count": 12,
    },
    {
        "common_name": "Red-tailed Hawk",
        "scientific_name": "Buteo jamaicensis",
        "location": "Belvedere Castle",
        "count": 1,
    },
    {
        "common_name": "Mallard",
        "scientific_name": "Anas platyrhynchos",
        "location": "The Lake",
        "count": 7,
    },
]

sorted_birds = sorted(central_park_birds, key=lambda bird: bird["count"])

print(sorted_birds)
</script>

The birds now run from smallest `count` to largest. Note the two birds
tied at `1` (the Northern Cardinal and the Red-tailed Hawk) keep their
original relative order — Python's sort is *stable*, so equal items stay
put. And because `sorted()` returned a new list, `central_park_birds`
still holds the birds in the order they were observed.

To list the most numerous birds first, add `reverse=True` to sort from
largest `count` down to smallest:

```python
sorted_birds = sorted(central_park_birds, key=lambda bird: bird["count"], reverse=True)

print(sorted_birds)
```

<script type="py-editor">
central_park_birds = [
    {
        "common_name": "Blue Jay",
        "scientific_name": "Cyanocitta cristata",
        "location": "The Ramble",
        "count": 2,
    },
    {
        "common_name": "Northern Cardinal",
        "scientific_name": "Cardinalis cardinalis",
        "location": "The Ramble",
        "count": 1,
    },
    {
        "common_name": "American Robin",
        "scientific_name": "Turdus migratorius",
        "location": "Great Lawn",
        "count": 12,
    },
    {
        "common_name": "Red-tailed Hawk",
        "scientific_name": "Buteo jamaicensis",
        "location": "Belvedere Castle",
        "count": 1,
    },
    {
        "common_name": "Mallard",
        "scientific_name": "Anas platyrhynchos",
        "location": "The Lake",
        "count": 7,
    },
]

sorted_birds = sorted(central_park_birds, key=lambda bird: bird["count"], reverse=True)

print(sorted_birds)
</script>

### Appending a dictionary to a list

`central_park_birds` holds five sightings, in first-to-last order. Say the
birder keeps walking and spots a sixth bird. The `.append()` method is
already familiar — it added the string `"Cockatoo"` to the `birds` list in
the "Adding an item to a list" section earlier in this part. The only new
thing here is *what* gets appended: a whole dictionary instead of a single
string. `.append()` doesn't care about the item's type — it always adds it
onto the end of the list, so the new sighting takes the last position,
right where the observation order says it belongs:

```python
central_park_birds = [
    {
        "common_name": "Blue Jay",
        "scientific_name": "Cyanocitta cristata",
        "location": "The Ramble",
        "count": 2,
    },
    {
        "common_name": "Northern Cardinal",
        "scientific_name": "Cardinalis cardinalis",
        "location": "The Ramble",
        "count": 1,
    },
    {
        "common_name": "American Robin",
        "scientific_name": "Turdus migratorius",
        "location": "Great Lawn",
        "count": 12,
    },
    {
        "common_name": "Red-tailed Hawk",
        "scientific_name": "Buteo jamaicensis",
        "location": "Belvedere Castle",
        "count": 1,
    },
    {
        "common_name": "Mallard",
        "scientific_name": "Anas platyrhynchos",
        "location": "The Lake",
        "count": 7,
    },
]

central_park_birds.append({
    "common_name": "Rock Pigeon",
    "scientific_name": "Columba livia",
    "location": "Sheep Meadow",
    "count": 9,
})

print(central_park_birds[-1])   # the newest sighting
print(len(central_park_birds))  # total distinct sightings: 6
```

<script type="py-editor">
central_park_birds = [
    {
        "common_name": "Blue Jay",
        "scientific_name": "Cyanocitta cristata",
        "location": "The Ramble",
        "count": 2,
    },
    {
        "common_name": "Northern Cardinal",
        "scientific_name": "Cardinalis cardinalis",
        "location": "The Ramble",
        "count": 1,
    },
    {
        "common_name": "American Robin",
        "scientific_name": "Turdus migratorius",
        "location": "Great Lawn",
        "count": 12,
    },
    {
        "common_name": "Red-tailed Hawk",
        "scientific_name": "Buteo jamaicensis",
        "location": "Belvedere Castle",
        "count": 1,
    },
    {
        "common_name": "Mallard",
        "scientific_name": "Anas platyrhynchos",
        "location": "The Lake",
        "count": 7,
    },
]

central_park_birds.append({
    "common_name": "Rock Pigeon",
    "scientific_name": "Columba livia",
    "location": "Sheep Meadow",
    "count": 9,
})

print(central_park_birds[-1])
print(len(central_park_birds))
</script>

The new dictionary sits at index `5` — the sixth position — and the five
sightings before it are left completely unchanged.
