# Step 0 — Language Slice Coverage Check

Run before a line of the collector was written. The question was not a detail of
implementation but whether the intended analysis was viable at all: if a retention
cut by language leaves half the languages with three or four repositories per cell,
any share computed there is noise, and it is better to find that out on paper than
after the pipeline is built.

The check costs almost nothing. GitHub's search endpoint returns `total_count` for
any query without downloading a single repository, so coverage can be measured with
a few dozen calls and no collection.

---

## Two-stage verification

**(a) Coarse grid at a fixed 500-star threshold**
Output: `data/step0/result.csv`

**(b) Finding the real top-750 entry threshold per year**
Method: exponential then binary search.
Output: `data/step0/star_threshold.csv`

Then: recount of `total_count` per language using the per-year threshold.
Output: `data/step0/final_check.csv`

---

## Why stage (b) was necessary

A 500-star threshold applies independently to each language. But the final sample is
a shared **top-750 by stars per year across all languages combined**.

Stage (a) therefore produced misleadingly optimistic numbers: it ignored competition
between languages. In competitive years the real entry bar for the top 750 turns out
to be several times higher than 500, and that bar — not a fixed number — determines
what actually makes it into the sample.

---

## Results for the 2016–2020 cohort, at the real threshold

Total `total_count` per language over five years:

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

The concern that prompted the check was that **young languages** would be missing:
Rust, TypeScript and Go might not have aged into the 2016–2020 cohort in any number,
since a language needs years to accumulate top-starred repositories. That did not
happen. All three clear a threshold of 30–50 repositories with a comfortable margin;
Rust is the smallest of them at 171 and still an order of magnitude above the line.

The only language that fails is **Ruby**, with 9 repositories across the entire
five-year cohort. The likely cause is the smaller size of Ruby's starred ecosystem
on GitHub rather than the language's age, but this was not investigated and remains
open.

**Decision.** Ruby is dropped from the language cut. The remaining nine languages
stay as they are. The fix is to the question, not to the code: the cut is defined
over languages with enough repositories to support a share, and the one that is not
is named rather than quietly averaged in.

---

## 2023 anomaly

In `star_threshold.csv` the 2023 threshold is **5158** — well above its neighbours,
3808 in 2022 and 3850 in 2024.

The likely cause is the surge of AI and LLM repositories after the release of ChatGPT
in late 2022, which pushed the entry bar up in that year specifically. Not verified in
detail; recorded as an observation.

The same spike reappears independently in the collected data, where the 750th
repository of 2023 has 5,163 stars (`FINDINGS.md`, section 2). The two figures are
close but not identical, here and in every other year, because they were measured
at different times: this file records the bar as the search API reported it before
collection, and stars keep accruing between the two runs.