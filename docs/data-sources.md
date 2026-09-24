# Data sources and attribution

## Provider and retrieval

The data are supplied through the City of Calgary's **BenchmarkYYC** program. The public performance map is operated by **OPEN Technologies**.

- Program: https://www.calgary.ca/environment/programs/building-energy-benchmarking-program.html
- Public map: https://grid.opentech.eco/orgs/calgary/viz
- Public configuration: https://grid.opentech.eco/orgs/calgary/api/public/v2/viz/config
- Annual records: `https://grid.opentech.eco/orgs/calgary/api/public/v2/viz/properties?cycle-id=<cycle-id>`

The downloader discovers reporting cycles from the public configuration rather than guessing identifiers. Each response is checked against its requested cycle. Numeric values are read with their declared units. The source manifest records retrieval time, endpoints, response hashes, row counts and the normalized CSV checksum.

The endpoint is part of the public map and may change. It is not treated as a guaranteed versioned research API. Failures or changed units stop the download; incompatible values are not silently converted.

## Reference snapshot

Retrieved: **24 September 2026**. Coverage: **2019–2025**. Public records: **2,781**. Distinct property identifiers: **654**. Site EUI available: **2,780**.

Annual counts: 2019: 269; 2020: 278; 2021: 282; 2022: 346; 2023: 580; 2024: 559; 2025: 467.

Reporting year 2025 is marked provisional because the program page listed a submission period ending 15 October 2026 at retrieval. This is a snapshot-specific judgment, not a permanent designation of that year. Reassess it for later releases.

## Storage and reuse

Raw annual responses and the normalized record-level CSV are downloaded to `data/snapshots/`, which is excluded from Git. This repository distributes authored code, documentation, aggregate metrics, figures and provenance. It does not assign the code license to the source records or mirror the map's full configuration.

Public access alone is not a grant of a new license from this repository. Refer to the original provider's terms for source-data reuse. Logos and other provider branding are not included. Cite both the program and map when using the data, and identify the retrieval date and reporting years.

Recommended attribution:

> Data source: City of Calgary, BenchmarkYYC, public Building Performance Map operated by OPEN Technologies. Retrieved 24 September 2026; reporting years 2019–2025. Analysis and conclusions are independent of the data provider.

No private property names or addresses are requested or reconstructed. Coordinates and organization labels are used locally for audit and validation; row-level predictions are not included in the published result tables.

## Versioning limits

The source can revise historical records. The published manifest identifies the snapshot underlying the reported findings, but it does not guarantee that the source will return identical bytes later. Preserve local raw responses when exact reruns are required. Changes to the data should produce a new manifest and a new result set, rather than silently replacing the reference findings.

## خلاصهٔ فارسی

ارائه‌دهندهٔ داده شهرداری کلگری و برنامهٔ BenchmarkYYC است؛ نقشهٔ عمومی توسط OPEN Technologies میزبانی می‌شود. شناسهٔ دوره‌ها از تنظیمات عمومی خوانده و واحدها کنترل می‌شوند. زمان دریافت، نشانی، هش و تعداد ردیف‌ها در فایل منشأ ثبت شده‌اند.

رکوردهای خام و CSV در پوشهٔ محلیِ خارج از کنترل نسخه ذخیره می‌شوند. مجوز کد به دادهٔ منبع تسری ندارد. در استفاده از داده، نام شهرداری، برنامه، میزبان نقشه، تاریخ دریافت و سال‌های گزارش ذکر شود. نتایج پروژه مستقل از ارائه‌دهندهٔ داده‌اند.

نسخهٔ مرجع مربوط به ۲۴ سپتامبر ۲۰۲۶ است. دادهٔ ۲۰۲۵ در این تاریخ موقت محسوب شده است. ممکن است منبع، مقادیر تاریخی را اصلاح کند؛ برای بازتولید دقیق باید پاسخ‌های خام همان دریافت نگهداری شوند.
