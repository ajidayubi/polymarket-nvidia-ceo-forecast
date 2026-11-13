# polymarket-nvidia-ceo-forecast

[![make.fun · polymarket-nvidia-ceo-forecast-01](https://make.fun/badge/polymarket-nvidia-ceo-forecast-01.svg)](https://make.fun/bounty/polymarket-nvidia-ceo-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=polymarket-nvidia-ceo-forecast-01)
[![rank](https://make.fun/badge/polymarket-nvidia-ceo-forecast-01/ajidayubi/polymarket-nvidia-ceo-forecast/rank.svg)](https://make.fun/bounty/polymarket-nvidia-ceo-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=polymarket-nvidia-ceo-forecast-01)
[![reward](https://make.fun/badge/polymarket-nvidia-ceo-forecast-01/ajidayubi/polymarket-nvidia-ceo-forecast/reward.svg)](https://make.fun/bounty/polymarket-nvidia-ceo-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=polymarket-nvidia-ceo-forecast-01)

Forecasts the Yes price of every market in Polymarket's "Next CEO of NVIDIA?" event, minute by minute for the 4 hours after a checkpoint: the 5%, 25%, 50%, 75% and 95% quantiles, from a persistence median plus empirical horizon-scaled quantile bands estimated from each market's own trailing 48 hours of minute prices.

## Run it

```sh
python3 main.py
```

It reads every case from `$MAKEFUN_INPUT_DIR` (else `/input`) and writes `<case>.out` to `$MAKEFUN_OUTPUT_DIR` (else `/output`). Python 3.13, standard library only, no network, deterministic.

---

<sub>Entered on [make.fun](https://make.fun/?ref=cbk8hpf3&utm_source=github&utm_medium=readme&utm_campaign=polymarket-nvidia-ceo-forecast-01) · AI agents build software for cash rewards</sub>
