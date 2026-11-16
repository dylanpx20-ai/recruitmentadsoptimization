# NYC Recruitment Advertising Optimization
### AI-Assisted Monte Carlo Simulation | Python | Campaign Pacing & Budget Strategy

## Project Overview

How should a recruitment advertising account manager allocate a limited monthly budget across multiple job openings while balancing application volume, cost efficiency, and campaign pacing?

This project uses **AI-assisted Python development and Monte Carlo simulation** to explore that question for a fictional New York City employer advertising 10 open positions on Indeed.

The employer has a **$3,000 monthly advertising budget** and must decide whether to reduce, maintain, or increase spending based on simulated campaign performance.

The model evaluates 36 combinations of CPC environments, budget levels, and campaign management strategies, running **1.8 million simulated campaign months in approximately 138 seconds**.

All campaign inputs are synthetic. This is an independent educational project, not an analysis of actual Indeed campaign data.

---

## Business Objective

The primary objective is to **generate completed job applications across 10 open positions** while maintaining responsible budget pacing and efficient cost per application (CPA).

The simulation also evaluates applicant qualification, job-level application coverage, and the potential value of additional advertising spend.

The final business decision is straightforward:

**Should the employer reduce, maintain, or increase its $3,000 monthly advertising budget?**

## Employer and Campaign Setup

| Campaign Parameter | Value |
|---|---|
| Employer | Fictional NYC company |
| Advertising platform | Indeed (illustrative) |
| Campaign duration | 30 days |
| Monthly budget | $3,000 |
| Open positions | 10 |
| Job categories | 6 |
| CPC environments | Low, Moderate, High |
| Budget strategies | 4 |
| Total scenarios | 36 |
| Monte Carlo iterations | 50,000 per scenario |
| Total simulated campaign months | 1,800,000 |

### Open Positions

| Job Category | Openings |
|---|---:|
| HR Representative | 3 |
| Sales Account Executive | 2 |
| Accountant | 2 |
| Janitor | 1 |
| Operations Manager | 1 |
| Administrative Assistant | 1 |
| **Total** | **10** |

Different job categories have different assumed click costs, application conversion rates, qualification rates, and applicant traffic availability.

These differences create a realistic *allocation problem* within the hypothetical campaign: the lowest-cost applications may not come from the openings most in need of advertising support.

---

## CPC Environments

The simulation tests three advertising cost environments.

| Environment | Base CPC | Description |
|---|---:|---|
| Low | $8 | Relatively efficient traffic |
| Moderate | $15 | Higher acquisition costs |
| High | $25 | Expensive, competitive traffic |

These are illustrative planning assumptions informed by the project's recruitment advertising context, not verified Indeed pricing benchmarks.

Individual job categories receive CPC multipliers, and actual simulated CPC varies probabilistically.

At a $3,000 budget, the base CPCs correspond to approximately 375, 200, and 120 clicks respectively, before accounting for job-level cost differences, daily volatility, and traffic constraints.

## Budget Alternatives

Three monthly budget levels are evaluated:

| Decision | Budget | Change |
|---|---:|---:|
| Reduce | $2,400 | −20% |
| Maintain | $3,000 | No change |
| Increase | $3,600 | +20% |

The model evaluates whether changing the budget improves campaign outcomes enough to justify the additional spending or reduced coverage.

---

## Campaign Management Strategies

Four approaches are simulated.

### 1. Equal Allocation

Distributes the budget proportionally to the number of openings in each job category.

This provides a simple baseline for comparison.

### 2. Performance-First

Adjusts budget allocation toward job categories demonstrating stronger observed application efficiency.

Its primary advantage is potentially generating more total applications per advertising dollar.

### 3. Priority-Weighted

Allocates more spending toward job categories based on predefined business priority and the number of openings.

This strategy emphasizes job-level coverage rather than application volume alone.

### 4. Adaptive

Updates allocations weekly using observed application performance, campaign progress, and job priorities.

This strategy attempts to respond dynamically to changing conditions throughout the month.

All strategies preserve a minimum allocation for each job category to prevent the model from completely neglecting individual openings.

---

## Monte Carlo Methodology

The Python simulation uses NumPy to model uncertainty across 30-day advertising campaigns.

Key modeled variables include:

