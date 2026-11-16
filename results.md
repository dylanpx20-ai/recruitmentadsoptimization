# NYC Recruitment Advertising Simulation — Results

## Executive Summary

This project evaluates how a fictional New York City employer could manage a monthly recruitment advertising budget across 10 open positions using AI-assisted Python and Monte Carlo simulation.

The model tested **36 scenarios**, combining three cost-per-click (CPC) environments, three budget levels, and four campaign allocation strategies.

Each scenario was simulated 50,000 times, producing **1,800,000 simulated campaign months in 137.8 seconds** using Google Colab.

### Key Findings

- **Performance-First generated the highest median number of completed applications in all nine budget/CPC combinations.**
- **Priority-Weighted was selected by the recommendation engine**, which emphasizes combined budget pacing and job-category coverage rather than application volume alone.
- **Low CPC:** The model recommends increasing the monthly budget from $3,000 to $3,600.
- **Moderate and High CPC:** The model recommends maintaining the $3,000 budget while investigating opportunities to improve campaign performance.
- **Higher spending generally produced more applications**, but additional volume alone was not sufficient to justify a budget increase under the model's decision criteria.

All results are based on synthetic assumptions, not actual Indeed advertising data.

---

## 1. Simulation Setup

| Parameter | Value |
|---|---|
| Advertising platform | Indeed (illustrative) |
| Market | New York City |
| Open positions | 10 across 6 job categories |
| Campaign duration | 30 days |
| Starting monthly budget | $3,000 |
| Budget alternatives | $2,400 / $3,000 / $3,600 |
| CPC environments | $8 / $15 / $25 |
| Allocation strategies | Equal, Performance-First, Priority-Weighted, Adaptive |
| Simulations per scenario | 50,000 |
| Total scenarios | 36 |
| Total simulated campaign months | 1,800,000 |
| Execution time | 137.8 seconds |

### CPC Environments

| Environment | Assumed Base CPC |
|---|---:|
| Low | $8 |
| Moderate | $15 |
| High | $25 |

These CPCs are illustrative planning assumptions. Actual recruitment advertising costs vary by job category, competition, location, and campaign conditions.

### Budget Alternatives

| Budget Decision | Monthly Budget | Change |
|---|---:|---:|
| Reduce | $2,400 | −20% |
| Maintain | $3,000 | Baseline |
| Increase | $3,600 | +20% |

---

## 2. Complete Simulation Results — All 36 Scenarios

The following tables report the **median number of completed applications** generated across 50,000 simulated campaign months for each scenario.

### Low CPC Environment — $8

| Scenario | Budget Decision | Monthly Budget | Allocation Strategy | Median Applications |
|---|---|---:|---|---:|
| 01 | Reduce | $2,400 | Equal | 27 |
| 02 | Reduce | $2,400 | Performance-First | **35** |
| 03 | Reduce | $2,400 | Priority-Weighted | 25 |
| 04 | Reduce | $2,400 | Adaptive | 26 |
| 05 | Maintain | $3,000 | Equal | 34 |
| 06 | Maintain | $3,000 | Performance-First | **43** |
| 07 | Maintain | $3,000 | Priority-Weighted | 31 |
| 08 | Maintain | $3,000 | Adaptive | 33 |
| 09 | Increase | $3,600 | Equal | 40 |
| 10 | Increase | $3,600 | Performance-First | **51** |
| 11 | Increase | $3,600 | Priority-Weighted | 37 |
| 12 | Increase | $3,600 | Adaptive | 39 |

**Finding:** Performance-First generated the highest median application volume at every budget level.

At the $3,000 baseline, Performance-First produced 43 median applications, compared with 31 under Priority-Weighted.

Increasing the budget to $3,600 raised Performance-First's median application count to 51.

### Moderate CPC Environment — $15

