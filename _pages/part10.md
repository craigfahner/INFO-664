---
layout: page
title: Part 10
permalink: /part10/
---

## Part 10: APIs

In [Part 7](../part7/) and [Part 9](../part9/) we worked with data that was
already sitting in a file on our own computer. Plenty of data lives
somewhere else: on a museum's, library's, or archive's server. An **API**
(application programming interface) is a way for a program to ask a server
for exactly the data it wants and get the answer back, usually as JSON,
like the UNESCO file in Part 9. Instead of downloading a whole dataset
and searching through it ourselves, we can send a request like "find every
object that matches *antelope*" and let the server do the searching.

This part uses the Metropolitan Museum of Art's
[Collection API](https://metmuseum.github.io/). The API is free, and you don't need an
account or a key to use it. (The Met does ask that you keep to 80 requests
per second or fewer, which is worth remembering once we start making
requests in a loop.)

### Assembling a request

An API request is a web address, the same kind you'd type into a browser.
It helps to build it out of named pieces:

```python
import requests

base_url = "https://collectionapi.metmuseum.org"
search_path = "/public/collection/v1.1/search"
search_query = "?q=Antelope"
```

- **`base_url`** is the address of the server.
- **`search_path`** says which service on that server we want. This one is
  the *search* service, and `/public/collection/v1.1` is the API's own name
  and version number.
- **`search_query`** is where we say what we're searching for. The `?`
  marks the start of the query, `q` is the name of the setting (short for
  "query"), and `Antelope` is the value we're giving it. More settings can
  be added after it, separated by `&`.

Putting the three together with an f-string (from [Part 2](../part2/))
gives the full address:

```python
url = f'{base_url}{search_path}{search_query}'
search_response = requests.get(url)

print(url)   # https://collectionapi.metmuseum.org/public/collection/v1.1/search?q=Antelope
```

`requests.get(url)` sends the request, the same as typing that address into
a browser and pressing return. The server's answer is stored in
`search_response`. (Try pasting the printed address into a browser tab to
see what the server sends back.)

`requests` is the one library in this course that doesn't come with Python.
If `import requests` gives you a `ModuleNotFoundError` in a notebook, install it
by running `%pip install requests` in a cell, then try again. The editors on
this page already have it, and each time you press Run, they send a real
request to the Met's server, so they may take a second or two.

<script type="py-editor" config='{"packages": ["requests", "pyodide-http"]}'>
import requests

base_url = "https://collectionapi.metmuseum.org"
search_path = "/public/collection/v1.1/search"
search_query = "?q=Antelope"

url = f'{base_url}{search_path}{search_query}'
search_response = requests.get(url)

print(url)
</script>

### What did we get back?

`search_response` isn't the list of search results yet. Let's ask Python
what it is, with `type()` (from [Part 1](../part1/)):

```python
print(type(search_response))
```

```text
<class 'requests.models.Response'>
```

(In a Jupyter notebook, the last line of a cell is displayed automatically,
so `type(search_response)` on its own, without `print()`, shows the same
thing as `requests.models.Response`. The examples on this page use
`print()` throughout, so they work the same in the editors.)

It's a `Response` object: a package holding everything the server sent
back, including the data itself, plus information *about* the reply.

**`dir()`.** To see what's inside such an object, use `dir()`. It returns a
list of the names of everything attached to the object, meaning all the
values it holds and all the actions (methods, like `.split()` on a string)
we can run on it:

```python
print(dir(search_response))
```

```text
['__annotations__', '__attrs__', '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_content', '_content_consumed', '_next', 'apparent_encoding', 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']
```

(The exact list can differ a little between versions of Python and
`requests`.) That's a long list, because most of the names start with an
underscore. Those are Python's own internal machinery, and we can ignore
them. Filtering them out uses the filter-and-append pattern from earlier,
with a string index (from [Part 2](../part2/)) to test whether the first
character of each name is an underscore:

```python
public_names = []

for name in dir(search_response):
    if name[0] != "_":
        public_names.append(name)

print(public_names)
```

```text
['apparent_encoding', 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']
```

That's the real menu of things we can do with a response. The ones we'll
use in this part:

| Name | What it is |
| --- | --- |
| `ok` | `True` if the request succeeded |
| `status_code` | a number describing the result of the request (200 means success) |
| `headers` | a dictionary of extra information about the reply, like its format |
| `text` | the data the server sent, as one long string |
| `json()` | a **method** (note the parentheses): converts the data into Python lists and dictionaries |

<script type="py-editor" config='{"packages": ["requests", "pyodide-http"]}'>
import requests

base_url = "https://collectionapi.metmuseum.org"
search_path = "/public/collection/v1.1/search"
search_query = "?q=Antelope"

url = f'{base_url}{search_path}{search_query}'
search_response = requests.get(url)

print(type(search_response))

public_names = []

for name in dir(search_response):
    if name[0] != "_":
        public_names.append(name)

print(public_names)
</script>

`dir()` works on any Python object, by the way. Try `print(dir("hello"))`
to see the string methods from Part 2, like `upper` and `split`, in the
list.

### Checking that the data arrived

Before using a response, check that the request actually worked.
`.ok` is the quickest check:

```python
print(search_response.ok)
```

```text
True
```

`True` means the server received our request and sent back what we asked
for. Behind it is the **status code**, a standard number every web server
uses to report how a request went:

```python
print(search_response.status_code)
```

```text
200
```

| Status code | Meaning |
| --- | --- |
| `200` | OK: success |
| `404` | Not Found: no such address |
| `403` | Forbidden: you aren't allowed to ask for that |
| `429` | Too Many Requests: slow down |
| `500` | Server Error: the problem is on their end |

`.ok` is `True` for any success code (anything below 400), and `False`
otherwise. To see what a failure looks like, ask for a service that
doesn't exist:

```python
missing = requests.get(base_url + "/public/collection/v1.1/nothing")

print(missing.ok)            # False
print(missing.status_code)   # 404
```

This is worth building into your code with an `if`
(from [Part 5](../part5/)). A request can come back unsuccessful for
reasons that have nothing to do with your code, such as a typo in the
address, too many requests too quickly, or a problem on the server's end.
Python doesn't stop with an error when that happens. It hands you a
response whose `.ok` is `False`, and it's up to your code to check:

```python
if search_response.ok:
    print("Data received!")
else:
    print("Something went wrong:", search_response.status_code)
```

Two more things on the response confirm what arrived. The `headers`
dictionary says what *kind* of data it is, and `text` holds the data
itself:

```python
print(search_response.headers["Content-Type"])   # application/json
print(search_response.text[:60])                 # the first 60 characters of the data
```

```text
application/json
{"total":288,"objectIDs":[544070,488255,316188,844668,324030
```

`application/json` confirms that the data is JSON, the format from
[Part 9](../part9/). And the first 60 characters of `text` show that
it looks like a Python dictionary: a `total`, and a list called
`objectIDs`. But `text` is just a single long *string* (check with
`type(search_response.text)`), so we can't look things up in it by key yet.

<script type="py-editor" config='{"packages": ["requests", "pyodide-http"]}'>
import requests

base_url = "https://collectionapi.metmuseum.org"
search_path = "/public/collection/v1.1/search"
search_query = "?q=Antelope"

url = f'{base_url}{search_path}{search_query}'
search_response = requests.get(url)

print(search_response.ok)
print(search_response.status_code)

missing = requests.get(base_url + "/public/collection/v1.1/nothing")

print(missing.ok)
print(missing.status_code)

if search_response.ok:
    print("Data received!")
else:
    print("Something went wrong:", search_response.status_code)

print(search_response.headers["Content-Type"])
print(search_response.text[:60])
print(type(search_response.text))
</script>

### Parsing the response as JSON

The `json()` method converts the string into real Python data, the same
way `json.load()` did for a file in Part 9:

```python
parsed_json_data = search_response.json()

print(type(parsed_json_data))
```

```text
<class 'dict'>
```

It's a dictionary now, so everything from [Part 3](../part3/) applies. And
since it's a different kind of object from the response, `dir()` shows a
different menu:

```python
print(dir(parsed_json_data))
```

```text
['__class__', '__class_getitem__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__ior__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__or__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__ror__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']
```

Ignoring the underscore names again, what's left is the list of dictionary
methods: `get` and `items` (both from earlier parts), `keys`, `values`,
`pop`, `update`, and so on. This is the same toolbox as any other
dictionary. `.keys()` shows which keys this one has:

```python
print(parsed_json_data.keys())
```

```text
dict_keys(['total', 'objectIDs'])
```

Printing the whole dictionary shows what's behind those two keys:

```python
print(parsed_json_data)
```

```text
{'total': 288, 'objectIDs': [544070, 488255, 316188, 844668, 324030, 316653, 312229, 310284, 21465, 314371, 309875, 255403, 546611, 312228, 310374, ... 
```

(Trimmed here: the real output goes on for 100 ID numbers.)

- **`total`** is how many objects in the Met's collection matched the
  search: here, 288.
- **`objectIDs`** is a list of ID numbers for those objects. We can count
  them with `len(parsed_json_data["objectIDs"])`, which gives `100`.
  When a search has more matches than that, only the first *page* of
  100 comes back by default. (The API's `limit` and `offset` settings
  control the page size and which page you get. Adding `&limit=10` to the
  query would ask for 10 at a time. We'll use both of them at the end of
  this section to collect every result.)

The numbers here come from the Met's live collection, so what you see may
differ a little from this page. The order of the IDs can shift slightly
from one request to the next, too.

<script type="py-editor" config='{"packages": ["requests", "pyodide-http"]}'>
import requests

base_url = "https://collectionapi.metmuseum.org"
search_path = "/public/collection/v1.1/search"
search_query = "?q=Antelope"

url = f'{base_url}{search_path}{search_query}'
search_response = requests.get(url)

parsed_json_data = search_response.json()

print(type(parsed_json_data))
print(parsed_json_data.keys())
print(parsed_json_data["total"])
print(len(parsed_json_data["objectIDs"]))
print(parsed_json_data)
</script>

### Picking items from the results

`parsed_json_data["objectIDs"]` is an ordinary list, so indexing works as
it did in [Part 3](../part3/). Index `0` is the first item found:

```python
first_found_item = parsed_json_data["objectIDs"][0]

print(first_found_item)
```

```text
544070
```

To see the first 10 instead, use a slice (see [Part 2](../part2/) and
[Part 7](../part7/)):

```python
first_ten = parsed_json_data["objectIDs"][:10]

print(first_ten)
```

```text
[544070, 488255, 316188, 844668, 324030, 316653, 312229, 310284, 21465, 314371]
```

### Getting the details for one object

These are just ID numbers: each one identifies a single object in the
Met's collection. To get an object's details, we make a **second request**
to a different service of the API, the *objects* service, with the ID at
the end of the address. It takes the same steps as the first request: build
the address, send it, and check the result.

```python
# now we use another API endpoint for object data rather than search results
object_path = "/public/collection/v1/objects/"
url = f"{base_url}{object_path}{first_found_item}"

response_object = requests.get(url)
```

This reuses the `base_url` from before and the `first_found_item` we picked
out of the search results. Note that the objects service is still under
`/v1/` in its path, not `/v1.1/` like the search. (Each service of an API
can have its own version.) The `url` variable now holds the new address,
replacing the search one, which is fine since we're done with it.

Just like before, we confirm that the request worked before going further.
Printing the response object itself shows its status code in angle
brackets:

```python
print(response_object)   # confirm it's good (response code 200)
```

```text
<Response [200]>
```

`[200]` is the success code from the table above. Then `.json()` converts
this reply into a dictionary, as before:

```python
object_json_data = response_object.json()

print(object_json_data)
```

The result is one long dictionary, with more than fifty keys describing the
object.
This is the start of it:

```text
{'objectID': 544070, 'isHighlight': True, 'accessionNumber': '1992.55', 'accessionYear': '1992', 'isPublicDomain': True, 'primaryImage': 'https://images.metmuseum.org/CRDImages/eg/original/DT6857.jpg', ... 'department': 'Egyptian Art', 'objectName': 'Head, antelope', 'title': 'Antelope Head', ... 'objectDate': '525–404 BCE', ... 'medium': 'Greywacke, travertine (Egyptian alabaster), agate', ...
```

(Trimmed. The full output goes on to include the dimensions, credit line,
find location, tags, and a link to the object's page on the Met's website.)
It's a dictionary, so we can pick out any of the keys we can see in
the printout, and use them in an f-string (from [Part 2](../part2/)):

```python
title = object_json_data["title"]
date = object_json_data["objectDate"]
department = object_json_data["department"]

print(f"{title} ({date}) is in the Met's {department} department")
```

```text
Antelope Head (525–404 BCE) is in the Met's Egyptian Art department
```

<script type="py-editor" config='{"packages": ["requests", "pyodide-http"]}'>
import requests

base_url = "https://collectionapi.metmuseum.org"
search_path = "/public/collection/v1.1/search"
search_query = "?q=Antelope"

url = f'{base_url}{search_path}{search_query}'
search_response = requests.get(url)

parsed_json_data = search_response.json()
first_found_item = parsed_json_data["objectIDs"][0]

# now we use another API endpoint for object data rather than search results
object_path = "/public/collection/v1/objects/"
url = f"{base_url}{object_path}{first_found_item}"

response_object = requests.get(url)
print(response_object)

object_json_data = response_object.json()
print(len(object_json_data))

title = object_json_data["title"]
date = object_json_data["objectDate"]
department = object_json_data["department"]

print(f"{title} ({date}) is in the Met's {department} department")
</script>

Try changing `"?q=Antelope"` to another search term, like `"?q=cat"` or
`"?q=sunflowers"`, and run it again to see how `total` and the first object
change. (If a search finds nothing, `total` is `0` and `objectIDs` is
`None` instead of a list, so trying to index it with `[0]` raises a
`TypeError`.)

### Getting every result: pagination

So far we've seen only the first page of the Antelope search: 100 IDs,
even though `total` says there are 288 matches. The Met's search service
(version `v1.1`, which is the version in our path) returns its results one
**page** at a time, and two settings in the query control which page we get:

- **`limit`** is how many IDs to return per page. It defaults to 100, and
  the largest value allowed is 500.
- **`offset`** is how many results to skip before the page starts. It
  defaults to 0, which means "start at the first result."

Here they are by hand, asking for five IDs at a time. Page one starts at
offset `0`, and page two skips the first five results, so it starts at
offset `5`:

```python
url = f"{base_url}{search_path}{search_query}&limit=5&offset=0"
page_one = requests.get(url).json()

url = f"{base_url}{search_path}{search_query}&limit=5&offset=5"
page_two = requests.get(url).json()

print(page_one["objectIDs"])
print(page_two["objectIDs"])
```

```text
[544070, 488255, 316188, 844668, 324030]
[316653, 312229, 310284, 21465, 314371]
```

The two lists pick up where the other left off, and together they are the
first ten IDs we printed earlier. Now we need to automate this: make one
request per page, and combine all the pages into a single list of IDs.
The plan:

1. Request the first page. Its `total` tells us how many results there are
   in all, so we know how many more pages to ask for.
2. Loop over the offsets of the remaining pages, requesting each one.
3. Add each page's IDs onto the end of one big list.

**Counting offsets with `range()`.** The offsets of the remaining pages
are 100, 200, and so on, up to the total. Python's `range()` function
generates a sequence of numbers like that. Given three values,
`range(start, stop, step)` counts from `start` up to (but not including)
`stop`, adding `step` each time. Wrapping it in `list()` (from
[Part 7](../part7/)) lets us see the numbers it makes:

```python
print(list(range(100, 288, 100)))
```

```text
[100, 200]
```

Counting from 100 in steps of 100 and stopping before 288 gives the two
offsets we still need: page two starts at 100, and page three at 200.

**Combining lists with `.extend()`.** There are two ways to add a list's
contents to another list, and they give different results:

```python
a = [1, 2]
a.append([3, 4])
print(a)   # [1, 2, [3, 4]]

b = [1, 2]
b.extend([3, 4])
print(b)   # [1, 2, 3, 4]
```

`.append()` (from [Part 3](../part3/)) adds its argument as *one* item, so
appending a list nests it inside the other. `.extend()` adds each item of
the list separately, which is the behavior we want here: one flat list of
IDs.

Now all three pieces together:

```python
limit = 100

url = f"{base_url}{search_path}{search_query}&limit={limit}&offset=0"
first_response = requests.get(url)
first_page = first_response.json()

total = first_page["total"]
all_ids = first_page["objectIDs"]

for offset in range(limit, total, limit):
    url = f"{base_url}{search_path}{search_query}&limit={limit}&offset={offset}"
    response = requests.get(url)

    if response.ok:
        page = response.json()
        all_ids.extend(page["objectIDs"])
    else:
        print("offset", offset, "failed with status code", response.status_code)

print(total)
print(len(all_ids))
print(all_ids[:5])
```

```text
288
288
[544070, 488255, 316188, 844668, 324030]
```

`all_ids` now holds the IDs from all three pages, 288 of them, matching the
`total` the API reported. The `if response.ok` check from earlier guards
each request. Using `limit` as a variable means the page size is only
written once, in the first request, and the loop uses it for both the step
and the address.

The loop made only 3 requests in all (one before it, and two inside it), so
there's no need to slow it down: the Met asks for no more than 80 requests
per second. Since `limit` can be as high as 500, a search this small could
have been fetched in a single request with `&limit=500`. Paging matters
when there are more results than one page can hold, so try the code with
a bigger search, like `"?q=cat"`, which has well over a thousand matches.

One more limit to know about: the API's documentation says `offset` plus
`limit` can't add up to more than 10,000, so a very broad search (like
`"?q=gold"`, with tens of thousands of matches) can't be paged through to the
end. For results that large, narrow the search first, for example by adding
a department or date range, which the Met's documentation describes.

