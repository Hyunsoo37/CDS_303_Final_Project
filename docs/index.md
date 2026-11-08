---
layout: default
title: Project Overview
---

# Seoul Commercial District Sales Patterns

**CDS 303 Data Mining Final Project · Hyunsoo Lee and Taejoon Ha**

## Project overview

We use 2025 estimated sales to describe which customer age groups and times of day account for sales in each Seoul commercial district. Clustering will summarize those profiles into recurring sales types. A classification step will help explain what distinguishes the types, and store data will provide context on which businesses are already present.

## Research question

What do 2025 estimated sales by age group and time of day reveal about Seoul's commercial districts, and how can these patterns inform prospective business owners' decisions about target customers and operating hours?

## Primary dataset

**Seoul Commercial District Analysis Service: Estimated Sales by District (서울시 상권분석서비스(추정매출-상권)), 2025.** The file contains 85,732 rows and 55 columns covering 1,577 districts, 62 reported service categories, and all four quarters of 2025. Each row is a district, service category, and quarter. The data report estimated sales in Korean won and transaction counts, with separate breakdowns by customer age, time of day, day of week, and gender. The Seoul Credit Guarantee Foundation provides the file through [Seoul Open Data Plaza](https://data.seoul.go.kr/dataList/OA-15572/S/1/datasetView.do).

## Project updates

- [Session 1: Research design](./session-1/index.md)
- **Next: Data preparation.** Build district profiles, check coverage, and test the connection to store data.
- **Later: Modeling and interpretation.** Compare clustering solutions and prepare explanations for prospective owners.