| Scenario | Budget Decision | Monthly Budget | Allocation Strategy | Median Applications |
|---|---|---:|---|---:|
| 13 | Reduce | $2,400 | Equal | 15 |
| 14 | Reduce | $2,400 | Performance-First | **21** |
| 15 | Reduce | $2,400 | Priority-Weighted | 14 |
| 16 | Reduce | $2,400 | Adaptive | 15 |
| 17 | Maintain | $3,000 | Equal | 19 |
| 18 | Maintain | $3,000 | Performance-First | **25** |
| 19 | Maintain | $3,000 | Priority-Weighted | 17 |
| 20 | Maintain | $3,000 | Adaptive | 18 |
| 21 | Increase | $3,600 | Equal | 22 |
| 22 | Increase | $3,600 | Performance-First | **29** |
| 23 | Increase | $3,600 | Priority-Weighted | 20 |
| 24 | Increase | $3,600 | Adaptive | 21 |

**Finding:** Application volume decreased substantially compared with the low-CPC environment.

At the $3,000 baseline, Performance-First generated 25 median applications, while Priority-Weighted generated 17.

Increasing spending produced additional applications, but the model did not find sufficient improvement under its combined decision criteria to recommend a higher budget.

### High CPC Environment — $25

| Scenario | Budget Decision | Monthly Budget | Allocation Strategy | Median Applications |
|---|---|---:|---|---:|
| 25 | Reduce | $2,400 | Equal | 9 |
| 26 | Reduce | $2,400 | Performance-First | **13** |
| 27 | Reduce | $2,400 | Priority-Weighted | 8 |
| 28 | Reduce | $2,400 | Adaptive | 9 |
| 29 | Maintain | $3,000 | Equal | 12 |
| 30 | Maintain | $3,000 | Performance-First | **16** |
| 31 | Maintain | $3,000 | Priority-Weighted | 10 |
| 32 | Maintain | $3,000 | Adaptive | 11 |
| 33 | Increase | $3,600 | Equal | 14 |
| 34 | Increase | $3,600 | Performance-First | **19** |
| 35 | Increase | $3,600 | Priority-Weighted | 12 |
| 36 | Increase | $3,600 | Adaptive | 14 |

**Finding:** Higher CPCs significantly restricted application volume within the available budget.

At the $3,000 baseline, Performance-First generated 16 median applications, compared with 10 under Priority-Weighted.

Even with a $3,600 budget, Performance-First generated only 19 median applications.

This demonstrates how rising click costs can limit applicant acquisition, even when the employer increases advertising investment.

---

## 3. Comparing Application Volume Across CPC Environments

The table below compares median applications at the original **$3,000 monthly budget**.

| Allocation Strategy | Low CPC | Moderate CPC | High CPC |
|---|---:|---:|---:|
| Equal | 34 | 19 | 12 |
| Performance-First | **43** | **25** | **16** |
| Priority-Weighted | 31 | 17 | 10 |
| Adaptive | 33 | 18 | 11 |

### What the Results Show

**Performance-First consistently maximized total application volume.**

However, directing spending toward the most efficient job categories may leave other openings with insufficient applicant coverage.

Priority-Weighted generated fewer total applications but was selected by the model's broader decision framework, which evaluates job-category coverage and budget pacing.

This illustrates a practical account management trade-off:

**Generating the highest total number of applications does not necessarily mean every open position is receiving adequate advertising support.**

---

## 4. Final Budget Recommendations

The simulation's recommendation engine evaluates budget alternatives using combined pacing and job-coverage criteria, alongside qualified application volume and cost efficiency.

| CPC Environment | Recommendation | Monthly Budget | Preferred Strategy | Joint Success Probability | Median Qualified Applications |
|---|---|---:|---|---:|---:|
| Low ($8) | **Increase** | $3,600 | Priority-Weighted | 48.41% | 14 |
| Moderate ($15) | **Maintain** | $3,000 | Priority-Weighted | 0.63% | 6 |
| High ($25) | **Maintain** | $3,000 | Priority-Weighted | 0.00% | 4 |

*Joint success probability is the modeled likelihood of satisfying the simulation's combined budget pacing and job-category coverage criteria. It is not a hiring probability.*

### Low CPC: Increase to $3,600

Under the low-CPC environment, the model recommends increasing the budget by 20%.

The additional spending improves modeled campaign success and qualified application volume without disproportionate growth in cost per qualified application (CPQA).

At lower click costs, additional budget can generate more advertising traffic and potentially more completed applications.

