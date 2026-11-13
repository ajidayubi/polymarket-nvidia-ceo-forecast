#!/usr/bin/env python3
"""Forecast Polymarket's Next CEO of NVIDIA Yes prices, 240 minutes ahead.

Model, per market, from the case's own 72h of 1-minute prices:
  * Median: persistence (the last price). Prediction-market prices are close
    to martingales at these checkpoints: mean reversion, trend following and
    the cross-market sum correction were all tested and all made the
    checkpoint forecasts worse, so the median stays put.
  * Widths: empirical quantiles of the horizon-h price change, estimated
    from the trailing 48h of the market's own history at horizon knots
    {1,2,4,8,16,32,64,128,240} minutes and interpolated in log(h).
    q_tau(h) = x + Q_tau(delta_h) - Q_50(delta_h), scaled by 0.90.
    This captures what a fixed normal spread misses: prices are step
    functions (often exactly unchanged for minutes, so the 5%-95% band is
    narrow at short horizons) with rare large jumps (fat tails at long
    horizons). The 0.90 scale and 48h window were chosen on 12 validation
    cases (6 official practice cases plus 6 extra cases cut from the
    volatile Nov 11 repricing): they beat the house baseline on both
    regimes, while narrower/shorter settings only won on the calm ones.
Stdlib only, no network, deterministic (fixed sampling, no randomness).
Reads $MAKEFUN_INPUT_DIR (else /input), writes $MAKEFUN_OUTPUT_DIR (else /output).
"""
import json
import math
import os

INPUT_DIR = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

QUANTILES = [0.05, 0.25, 0.5, 0.75, 0.95]
WIDTH = 0.90            # scale on empirical quantile offsets
RES_WIN = 2880          # minutes of trailing history for the change distribution
RES_STEP = 1            # sample every minute of that window
KNOTS = [1, 2, 4, 8, 16, 32, 64, 128, 240]
BASE_SIGMA = 0.0025     # fallback spread (house baseline's) if history is too short
BASE_Z = [-1.644854, -0.67449, 0.0, 0.67449, 1.644854]


def price6(x):
    v = round(min(1.0, max(0.0, x)) * 1e6) / 1e6
    return v + 0.0  # avoid -0.0


def quantile(sorted_vals, tau):
    """Linear-interpolated empirical quantile (type 7)."""
    n = len(sorted_vals)
    if n == 0:
        return 0.0
    if n == 1:
        return sorted_vals[0]
    pos = tau * (n - 1)
    lo = int(pos)
    frac = pos - lo
    if lo + 1 >= n:
        return sorted_vals[-1]
    return sorted_vals[lo] * (1.0 - frac) + sorted_vals[lo + 1] * frac


def market_rows(prices, horizon):
    """240 rows x 5 quantiles for one market."""
    n = len(prices)
    x = prices[-1]
    # --- empirical quantiles of the h-ahead change at the knots ---
    start = max(0, n - RES_WIN)
    knot_q = {}
    for hk in KNOTS:
        if hk >= n:
            continue
        res = []
        t = start
        last_t = n - 1 - hk
        while t <= last_t:
            res.append(prices[t + hk] - prices[t])
            t += RES_STEP
        if len(res) < 20:
            continue
        res.sort()
        knot_q[hk] = [quantile(res, tau) for tau in QUANTILES]
    if not knot_q:
        # Too little history: fall back to the house baseline's normal spread.
        return [[price6(x + z * BASE_SIGMA * math.sqrt(h)) for z in BASE_Z]
                for h in range(1, horizon + 1)]

    ks = sorted(knot_q)
    logk = [math.log(k) for k in ks]
    rows = []
    for h in range(1, horizon + 1):
        lh = math.log(h)
        if h <= ks[0]:
            q = knot_q[ks[0]]
        elif h >= ks[-1]:
            q = knot_q[ks[-1]]
        else:
            j = 0
            while j + 1 < len(ks) and ks[j + 1] < h:
                j += 1
            w = (lh - logk[j]) / (logk[j + 1] - logk[j])
            qa, qb = knot_q[ks[j]], knot_q[ks[j + 1]]
            q = [qa[i] * (1.0 - w) + qb[i] * w for i in range(5)]
        med = q[2]
        row = []
        prev = None
        for j in range(5):
            v = price6(x + (q[j] - med) * WIDTH)
            if prev is not None and v < prev:
                v = prev
            row.append(v)
            prev = v
        rows.append(row)
    return rows


def forecast_case(case):
    horizon = case["horizon_minutes"]
    forecasts = []
    for m in case["markets"]:
        forecasts.append({"id": m["id"], "q": market_rows(m["prices"], horizon)})
    return {"forecasts": forecasts}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = sorted(f for f in os.listdir(INPUT_DIR) if f.endswith(".in"))
    for fname in files:
        cid = fname[: -len(".in")]
        with open(os.path.join(INPUT_DIR, fname), "r") as f:
            case = json.load(f)
        if case.get("quantiles", QUANTILES) != QUANTILES:
            raise ValueError(f"{fname} asks for quantiles {case.get('quantiles')}")
        out = forecast_case(case)
        with open(os.path.join(OUTPUT_DIR, f"{cid}.out"), "w") as f:
            f.write(json.dumps(out) + "\n")


if __name__ == "__main__":
    main()
