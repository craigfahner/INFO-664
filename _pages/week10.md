---
layout: page
title: Week 10
permalink: /week10/
---

## Week 10 activities: 

* [in-class notebook: web scraping + JSON saving](https://github.com/craigfahner/INFO-664/blob/main/week9/week9.ipynb)
* [External tutorial: Pandas basics (Melanie Walsh)](https://melaniewalsh.github.io/Intro-Cultural-Analytics/03-Data-Analysis/01-Pandas-Basics-Part1.html)

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


## HOMEWORK:

1. Have a look at the following example galleries for the data visualization libraries:
- [Pandas plot examples](https://pandas.pydata.org/docs/user_guide/visualization.html)
- [Plotly examples](https://plotly.com/python/)
- [seaborn examples](https://seaborn.pydata.org/examples/index.html)
- [pydeck examples](https://deckgl.readthedocs.io/en/latest/)
- [wordcloud examples](https://amueller.github.io/word_cloud/auto_examples/index.html)

Select one data visualization method from the above galleries that is of interest to you, or that you might be interested in integrating into your project.
2. Bring the example code for the selected method into a Jupyter notebook and modify some of the parameters (around color, scale, input data, etc), documenting what you've changed in your comments

