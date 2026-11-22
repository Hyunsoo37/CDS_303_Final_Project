# Data sources and reproduction

These are public commercial-district aggregates, not customer-level records. Provider: **Seoul Credit Guarantee Foundation**, distributed by **Seoul Open Data Plaza**. Source pages list unrestricted use; credit the provider and source links when reusing the data. The source CSV bytes are unchanged, with short English ZIP filenames for portability. The sales ZIP was repacked using ZIP-LZMA to fit the upload limit; Python reads it directly. The original download is preserved in our local course materials. The stores ZIP is unchanged. CSV hashes below verify source-data identity independently of archive compression.

| Included file | Original download | Source |
| --- | --- | --- |
| `raw/sales_2025.zip` | 서울시 상권분석서비스(추정매출-상권)_2025년.zip | [Official sales page](https://data.seoul.go.kr/dataList/OA-15572/S/1/datasetView.do) |
| `raw/stores_2025.zip` | 서울시 상권분석서비스(점포-상권)_2025년.zip | [Official stores page](https://data.seoul.go.kr/dataList/OA-15577/F/1/datasetView.do) |

Sales are the existing Project 0/1 2025 file (source file date May 18, 2026). The stores file was downloaded November 22, 2026 (source file date May 21, 2026). Each ZIP contains one CP949 CSV. The notebook reads ZIPs directly; no download, API key, login or manual extraction is needed to rerun it.

To reacquire an original, use its official page, find the 2025 ZIP under file downloads, and save it under the corresponding short filename above. The online sheet preview is limited to 1,000 rows and is not the full input. If extracting manually, retain CP949 encoding.

## Raw file identity

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `sales_2025.zip` | 11886606 | `9e055e94b3647ddecbdc033c9b80817bcf774fcde2fe423af57fd179153633dc` |
| `stores_2025.zip` | 2119809 | `133bfc6ce79e13ee5b289490e4667dfba46a0af5d0d71df360a0d324e030a4e6` |

Extracted `sales_2025.zip` CSV SHA-256: `2e299cd3e78a98d9b46634af0cc768276d8d270eb4c38b5f1b1ce54f8dcd828f`.

Extracted `stores_2025.zip` CSV SHA-256: `afe3c49336e4c64e3e4066db1bb61034ab7c238916ff473a37d7667fbb4e1d68`.

## Linkage and field mapping

Original unit: district × industry × quarter. Read codes as text. Sales have Korean field names; stores use English field names. `stdr_yyqu_cd`, `trdar_cd`, `svc_induty_cd` correspond to `기준_년분기_코드`, `상권_코드`, `서비스_업종_코드`. `similr_induty_stor_co` is total stores; `stor_co` is general stores; `frc_stor_co` is franchise stores. The notebook verifies total = general + franchise. See [official field descriptions](https://data.seoul.go.kr/dataList/datasetView.do?currentPageNo=1&infId=OA-15577&serviceKind=1&srvType=A) and saved [sales schema](../docs/session-2/results/sales_schema.csv), [store schema](../docs/session-2/results/stores_schema.csv).

Sales amounts are summed across reported quarters and industries before shares are calculated. Stores are summed over all 100 reported categories within each district-quarter, then averaged over available quarters. No original missing industry row is inferred to be zero. Store data are aggregated independently of sales to preserve the extra 38 categories. Final integration is a one-to-one left join on district code. These code/name checks do not validate geometry; no older boundary file is used.

## Included processed files

| File | Unit and contents |
| --- | --- |
| `processed/integrated_districts_2025.csv` | All 1,577 sales districts; summed source amounts, 12 shares, context, quarter coverage, match and exclusion status |
| `processed/store_quarterly.csv` | District × quarter counts summed across all reported store industries |
| `processed/pca_inputs_2025.csv` | 1,560 complete-year districts; identifier plus 12 unstandardized age/time percentages |
| `processed/pca_scores_2025.csv` | Same 1,560 districts; identifier plus six retained PC scores |

Processed CSVs are UTF-8. Age shares use total age-attributed sales, while time shares use total sales. Age coverage and weekend/franchise shares are percentages. Sales amounts are KRW, transaction totals are counts, and mean quarterly stores may be fractional. Store context has a broader industry universe than sales. IDs are for linkage only, never passed to PCA. Other context/coverage fields are explained in the [variable table](../docs/session-2/results/variables.csv) and [report](../docs/session-2/index.md).

## Run in Jupyter

1. Clone or download the full repository, including `data/raw/`.
2. In a Python environment, run `python -m pip install -r requirements.txt` from the repository root.
3. Run `jupyter notebook`, open `docs/session-2/CDS303_Project2.ipynb`, select that Python environment and use **Restart Kernel and Run All**.
4. The notebook finds the repository root using the included raw ZIP path. Run from the repository root or the notebook directory. It recreates processed CSVs, result tables and figures. Save the notebook to retain new outputs.

The Python packages were validated with Python 3.13.9; exact analytical package versions are recorded in requirements.txt and results/summary.json. There is no train/test split or stochastic clustering at this stage. Full-SVD PCA is deterministic; the seed 2000 follows Demo 6. The execution environment used a new in-process IPython kernel because network sockets were blocked; the report states that validation limit explicitly.