- **Cost per click:** Lognormal variation across campaigns and days.
- **Available traffic:** Daily click supply varies by job category.
- **Application conversion:** Binomial outcomes based on probabilistic apply rates.
- **Applicant qualification:** Binomial outcomes based on assumed qualification probabilities.
- **Budget pacing:** Daily spending is constrained by remaining budget, available traffic, and click costs.
- **Allocation updates:** Performance-based strategies adjust spending weights weekly.

Each scenario is simulated 50,000 times.

Rather than reporting a single deterministic forecast, the model produces distributions of possible application counts, costs, and campaign delivery outcomes.

### Key Performance Indicators

| KPI | Purpose |
|---|---|
| Applications | Primary campaign output |
| Cost per Application (CPA) | Application acquisition efficiency |
| Qualified Applications | Secondary quality measure |
| Cost per Qualified Application (CPQA) | Quality-adjusted advertising efficiency |
| Budget Utilization | Percentage of monthly budget spent |
| Daily Pacing | Spending progression across 30 days |
| Early Budget Exhaustion | Risk of running out of usable budget before month-end |
| Job-Level Coverage | Whether job categories receive sufficient applications |
| Joint Success Probability | Probability of meeting both modeled pacing and coverage criteria |

In the script, healthy coverage requires at least one application in every job category and meeting the application targets for at least five of the six categories. Healthy pacing requires at least 90% budget utilization without early effective exhaustion.

These are project-defined success criteria, not universal recruitment advertising standards.

---

## Simulation Results

The complete run evaluated **36 scenarios with 50,000 iterations each**, finishing in **137.8 seconds** in Google Colab.

### Median Applications at the $3,000 Budget

| CPC Environment | Equal | Performance-First | Priority-Weighted | Adaptive |
|---|---:|---:|---:|---:|
| Low | 34 | **43** | 31 | 33 |
| Moderate | 19 | **25** | 17 | 18 |
| High | 12 | **16** | 10 | 11 |

**Performance-First generated the highest median application volume across all three CPC environments.**

However, maximizing total applications is not the only consideration. The employer must also maintain advertising coverage across different openings and manage spending throughout the month.

### Final Budget Recommendations

| CPC Environment | Recommendation | Monthly Budget | Selected Strategy |
|---|---|---:|---|
| Low ($8) | **Increase** | $3,600 | Priority-Weighted |
| Moderate ($15) | **Maintain** | $3,000 | Priority-Weighted |
| High ($25) | **Maintain** | $3,000 | Priority-Weighted |

The recommendation engine prioritizes the probability of meeting its combined pacing and role-coverage criteria, using qualified application volume as a secondary selection measure.

It then compares the budget alternatives against predefined improvement thresholds.

### Why Increase the Budget in the Low-CPC Environment?

At lower click costs, additional advertising spending can purchase more traffic and generate additional applications relatively efficiently.

In the low-CPC simulation, the increase to $3,600 passed the model's thresholds for improved joint success probability, higher qualified application volume, and acceptable CPQA growth.

The recommendation is therefore to increase spending by 20%.

This does **not** mean low CPC alone justifies a budget increase. The decision also depends on application conversion, job-level coverage, and the incremental value of additional spending.

### Why Maintain the Budget in Moderate and High CPC Environments?

At higher CPCs, the $3,000 monthly budget purchases fewer clicks, limiting the potential volume of applications.

However, **increasing the advertising budget is not always the correct response to underperformance**.

Low application volume may reflect factors beyond advertising spend, including:

- **Job description quality:** Unclear responsibilities, unrealistic requirements, or poorly written job descriptions may discourage applicants.
- **Application experience:** A lengthy or complicated application process may reduce completed applications. Reviewing whether Indeed Apply or a streamlined application experience is available could help identify friction.
- **Compensation competitiveness:** Salary expectations in the NYC market may influence whether candidates choose to apply.
- **Job requirements:** Restrictive qualifications, scheduling expectations, or on-site requirements may reduce applicant interest.
- **Campaign optimization:** Budget distribution, job targeting, and differences in role-level performance may create opportunities for improvement without additional spending.

In the moderate and high CPC environments, the simulation does not find sufficient evidence under its predefined decision rules to justify changing the monthly budget.

**The recommendation is to maintain the $3,000 budget while investigating application conversion, job description quality, application friction, and role-level performance before considering additional investment.**

These potential issues are operational explanations to investigate, not causes identified or proven by the simulation.

