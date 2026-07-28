# Findings

Results of the exploratory queries in `sql/exploration.sql`, run against
`data/github_oss.db` (snapshot 2026-07-17). Every figure below is reproducible
from those queries.

---

## 1. Cohort cutoff — no plateau in the data

**Method.** Share of "silent" repos per creation year, where silent means
`days_since_push > X`. Three values of X (180 / 400 / 700) were run rather than
one: X here is a ruler, not a threshold, and running several tests whether the
conclusion depends on the choice.

**Censoring correction.** A repo cannot have been silent for longer than it has
existed. At X = 700 the 2025 cohort returns exactly 0 — not "all alive" but "the
ruler does not fit". Each run therefore filters `age_days > X` so that only repos
that could have answered are counted. This drops 2025 entirely at X = 700 and
2024 partially (504 of 750).

**Silent share by creation year:**

| year | X=180 | X=400 | X=700 |
|------|-------|-------|-------|
| 2024 | 0.228 | 0.119 | 0.042 |
| 2023 | 0.305 | 0.216 | 0.119 |
| 2022 | 0.279 | 0.193 | 0.121 |
| 2021 | 0.307 | 0.229 | 0.155 |
| 2020 | 0.301 | 0.228 | 0.136 |
| 2019 | 0.357 | 0.288 | 0.223 |
| 2018 | 0.377 | 0.300 | 0.239 |
| 2017 | 0.441 | 0.367 | 0.295 |
| 2016 | 0.363 | 0.300 | 0.236 |

**Year-over-year change (percentage points):**

| step | X=180 | X=400 | X=700 |
|------|-------|-------|-------|
| 2020→2019 | +5.6 | +6.0 | +8.7 |
| 2018→2017 | +6.4 | +6.7 | +5.6 |
| 2017→2016 | −7.8 | −6.7 | −5.9 |

**Reading.** The share keeps rising all the way to the oldest cohort. There is a
flat stretch from 2023 to 2020, then a break at 2020/2019, then a second break of
comparable size at 2018/2017. The 2020/2019 break stands out only under the
strictest ruler; under 180 and 400 days it is matched by 2018/2017. The direction
is stable across rulers, the magnitude is not.

**Conclusion.** There is no plateau: outcomes have not settled even after ten
years, so the point at which a repo becomes judgeable cannot be read off the
data. The cohort cutoff is therefore an **explicit assumption justified by
observation period**, not a finding. Section 4 shows the core result is
insensitive to where that cutoff falls.

**Composition hypothesis — rejected.** The flat 2020–2023 stretch could have been
a property of those particular cohorts rather than of age (COVID years, the AI
boom). Checked against `owner_type`: the organisation share stays between 0.50
and 0.59 across all ten years with no trend. 2019 and 2020 have near-identical
composition (0.500 vs 0.512) yet differ almost twofold in silence (0.223 vs
0.136). The effect is age, not composition.

**2017 is anomalous and stays unexplained.** It is quieter than both its
neighbours under all three rulers, and the inversion against 2016 — the older
cohort being the calmer one — is a stable 6–8 points. Three composition checks
were run: minimum and mean stars, share of repos with no language, share of small
teams. 2017 sits mid-range on every one of them. No explanation found; recorded
as an observation. This is the second such case after the 2023 spike in the entry
bar (section 2).

---

## 2. Sample entry bar is not constant across years

Not a threshold decision, but a property of the sample worth stating explicitly.

Minimum stars within the top-750 of each year:

| year | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|------|------|------|------|------|------|------|------|------|------|------|
| min stars | 7055 | 6214 | 5982 | 5464 | 5260 | 3884 | 3807 | 5163 | 3859 | 3837 |

Older cohorts were selected roughly twice as strictly. These figures match
`data/step0/star_threshold.csv`, obtained independently by binary search before
collection — including the 2023 spike — which also confirms the loaded data is
intact.

