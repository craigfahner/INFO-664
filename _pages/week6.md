---
layout: page
title: Week 6
permalink: /week6/
---

## Week 6 activities


* [Regular expressions (wikipedia)](https://en.wikipedia.org/wiki/Regular_expression)
* [Pythex - in-browser regular expression editor](https://pythex.org/)
* [Python's regular expression documentation](https://docs.python.org/3/library/re.html)
* [Met Museum API](https://metmuseum.github.io/)
* [NYTimes API registration](https://developer.nytimes.com/get-started)
* [NYTimes Article Search API](https://developer.nytimes.com/docs/articlesearch-product/1/overview)
* [List of public apis](https://github.com/public-apis/public-apis)
* [Lecture notes Part 9: CSV saving and regular expressions](https://craigfahner.github.io/INFO-664/part9/)
* [Lecture notes Part 10: APIs](https://craigfahner.github.io/INFO-664/part9/)
* [In-class jupyter notebook](https://github.com/craigfahner/INFO-664/blob/main/week6/week6.ipynb)

**Download the MoMA Art CSV (optional)**

I will show a quick example with the [MoMA Art dataset](https://github.com/craigfahner/INFO-664/blob/main/week6/moma_art.csv) today. If you like, you can move a copy of it into your week6 folder to follow along. This is different from the MoMA artists dataset, as it contains information about all the artworks, rather than just the artists.

**Download the UNESCO cultural heritage sites JSON dataset**

[Download it here!](https://github.com/craigfahner/INFO-664/blob/main/week6/unesco_cultural_sites.json) 

**Download the XML example file**

[Download it here!](https://github.com/craigfahner/INFO-664/blob/main/week6/loc_book.xml) 

### Code Snippets for in-class demos

At various times today you'll need these code snippets! Keep them handy so you don't have to type out lengthy URLs:

**Reading the moma_art.csv file**

```
import csv   # brings in all the csv-related functions

with open("moma_art.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)   # read the file as dictionaries
    data = list(reader)             # convert that into a usable list called "data"
```

**The Whitney artwork caption we will parse with regular expressions**:
```python
caption = "William Wegman, Cotto, 1970. Gelatin silver print, 7 7/8 × 7 3/4 in. (20 × 19.7 cm). Whitney Museum of American Art, New York; purchase with funds from the Mrs. Percy Uris Purchase Fund and the Photography Committee 92.14 © William Wegman"
```

**A list of test words we can check for matches for "love" or "loving"**

`test_words = ["Love", "Loving", "love", "lovely", "glove", "beloved"]`

**Met API snippets!**

*doing a search*:

```python
import requests

base_url = "https://collectionapi.metmuseum.org"
search_path = "/public/collection/v1.1/search"
search_query = "?q=Antelope"
```

```python
url = f'{base_url}{search_path}{search_query}'
search_response = requests.get(url)

print(url)   # https://collectionapi.metmuseum.org/public/collection/v1.1/search?q=Antelope
```

*looking up info about specific MET objects*:

```python
object_path = "/public/collection/v1/objects/"
url = f"{base_url}{object_path}{first_found_item}"

response_object = requests.get(url)
```

**NYTimes API snippets!**

*Setting up API key and imports*:

```python
import requests
from getpass import getpass
from time import sleep

key = getpass("Paste your NYT API key: ")
```

*Making a query*:

```python
query = "migrant"

begin_date = "20260901"
end_date = "20260930"

url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&begin_date={begin_date}&end_date={end_date}&api-key={key}"
response = requests.get(url)
```

*Getting Paginated Results*:

```python
results = []

for page in range(0, 5):
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&begin_date={begin_date}&end_date={end_date}&page={page}&api-key={key}"
    response = requests.get(url)

    if response.ok:
        parsed = response.json()
        articles = parsed["response"]["docs"]
        results.append(articles)
    else:
        print("page", page, "failed with status code", response.status_code)

    sleep(12)
```

### In-class coding challenge

1. Search for APIs related to your final project and list them in a markdown cell (if any! if there are none, make note of this, but try to find some resources that are adjacent to your project. If there are no directly related APIs, this may be a strong case for web scraping which we will cover in the coming weeks)

2. Find a website (or set of websites) that contains information related to your topic that you could build a dataset from by scraping, which we will explore next week.

3. Use the MET API to assemble a new list of dictionaries containing only items that relate to a specific **animal**, **person**, **place**. This doesn't have to be comprehensive, as you may end up with thousands of items, so make a list that has at least 5 items in it.

*4. Use the NYTimes API to search for articles related to your final project research topic within a specific time period. Assemble all of the **abstract** data into a new list. You will search for specific "terms" in the data that are relevant – for instance `"A.I."`, counting how many abstracts contain the term. **For** each abstract in the list, you will determine **if** there is a match within the string, in which case you will **add 1** to the count. Conclude with an f-string that reads `"The term {search_term} appears {count} times in the abstracts"`.* (pushed to next week! optional homework for this week.)
