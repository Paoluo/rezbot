import numpy as np
import pandas_ta as ta
import pandas as pd
import time


class MacdStrategy_0:
    def __init__(
        self,
        name,
        timeframe,
        take_profit,
        stoploss,
        entry_window,
        exit_window,
        macd_params={"fast": 12, "slow": 26, "signal": 9},
    ):
        self.name = name
        self.timeframe = timeframe
        self.stoploss = stoploss
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, trader):

        if np.alltrue(trader.data_window.histogram.tail(self.entry_window) < 0):
            trader.position_type = -1
            return True
        elif np.alltrue(trader.data_window.histogram.tail(self.entry_window) > 0):
            trader.position_type = 1
            return True            
        else:
            return False

    def exit_signal(self, trader):

        condition1 = trader.current_percentual_profit >= self.take_profit

        if trader.position_type == 1:
            condition2 = np.alltrue(trader.data_window.histogram.tail(self.exit_window) < 0)
        elif trader.position_type == -1:
            condition2 = np.alltrue(trader.data_window.histogram.tail(self.exit_window) >= 0)
        
        check = condition1 and condition2

        return check

    def stoploss_check(self, trader):

        check = trader.current_percentual_profit <= self.stoploss

        return check

class MacdStrategy:
    def __init__(
        self,
        name,
        timeframe,
        take_profit,
        stoploss,
        entry_window,
        exit_window,
        macd_params={"fast": 12, "slow": 26, "signal": 9},
    ):
        self.name = name
        self.timeframe = timeframe
        self.stoploss = stoploss
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, trader):

        if (np.alltrue(trader.data_window.histogram.tail(self.entry_window) <= 0)
            and np.alltrue(ta.increasing(trader.data_window.histogram.tail(self.entry_window)).values == 1)):
            
            trader.position_type = 1
            return True
        
        elif (np.alltrue(trader.data_window.histogram.tail(self.entry_window) >= 0)
            and np.alltrue(ta.decreasing(trader.data_window.histogram.tail(self.entry_window)).values == 1)):
            
            trader.position_type = -1
            return True            
        else:
            return False

    def exit_signal(self, trader):

        condition1 = trader.current_percentual_profit >= self.take_profit

        if trader.position_type == 1:
            condition2 = (np.alltrue(trader.data_window.histogram.tail(self.entry_window) > 0)
                            and ta.decreasing(trader.data_window.histogram.tail(self.entry_window)))
        elif trader.position_type == -1:
            condition2 = (np.alltrue(trader.data_window.histogram.tail(self.entry_window) < 0)
                            and ta.increasing(trader.data_window.histogram.tail(self.entry_window)))
        
        check = condition1 and condition2

        return check

    def stoploss_check(self, trader):

        check = trader.current_percentual_profit <= self.stoploss

        return check

class MacdTAStrategy:
    def __init__(
        self,
        name,
        timeframe,
        take_profit,
        stoploss,
        entry_window,
        exit_window,
        macd_params={"fast": 12, "slow": 26, "signal": 9},
    ):
        self.name = name
        self.timeframe = timeframe
        self.stoploss = stoploss
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, trader):

        if (np.alltrue(trader.data_window.histogram.tail(self.entry_window) <= 0)
            and np.alltrue(ta.increasing(trader.data_window.histogram.tail(self.entry_window)).values == 1)
            and trader.ta_handler.signal == 1):
            
            trader.position_type = 1
            return True
        
        elif (np.alltrue(trader.data_window.histogram.tail(self.entry_window) >= 0)
            and np.alltrue(ta.decreasing(trader.data_window.histogram.tail(self.entry_window)).values == 1)
            and trader.ta_handler.signal == -1):
            
            trader.position_type = -1
            return True            
        else:
            return False

    def exit_signal(self, trader):

        condition1 = trader.current_percentual_profit >= self.take_profit

        if trader.position_type == 1:
            condition2 = (np.alltrue(trader.data_window.histogram.tail(self.entry_window) > 0)
                            and ta.decreasing(trader.data_window.histogram.tail(self.entry_window)))
        elif trader.position_type == -1:
            condition2 = (np.alltrue(trader.data_window.histogram.tail(self.entry_window) < 0)
                            and ta.increasing(trader.data_window.histogram.tail(self.entry_window)))
        
        check = condition1 and condition2

        return check


    def stoploss_check(self, trader):

        condition1 = trader.current_percentual_profit <= self.stoploss
        condition2 = trader.position_type == -trader.ta_handler.signal
        check = condition1 and condition2

        return check