The effect runs *against* the observed trend: more strictly selected repos should
survive better, yet older cohorts are the quieter ones. The age effect outweighs
the selection effect.

---

## 3. Team size — no boundary in the data

**Method.** Distribution of `contributors` over buckets, cohort 2016–2020.

| bucket | n | values covered | n per value |
|--------|---|----------------|-------------|
| 1 | 97 | 1 | 97 |
| 2 | 74 | 1 | 74 |
| 3–5 | 201 | 3 | 67 |
| 6–10 | 259 | 5 | 52 |
| 11–50 | 1035 | 40 | 26 |
| 51+ | 2084 | — | — |

**Reading.** Raw counts appear to jump at 11–50, but that is bucket width. Per
value the density falls monotonically: 97 → 74 → 67 → 52 → 26. No gap, no
shoulder — a plain long tail.

**Conclusion.** There is no data-driven boundary for "small team". The 1–2 cutoff
used below is a **definition**, not a finding: it is the range where "a single
maintainer" is unambiguous given that the metric counts contributors cumulatively
over the project's whole life. Widening it to 5 or 10 in order to fill cells was
rejected — any such line would be arbitrary, and the point of this cutoff is that
its interpretation is beyond dispute.

---

## 4. Core result — retention gap by team size

Share of repos still active, split by team size, across two cohort cutoffs and
two activity rulers:

| cohort | active if | rest (3+) | small (1–2) | gap |
|--------|-----------|-----------|-------------|-----|
| ≤ 2020 | `days_since_push < 400` | 0.719 (2575/3579) | 0.363 (62/171) | 35.6 pp |
| ≤ 2020 | `days_since_push < 700` | 0.788 (2822/3579) | 0.450 (77/171) | 33.8 pp |
| ≤ 2019 | `days_since_push < 400` | 0.701 (2010/2867) | 0.361 (48/133) | 34.0 pp |
| ≤ 2019 | `days_since_push < 700` | 0.765 (2193/2867) | 0.451 (60/133) | 31.4 pp |

**Reading.** Both shares move with the ruler, the gap does not. It stays within
31–36 points under every combination, and the small-team share barely moves at
all when the cohort boundary shifts (0.363 → 0.361 at 400 days). The result
depends neither on where the activity line is drawn nor on where the cohort
begins — the two weakest points of the methodology.

**Statement.** *Among already-popular repositories in the old cohort, projects run
by one or two contributors remain active roughly half as often as the rest.*

This answers the project's central question with the opposite sign to the
original hypothesis. Single-author long-timers are not absent — 62 of them are
still active — but as a class they retain markedly worse.

---

## 5. The lower edge empties with age

Repos with 1–2 contributors, per creation year (out of 750 each):

| year | 2025 | 2024 | 2023 | 2022 | 2021 | 2020 | 2019 | 2018 | 2017 | 2016 |
|------|------|------|------|------|------|------|------|------|------|------|
| n | 75 | 74 | 66 | 68 | 52 | 38 | 57 | 33 | 30 | 13 |

From about 10% in recent years down to 1.7% in 2016.

**Two readings, not separable from a snapshot:**

1. Solo projects do not survive — a popular one-person project either dies or
   grows a team.
2. A long-lived solo project stops *looking* solo. The metric is cumulative: over
   ten years a handful of drive-by contributors push the count from 1 to 8 while
   one person still does all the work.

Both go in the README. This follows directly from what the contributor count
actually measures: everyone who ever committed, not the size of the team working
today.

---

## 6. Retention class — definition and composition

**Two signals, not four.** Age became the cohort filter rather than a class
signal. Support was dropped: `open_issues` is meaningless unnormalised against
project size, and every available denominator fails — `stars` and `forks` are
proxies for the popularity the sample is selected on, `contributors` is already a
signal in its own right, and `age_days` only measures how long issues have had to
accumulate. Repository size would work but was never collected. So the class
rests on activity and team size.

