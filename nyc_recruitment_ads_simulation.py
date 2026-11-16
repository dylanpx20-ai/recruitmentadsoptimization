"""NYC recruitment advertising: synthetic Monte Carlo campaign-management model.

Run in Google Colab or locally: python nyc_job_ads_simulation.py
Dependencies: numpy, pandas, matplotlib.

No proprietary Indeed data is used. All parameters are illustrative and editable.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DAYS = 30
BASE_BUDGET = 3000
BUDGETS = {"Reduce": 2400, "Maintain": 3000, "Increase": 3600}
CPC_ENVS = {"Low": 8.0, "Moderate": 15.0, "High": 25.0}
STRATEGIES = ("Equal", "Performance-First", "Priority-Weighted", "Adaptive")
# Ten openings across six job families. All parameters are SYNTHETIC.
ROLES = pd.DataFrame([
    ("HR Representative", 3, 1.00, .095, .35, 6, 1.0),
    ("Sales Account Executive", 2, 1.20, .065, .32, 4, 1.2),
    ("Accountant", 2, 1.30, .055, .42, 4, 1.3),
    ("Janitor", 1, .75, .145, .45, 3, .8),
    ("Operations Manager", 1, 1.45, .045, .30, 2, 1.6),
    ("Administrative Assistant", 1, .90, .105, .38, 3, .9),
], columns=["role", "openings", "cpc_multiplier", "apply_rate", "qualification_rate", "monthly_application_target", "priority"])
# Application targets are per JOB FAMILY, not per opening.
# Traffic supply = potential clicks per role family per day; may limit spend.
ROLES["daily_click_supply"] = [32, 21, 17, 30, 11, 25]


def allocation(strategy: str, state: dict, roles: pd.DataFrame, day: int) -> np.ndarray:
    """Per-run role weights. Performance/adaptive decisions use prior observed outcomes."""
    n = len(roles)
    openings = roles.openings.to_numpy(float)
    priority = roles.priority.to_numpy(float)
    if strategy == "Equal":
        raw = openings
    elif strategy == "Priority-Weighted":
        raw = openings * priority
    else:
        # Smoothed conversion estimates prevent overreacting to small samples.
        clicks = state["clicks"]
        apps = state["apps"]
        prior_strength = 30.0
        prior_rate = roles.apply_rate.to_numpy(float)
        estimated_apply = (apps + prior_strength * prior_rate) / (clicks + prior_strength)
        cpc = state["cpc_estimate"]
        efficiency = estimated_apply / np.maximum(cpc, .01)
        if strategy == "Performance-First":
            raw = openings * efficiency
        elif strategy == "Adaptive":
            targets = roles.monthly_application_target.to_numpy(float)
            progress = (apps + 1) / (targets * max(day / DAYS, .1) + 1)
            gap = np.clip(1 / np.sqrt(progress), .6, 2.0)
            raw = openings * priority * np.sqrt(efficiency) * gap
        else:
            raise ValueError(strategy)
    raw = np.broadcast_to(raw, (state["clicks"].shape[0], n)) if raw.ndim == 1 else raw
    return raw / raw.sum(axis=1, keepdims=True)


def simulate(budget: int, env: str, strategy: str, iterations: int, seed: int, batch_size: int = 1000):
    rng = np.random.default_rng(seed)
    n_roles = len(ROLES)
    base_cpc = CPC_ENVS[env] * ROLES.cpc_multiplier.to_numpy()
    base_apply = ROLES.apply_rate.to_numpy()
    base_qual = ROLES.qualification_rate.to_numpy()
    supply = ROLES.daily_click_supply.to_numpy()
    target = ROLES.monthly_application_target.to_numpy()
    priority = ROLES.priority.to_numpy()
    results = []
    daily_sum = np.zeros(DAYS)
    role_app_sum = np.zeros(n_roles)
    role_spend_sum = np.zeros(n_roles)
    role_qual_sum = np.zeros(n_roles)
    for start in range(0, iterations, batch_size):
        m = min(batch_size, iterations - start)
        # Heterogeneity across simulated campaigns, plus daily volatility.
        cpc_factor = rng.lognormal(-.5 * .17**2, .17, size=(m, n_roles))
        apply_factor = rng.lognormal(-.5 * .25**2, .25, size=(m, n_roles))
        qual_factor = rng.lognormal(-.5 * .20**2, .20, size=(m, n_roles))
        total_spend = np.zeros(m)
        spent_by_role = np.zeros((m, n_roles))
        clicks_by_role = np.zeros((m, n_roles))
        apps_by_role = np.zeros((m, n_roles))
        qualified_by_role = np.zeros((m, n_roles))
        early_exhaust = np.zeros(m, bool)
        day_spends = np.zeros((m, DAYS))
        # Allocation refreshed weekly for performance-based strategies.
        weights = np.broadcast_to(ROLES.openings.to_numpy(float) / ROLES.openings.sum(), (m, n_roles)).copy()
        for day in range(1, DAYS + 1):
            if day == 1 or (day - 1) % 7 == 0:
                state = {"clicks": clicks_by_role, "apps": apps_by_role,
                         "cpc_estimate": np.broadcast_to(base_cpc, (m, n_roles))}
                weights = allocation(strategy, state, ROLES, day)
                # Preserve minimum role coverage: >= 6% per family.
                weights = .06 + (1 - .06 * n_roles) * weights
            remaining = np.maximum(0, budget - total_spend)
            remaining_days = DAYS - day + 1
            # Planned daily spend, allowing limited catch-up if under-paced.
            desired_daily = np.minimum(remaining, remaining / remaining_days * 1.10)
            desired_role = desired_daily[:, None] * weights
            # Daily market supply fluctuates, and each role may saturate.
            daily_cpc = base_cpc * cpc_factor * rng.lognormal(-.5 * .13**2, .13, size=(m, n_roles))
            daily_supply = rng.poisson(np.maximum(supply * rng.lognormal(-.5 * .25**2, .25, size=(m, n_roles)), 0))
            # Actual clicks bounded by demand and spend; binomial conversion follows.
            clicks = np.minimum(daily_supply, np.floor(desired_role / daily_cpc)).astype(int)
            spend = clicks * daily_cpc
            # Reinvest unused spend from constrained roles in remaining roles (same day),
            # subject to additional supply; approximate one redistribution pass.
            unused = np.maximum(0, desired_daily - spend.sum(axis=1))
            extra_capacity = np.maximum(0, daily_supply - clicks)
            extra_budget = unused[:, None] * weights
            extra_clicks = np.minimum(extra_capacity, np.floor(extra_budget / daily_cpc)).astype(int)
            clicks += extra_clicks
            spend += extra_clicks * daily_cpc
            # Ensure spending never exceeds the remaining monthly budget.
            # Floors and redistribution preserve this to floating-point tolerance.
            apply_p = np.clip(base_apply * apply_factor * rng.lognormal(-.5 * .15**2, .15, size=(m, n_roles)), .001, .95)
            qual_p = np.clip(base_qual * qual_factor, .001, .95)
            apps = rng.binomial(clicks, apply_p)
            qualified = rng.binomial(apps, qual_p)
            total_spend += spend.sum(axis=1)
            spent_by_role += spend
            clicks_by_role += clicks
            apps_by_role += apps
            qualified_by_role += qualified
            day_spends[:, day - 1] = spend.sum(axis=1)
            if day < DAYS:
                early_exhaust |= total_spend >= budget - min(base_cpc)  # less than one minimum-cost click left
        total_apps = apps_by_role.sum(axis=1)
        total_qual = qualified_by_role.sum(axis=1)
        coverage = (apps_by_role >= target).sum(axis=1)
        # At least one application for every family, and 80% of family targets met.
        healthy_coverage = (apps_by_role > 0).all(axis=1) & (coverage >= 5)
        spend_pct = total_spend / budget
        # Healthy pacing: budget utilized and not effectively exhausted early.
        healthy_pacing = (spend_pct >= .90) & (~early_exhaust)
        results.append(pd.DataFrame({
            "spend": total_spend, "utilization": spend_pct, "clicks": clicks_by_role.sum(axis=1),
            "applications": total_apps, "qualified_applications": total_qual,
            "cpa": np.divide(total_spend, total_apps, out=np.full(m, np.nan), where=total_apps > 0),
            "cpqa": np.divide(total_spend, total_qual, out=np.full(m, np.nan), where=total_qual > 0),
            "families_meeting_target": coverage, "healthy_coverage": healthy_coverage,
            "healthy_pacing": healthy_pacing, "early_exhaustion": early_exhaust,
            "success": healthy_coverage & healthy_pacing,
        }))
        daily_sum += day_spends.sum(axis=0)
        role_app_sum += apps_by_role.sum(axis=0)
        role_spend_sum += spent_by_role.sum(axis=0)
        role_qual_sum += qualified_by_role.sum(axis=0)
    out = pd.concat(results, ignore_index=True)
    detail = ROLES[["role", "openings", "monthly_application_target"]].copy()
    detail["mean_spend"] = role_spend_sum / iterations
    detail["mean_applications"] = role_app_sum / iterations
    detail["mean_qualified_applications"] = role_qual_sum / iterations
    return out, daily_sum / iterations, detail


def summarize(df, env, strategy, label, budget):
    return {
        "environment": env, "strategy": strategy, "budget_decision": label, "budget": budget,
        "median_spend": df.spend.median(), "median_utilization_pct": 100 * df.utilization.median(),
        "median_clicks": df.clicks.median(), "median_applications": df.applications.median(),
        "p10_applications": df.applications.quantile(.10), "p90_applications": df.applications.quantile(.90),
        "median_qualified_applications": df.qualified_applications.median(),
        "median_cpa": df.cpa.median(), "median_cpqa": df.cpqa.median(),
        "mean_families_meeting_target": df.families_meeting_target.mean(),
        "healthy_coverage_pct": 100 * df.healthy_coverage.mean(),
        "healthy_pacing_pct": 100 * df.healthy_pacing.mean(),
        "early_exhaustion_pct": 100 * df.early_exhaustion.mean(),
        "joint_success_pct": 100 * df.success.mean(),
    }


def recommend(summary: pd.DataFrame) -> pd.DataFrame:
    """Transparent scenario-based rule, not a claim of causal budget lift.

    Per CPC environment choose strategy maximizing joint success, then qualified
    applications. Compare budget alternatives to $3k using meaningful improvement
    thresholds. If no alternative clears a threshold, maintain.
    """
    decisions = []
    for env, group in summary.groupby("environment", sort=False):
        best = (group.sort_values(["joint_success_pct", "median_qualified_applications"], ascending=False)
                .drop_duplicates("budget_decision").set_index("budget_decision"))
        base = best.loc["Maintain"]
        down = best.loc["Reduce"]
        up = best.loc["Increase"]
        # Reduced spend should preserve coverage and lose <5% qualified apps.
        if (base.joint_success_pct >= 40 and
            down.joint_success_pct >= base.joint_success_pct - 5 and
            down.median_qualified_applications >= .95 * base.median_qualified_applications and
            down.healthy_coverage_pct >= base.healthy_coverage_pct - 5):
            choice = "Reduce"
            reason = "Lower spend preserves modeled application coverage and nearly all qualified volume."
        elif (up.joint_success_pct >= base.joint_success_pct + 5 and
              up.median_qualified_applications >= 1.10 * max(base.median_qualified_applications, 1) and
              up.median_cpqa <= 1.15 * base.median_cpqa):
            choice = "Increase"
            reason = "Higher spend meaningfully improves modeled success and qualified volume without disproportionate CPQA growth."
        else:
            choice = "Maintain"
            reason = "Neither budget change clears the prespecified evidence thresholds; prioritize pacing and role-level allocation."
        selected = best.loc[choice]
        decisions.append({"environment": env, "recommendation": choice,
                          "recommended_budget": int(selected.budget),
                          "preferred_strategy": selected.strategy,
                          "joint_success_pct": round(selected.joint_success_pct, 2),
                          "median_qualified_applications": selected.median_qualified_applications,
                          "reason": reason})
    return pd.DataFrame(decisions)


def make_charts(summary, pacing, out_dir):
    for env in CPC_ENVS:
        data = pacing[(pacing.environment == env) & (pacing.budget_decision == "Maintain")]
        fig, ax = plt.subplots(figsize=(9, 5))
        for strategy, g in data.groupby("strategy"):
            g = g.sort_values("day")
            ax.plot(g.day, g.mean_cumulative_spend, label=strategy)
        ax.plot([1, 30], [100, BASE_BUDGET], "k--", linewidth=1, label="Linear target")
        ax.set(title=f"30-Day Mean Budget Pacing — {env} CPC", xlabel="Day", ylabel="Cumulative spend ($)")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(out_dir / f"01_pacing_{env.lower()}.png", dpi=160)
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 5))
    subset = summary[summary.budget_decision == "Maintain"]
    pivot = subset.pivot(index="environment", columns="strategy", values="joint_success_pct").reindex(CPC_ENVS)
    pivot.plot(kind="bar", ax=ax)
    ax.set(title="Probability of Healthy Pacing AND Role Coverage ($3,000)", xlabel="CPC environment", ylabel="Probability (%)")
    ax.tick_params(axis="x", rotation=0)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "02_joint_success_comparison.png", dpi=160)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot = summary.groupby(["environment", "budget_decision"])["median_applications"].max().unstack().reindex(CPC_ENVS)
    pivot = pivot[["Reduce", "Maintain", "Increase"]]
    pivot.plot(kind="bar", ax=ax)
    ax.set(title="Median Applications by Budget Alternative (Best Strategy per Cell)", xlabel="CPC environment", ylabel="Median applications")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(out_dir / "03_budget_alternatives.png", dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=50000, help="Monte Carlo runs per scenario (default 50000)")
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20261115)
    parser.add_argument("--output", type=Path, default=Path("jobads_results"))
    args, _ = parser.parse_known_args()  # Ignore Jupyter/Colab kernel arguments
    if args.iterations < 1 or args.batch_size < 1:
        parser.error("iterations and batch-size must be positive")
    args.output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    summary_rows, pacing_rows, role_rows = [], [], []
    scenario_id = 0
    for env in CPC_ENVS:
        for label, budget in BUDGETS.items():
            for strategy in STRATEGIES:
                scenario_id += 1
                df, daily, role = simulate(budget, env, strategy, args.iterations,
                                           args.seed + scenario_id * 1009, args.batch_size)
                summary_rows.append(summarize(df, env, strategy, label, budget))
                cumulative = np.cumsum(daily)
                for day, (daily_spend, cum_spend) in enumerate(zip(daily, cumulative), 1):
                    pacing_rows.append({"environment": env, "strategy": strategy,
                                        "budget_decision": label, "budget": budget,
                                        "day": day, "mean_daily_spend": daily_spend,
                                        "mean_cumulative_spend": cum_spend})
                role.insert(0, "environment", env)
                role.insert(1, "strategy", strategy)
                role.insert(2, "budget_decision", label)
                role_rows.append(role)
                print(f"[{scenario_id:02d}/36] {env:8s} {label:8s} {strategy:19s} median apps={df.applications.median():.0f}", flush=True)
    summary = pd.DataFrame(summary_rows)
    pacing = pd.DataFrame(pacing_rows)
    roles = pd.concat(role_rows, ignore_index=True)
    decisions = recommend(summary)
    summary.to_csv(args.output / "scenario_summary.csv", index=False)
    pacing.to_csv(args.output / "daily_pacing.csv", index=False)
    roles.to_csv(args.output / "role_level_results.csv", index=False)
    decisions.to_csv(args.output / "budget_recommendations.csv", index=False)
    make_charts(summary, pacing, args.output)
    elapsed = time.perf_counter() - started
    print("\nRECOMMENDATIONS (illustrative synthetic model):")
    print(decisions.to_string(index=False))
    print(f"\n{args.iterations * 36:,} simulated campaign months across 36 scenarios in {elapsed:.1f}s")
    print(f"Files saved in: {args.output.resolve()}")


if __name__ == "__main__":
    main()
