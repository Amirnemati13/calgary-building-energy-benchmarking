# Data dictionary

The analytical unit is one property in one reporting year. A property may contain more than one building. Values are parsed from the public annual responses without filling missing measurements.

| Column | Meaning | Unit or type | Use |
|---|---|---|---|
| `property_id` | Public property identifier | String | Grouped validation |
| `report_year` | Calendar reporting year | Integer | Predictor and temporal split |
| `organization` | Disclosed organization | String, nullable | Audit |
| `city` | Source municipality label | String | Audit; labels are not normalized |
| `latitude` | Public latitude | Decimal degrees | Spatial grouping |
| `longitude` | Public longitude | Decimal degrees | Spatial grouping |
| `floor_area_m2` | Gross floor area | m² | Predictor after logarithm |
| `year_built` | Construction year | Year | Predictor |
| `property_type` | Use category in reporting cycle | String | Predictor |
| `site_eui` | Site energy-use intensity | kWh/m²/year | Target |
| `source_eui` | Source energy-use intensity | kWh/m²/year | Audit; excluded from predictors |
| `ghg_intensity` | Greenhouse-gas intensity | kgCO₂e/m²/year | Audit |
| `total_ghg_t` | Total greenhouse-gas emissions | tCO₂e/year | Audit |
| `energy_star_score` | Reported ENERGY STAR score | Score, nullable | Audit |
| `water_intensity` | Water-use intensity | m³/m²/year | Audit |

The download validates declared units. Site EUI is not assumed to be weather-normalized. Missing ENERGY STAR scores can reflect eligibility or disclosure, and must not be interpreted as zero performance.

`reference_manifest.json` describes the published run. `snapshots/` is reserved for local downloads and is ignored by Git. See [source attribution](../docs/data-sources.md).

**راهنمای فارسی:** هر ردیف یک ملک در یک سال است. متغیر هدف Site EUI و ورودی‌ها کاربری، مساحت، سال ساخت و سال گزارش‌اند. شناسه و مختصات برای جداسازی نمونه‌ها استفاده می‌شوند؛ مصرف و انتشار هم‌زمان وارد مدل نمی‌شوند. فقدان امتیاز ENERGY STAR به معنای امتیاز صفر نیست. واحدها هنگام دریافت کنترل می‌شوند و نرمال‌سازی آب‌وهوایی فرض نمی‌شود.
