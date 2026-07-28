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

`too_young` is a label rather than NULL: the exclusion is a known methodological
decision, and as a named category it stays visible in the dashboard legend
instead of reading as missing data.

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