However, the recommendation depends on the model's combined performance criteria, not simply on CPC being low.

### Moderate CPC: Maintain at $3,000

Under moderate CPC conditions, the model recommends maintaining the existing budget.

Although additional spending increases median application volume, neither the budget reduction nor increase meets the model's predefined evidence thresholds for changing spending.

The recommendation is to maintain the budget while evaluating campaign performance and identifying opportunities to improve applicant conversion.

### High CPC: Maintain at $3,000

Under high CPC conditions, the model also recommends maintaining the existing budget.

With clicks costing substantially more, additional spending produces relatively limited application gains.

The model's joint success probability of 0.00% indicates that the selected scenario did not meet its combined pacing and coverage criteria in the simulation runs.

This does not mean the campaign has no value. It means that the modeled campaign struggles to meet its specific combined objectives under high-CPC conditions.

---

## 5. Account Management Interpretation: Why More Budget Is Not Always the Answer

A key takeaway from this simulation is that **underperforming recruitment advertising campaigns do not automatically need additional spending**.

Higher CPCs reduce the number of clicks a fixed budget can purchase, but low application volume can also reflect issues beyond advertising investment.

Before recommending a budget increase, an account manager should investigate:

- **Job description quality:** Are responsibilities, requirements, and expectations clearly communicated?
- **Application experience:** Is the application process unnecessarily complicated? Could a streamlined experience, such as Indeed Apply where available, reduce friction?
- **Compensation competitiveness:** Is the advertised salary competitive for the NYC job market?
- **Job requirements:** Are restrictive qualifications or scheduling requirements discouraging otherwise suitable candidates?
- **Application conversion:** Are candidates clicking the job advertisement but failing to complete an application?
- **Budget allocation:** Are some openings consuming advertising spend without generating sufficient applications?

These are potential explanations to investigate, not issues diagnosed by the simulation itself.

### Recommended Account Management Approach

For moderate and high CPC environments, the model's recommendation is to maintain the budget rather than immediately increase spending.

From an account management perspective, the next step would be to review job descriptions, application conversion, campaign allocation, and employer expectations before proposing additional investment.

**Increasing advertising spend may generate more clicks, but it will not automatically correct problems with the job posting or application experience.**

This distinction is especially important when advising employers on how to improve recruitment advertising performance.

---

## 6. Limitations and Model Interpretation

This analysis is based entirely on synthetic assumptions and is intended to demonstrate quantitative decision-making rather than forecast actual Indeed advertising results.

Important limitations include:

- CPC, traffic availability, application conversion, and qualification probabilities are simulated.
- The results are not based on proprietary Indeed campaign data.
- Median application counts describe modeled outcomes, not guaranteed results.
- The recommendation engine prioritizes combined pacing and coverage criteria, which may differ from a business objective focused exclusively on total applications.
- Potential issues such as job description quality, compensation competitiveness, and application friction are not independently diagnosed by the model.
- Qualified application outcomes are simulated, not verified through an applicant tracking system.
- Hiring outcomes and cost per hire are excluded because employer-controlled screening and hiring decisions extend beyond advertising campaign performance.

The results should be interpreted as **scenario-based planning insights**, not causal evidence that a specific budget change will produce the same outcome in a real campaign.

---

## 7. Final Conclusion

Across 1.8 million simulated campaign months, the analysis demonstrates how CPC conditions, advertising budgets, and allocation strategies influence recruitment advertising outcomes.

**Performance-First consistently produced the highest median application volume**, while the model's combined pacing and job-coverage criteria favored Priority-Weighted.

The final recommendations were:

| CPC Environment | Budget Decision |
|---|---|
| Low | Increase to $3,600 |
| Moderate | Maintain at $3,000 |
| High | Maintain at $3,000 |

The broader lesson is that **effective recruitment advertising account management requires both quantitative analysis and business judgment**.

Monte Carlo simulation can help evaluate uncertainty and compare budget alternatives, but account managers must also consider job posting quality, application experience, and employer needs before recommending additional spending.

The goal is not simply to spend more advertising dollars. It is to generate meaningful application volume efficiently while supporting the employer's open positions.
