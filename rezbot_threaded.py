# %%

from src import *
from src.threaded_manager import ThreadedManager
from src.threaded_atrader import ThreadedATrader
from src.strategy import MacdStrategy, TAStrategy
import argparse

# %%
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--rate", default=1, type=int)
parser.add_argument("-sl", "--stoploss", default=-0.2, type=float)
parser.add_argument("-tp", "--takeprofit", default=1.5, type=float)
parser.add_argument("-ew", "--entry_window", default=2, type=int)
parser.add_argument("-xw", "--exit_window", default=1, type=int)
parser.add_argument("-L", "--leverage", default=1, type=int)
parser.add_argument("-R", "--is_real", default=False, type=bool)
parser.add_argument("-Q", "--qty", default=1, type=float)
args = parser.parse_args()

rate = args.rate
tp = args.takeprofit
sl = args.stoploss
leverage = args.leverage
ew = args.entry_window
xw = args.exit_window
is_real = args.is_real
qty = args.qty
# %%

# from src.grabber import *
# from src.strategy import *
if __name__ == "__main__":

    m = ThreadedManager(API_KEY, API_SECRET, rate=rate)

    # macd_params = {"fast": 7, "slow": 14, "signal": 5}

    strategy_params = ["macd", "1m", tp, sl, ew, xw]
    strat = TAStrategy(*strategy_params)

    # %%

    symbols = ["ethusdt", "bnbusdt", "btcusdt", "xrpusdt"]

    # %%

    t1 = m.start_trader(
        strat, symbols[0], leverage=leverage, is_real=is_real, qty=qty)
    t2 = m.start_trader(
        strat, symbols[1], leverage=leverage, is_real=is_real, qty=qty)
    # t3 = m.start_trader(
    #     strat, symbols[2], leverage=leverage, is_real=is_real, qty=qty)
    # t4 = m.start_trader(
    #     strat, symbols[3], leverage=leverage, is_real=is_real, qty=qty)
# %%
# rate = 60
# m = ThreadedManager(API_KEY, API_SECRET, rate=rate)
# # %%
# symbols = ["ethusdt", "bnbusdt", "btcusdt", "xrpusdt"]
# strategy_params = ["macd", "1m", 1.5, -0.2, 3, 0]
# strat = TAStrategy(*strategy_params)
# # tp = args.takeprofit
# # sl = args.stoploss
# leverage = 50
# # ew = args.entry_window
# # xw = args.exit_window
# is_real = False
# # %%

# t1 = m.start_trader(
#     strat, symbols[0], leverage=leverage, is_real=is_real)
# # %%

# t2 = m.start_trader(
#     strat, symbols[1], leverage=leverage, is_real=is_real)
# # %%