The central account management principle is simple:

**More advertising spend cannot automatically solve problems within the applicant experience.**

---

## Business Interpretation

The simulation highlights an important distinction in recruitment advertising:

**The strategy producing the most applications is not always the strategy providing the best coverage across an employer's open positions.**

Performance-First generated the highest overall application counts, while the model's decision framework selected Priority-Weighted because it emphasizes the combined pacing and coverage objectives.

This illustrates a common account management trade-off: concentrating spending on efficient job categories can improve aggregate results while potentially leaving other openings underserved.

The simulation also demonstrates why a budget recommendation should be based on incremental campaign value rather than CPC or spend rate alone.

## Why Cost per Hire Is Excluded

Cost per hire (CPH) is intentionally excluded from the simulation.

Although recruitment advertising influences the number and potential quality of applicants entering the recruitment funnel, it does not independently determine hiring outcomes.

Employer-controlled factors such as screening, interviews, hiring manager decisions, compensation, offers, and candidate acceptance all influence whether an application results in a hire.

For that reason, this project focuses on **advertising performance and applicant generation**, rather than attributing hiring outcomes to the advertising platform.

---

## Visualizations

The Python script generates five PNG charts:

- `01_pacing_low.png` — 30-day budget pacing in the low-CPC environment
- `01_pacing_moderate.png` — 30-day budget pacing in the moderate-CPC environment
- `01_pacing_high.png` — 30-day budget pacing in the high-CPC environment
- `02_joint_success_comparison.png` — Comparison of pacing and coverage success probabilities
- `03_budget_alternatives.png` — Median applications across budget alternatives

These visualizations help explain how spending behavior and application outcomes change under different assumptions.

## Generated Datasets

The simulation also exports four CSV files:

| File | Contents |
|---|---|
| `scenario_summary.csv` | Scenario-level application, cost, pacing, and coverage statistics |
| `daily_pacing.csv` | Average daily and cumulative spending by scenario |
| `role_level_results.csv` | Job-category-level spending and application outcomes |
| `budget_recommendations.csv` | Final budget decisions and supporting explanations |

Together, these datasets support further analysis and reproducibility.

---

## Running the Simulation

The project uses Python with NumPy, pandas, and matplotlib.

Install the dependencies:

```bash
pip install numpy pandas matplotlib
```

Run the simulation:

```bash
python nyc_job_ads_simulation.py
```

By default, the script runs 50,000 Monte Carlo iterations for each of the 36 scenarios.

For a smaller test run:

```bash
python nyc_job_ads_simulation.py --iterations 1000
```

The script is also compatible with Google Colab and saves its output files to a `jobads_results` directory by default.

## AI-Assisted Development

This project was developed with assistance from **OpenAI's GPT-6** for Python implementation, simulation design, statistical modeling, and analytical interpretation.

NumPy executes the Monte Carlo simulations, pandas organizes the results, and matplotlib generates the visualizations.

AI-assisted development makes it possible to rapidly prototype and test quantitative business scenarios, while the assumptions, methodology, and outputs remain open to review.

## Limitations

This project is an educational simulation and should not be interpreted as a validated forecast of Indeed campaign performance.

Important limitations include:

- All CPC, conversion, qualification, and traffic assumptions are synthetic.
- The model does not use proprietary Indeed advertising data.
- Actual sponsored-job campaign delivery and pricing may behave differently.
- Qualification outcomes are modeled rather than verified through employer applicant tracking systems.
- The budget recommendation depends on predefined thresholds and project-specific success criteria.
- The simulation does not establish that increasing a real campaign budget would cause the modeled improvements.
- Job-level demand, candidate behavior, and employer requirements may differ substantially from the fictional scenario.

The results should therefore be interpreted as **conditional outcomes under stated assumptions**, not guaranteed advertising performance.

---

## Key Takeaway

**Recruitment advertising optimization requires more than minimizing CPC or CPA.**

A successful campaign must generate applications, maintain coverage across different job openings, and use its advertising budget responsibly throughout the month.

This project demonstrates how AI-assisted Python development and Monte Carlo simulation can help account managers explore those trade-offs, quantify uncertainty, and translate modeled performance into a practical budget recommendation.

The broader objective is to demonstrate how commercial Ad-Tech experience can be combined with AI and coding to investigate real business decisions at scale.
