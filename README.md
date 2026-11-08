# Seoul Commercial District Sales Patterns

CDS 303 Final Project · Hyunsoo Lee and Taejoon Ha

## Research question

What do 2025 estimated sales by age group and time of day reveal about Seoul's commercial districts, and how can these patterns inform prospective business owners' decisions about target customers and operating hours?

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
