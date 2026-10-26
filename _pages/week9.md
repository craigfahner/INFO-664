---
layout: page
title: Week 9
permalink: /week9/
---

## Week 9 activities

* [in-class notebook: web scraping + JSON saving](https://github.com/craigfahner/INFO-664/blob/main/week9/week9.ipynb)
* [Lecture notes part 12: Pandas](https://craigfahner.github.io/INFO-664/part12/)
* [External tutorial: Pandas basics (Melanie Walsh)](https://melaniewalsh.github.io/Intro-Cultural-Analytics/03-Data-Analysis/01-Pandas-Basics-Part1.html)

## Before you begin...

We need to install a new library called `matplotlib` to visualize datasets as graphs

1. In the terminal, ensure that jupyter lab is closed (`ctrl-c`) and that your INFO-664 conda environment is activated
2. type the following:
- `conda install matplotlib` 
- and hit enter
3. follow any prompts (press `y` to proceed)
4. launch `jupyter lab` as normal

### Code Snippets for in-class demos

*dataset for today's pandas lesson*

Download this dataset and put it in your week9 folder:
[https://github.com/craigfahner/INFO-664/blob/main/week9/woman_500.csv](https://github.com/craigfahner/INFO-664/blob/main/week9/woman_500.csv)

*unwanted columns to filter out of MET dataset*

`unwanted_columns = ['primaryImageSmall', 'portfolio', 'artistRole', 'artistPrefix', 'artistSuffix', 'artistAlphaSort', 'subregion', 'locale', 'locus', 'excavation', 'river', 'classification', 'rightsAndReproduction', 'linkResource', 'metadataDate', 'repository']
`

### Pandas functions:

| Tool | What it does | What it gives back |
| --- | --- | --- |
| `pd.read_csv("file.csv")` | Reads a CSV file | A DataFrame |
| `df` (just the name) | Displays the table | The table, with the middle left out if it's large |
| `df.info()` | Summarizes the columns, their types, and missing values | Prints a summary |
| `df.head()` / `df.tail()` | Shows the first / last rows | A smaller DataFrame |
| `df.shape` | The size of the table | A pair: (rows, columns) |
| `df.columns` | The column names | An index of names |
| `df.drop(...)` | Removes columns (or rows) | A **new** DataFrame |
| `df['name']` or `df.name` | Selects one column | A Series |
| `series.tolist()` | The values of a column | A plain Python list |
| `df[100:105]` | Selects rows by position | A smaller DataFrame |
| `df.describe()` | Summary statistics of the numeric columns | A DataFrame of statistics |
| `df.value_counts('name')` | Counts how often each value appears in a column | A Series, most common first |
| `df.sort_values('name')` | Sorts the rows by a column | A **new** DataFrame |
| `df[mask]` | Keeps only the rows where a True/False test is `True` | A smaller DataFrame |
| `series.str.contains('text')` | Tests whether each text value contains some text | A Series of True/False |
| `series.nlargest(n)` | Keeps the `n` largest values | A smaller Series |
| `.plot(kind='bar')` | Draws a chart | A chart |



## HOMEWORK:

1. Take either the MET dataset or your own dataset and convert it to a dataframe
2. filter your dataset according to a specific term using the `==` operator or the `str.contains` method (using filtering criteria different from those used in class if using the MET dataset)
3. create a simple graph of your dataset using the df.plot() method (plotting a different aspect of the dataset than the ones we looked at in class, if using the MET set)

