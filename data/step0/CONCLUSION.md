# Step 0 — Language Slice Coverage Conclusion

## Context: Two-Stage Verification

The verification was carried out in two stages:

**(a) Coarse grid at a fixed 500-star threshold**
Output: `data/step0/result.csv`

**(b) Finding the real top-750 entry threshold per year**
Method: exponential + binary search.
Output: `data/step0/star_threshold.csv`

Then: recount of `total_count` per language using the honest per-year threshold.
Output: `data/step0/final_check.csv`

---

## Why Stage (b) Was Necessary

The 500-star threshold is independent per language. But the final sample is a shared
**top-750 by stars per year across all languages combined**.

This means the stage (a) check produced misleadingly optimistic numbers: it ignored
inter-language competition. The real top-750 entry bar in competitive years turns out
to be several times higher than 500 — and that is what actually determines what makes
it into the sample.

---

## Results for the 2016–2020 Cohort (after the honest threshold)

Total `total_count` per language over 5 years:

| Language     | total_count |
|--------------|-------------|
| Python       | 603         |
| TypeScript   | 487         |
| JavaScript   | 409         |
| Go           | 365         |
| C++          | 195         |
| Java         | 191         |
| Rust         | 171         |
| C#           | 99          |
| PHP          | 37          |
| Ruby         | 9           |

---

## Conclusion

This is outcome **B** from the plan, but in a form the plan did not predict exactly.

The plan expected a data shortage for **young languages** (Rust, TypeScript, Go) — the
assumption being that they had not yet aged into the older cohort. In practice this
hypothesis **was not confirmed**: Rust, TypeScript, and Go all cleared the 30–50 repo
threshold with comfortable margin.

The real problem turned out to be only **Ruby** (total of 9 across the entire cohort).
The likely cause is the smaller overall size of Ruby's starred ecosystem on GitHub,
not the language's age. The exact cause was not investigated and remains an open question.

---

## Practical Decision

Ruby is excluded from the language slice of dashboard page 2 (`retention_class × language`).
The remaining 9 languages stay in the slice as-is.

This follows the plan (section 2.5, option B): change the problem statement, not the code —
the slice is defined over languages with sufficient N.

---

## 2023 Anomaly

In `star_threshold.csv` the 2023 threshold is **5158** — notably higher than neighboring
values (3808 in 2022 and 3850 in 2024).

Likely cause: the surge of AI/LLM repositories following the ChatGPT release in late 2022
pushed the star bar up specifically in that year. The cause was not verified in detail;
recorded here as an observation.