**Do two signals suffice?** The original concern was that `pushed_at` alone is
fragile — a push can come from a dependency bot. Team size guards against this
only if the two signals disagree often enough, and they do: 36% of small teams
are active while 28% of larger ones are silent (section 4). Correlated, not
redundant.

**Thresholds are assumptions, and stated as such.** Activity is drawn at
`days_since_push < 400` and the cohort at `created_year <= 2020`. Neither follows
from the data — section 1 shows no natural break exists. The justification is
section 4: the core result holds at 31–36 points across both alternatives, so
neither line carries the conclusion. The wider cohort was preferred for the
larger N.

**Only one conflict is a conflict.** Crossing the two signals gives four cells
(cohort ≤ 2020, ruler 400):

| | active | silent |
|---|---|---|
| team 3+ | 2575 | 1004 |
| team 1–2 | 62 | 109 |

Silent-with-a-large-team looks like a conflict but is not: the contributor count
is cumulative, so a project dead for years still carries a high count from people
who passed through long ago. Those 1004 are ordinary fading projects and go to
`faded`. Active-with-a-team-of-two survives any reading of the metric — one or
two people over the entire history is unambiguously solo — and gets its own
class.

**Resulting distribution:**

| class | condition | n |
|-------|-----------|---|
| `too_young` | `created_year > 2020` | 3750 |
| `faded` | `days_since_push >= 400` | 1113 |
| `active_small_team` | active, `contributors <= 2` | 62 |
| `retained` | active, larger team | 2575 |

**Why `too_young` is a label and not NULL.** The original reason given — that a
named category stays visible in the dashboard legend — does not hold: page 2 is
filtered to `created_year <= 2020`, so the label never appears in that legend at
all. Two reasons that do hold:

1. NULL arrives in Power BI as `(Blank)`, behaves differently inside measures,
   and reads as missing data in exactly the place where a deliberate
   methodological exclusion is being shown.
2. It makes the column self-checking. After `classify.py` there are no empty
   values anywhere, verifiable by a single `COUNT(*) WHERE retention_class IS
   NULL`. With NULL for young repos, "excluded by methodology" would be
   indistinguishable from "the script did not run".

The legend argument becomes true only on page 1, where a visual showing what
share of the sample enters the retention analysis is planned. That is a bonus,
not the justification.

**Caveats on `active_small_team`.** Reviewing all 62 by description showed the
class mixes project types:

- Most are what the question was about: popular libraries and applications
  maintained by one or two people for years (`ethers.js`, `legado`, `screenity`,
  `BBDown`, `MaterialFiles`).
- Some are curated lists, tutorials and corpora, where a push means adding an
  entry, not development.
- Three are automated: `trackerslist`, `PoC-in-GitHub` and Unity's source dump
  push on a schedule, not by hand. There is no field that distinguishes automated
  pushes from human ones — these were spotted by description, and others may
  remain.

The class is kept whole for the statistics: a link list maintained for five years
is genuine retention, merely of a different kind, and removing it from the
numerator while leaving the denominator intact would deflate the small-team share
by construction. For named examples on the dashboard the subset with a defined
`language` is used (42 of 62) — where no code is in the repository, `pushed_at`
does not stand for development.

---

## 7. No workable segmentation inside organisations

A second segmentation level inside organisations was considered: a flag for
major tech corporations, set from a frozen external ranking. Two criteria were
tested and both failed.

**Market capitalisation.** A ranking by company value answers "how expensive is
this company", not "how large a player is it in open source". Apache, Mozilla and
the Linux Foundation are not companies at all; Red Hat, JetBrains and Vercel are
far outside any capitalisation top list yet visible here; Berkshire Hathaway and
Saudi Aramco would be inside it with zero repositories in the sample.

**Repository count within the sample.** The alternative was to define the flag
from the data — organisations with the most repos in the sample. Counts run 101,
41, 40, 32, 28, 27, 27, 24, 19, 17, 16 … 8. Only one gap exists, between
Microsoft and everyone else; below that the decline is smooth, so any cutoff
would be arbitrary. The criterion also fails to remove the manual step it was
meant to avoid: `facebookresearch` (41) and `facebook` (11) are one company, as
are `google` (40) and `google-deepmind` (9), and collapsing logins to companies
is still a judgement call.

