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
[Collection API](https://metmuseum.github.io/), and follows the
[`met_api.ipynb`](https://github.com/craigfahner/INFO-664/blob/main/week6/met_api.ipynb)
notebook in the week 6 folder. The API is free, and you don't need an
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
  query would ask for 10 at a time.)

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
