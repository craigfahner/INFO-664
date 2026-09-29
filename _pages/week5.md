---
layout: page
title: Week 5
permalink: /week5/
---

## Week 5 activities

* Where we're headed
    * JSON
    * APIs
    * [Regular Expressions](https://www.w3schools.com/python/python_regex.asp) - finding patterns in strings
    * [Web scraping](https://beautiful-soup-4.readthedocs.io/en/latest/)
    * [Pandas](https://pandas.pydata.org/) - data analysis library [(more info)](https://medium.com/learning-data/a-gentle-introduction-to-pythons-pandas-library-the-first-5-functions-you-need-to-know-fc045e24f3c8)
    * Image analysis
    * [Plotly](https://plotly.com/python/)
* [Final project info](https://craigfahner.github.io/INFO-664/final/)
* [Final project proposal](https://docs.google.com/document/d/1s8dxITVsdydEv0ruppHDsOejC7CLYqfA8zM2fhsiEAM/edit?usp=sharing)
* Individual discussions about final project ideas
* [Lecture notes Part 8: Review](https://craigfahner.github.io/INFO-664/part8/)
* [Link to in-class notebook](https://github.com/craigfahner/INFO-664/blob/main/week5/week5.ipynb)


**Download the MoMA Artists CSV**

We will use the [MoMA dataset](https://github.com/craigfahner/INFO-664/blob/main/notebooks/moma_artists.csv) again today. Please move a copy of it into your week5 folder. 

### In-class coding challenge

MoMA's artists were born across hundreds of years. Which birth years show up the most often in the collection?

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
takes a `lambda` key, which we covered in [week 3](https://craigfahner.github.io/INFO-664/part3/). 

### Homework 

1. **complete the in-class coding challenge** if you haven't already
2. **complete the final project proposal** and submit via Canvas