<script type="py-editor" config='{"packages": ["requests", "pyodide-http"]}'>
import requests

base_url = "https://collectionapi.metmuseum.org"
search_path = "/public/collection/v1.1/search"
search_query = "?q=Antelope"

limit = 100

url = f"{base_url}{search_path}{search_query}&limit={limit}&offset=0"
first_response = requests.get(url)
first_page = first_response.json()

total = first_page["total"]
all_ids = first_page["objectIDs"]

for offset in range(limit, total, limit):
    url = f"{base_url}{search_path}{search_query}&limit={limit}&offset={offset}"
    response = requests.get(url)

    if response.ok:
        page = response.json()
        all_ids.extend(page["objectIDs"])
    else:
        print("offset", offset, "failed with status code", response.status_code)

print(total)
print(len(all_ids))
print(all_ids[:5])
</script>

### A second API: the New York Times Article Search

The Met's API is about as simple as an API gets: no account, no key, and a
short response. Many APIs work differently. The New York Times'
**Article Search API** lets you search the Times' archive by keyword and
date, and get back the details of each matching article: its headline, abstract,
lead paragraph, web address, publication date, section, byline, and
keywords. (It returns the *metadata* about each article, not its full text.)

Compared to the Met, four things change:

- **You need an API key.** A key is a long string of letters and numbers
  that identifies who is making the requests.
