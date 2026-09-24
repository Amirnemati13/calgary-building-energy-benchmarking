# Methods

[فارسی](methods.fa.md)

## Question and unit of analysis

The target is Site EUI in kWh/m²/year. Each row is a disclosed property in a reporting year. Repeated years increase the number of observations but not the number of independent properties. The reference panel has 654 distinct property IDs and 2,780 labeled observations.

## Data preparation

The download checks cycle identifiers, property identifiers and units. Duplicate property-year keys cause a failure. Missing values remain missing; zero is not converted to missing during parsing. The modeling stage excludes non-positive or missing targets. In the reference snapshot only one target is missing and no observed target is non-positive.

One construction year exceeds its reporting year. It is set to missing in the modeling copy. Numeric medians and categorical modes are estimated on each training set. Log floor area is a fixed transformation; scaling and one-hot encoding are fitted within the same training pipeline. Unknown test categories are handled without learning their target values.

High EUI values remain in the sample. An audit compares total emissions with area multiplied by emissions intensity. Its screening threshold is the larger of 1 tonne and 1% of reported emissions; the check is not a proof of physical accuracy. Ninety-eight properties have more than 1% variation in reported area. Raw observations are preserved.

## Predictors and models

The predictors are property type, log gross floor area, construction year and reporting year. Same-year Source EUI, GHG emissions, ENERGY STAR score and water intensity are excluded. IDs, organization and coordinates do not enter the predictive model.

Ridge uses alpha=10 after numeric scaling and categorical encoding. Random Forest uses 200 trees, maximum depth 6, a minimum leaf size of 5 and random seed 42. No hyperparameter search is performed. Single-worker execution improves portability. Rows receive equal training weight, so properties reported for more years receive more total weight.

Baselines are the training-set median, the within-type training median with a global fallback, and previous-year EUI where available. The last baseline is evaluated only on properties having an observation exactly one year earlier. Competing models use the same subset for that comparison.

## Evaluation scenarios

| Scenario | Training and test boundary | Interpretation |
|---|---|---|
| Unseen property | Five property-grouped folds within 2019–2023 | Generalization to a different disclosed property |
| Spatial transfer | Five folds of approximate 5 km blocks within 2019–2023 | Transfer to held-out areas within Calgary |
| Later reporting year | Train on all years before each test year, 2022–2025 | Prediction in a subsequent year from basic characteristics |

All years of a property remain together in grouped and spatial evaluation. Spatial blocks use median property coordinates, a fixed origin at latitude 50.8 and longitude −114.3, and a local degree-to-distance approximation at latitude 51.05. Blocks have no exclusion buffer. Boundary proximity, alternative grid origins and block sizes remain sensitivity questions.

Temporal tests separate previously seen and unseen properties. They permit earlier years of the same property in training, which matches the known-property scenario. No future-year observation is used for fitting. Nevertheless, the source is a current snapshot of historical disclosures: post-reporting corrections may be present. These tests do not reconstruct exactly what was known at the historical prediction date.

2024 is the principal test. Earlier tests describe historical behavior; 2025 is provisional because the program's 2025 submission window was still open at retrieval. Only 11 properties in the 2024 test are entirely unseen in training, so that subgroup provides weak evidence on its own.

## Metrics and uncertainty

MAE is the primary error measure; RMSE and R² provide complementary information. Grouped and spatial summaries pool out-of-fold predictions across records. Fold-level variation and equal-property weighting should be examined before stronger inferential claims.

The paired bootstrap compares 2024 Random Forest MAE with type-median MAE. It samples the 559 test properties with replacement 2,000 times, using seed 42 and fixed predictions. Its percentile interval reflects conditional test-sample uncertainty, not training variability, temporal dependence, source revision or sample selection.

## Model interpretation

Exact SHAP is computed for 100 randomly selected 2024 test properties with 50 training observations as the background. Construction year, reporting year and log area are represented on the model's transformed scale. Property type is reconstructed as a single categorical feature. All 16 feature coalitions are enumerated. Additivity is verified against the fitted model's prediction function at tolerance 1e-6.

Attributions depend on the chosen background, model and sample. Coalitions may combine correlated attributes in uncommon ways. Importance is not a causal effect, and a positive residual is not an estimate of retrofit savings. The current release does not assess SHAP stability across training splits.

## Limits on interpretation

The disclosed population is selected and not representative by design. The available fields omit occupancy, operating hours, weather, envelope performance, HVAC and retrofit histories. Source updates can change historical values. A property can include multiple buildings. The results support cautious within-sample benchmarking and investigation of error patterns, not a citywide efficiency ranking or causal design prescription.

Useful extensions include weather and occupancy data, equal-property weighting, buffered spatial evaluation, grid-size sensitivity and external-city validation. Any further model selection should use nested training validation and an untouched evaluation set.

## Method references

- [scikit-learn: common pitfalls and data leakage](https://scikit-learn.org/stable/common_pitfalls.html)
- [scikit-learn: cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)
- [SHAP: predictive explanations and causal interpretation](https://shap.readthedocs.io/en/latest/example_notebooks/overviews/Be%20careful%20when%20interpreting%20predictive%20models%20in%20search%20of%20causal%20insights.html)