**Decision.** Segmentation stays on `owner_type` (organisation vs individual),
which comes free from the API and needs no external source or manual mapping.
No finer split inside organisations is supportable from what is available.

**Side observation.** The top of the organisation list is almost entirely AI:
`openai`, `huggingface`, `deepseek-ai`, `anthropics`, `QwenLM`, `langchain-ai`,
`google-deepmind`, `modelcontextprotocol`. These sit in recent cohorts and are
classified `too_young`, so they carry no weight in the retention analysis — but
they are context for the language and ecosystem trends.

---

## 8. Censoring on the activity axis

Section 1 applied a censoring correction to a table. The same correction has to
be applied again when the same values become a chart axis, and it lands
differently there.

**The constraint.** A repo cannot have been silent for longer than it has
existed, so a point's `days_since_push` is capped by its own `age_days`. On a
scatter with `days_since_push` on Y, the upper region is reachable only by the
older part of the cohort — not because old repos go quiet more often, but
because young ones cannot physically get there.

**Measurements (cohort ≤ 2020, 3750 repos):**

| quantity | value |
|---|---|
| `age_days` range | 2023 … 3847 |
| `days_since_push` range | 0 … 3024 |
| repos above 2023 days of silence | 72 (1.9%) |
| 95th percentile of `days_since_push` | 1414 |

**Where the axis stops being trustworthy: 2023 days.** Below it every repo in
the cohort could appear; above it only those old enough, which is a selection on
precisely the variable the chart invites conclusions about.

**The classification is unaffected.** The activity threshold of 400 days sits far
below 2023, so every repo in the cohort had a full opportunity to fall on either
side of it. `retention_class` carries no censoring. The distortion is purely
visual and confined to the upper third of the axis, where 1.9% of the points sit.

**Why the axis is not truncated.** Cutting Y at the 95th percentile was
considered and rejected. In Power BI, points outside a manually set axis maximum
are not clamped to the edge — they are not drawn at all, so 188 repos would
disappear without leaving a trace. That is worse than the problem it solves: a
visible cluster at the top edge at least prompts a question. *(To be confirmed
against the actual rendering when the dashboard is built.)*

**Decision — logarithmic Y axis.** Nothing is removed and no artificial cluster
is created; the tail compresses and the mass between 0 and 400 days, which would
otherwise occupy the bottom 13% of the plot, takes up most of the height. Two
consequences to state on the visual itself:

- `MIN(days_since_push) = 0`, which a log scale cannot render. The axis uses
  `days_since_push + 1`, a **calculated column in Power BI, not in SQLite**: the
  shift exists because of how the renderer behaves, not because of anything in
  the data, and the database should not carry a column that only makes sense
  downstream. Half a line in the README covers it.
- A log axis is harder to read — the distance from 10 to 100 equals the distance
  from 100 to 1000. The axis label must say so outright rather than leave the
  reader to infer it from uneven gridlines.

The alternative kept in reserve is a plain linear axis over the full 0–3024
range: visually poor, analytically flawless, and requiring no caveat at all.

---

## 9. Choosing the colour variable for the main scatter

**The problem.** `retention_class` is a deterministic function of
`days_since_push` and `contributors` — both of which are the scatter's axes.
Colouring points by it produces three rectangular blocks divided by the lines
x = 2 and y = 400. No point can land outside its own colour; the colour shows
where the thresholds were drawn, not anything about the data. Colour therefore
has to carry a variable that is not part of the axes, not part of the class
definition, and not a proxy for the popularity the sample was selected on.

The class boundaries stay on the chart as **annotation lines**, which is what
they are.

