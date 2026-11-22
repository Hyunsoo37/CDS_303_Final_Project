# Seoul Commercial District Sales Patterns

CDS 303 Final Project · Hyunsoo Lee and Taejoon Ha

## Research question

What do 2025 estimated sales by age group and time of day reveal about Seoul's commercial districts, and how can these patterns inform prospective business owners' decisions about target customers and operating hours?

## Current stage: Final Project 2

We integrated the 2025 sales and store datasets into one row per commercial district. PCA uses 12 standardized age/time sales shares for 1,560 complete-year districts; six components retain 87.14% of variation. Store counts and franchise share provide context. Clustering and classification are reserved for later stages.

**Refined question:** What are the main dimensions of variation in the age-group and time-of-day sales shares of Seoul commercial districts in 2025, and how can these differences be compared alongside store composition when screening candidate locations?

- [Project 2 report and figures](docs/session-2/index.md)
- [Project 2 executed notebook](docs/session-2/CDS303_Project2.ipynb)
- [Included data and Jupyter run instructions](data/README.md)
- [Python dependencies](requirements.txt)

## Project materials

- [Project overview and research question](docs/index.md)
- [Session 1 research design](docs/session-1/index.md)
- [Final Project 0 notebook](docs/session-1/CDS303_Project0.ipynb)
- [Source data audit script](docs/session-1/audit.py)

The audit uses Python 3. Extract the 2025 sales CSV from the official download. Pass the boundary ZIP as a second argument only to check mapping-code coverage.

```sh
python3 docs/session-1/audit.py "<path to 2025 sales CSV>"
python3 docs/session-1/audit.py "<path to 2025 sales CSV>" "<optional path to boundary ZIP>"
```

To rerun the Project 0 notebook, use pandas and place the extracted 2025 sales CSV under its original filename in the notebook's working directory.
