"""Read-only checks for the source files used in CDS 303 Final Project 1."""

import argparse
import csv
import struct
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

QUARTER = "기준_년분기_코드"
DISTRICT = "상권_코드"
INDUSTRY = "서비스_업종_코드"
TOTAL = "당월_매출_금액"
WEEK = ("주중_매출_금액", "주말_매출_금액")


def audit_sales(path):
    quarters = defaultdict(set)
    district_age_totals = Counter()
    keys = Counter()
    checks = Counter()
    industries = set()

    with path.open(encoding="cp949", newline="") as source:
        reader = csv.DictReader(source)
        columns = reader.fieldnames or []
        age_columns = [c for c in columns if c.startswith("연령대_") and c.endswith("_금액")]
        time_columns = [c for c in columns if c.startswith("시간대_") and c.endswith("_금액")]
        if len(age_columns) != 6 or len(time_columns) != 6:
            raise ValueError("Expected six age and six time-of-day amount fields.")

        for row in reader:
            quarter, district, industry = (row[c].strip() for c in (QUARTER, DISTRICT, INDUSTRY))
            keys[quarter, district, industry] += 1
            quarters[district].add(quarter)
            industries.add(industry)
            checks["Rows"] += 1
            checks["Blank cells"] += sum(not row[c] or not row[c].strip() for c in columns)
            total = int(row[TOTAL])
            age_total = sum(int(row[c]) for c in age_columns)
            district_age_totals[district] += age_total
            checks["Rows with nonpositive total sales"] += total <= 0
            checks["Rows with zero age-attributed sales"] += age_total == 0
            checks["Rows with age sum different from total"] += age_total != total
            checks["Rows with time sum different from total"] += (
                sum(int(row[c]) for c in time_columns) != total
            )
            checks["Rows with weekday/weekend sum different from total"] += (
                sum(int(row[c]) for c in WEEK) != total
            )

    all_quarters = {"20251", "20252", "20253", "20254"}
    checks["Columns"] = len(columns)
    checks["Duplicate quarter–district–category rows"] = sum(n - 1 for n in keys.values())
    checks["Districts"] = len(quarters)
    checks["Service categories"] = len(industries)
    checks["Districts observed in all four 2025 quarters"] = sum(
        all_quarters <= observed for observed in quarters.values()
    )
    checks["Districts with zero age-attributed sales"] = sum(
        value == 0 for value in district_age_totals.values()
    )
    for label, count in checks.items():
        print(f"{label}: {count:,}")
    return set(quarters)


def boundary_codes(path):
    """Read the ASCII district code from the shapefile's DBF attribute table."""
    with ZipFile(path) as archive:
        dbf_name, = [name for name in archive.namelist() if name.lower().endswith(".dbf")]
        data = archive.read(dbf_name)

    records, header_size, record_size = struct.unpack_from("<IHH", data, 4)
    field_start = 1
    for descriptor in range(32, header_size - 1, 32):
        name = data[descriptor:descriptor + 11].split(b"\0", 1)[0].decode("ascii")
        width = data[descriptor + 16]
        if name == "TRDAR_CD":
            break
        field_start += width
    else:
        raise ValueError("District code field TRDAR_CD was not found.")

    return {
        data[offset + field_start:offset + field_start + width].decode("ascii").strip()
        for offset in range(header_size, header_size + records * record_size, record_size)
        if data[offset:offset + 1] != b"*"
    } - {""}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sales_csv", type=Path, help="2025 estimated sales CSV")
    parser.add_argument(
        "boundary_zip", nargs="?", type=Path, help="Optional commercial district boundary shapefile ZIP"
    )
    args = parser.parse_args()
    sales = audit_sales(args.sales_csv)
    if args.boundary_zip is not None:
        boundaries = boundary_codes(args.boundary_zip)
        print(f"Distinct boundary codes: {len(boundaries):,}")
        print(f"Sales codes present in boundaries: {len(sales & boundaries):,}")