**Test used for every candidate.** Compare the outcome across the candidate's
values *within a narrow band of `contributors`*. Comparing across the whole
cohort mixes the candidate's own effect with team size, which is the X axis. A
difference below **10 percentage points** was fixed in advance as noise — the
smallest cells hold a few dozen repos.

### 9.1 `owner_type` — rejected

Share of organisations among active vs silent repos, cohort ≤ 2020:

| band | active | silent | gap |
|---|---|---|---|
| all `team 3+` | 0.630 (1623/2575) | 0.379 (381/1004) | +25.1 pp |
| 3–10 | 0.185 (30/162) | 0.232 (69/298) | −4.7 pp |
| 11–50 | 0.362 (211/583) | 0.338 (153/452) | +2.4 pp |
| 51+ | 0.755 (1379/1827) | 0.626 (159/254) | +12.9 pp |
| 51–200 | 0.665 (686/1031) | 0.589 (116/197) | +7.6 pp |
| 201–1000 | 0.862 (601/697) | 0.764 (42/55) | +9.8 pp |
| 1001+ | 0.929 (92/99) | n = 2 | not computable |

**Reading.** The 25-point gap on the wide bucket does not survive
stratification: it falls to 12.9 within 51+, then to 7.6 and 9.8 as the band
narrows further, and reverses sign in the smallest band. The mechanism is
composition. The organisation share rises steeply with team size (0.215 → 0.352 →
0.739 across the three bands), while active repos are concentrated in the large
band (1827 active vs 254 silent) and silent ones in the small band (162 vs 298).
Pooling the two produces a gap that reports "active repos are larger, and large
repos belong to organisations", not "organisations retain better".

`owner_type` describes the **size** of a project, not its survival. As colour on
an axis of team size it would restate X.

### 9.2 `created_year` — rejected

Above 2023 days of silence the colour would be fully determined by the Y
coordinate (section 8), and below it the two remain linked through the age effect
of section 1. Weaker than the `owner_type` failure — the hard determination
covers 72 points — but it would display what sections 1 and 5 already state.

### 9.3 `language` — accepted

Share still active (`days_since_push < 400`), cohort ≤ 2020, languages with
n ≥ 50:

| language | n | share | language | n | share |
|---|---|---|---|---|---|
| Rust | 172 | 0.901 | Swift | 65 | 0.708 |
| Go | 365 | 0.890 | Python | 606 | 0.675 |
| TypeScript | 487 | 0.860 | Shell | 90 | 0.667 |
| C# | 99 | 0.828 | HTML | 87 | 0.655 |
| C++ | 194 | 0.820 | Java | 192 | 0.583 |
| C | 108 | 0.759 | Vue | 50 | 0.580 |
| | | | JavaScript | 410 | 0.568 |
| | | | Jupyter Notebook | 110 | 0.464 |

A spread of 44 points — wider than the project's core result. Two competing
explanations were tested.

**Age — rejected.** Mean `created_year` per language spans 0.65 of a year in
total (2017.70 for Java and C, 2018.35 for Rust). At roughly 6 points of silence
per cohort year (section 1), age can account for about 4 of the 44 points. The
orderings also disagree: Python is second youngest and eighth by retention,
Jupyter Notebook fifth youngest and last.

**Team size — tested and survived.** Median team size per language does track the
retention ranking closely (Rust 145.5, Go 125, TypeScript 109 at the top;
Jupyter Notebook 16 at the bottom), so the effect was re-checked inside bands of
`contributors`:

| band | Rust | Go | JavaScript | Jupyter Notebook |
|---|---|---|---|---|
| 3–10 | n < 20 | 0.450 (20) | 0.339 (56) | 0.226 (31) |
| 11–50 | 0.750 (28) | 0.692 (65) | 0.483 (143) | 0.486 (37) |
| 51+ | 0.935 (139) | 0.975 (276) | 0.708 (195) | 0.793 (29) |

