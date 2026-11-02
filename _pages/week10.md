---
layout: page
title: Week 10
permalink: /week10/
---

## Week 10 activities: 

* [Lecture notebook: Data Visualization](https://github.com/craigfahner/INFO-664/blob/main/week10/week10_notes.ipynb)

## Visualization in Python

There are a few advanced libraries for generating graphs, charts, maps and more in Python:

* [plotly](https://plotly.com/python/getting-started/)
    * [choropleth maps in plotly](https://plotly.com/python/choropleth-maps/)
* [pydeck](https://deckgl.readthedocs.io/en/latest/)
* [seaborn](https://seaborn.pydata.org/tutorial/introduction.html)
* [wordcloud](https://amueller.github.io/word_cloud/)

## Before you begin...

We need to install a couple new libraries – please use the following instructions to install!

1. In the terminal, ensure that jupyter lab is closed (`ctrl-c`) and that your INFO-664 conda environment is activated
2. type the following:
- `conda install -c conda-forge plotly pydeck wordcloud pillow` 
- and hit enter
3. follow any prompts (press `y` to proceed)
4. launch `jupyter lab` as normal

### Code Snippets and datasets for in-class demos

Please download these datasets:
- [Senate polling data](https://github.com/craigfahner/INFO-664/blob/main/week10/senate_average_recent.csv)
- [House polling data](https://github.com/craigfahner/INFO-664/blob/main/week10/house_average_recent.csv)
- [US districts geojson file](https://github.com/craigfahner/INFO-664/blob/main/week10/districts_120th.geojson)
- [How the Other Half Lives: Studies Among the Tenements of New York (from Project Gutenberg)](http://github.com/craigfahner/INFO-664/blob/main/week10/riis.txt)

**Bar chart snippet**
```
# a dictionary of the names we want in the legend: {old column name: new name}
party_names = {"dem": "Democrat", "other": "Other / undecided", "rep": "Republican"}

# the color of each bar segment, by its new name 
colors = {"Democrat": "blue", "Other / undecided": "grey", "Republican": "red"}

# sort the states from the smallest margin (most Republican) to the largest (most Democratic),
# and rename the columns using the dictionary above
senate_sorted = senate.sort_values("margin").rename(columns=party_names)

fig = px.bar(
    senate_sorted,
    x=["Democrat", "Other / undecided", "Republican"],   # a list of columns: each one becomes a segment, stacked left to right
    y="state",                                           # one bar for each state
    orientation="h",                                     # "h" for horizontal bars
    color_discrete_map=colors,                           # which color goes with which segment
    labels={"value": "Percent", "state": "State"},       # px calls the length of each segment "value" in the hover box
    hover_data={"polls": True, "latest": True},          # also show the number of polls and the latest poll date
    height=800,                                          # tall enough for 29 bars
    title="U.S. Senate polling: each state's latest week",
)

fig.update_layout(
    legend_title_text="",                  # remove the legend's default title
    xaxis_title="Percent of those polled",
    xaxis_range=[0, 100],                  # always show the full 0 to 100 percent
    yaxis_title="",
    yaxis={"dtick": 1},                    # label every bar (otherwise Plotly may label every other one)
)

fig.show()
```

## HOMEWORK:

1. Have a look at the following example galleries for the data visualization libraries:
- [Pandas plot examples](https://pandas.pydata.org/docs/user_guide/visualization.html)
- [Plotly examples](https://plotly.com/python/)
- [seaborn examples](https://seaborn.pydata.org/examples/index.html)
- [pydeck examples](https://deckgl.readthedocs.io/en/latest/)
- [wordcloud examples](https://amueller.github.io/word_cloud/auto_examples/index.html)

Select one data visualization method from the above galleries that is of interest to you, or that you might be interested in integrating into your project.

2. Bring the example code for the selected method into a Jupyter notebook and modify some of the parameters (around color, scale, input data, etc), documenting what you've changed in your comments

