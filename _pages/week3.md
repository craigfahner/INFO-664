---
layout: page
title: Week 3
permalink: /week3/
---

## Week 3 activities


* [Python lists and loops tutorial (Melanie Walsh)](https://melaniewalsh.github.io/Intro-Cultural-Analytics/02-Python/09-Lists-Loops-Part1.html)
* [Python dictionaries tutorial (Melanie Walsh)](https://melaniewalsh.github.io/Intro-Cultural-Analytics/02-Python/11-Dictionaries.html)
* [Advanced list sorting (python.org official docs)](https://docs.python.org/3/howto/sorting.html)
* [Previous students' INFO-664 final projects (updated)](https://gofilipa.github.io/664-projects/)

### Copy-and-paste snippets

copy and paste the below lists so you don't have to worry about typing them out during lecture!

```
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


### Homework: 

1. Convert your dataset into a *list* or a *dictionary* (or, a *list of dictionaries*). If you are using dictionaries, be sure to use naming conventions for your keys that are related to the data represented, and use valid syntax. Print the contents of your dataset in your notebook.
2. Using the `sorted()` function, generate two new lists that are sorted according to two different quantities in your data (for instance, if you've tracked step count and weather per day, sort by step count and sort by temperature). Print these sorted lists in your notebook using `for` loops, printing one item at a time.
3. Record another day's worth of data. Use the `append()` function to add the additional data to the original dataset. Print the resulting appended dataset.