- **The JSON is nested more deeply**, so we'll spend more time finding our
  way around inside it.
- **Results come in pages of 10**, and the API limits how fast you can
  request them, so getting a lot of results means making a series of
  requests, with pauses in between.
- **The archive is enormous**, so every search in this section is limited to
  a **date range**. That keeps the number of results small enough to
  collect and work with.

This section follows the `nyt_api.ipynb` notebook. Every code block here
needs your own API key, so they're meant to be run in a notebook, not in
the editors on this page. The output shown under each block was recorded from
an earlier run of the notebook, with a different search window, so the
particular articles, dates, and counts you get will be different. The
structure of the data will be the same.

#### Getting an API key

1. Go to [developer.nytimes.com](https://developer.nytimes.com/) and create
   an account (it's free).
2. Create a new **app**. This is the project the key will belong to.
3. In the app's settings, enable the **Article Search API**. If this step
   is skipped, your requests will be rejected even with a valid key.
4. Copy the key the site gives you.

A key works like a password, so **don't paste it into a notebook that you
will commit to GitHub.** Public repositories are scanned by bots looking for
exactly this, and a leaked key can be used by somebody else, using up your
daily limit or worse. A safer way to enter it is `getpass`, a function that
prompts for the key, hides what you type, and keeps the key in memory only
for as long as the notebook is running. (If a key ever does end up
somewhere public, delete it on the NYT developer site and create a new one.)

```python
import requests
from getpass import getpass
from time import sleep

key = getpass("Paste your NYT API key: ")
```

The two new imports use a different form from the `import csv` we've seen:
`from time import sleep` brings in just the one function we want from the
`time` module, so we can write `sleep(...)` instead of `time.sleep(...)`.

#### Making a request with a key

The key goes into the address itself, as one more setting in the query. So
do the other things we're asking for. The settings are joined with `&`:

- **`q`** is the search term.
- **`begin_date`** and **`end_date`** limit the search to articles published
  between those two days, inclusive. Dates are written as `YYYYMMDD`, with no
  dashes, so September 1, 2026 is `20260901`.
- **`api-key`** is the key.

Without a date range, the API searches the Times' entire archive, which goes
back more than a century, and a common word can match tens of thousands of
articles. At 10 results per request and a limit of 500 requests a day, we
could never collect them all, so we'll always include a date range. For these
examples, we'll use the last month: all of September 2026.

```python
query = "migrant"

begin_date = "20260901"
end_date = "20260930"

url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&begin_date={begin_date}&end_date={end_date}&api-key={key}"
response = requests.get(url)
```

Because the key is now part of `url` (and also part of `response.url`),
**don't `print(url)`** or share the output of a cell that shows it.

Everything from the Met example about checking a response applies here
too: it's the same kind of `Response` object, with the same `.ok`,
`.status_code`, `.json()` and the rest of the `dir()` list. Printing the
response itself shows its status code:

```python
print(response)
```

```text
<Response [200]>
```

If you get a different code, it's one from the table earlier in this part.
Two are especially common with this API: `401` means the key is missing,
mistyped, or the Article Search API isn't enabled for it, and `429` means
you've made too many requests too quickly.

#### Exploring the nested JSON

Convert the response into Python data, then look at what's in it. With a
structure this deep, the trick is to go one level at a time, asking `type()`
or `.keys()` at each step to find out what you're looking at:

```python
parsed = response.json()

print(parsed.keys())
```

```text
dict_keys(['status', 'copyright', 'response'])
```

The article data we want is under `response`, so we go one level deeper:

```python
print(parsed["response"].keys())
```

```text
dict_keys(['docs', 'meta'])
```

Two keys: `metadata` and `docs`. Let's look at `metadata` first, which is information
about the search itself:

```python
print(parsed["response"]["metadata"])
```

```text
{'hits': 32616, 'offset': 0, 'time': 82}
```

`hits` is the number of articles that matched the search within our date
range. (Yours will be different, since it depends on your search term and
dates.) `docs` is where
the articles are. Is it a dictionary, or a list?

```python
print(type(parsed["response"]["docs"]))
```

```text
<class 'list'>
```

A list, so we can index into it and count it. The data in `docs` is huge,
so rather than printing all of it, let's save it into a variable and look at
just the first item:

```python
articles = parsed["response"]["docs"]

print(len(articles))
print(articles[0].keys())
```

```text
10
dict_keys(['abstract', 'web_url', 'snippet', 'lead_paragraph', 'print_section', 'print_page', 'source', 'multimedia', 'headline', 'keywords', 'pub_date', 'document_type', 'news_desk', 'section_name', 'subsection_name', 'byline', 'type_of_material', '_id', 'word_count', 'uri'])
```

So `articles` is a list of 10 articles, and each article is a dictionary with
20 keys. Here is the first one, with the long `multimedia` list (75 image
entries, in this case) left out:

```text
{'abstract': 'There has been a dramatic drop in the number of people gathering at the U.S. border and trying to cross. Can it help Mexico stave off President Trump’s threatened tariffs?',
 'web_url': 'https://www.nytimes.com/2025/03/03/world/americas/mexico-border-migration-trump-tariffs-deadline.html',
 'snippet': 'There has been a dramatic drop in the number of people gathering at the U.S. border and trying to cross. Can it help Mexico stave off President Trump’s threatened tariffs?',
 'lead_paragraph': 'On the eve of President Trump’s deadline to impose tariffs on Mexico, one thing is hard to miss on the Mexican side of the border: The migrants are gone.',
 'print_section': 'A',
 'print_page': '4',
 'source': 'The New York Times',
 'multimedia': [ ... ],
 'headline': {'main': 'On Mexico’s Once-Packed Border, Few Migrants Remain', 'kicker': None, 'content_kicker': None, 'print_headline': 'On a Once-Packed Border,  Just a Few Migrants Remain', 'name': None, 'seo': None, 'sub': None},
 'keywords': [{'name': 'subject', 'value': 'United States International Relations', 'rank': 1, 'major': 'N'}, {'name': 'subject', 'value': 'Illegal Immigration', 'rank': 2, 'major': 'N'}, ... ],
 'pub_date': '2025-03-03T14:00:34+0000',
 'document_type': 'article',
 'news_desk': 'Foreign',
 'section_name': 'World',
 'subsection_name': 'Americas',
 'byline': {'original': 'By Annie Correal and Alejandro Cegarra', 'person': [{'firstname': 'Annie', 'middlename': None, 'lastname': 'Correal', ...}, {'firstname': 'Alejandro', 'middlename': None, 'lastname': 'Cegarra', ...}], 'organization': None},
 'type_of_material': 'News',
 '_id': 'nyt://article/5a74da49-82a5-5147-ae1f-58f9c66437f0',
 'word_count': 1595,
 'uri': 'nyt://article/5a74da49-82a5-5147-ae1f-58f9c66437f0'}
```

#### Reaching a value inside the nesting

Reading that printout, you can see all three kinds of nesting from
[Part 3](../part3/) at once: some values are plain strings (`abstract`),
some are dictionaries (`headline`, `byline`), and some are lists of
dictionaries (`keywords`). To reach a value, write out the path to it, one
`[ ]` per level, from the outside in:

```python
article = articles[0]

print(article["abstract"])
print(article["headline"]["main"])
print(article["byline"]["original"])
```

```text
There has been a dramatic drop in the number of people gathering at the U.S. border and trying to cross. Can it help Mexico stave off President Trump’s threatened tariffs?
On Mexico’s Once-Packed Border, Few Migrants Remain
By Annie Correal and Alejandro Cegarra
```

`article["headline"]["main"]` reads as "the `headline` of the article, and
then the `main` part of that." Going deeper works the same way. The
`byline` has a `person` key, which is a *list* with one dictionary per
author, so the first author's first and last names are:

```python
print(article["byline"]["person"][0]["firstname"])   # Annie
print(article["byline"]["person"][0]["lastname"])    # Correal
```

That path alternates between the three kinds of lookup: a dictionary key
(`"byline"`), another key (`"person"`), a list index (`[0]`), and then a
key again (`"firstname"`). If you're ever unsure which kind of thing you're
looking at, `type()` will tell you, and `.keys()` or `len()` will tell you
what's inside.

The `pub_date` is a timestamp, `2025-03-03T14:00:34+0000`. To keep just the
date, we can slice the first 10 characters (from [Part 2](../part2/)), or,
if you prefer, pull the date out with a regular expression from
[Part 9](../part9/):

```python
import re

print(article["pub_date"][:10])                                      # 2025-03-03
print(re.search(r"\d{4}-\d{2}-\d{2}", article["pub_date"]).group())   # 2025-03-03
```

Putting a few pieces into an f-string:

```python
headline = article["headline"]["main"]
byline = article["byline"]["original"]
date = article["pub_date"][:10]

print(f"{headline} ({byline}, {date})")
```

```text
On Mexico’s Once-Packed Border, Few Migrants Remain (By Annie Correal and Alejandro Cegarra, 2025-03-03)
```

**Try it yourself.** Explore some of the other keys in `article`. `keywords`,
`section_name`, and `word_count` are all worth a look, and `keywords` is
nested too: how would you get the `value` of the first keyword?

#### Getting more than 10 results

We have 10 articles, because the API only returns 10 results at a time.
To get the next ones, we ask for another **page**, by adding `&page=` to the
address. Page `0` is the first page, page `1` is the second, and so on.

To get several pages, we make the request in a loop, as we did with the
Met. `range(0, 5)` produces the numbers `0, 1, 2, 3, 4`, so the loop runs
five times, once for each page. (The number it stops at is not included, the
same way the end of a slice isn't.) Each pass does what we did by hand
above:

- build the address, with the page number in it, along with the search term
  and the same date range as before
- make the request and save the response
- check that it worked, parse it, and pull out the `docs`
- add that page of articles to a list

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

The `sleep(12)` at the end of each pass makes Python wait 12 seconds before
the next request. The NYT limits each key to about 5 requests per minute
(and 500 per day), and a loop can fire requests much faster than that. Without
the pause, the server would start answering with `429 Too Many Requests`
errors, which is why the loop checks `response.ok` before using a response.
This loop takes about a minute to run, and if you run other requests in the
same minute, count them too.

Each pass added one list of 10 articles to `results` with `.append()`, so
in the end we have a list of 5 lists. (That's the `.append()` behavior from
the Met pagination example: the whole page goes in as one item. We use it here
on purpose, to keep each page separate.)

```python
print(type(results))
print(len(results))
print(len(results[0]))
print(type(results[0][0]))
```

```text
<class 'list'>
5
10
<class 'dict'>
```

That's a dictionary, inside a list (the page), inside another list
(`results`). To get the first article's abstract, index once for the
page, once for the article, and then use the key:

```python
print(results[0][0]["abstract"])
```

```text
There has been a dramatic drop in the number of people gathering at the U.S. border and trying to cross. Can it help Mexico stave off President Trump’s threatened tariffs?
```

#### Looping through every article

To work with all 50 articles, we need a loop inside a loop: the outer one
steps through the pages, and the inner one steps through the articles on each
page (the same shape as the Beatles albums and tracks in
[Part 5](../part5/)):

```python
for result in results:           # each page
    for article in result:       # each article on that page
        print(article["abstract"])
```

```text
There has been a dramatic drop in the number of people gathering at the U.S. border and trying to cross. Can it help Mexico stave off President Trump’s threatened tariffs?
The new case, which for now is asking for a court to block the transfer of 10 men to the offshore base, is the first to directly challenge the policy.
The missing people were on two boats that capsized off Yemen, which is on a major route for migrants trying to reach Gulf countries for work.
...
```

(Fifty lines in all; only the first three are shown here.) Printing is fine
for a look, but usually we want to *keep* the pieces we're interested in.
The same nested loop can collect them into lists, with the filter-and-append
pattern from earlier, this time picking out three details from every
article: the abstract, the publication date, and the first keyword (the
`value` of the first dictionary in the `keywords` list):

```python
abstracts = []
dates = []
keywords = []

for result in results:
    for article in result:
        abstracts.append(article["abstract"])
        dates.append(article["pub_date"])
        keywords.append(article["keywords"][0]["value"])

print(len(abstracts))
print(dates[:3])
print(keywords[:3])
```

```text
50
['2025-03-03T14:00:34+0000', '2025-03-01T19:34:05+0000', '2025-03-07T12:33:25+0000']
['United States International Relations', 'Guantanamo Bay Naval Base (Cuba)', 'Drownings']
```

Three parallel lists, each with 50 items, where item `0` of each list
describes the same article. One caution: `article["keywords"][0]` assumes
every article has at least one keyword. If one doesn't, `keywords` is an
empty list and `[0]` raises an `IndexError`, so with a bigger search it's
worth checking `if len(article["keywords"]) > 0` first.

#### Saving the results as a CSV

To take this data out of Python, we can write it to a CSV file with
`DictWriter`, as in the first section of [Part 9](../part9/). Each article
becomes one dictionary with the three details as keys, collected in a list
of rows:

```python
import csv

rows = []

for result in results:
    for article in result:
        rows.append({
            "date": article["pub_date"],
            "abstract": article["abstract"],
            "keyword": article["keywords"][0]["value"],
        })

with open("nyt_data.csv", "w", encoding="utf-8") as file:
    writer = csv.DictWriter(file, rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
```

This creates `nyt_data.csv` next to your notebook, with a header row and 50
rows. The abstracts contain commas and quotation marks, so the writer wraps
them in quotes, the same way the quoted `ArtistBio` values looked in
[Part 7](../part7/).

#### Getting the articles from one day

The examples so far searched a whole month. The same `begin_date` and
`end_date` settings can zoom in much further: if we set both of them to the
*same* day, we get only the articles from that one day. October 5, 2026 is
`20261005`.

This example also leaves out the `q=` search term, which means "everything",
and adds `sort=newest` so the most recent articles come first. It's the
paging loop from the last section, building one flat list of articles with
`.extend()` (the same way we combined the Met's pages of IDs):

```python
day = "20261005"   # YYYYMMDD
nyt_base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

todays_articles = []

for page in range(0, 3):
    url = f"{nyt_base_url}?begin_date={day}&end_date={day}&sort=newest&page={page}&api-key={key}"
    response = requests.get(url)

    if response.ok:
        parsed = response.json()
        todays_articles.extend(parsed["response"]["docs"])
    else:
        print("page", page, "failed with status code", response.status_code)

    sleep(12)

hits = parsed["response"]["meta"]["hits"]
print(f"{hits} articles were published on {day}; we collected {len(todays_articles)} of them")

for article in todays_articles[:5]:
    time_of_day = article["pub_date"][11:16]
    print(time_of_day, "-", article["headline"]["main"])
```

This reuses the `key`, `requests`, and `sleep` from earlier in the section.
If you've restarted your notebook since then, run the cells that import them
and ask for the key again first.

- **`hits`** is the number of articles the API says were published that day,
  read from the `meta` part of the last response we received (it's the same
  on every page). A busy day has far more than the 30 articles we collect
  here: three pages of 10. The final line of output compares the two
  numbers.
- **`pub_date[11:16]`** slices the time of day out of the timestamp
  (`2026-10-05T14:00:34+0000`), using a slice from
  [Part 2](../part2/). Printing it next to each headline makes it easy to
  see when the articles were published.
- **To collect more**, raise the number in `range(0, 3)`. At 12 seconds per
  page, ten pages takes two minutes.
- **To follow the current date automatically**, use Python's `datetime`
  module. `datetime.date.today()` is today's date, and `.strftime("%Y%m%d")`
  formats it the way the API wants it:

```python
import datetime

day = datetime.date.today().strftime("%Y%m%d")
print(day)   # 20261005, if you run it on October 5, 2026
```

Two things to keep in mind. If you run this part-way through the day, you
only get the articles published *so far*, so running it again later gives a
bigger `hits` number. And the `pub_date` timestamps end in `+0000`, which
means they're in UTC. An article published in the evening in New York can
show a time that looks like the next morning, so print a few `pub_date` values
and check that the day boundaries are what you expect.

**Try it yourself.** Add `&q=` and a search term to the query to find only
the articles from that day that match it, like `&q=museum`. Or go back
to the month-long range and change `begin_date` and `end_date` to look at a
different stretch of time.

### Coding challenge

1. Use the MET API to assemble a new list of dictionaries containing only items that relate to a specific **animal**, **person**, **place**. This doesn't have to be comprehensive, as you may end up with thousands of items, so make a list that has at least 5 items in it.

2. Use the NYTimes API to search for articles related to your final project research topic within a specific time period. Assemble all of the **abstract** data into a new list. You will search for specific "terms" in the data that are relevant – for instance `"A.I."`, counting how many abstracts contain the term. **For** each abstract in the list, you will determine **if** there is a match within the string, in which case you will **add 1** to the count. Conclude with an f-string that reads `"The term {search_term} appears {count} times in the abstracts"`.