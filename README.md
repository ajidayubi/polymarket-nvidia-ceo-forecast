# Polymarket Next-NVIDIA-CEO forecaster (make.fun bounty `polymarket-nvidia-ceo-forecast-01`)

`main.py` (Python 3.13, stdlib only, no network, deterministic) reads one case
from `/input/<id>.in` (or `$MAKEFUN_INPUT_DIR`) and writes `/output/<id>.out`
(or `$MAKEFUN_OUTPUT_DIR`): for each market and each of the 240 minutes after
the checkpoint, the 5%, 25%, 50%, 75% and 95% quantiles of the Yes price.

Method: persistence median plus empirical quantiles of the horizon-h price
change, estimated from the market's own trailing 48h at horizon knots and
interpolated in log(h), scaled by 0.90. See the docstring in `main.py`.

Local validation (own scorer, pinball loss, lower is better):
- Official practice cases p00–p05: **0.322** vs house baseline **0.364**
- Extra volatile cases v00–v05 (Nov 11 repricing): **1.564** vs baseline **1.681**

Mean reversion, trend following, the cross-market sum correction and the
empirical median were all tested and rejected: they only helped on the calm
practice cases and hurt on the volatile ones.