class TrendReversalStrategy:
    def __init__(
        self,
        name,
        timeframe,
        take_profit,
        stoploss,
        entry_window,
        exit_window,
        macd_params={"fast": 12, "slow": 26, "signal": 9},
    ):
        self.name = name
        self.timeframe = timeframe
        self.stoploss = stoploss
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, trader):

        if (
            np.alltrue(trader.data_window.histogram.tail(self.entry_window) <= 0)
            # and np.alltrue(ta.increasing(trader.data_window.histogram.tail(self.entry_window//2)).values == 1)
            and ta.increasing(trader.data_window.histogram.tail(2)).values[-1] == 1
            and ta.decreasing(trader.data_window.histogram.tail(2)).values[-2] == 1
            # and trader.ta_handler.signal == 1
        ):
            trader.position_type = 1
            return True
        elif (
            np.alltrue(trader.data_window.histogram.tail(self.entry_window) >= 0)
            # and np.alltrue(ta.decreasing(trader.data_window.histogram.tail(self.entry_window//2)).values == 1)
            # and trader.ta_handler.signal == -1
            and ta.decreasing(trader.data_window.histogram.tail(2)).values[-1] == 1
            and ta.increasing(trader.data_window.histogram.tail(2)).values[-2] == 1
        ):
            trader.position_type = -1
            return True
        else:
            return False

    def exit_signal(self, trader):

        condition1 = trader.current_percentual_profit >= self.take_profit

        # condition2 = np.alltrue(
        #     trader.data_window.histogram.tail(self.exit_window) > 0)
        check = condition1  # and condition2

        return check

    def stoploss_check(self, trader):

        condition1 = trader.current_percentual_profit <= self.stoploss
        # condition2 = trader.position_type == -trader.ta_handler.signal
        check = condition1 # and condition2

        return check

class TAStrategy:
    def __init__(
        self,
        name,
        timeframe,
        take_profit,
        stoploss,
        entry_window,
        exit_window,
        macd_params={"fast": 12, "slow": 26, "signal": 9},
    ):
        self.name = name
        self.timeframe = timeframe
        self.stoploss = stoploss
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, trader):

        if trader.ta_handler.signal == 1:
            trader.position_type = 1
            return True
        elif trader.ta_handler.signal == -1:
            trader.position_type = -1
            return True
        else:
            return False

    def exit_signal(self, trader):

        condition1 = trader.current_percentual_profit >= self.take_profit

        # condition2 = np.alltrue(
        #     trader.data_window.histogram.tail(self.exit_window) > 0)
        check = condition1  # and condition2

        return check

    def stoploss_check(self, trader):

        condition1 = trader.current_percentual_profit <= self.stoploss
        #condition2 = trader.position_type == -trader.ta_handler.signal
        check = condition1 # and condition2

        return check

class PullbackStrategy:
    def __init__(
        self,
        name,
        timeframe,
        take_profit,
        stoploss,
        entry_window,
        exit_window,
        macd_params={"fast": 12, "slow": 26, "signal": 9},
    ):
        self.name = name
        self.timeframe = timeframe
        self.stoploss = stoploss
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, trader):
        if (
            (trader.data_window.close.values[-1] <= trader.data_window.ci.values[-1])
            and (np.alltrue(trader.data_window.histogram.tail(self.entry_window) >= 0))
            and (ta.increasing(trader.data_window.hist_ema, length=self.entry_window))
        ):

# ta.below(kl.low, close_ema - close_std*1.2).astype("bool") & (ta.above(hist, hist*0) & ta.increasing(hist_ema))
#         if (
#             np.alltrue(trader.data_window.histogram.tail(self.entry_window) >= 0)
#             and np.alltrue(trader.data_window.histogram.tail(self.entry_window) >= 0)
#             and trader.ta_handler.signal == 1
#         ):
            trader.position_type = 1
            return True
        else:
            return False

    def exit_signal(self, trader):

        condition1 = trader.current_percentual_profit >= self.take_profit

        # condition2 = np.alltrue(
        #     trader.data_window.histogram.tail(self.exit_window) > 0)
        check = condition1  # and condition2

        return check

    def stoploss_check(self, trader):

        condition1 = trader.current_percentual_profit <= self.stoploss
        # condition2 = trader.position_type == -trader.ta_handler.signal
        check = condition1 #and condition2

        return check

class VolatilityStrategy:
    def __init__(
        self,
        name,
        timeframe,
        take_profit,
        stoploss,
        entry_window,
        exit_window,
        macd_params={"fast": 12, "slow": 26, "signal": 9},
    ):
        self.name = name
        self.timeframe = timeframe
        self.stoploss = stoploss
        self.take_profit = take_profit
        self.entry_window = entry_window
        self.exit_window = exit_window
        self.macd_params = macd_params

    def entry_signal(self, trader):

        if (
            np.alltrue(trader.data_window.histogram.tail(self.entry_window) <= 0)
            and trader.ta_handler.signal == 1
        ):
            trader.position_type = 1
            return True
        elif (
            np.alltrue(trader.data_window.histogram.tail(self.entry_window) >= 0)
            and trader.ta_handler.signal == -1
        ):
            trader.position_type = -1
            return True
        else:
            return False

    def exit_signal(self, trader):

        condition1 = trader.current_percentual_profit >= self.take_profit

        # condition2 = np.alltrue(
        #     trader.data_window.histogram.tail(self.exit_window) > 0)
        check = condition1  # and condition2

        return check

    def stoploss_check(self, trader):

        condition1 = trader.current_percentual_profit <= self.stoploss
        condition2 = trader.position_type == -trader.ta_handler.signal
        check = condition1 and condition2

        return check