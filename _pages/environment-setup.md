---
layout: page
title: Environment Setup
permalink: /environment-setup/
---

## Environment Setup

The examples so far have run right in the browser. Once we get into CSV
parsing, JSON, working with APIs, and scraping with BeautifulSoup, we'll
need a real local Python environment instead — this page covers getting
that set up once, ahead of time.

### Installing Anaconda from the command line

[Anaconda](https://www.anaconda.com/download) is a Python distribution
that bundles the interpreter, common data science packages, and `conda`,
a tool for managing isolated environments.

1. Download the command-line installer for your OS from
   [anaconda.com/download](https://www.anaconda.com/download) (choose the
   "Command Line Installer," not the graphical one). You can skip the registration prompt if it shows up.
2. Follow the instructions for a Command Line installation (CLI) for your operating system.

3. Close and reopen your terminal so the changes take effect, then
   confirm the install worked:

   ```bash
   conda --version
   ```

   This should print a version number, like `conda 24.x.x`.

### Creating the "INFO-664" environment in your repo folder

By now you should have used GitHub Desktop to clone the course repo,
**INFO-664**, to somewhere on your computer. We'll create the conda
environment from inside that same folder, so open a terminal (macOS/Linux)
or Anaconda Prompt (Windows) and navigate to it:

```bash
cd path/to/your/INFO-664
```

A conda **environment** is an isolated Python installation with its own
packages, so work in one project can't accidentally break another. Create
one named to match the repo, `INFO-664`:

```bash
conda create --name INFO-664 python=3.12
```

Type `y` when prompted to confirm. Then activate it:

```bash
conda activate INFO-664
```

Your terminal prompt should now show `(INFO-664)` at the start of the
line, confirming the environment is active. From here on, any `python`,
`conda install`, or `pip install` command run in this terminal applies
only to the `INFO-664` environment.

### Installing the libraries we'll need

With `INFO-664` activated, install everything in one go:

```bash
conda install jupyterlab numpy pandas bs4
```

Type `y` when prompted to confirm. That installs:

- **jupyterlab** — the notebook interface we'll use to follow along
- **numpy** — numerical arrays and math operations
- **pandas** — tabular data (reading CSVs, working with rows/columns)
- **bs4** (Beautiful Soup) — parsing HTML for web scraping

### Add a `.gitignore`

While you're set up, add a `.gitignore` to the repo so environment junk
and notebook checkpoint files never get committed. In your `INFO-664`
folder, create a plain text file named `.gitignore` (GitHub Desktop will
pick it up automatically once it exists) containing:

```
.ipynb_checkpoints/
__pycache__/
.DS_Store
```

You don't need to ignore a `.venv` folder here, since conda environments
live outside the repo by default — but double-check with `conda env list`
that `INFO-664` isn't sitting inside your repo folder.

### Using JupyterLab to follow along

Once it finishes installing, launch JupyterLab from within the activated
environment — make sure you're still `cd`'d into your `INFO-664` repo
folder first, so JupyterLab opens rooted there:

```bash
jupyter lab
```

This opens JupyterLab in your browser, pointed at whatever directory you
ran the command from.

**Create a notebook.** In JupyterLab, go to File → New → Notebook, (or select the New Python3 Notebook option from the launcher as pictured) and
pick the Python 3 kernel when prompted. This gives you a new `.ipynb`
file with a single empty cell.

![Creating a new notebook in JupyterLab](../assets/images/newnotebook.png)

**Cells are the unit of work.** A notebook is a stack of cells you write
and run one at a time, in whatever order you like. There are two kinds:

- **Code cells** — Python code. Run one with **Shift+Enter** (runs the
  cell and moves to/creates the next one) or **Ctrl+Enter** (runs it in
  place, without moving on).
- **Markdown cells** — plain-text notes, headers, etc. Turn the current
  cell into one with `Esc` then `M`. These are formatted using Markdown syntax, which you can learn about [here](https://www.markdownguide.org/cheat-sheet/).

![Editing cells in JupyterLab](../assets/images/editing.png)

**Write and run each example as its own cell.** Type a line of code (say,
`print("Hello, world!")`) into a cell and run it (shift or ctrl and enter)— the output appears
directly underneath that same cell. Move to the next cell for the next
example, and so on down the notebook.

**Save your work.** Ctrl+S saves the notebook file, including whatever
output is currently displayed under each cell.

### Organizing your repo for weekly notebooks

Once the environment is working, it's worth settling on a consistent
place to put each week's notebook so your `INFO-664` repo stays easy to
navigate (and easy to grade) all semester.

**Suggested structure:**

```
INFO-664/
├── .gitignore
├── notebooks/
│   ├── week01/
│   │   └── week01.ipynb
│   ├── week02/
│   │   └── week02.ipynb
│   └── template.ipynb       (starter notebook, copied each week)
└── data/
    └── (any local datasets, or a README noting where to download them)
```

A flat `notebooks/week01.ipynb`, `notebooks/week02.ipynb`, ... pattern
works fine too — pick one convention and keep it all semester.

**A starter template worth creating once (`notebooks/template.ipynb`):**

First cell (Markdown):
```markdown
# Week __ — [Topic]
**Name:**
**Date:**

## Goals for this notebook
-
```

Second cell (code) — a standard imports block so every week starts the
same way:
```python
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
```

Duplicating this template each week means every notebook in the repo
looks the same at a glance, which makes review and grading much faster.

**Weekly routine:**

1. **Open GitHub Desktop**, make sure you're on the `INFO-664` repo
   (top-left repo switcher), and click **Fetch origin** / **Pull origin**
   to get any updated course materials.
2. **Launch JupyterLab from the command line**: open Anaconda Prompt
   (Windows) or Terminal (macOS/Linux), `cd` into your `INFO-664` folder
   if you're not already there, then run:
   ```bash
   conda activate INFO-664
   jupyter lab
   ```
3. In JupyterLab's file browser, navigate into the repo's `notebooks/`
   folder.
4. **Create this week's notebook by duplicating the template**:
   right-click `template.ipynb` → Duplicate → rename the copy to, e.g.,
   `week03.ipynb` (move it into a `week03/` subfolder first if you're
   using that structure).
5. **Fill in the header cell** at the top (week number, date, topic).
6. **Do the week's work** — code cells, Markdown notes explaining your
   thinking as you go.
7. **Before your final save, do a clean run**: Kernel menu → "Restart
   Kernel and Run All Cells." This catches the common mistake of a
   notebook that only works because of leftover state from cells run out
   of order.
8. **Save the notebook** (Ctrl/Cmd+S).
9. **Switch to GitHub Desktop.** Your new/changed notebook will already
   be listed under the **Changes** tab, checked by default.
10. **Write a commit message** (e.g. "Week 3: pandas groupby and
    aggregation") and click **Commit to main**.
11. Click **Push origin** to send your commit to GitHub.

**A couple of things worth considering:**

- **Consistent naming** (`week03.ipynb`, not `week3_FINAL_v2.ipynb`)
- **One notebook per week**, not one giant notebook.
