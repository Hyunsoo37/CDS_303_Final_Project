---
layout: default
title: Session 1
---

# Seoul Commercial District Sales Patterns: Session 1

**CDS 303 Data Mining Final Project · Hyunsoo Lee and Taejoon Ha**

## Project overview

**Research question.** What do 2025 estimated sales by age group and time of day reveal about Seoul's commercial districts, and how can these patterns inform prospective business owners' decisions about target customers and operating hours?

**Purpose.** For each district, we will describe which age groups account for sales and when those sales are concentrated. Clustering will summarize recurring profiles across districts. For a candidate location, an owner could compare the district's own sales shares with typical shares for its cluster and review the mix of nearby businesses.

**Primary dataset.** We carry forward the 2025 estimated sales dataset from the [Final Project 0 notebook on GitHub](https://github.com/Hyunsoo37/CDS_303_Final_Project/blob/main/docs/session-1/CDS303_Project0.ipynb). The file, `서울시 상권분석서비스(추정매출-상권)_2025년.zip`, contains 85,732 rows and 55 columns covering 1,577 districts and 62 service categories across 2025 Q1–Q4. A row represents one district, service category, and quarter. The dataset reports estimated sales in Korean won (KRW) and transaction counts, with separate breakdowns by age, time of day, day of week, and gender. The Seoul Credit Guarantee Foundation provides the file through [Seoul Open Data Plaza](https://data.seoul.go.kr/dataList/OA-15572/S/1/datasetView.do).

**Scope of interpretation.** A district can have both a large sales share for people in their 20s and a large lunch share. The dataset reports these separately, so estimating the lunch share for people in their 20s would require a joint breakdown. Age shares refer to estimated sales amounts and cannot measure the number of customers. Time windows have different lengths, so sales shares and sales per hour answer different questions.

## Paper summary

Alvarez-Garcia, Ibar-Alonso, and Arenas-Parra (2024) propose a sequence that links data quality, clustering, and explanation. Their framework supports comparing algorithms and interpreting the resulting groups in the original variables. [A comprehensive framework for explainable cluster analysis](https://doi.org/10.1016/j.ins.2024.120282)

| Step | Why it matters | Methods in the paper | Our candidate approach |
| --- | --- | --- | --- |
| 1. Data preprocessing | Missing values, atypical observations, and inconsistent inputs can distort comparisons. | Use relationships between variables to fill missing values. Use Isolation Forest to flag unusual combinations of values. | Check district and quarter coverage, the consistency of sales totals, and small denominators. Inspect unusual profiles before deciding how to handle them. |
| 2. Dimensionality reduction | Related measures can repeat information and obscure the strongest patterns. | Use sparse principal component analysis (Sparse PCA) for numerical variables and multiple correspondence analysis for categorical variables. | Standardize numerical sales shares, then use PCA. Review explained variance and loadings to see which sales measures the retained components represent. |
| 3. Clustering | Groups districts with similar profiles and gives us a reference for comparing individual districts. | Compare candidate algorithms and cluster counts using validity measures. The paper's case study compares k-means, agglomerative clustering, and Gaussian mixtures using within-cluster sum of squares. | Compare k-means and Ward hierarchical clustering on the same retained components. Review silhouette scores, within-cluster sum of squares, cluster sizes, and stability across resamples. |
| 4. Classification for explainability | Helps explain what distinguishes the assigned groups in terms readers can interpret. | Predict the cluster labels with a tree model, using XGBoost by default. Tree SHAP summarizes feature contributions across predictions and for individual observations. | Use a shallow decision tree on the original sales shares. Read its rules alongside cluster profiles. If we compare a more flexible tree model, use Tree SHAP to explain its predictions. |

In Section 7 of the framework paper, the authors sampled 5,000 Spanish students from PISA 2018 and kept 4,241 after preprocessing. They summarized 80 original variables in 14 components and selected six clusters using k-means. In the separate PISA 2022 companion study, socioeconomic status and home access to and use of technology helped distinguish student profiles. [Uncovering student profiles: An explainable cluster analysis approach to PISA 2022](https://doi.org/10.1016/j.compedu.2024.105166)

### Why interpret the clusters?

A label such as “Cluster 3” does not tell a prospective owner which age bands or time windows account for sales. We will show each cluster's size and median shares alongside the medians across all analyzed districts. A district profile will show the district's own shares next to its cluster's typical values. For example, an owner considering lunch service could see whether a candidate's lunchtime share is high within its cluster or whether it is typical of that type.

### How classification helps

The **cluster label generated later** will be the classification target. A tree may use a combination such as a high lunch share and a high share for customers in their 20s to reproduce an assignment. These are two separate observations about the district. When the classifier uses the same sales shares as clustering, its performance measures how faithfully it reproduces the assignments. **It does not independently validate the clusters.** A separate check could examine whether comparable profiles recur in another year.

## Variable selection

The primary unit is **one district in 2025**. We propose starting with the 1,560 districts observed in all four quarters and retaining the other 17 for a coverage comparison. Within each district, we will sum the amounts across quarters and the service categories reported in the file, then calculate ratios from those sums. Averaging raw row ratios would give a low-sales category the same weight as a high-sales category. The overall profile can reflect the mix of businesses in the district, so we will consider separate profiles for categories relevant to prospective owners, such as coffee and beverages.

### Original columns

| Variable | Description and unit | Data type | Proposed role | Rationale / preparation needed |
| --- | --- | --- | --- | --- |
| `기준_년분기_코드` | Year and quarter code, 2025 Q1–Q4 | Categorical, ordered | Contextual Variable | Check period coverage and align quarters across the sales and store files. |
| `상권_코드`, `상권_코드_명` | District code and display name | Categorical identifiers | Exclude | Keep the code as text for aggregation and joins, and use the name for display. |
| `상권_구분_코드`, `상권_구분_코드_명` | Seoul's official district type | Categorical | Contextual Variable | Compare official types across the profiles. Keep one version of the field and one-hot encode it if a later comparison model uses it. |
| `서비스_업종_코드`, `서비스_업종_코드_명` | Service category code and name | Categorical | Contextual Variable | Use the code for joins and category comparisons. Verify the mapping before combining categories into broader groups. |
| `당월_매출_금액`, `당월_매출_건수` | Reported estimated sales (KRW) and transactions (count) | Numerical | Contextual Variable | Use as denominators, to describe commercial scale, and to flag thin records. Raw totals stay outside the baseline models. |
| `연령대_*_매출_금액` | Sales amounts for the 10s, 20s, 30s, 40s, 50s, and 60+ bands (KRW) | Numerical | Exclude | Exclude the raw amounts as direct inputs. Aggregate them to calculate age shares and age attribution coverage. |
| `시간대_*_매출_금액` | Sales amounts for six time windows (KRW) | Numerical | Exclude | Exclude the raw amounts as direct inputs. Use them to calculate time shares. The six amounts reconcile with total sales in the current file. |
| `주중_매출_금액`, `주말_매출_금액` | Weekday and weekend sales amounts (KRW) | Numerical | Exclude | Use the raw amounts to calculate one weekend share. The weekday share can be calculated from it. |
| Individual day, gender, and subgroup transaction-count columns | Day and gender amounts (KRW) and subgroup transactions (count) | Numerical | Exclude | Individual days overlap with the weekday/weekend split. Count breakdowns repeat the dimensions of the sales-amount breakdowns. Gender is outside the research question. |

### Derived variables

| Variable | Description and unit | Data type | Proposed role | Rationale / preparation needed |
| --- | --- | --- | --- | --- |
| Age sales shares (six variables) | Each age-band amount ÷ sum of all six age-band amounts × 100 (%) | Numerical | Clustering Input | Shows which ages account for sales among purchases with an age attribution. Keep the six age bands separate in the baseline. Model A also uses these shares to explain the resulting clusters. |
| Time-of-day sales shares (six variables) | Each window's sales ÷ total estimated sales × 100 (%) for 00–06, 06–11, 11–14, 14–17, 17–21, and 21–24 | Numerical | Clustering Input | Shows when sales are concentrated. Label windows with clock times because their lengths differ. Model A also uses these shares to explain the resulting clusters. |
| Weekend sales share | Weekend sales ÷ combined weekday and weekend sales × 100 (%) | Numerical | Contextual Variable | Adds context for opening days. A sensitivity check can add it to the clustering inputs. A per-day comparison would divide each total by the corresponding number of days. |
| Age attribution coverage | Sum of the six age-band amounts ÷ total estimated sales × 100 (%) | Numerical | Contextual Variable | Shows how much reported sales have an age attribution. Review low coverage before interpreting age shares. |
| Reported sales scale | Sum of reported sales over the four quarters (KRW) | Numerical | Contextual Variable | Compare district sizes after clustering. A separate sensitivity check can add log sales to see how much size changes the solution. |
| Average sales per transaction | Reported sales ÷ reported transactions (KRW per transaction) | Numerical | Classification Input | Candidate predictor for Model B. Gives context on transaction value and requires a positive transaction count. |
| Industry sales mix | Category or category-group sales ÷ total estimated sales × 100 (%) | Numerical | Classification Input | Candidate predictor for Model B. Verify the category mapping and use non-overlapping groups when comparing food service, coffee and beverages, services, or retail. |
| Store counts and franchise share | Reported category store counts and franchise stores ÷ total stores × 100 (%) for the same quarter and category | Numerical | Classification Input | Candidate predictors for Model B after checking linkage and count definitions. Also report them alongside district profiles where coverage permits. |

### How the clustering inputs answer the research question

The six age shares show which age groups account for sales in each district. The six time shares show which parts of the day account for sales. Together they can distinguish, for example, a district with relatively high lunch and 20s sales shares from one with a higher evening share. The age and lunch shares describe separate breakdowns. Comparing percentages also lets districts of different sizes share a profile when their sales are distributed similarly.

### Candidate classification inputs and target

The **cluster label generated by clustering is the classification target**. Neither that label nor any variable calculated from it will enter the predictor set.

- **Model A: Sales profiles.** Fit a shallow decision tree using the same 12 sales shares that informed clustering, in their original percentage units. Use held-out districts to see how closely the tree reproduces the assigned labels. Report a confusion matrix and per-cluster precision and recall. The resulting rules explain the assignments and do not provide an independent validation of the clusters.
- **Model B: Business mix, if coverage allows.** Use industry sales mix, sales per transaction, and verified store measures as candidates for predicting the same cluster labels. This shows whether the sales types are associated with particular business characteristics.

### Excluded inputs and why

- **Identifiers.** District codes and names identify locations. Quarter and industry codes are used to organize or link records. The model will use district-level sales measures as features.
- **Raw sales amounts.** Age, time, and weekday/weekend amounts are used to calculate shares. Including the amounts alongside the shares would give district sales scale more influence in the baseline.
- **Overlapping breakdowns.** Individual weekdays and subgroup transaction counts would repeat information already represented by sales shares. Weekday share is recoverable from weekend share. Gender sales are outside the scope of the question.

### Planned preparation

- **Coverage and missing values.** The current file has zero blank cells and zero duplicate district–category–quarter keys. Keep a record of missing rows and observed zeros. Review low transaction counts and low age attribution before setting a minimum-volume rule.
- **Check denominators.** Time windows and the weekday/weekend split reconcile with total sales in every raw row. The age amounts differ from total sales in 50,298 rows. The provider notes that total sales include corporate purchases without age information. Leave a share undefined if its denominator is zero. One raw row has zero age-attributed sales, and every district has positive age-attributed sales after aggregation. [Estimated-sales data FAQ](https://data.seoul.go.kr/dataList/OA-15572/A/1/datasetView.do)
- **Scaling and repeated information.** Check for shares with very little variation, then standardize the baseline shares before PCA. Within each set of six shares, the total is 100%. If we know five shares, we can calculate the sixth. Start with all six in each set and use PCA to keep the components that capture useful variation.
- **Categorical encoding.** The baseline uses numerical shares. If we test official district type in a separate model, one-hot encode one version of the field.
- **Sensitivity checks.** Compare the baseline with four age bands (10–19, 20–39, 40–59, and 60+). In a separate comparison, add weekend share. Changing one choice at a time helps explain any change in the profiles.

The [source data audit](./audit.py) reproduces the reported file and optional boundary-code checks. Model fitting and dataset integration are scheduled for later updates.

## Supplementary dataset

| Item | Proposed use |
| --- | --- |
| **Title** | Seoul Commercial District Analysis Service: Stores by District, 2025 (서울시 상권분석서비스(점포-상권)). |
| **Provider** | Seoul Credit Guarantee Foundation. The source lists Korea Open Government License Type 1 (attribution). |
| **Link** | [Seoul Open Data Plaza download](https://data.seoul.go.kr/dataList/OA-15577/F/1/datasetView.do) for `서울시 상권분석서비스(점포-상권)_2025년.zip). |
| **Variables** | Total, general, and franchise store counts (`전체_점포_수`, `일반_점포_수`, `프랜차이즈_점포_수`). Opening and closure counts and rates (`개업_점포_수`, `폐업_점포_수`, `개업_율`, `폐업_률`). [Official field list](https://data.seoul.go.kr/dataList/OA-15577/S/1/datasetView.do) |
| **Contribution** | A prospective café owner can start with districts where the age profile fits their intended customers, then compare how many cafés are already reported in each district. Opening and closure counts show where there has been more recent turnover. Franchise share adds context about the mix of cafés. These details help an owner decide which candidate districts to investigate further. |
| **Connection** | For the two 2025 files, compare reporting quarter, district code, and service category code (`기준_년분기_코드`, `상권_코드`, `서비스_업종_코드`). Check that the keys are unique in each file and that the codes have the same meaning. Report the match rate before adding store variables to district profiles. |

Use quarter-specific store counts or average the quarterly counts for a 2025 comparison. Adding the counts across quarters would count some stores more than once. If the category codes cannot be aligned, use verified district summaries as context. If district codes also cannot be aligned, use broader store summaries without a district-level join.

### Optional mapping dataset

| Item | Proposed use |
| --- | --- |
| **Title** | Seoul Commercial District Analysis Service: District Boundaries (서울시 상권분석서비스(영역-상권)). |
| **Provider** | Seoul Credit Guarantee Foundation. |
| **Link** | [Seoul Open Data Plaza boundary file](https://data.seoul.go.kr/dataList/OA-15560/S/1/datasetView.do). |
| **Variables** | District codes (`TRDAR_CD`) and boundary polygons. |
| **Contribution** | Map the sales profiles so a prospective owner can locate and compare candidate districts. |
| **Connection** | Match `TRDAR_CD` to the sales district code (`상권_코드`). All 1,577 sales district codes appear among the 1,650 boundary codes. The archive lists a 2023 file date, so confirm that each matched geometry still represents the district in the 2025 sales file before mapping. |

## Future project updates

- **Data preparation.** District-level profiles, coverage rules, and the store-data match check.
- **Dimensionality reduction and clustering.** Component selection, candidate cluster solutions, and sensitivity comparisons.
- **Classification and interpretation.** Model explanations and district profiles for prospective owners.