**Reading.** The ordering is the same in all three bands and the gap between the
top pair and the bottom pair holds at roughly 21–27 points — it does not decay as
the band narrows, which is exactly how `owner_type` failed. Team size is also
visibly at work *within* each language (JavaScript 0.339 → 0.483 → 0.708), so the
two effects are independent: X and colour show different things.

**Caveats.** Four languages from the ends of the ranking were tested; the middle
(Python, TypeScript, Java, C++) was not. Rust has fewer than 20 repos in the
3–10 band and drops out there.

### 9.4 Palette: K = 7, explicit assumption

Repo counts per language in the cohort: Python 606, TypeScript 487, JavaScript
410, *(no language)* 374, Go 365, C++ 194, Java 192, Rust 172, Jupyter Notebook
110, C 108, C# 99, Shell 90, HTML 87, Swift 65, Vue 50, Kotlin 48, PHP 38 …

The sharpest break in the distribution is 365 → 194, which would give K = 4. It
was **not** taken: that boundary excludes Rust, the retention leader and the
language carrying the verified effect in section 9.3. K = 7 (Python, TypeScript,
JavaScript, Go, C++, Java, Rust) plus an "other" bucket is a content-driven
boundary, recorded here as an **explicit assumption** in the same sense as the
cohort cutoff — not found in the data, and named rather than dressed up.

Of the seven, only Rust, Go and JavaScript were put through the stratification
test.

### 9.5 `language = NULL` — grey, outside the legend

374 repos, 10% of the cohort, are documentation projects with no code. Three
reasons they do not get a colour of their own:

- Section 6 already establishes that `pushed_at` there means adding an entry to
  a list, not development — their Y coordinate does not mean the same thing as
  everyone else's, and an equal place in a legend of languages would assert that
  it does.
- Seven languages plus "other" is already the readable ceiling for a scatter of
  3750 points; a ninth category would not be distinguishable inside the dense
  core of the cloud.
- The fact is more interesting on its own than as a shade. "374 of 3750 repos in
  the cohort contain no code" belongs on page 1 as a stated number, where it is
  legible, rather than buried as the ninth colour.

They stay on the chart in neutral grey with a note, so the density is visible and
no share is silently recomputed on a smaller denominator.

### 9.6 Resulting design of the main visual

| channel | variable | note |
|---|---|---|
| X | `contributors`, log | label: "contributors over the project's lifetime" |
| Y | `days_since_push + 1`, log | calculated column in Power BI; label states the log scale |
| colour | `language`, top 7 + other | NULL in grey, outside the legend |
| annotation | x = 2, y = 400 | class boundaries as lines, not as colour |

---

## 10. Data quality — language spelling collision

Found while building the Power BI model, not during analysis: the relationship
`repositories → languages` could not be created because the dimension contained
duplicate keys.

**Cause.** GitHub renames languages in linguist over time (`Matlab` → `MATLAB`,
`Vim script` → `Vim Script`). The `language` field is set when a repository is
analysed and is not rewritten afterwards, so older repos carry the old spelling.
SQLite compares text case-sensitively and accepted both as distinct primary keys;
VertiPaq does not, and rejected the dimension.

**Scale.** Two languages, 9 repos of 7500: MATLAB 3 / Matlab 1, Vim Script 4 /
Vim script 1. Neither is in the top-7 palette, and the split is uneven rather
than aligned with the rename date — so no year-over-year trend is distorted and
no figure in sections 1–9 changes.

**Fix.** Normalised in `load.py`, on both the fact and the dimension in one pass,
so the two cannot diverge. The surviving spelling is the more frequent one within
a case-insensitive group, with the name as tie-break: frequency alone is
undefined at equal counts, and a rebuild must not be able to produce a different
legend label from the same input. Lowercasing everything was rejected — `C#`,
`C++` and `Objective-C` carry meaning in their case, and these strings end up as
legend labels.

No guard was added for future collisions: the frequency rule absorbs a new
spelling on the next rebuild, so there is nothing to fail on. A hardcoded mapping
would have needed one.