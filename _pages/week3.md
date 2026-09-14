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
```


### Homework: 

1. Convert your dataset into a *list* or a *dictionary* (or, a *list of dictionaries*). If you are using dictionaries, be sure to use naming conventions for your keys that are related to the data represented, and use valid syntax. Print the contents of your dataset in your notebook.
2. Using the `sorted()` function, generate two new lists that are sorted according to two different quantities in your data (for instance, if you've tracked step count and weather per day, sort by step count and sort by temperature). Print these sorted lists in your notebook.
3. Record another day's worth of data. Use the `append()` function to add the additional data to the original dataset. Print the resulting appended dataset.