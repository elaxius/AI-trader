import ta
import pandas as pd
import numpy as np
from itertools import combinations

class TechLevels:
    def __init__(self):
        pass

    def calculate_indicators(self, df, close, high, low, vol):
        df['RSI'] = ta.momentum.RSIIndicator(df[close]).rsi()

        macd = ta.trend.MACD(df[close]).macd()
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['MACD_Hist'] = macd.macd_diff()

        df['ATR'] = ta.volatility.AverageTrueRange(df[high], df[low], df[close]).average_true_range()

        df['TEMA'] = ta.trend.EMAIndicator(df[close], window=30).ema_indicator()
        df['EMA4'] = ta.trend.EMAIndicator(df[close], window=4).ema_indicator()
        df['EMA9'] = ta.trend.EMAIndicator(df[close], window=9).ema_indicator()
        df['EMA18'] = ta.trend.EMAIndicator(df[close], window=18).ema_indicator()

        df['OBV'] = ta.volume.OnBalanceVolumeIndicator(df[close], df[vol], fillna=True).on_balance_volume()
        df['VWAP'] = ta.volume.VolumeWeightedAveragePrice(df[high], df[low], df[close], df[vol],
                                                          fillna=True).volume_weighted_average_price()

        stoch = ta.momentum.StochasticOscillator(df[high], df[low], df[close])
        df['SKDJ_K'] = stoch.stoch()
        df['SKDJ_D'] = stoch.stoch_signal()

        return df

    def calculate_flags(self, df, high, low, close, eps):
        df['Max_High_3d'] = df[high].rolling(window=3).max().shift(-3)
        df['Min_Low_3d'] = df[low].rolling(window=3).min().shift(-3)
        df['Flag'] = df.apply(lambda row: 2 if row['Max_High_3d'] > 1+eps and row['Min_Low_3d'] < 1-eps
                                            else (1 if row['Max_High_3d'] > 1+eps * row[close] else (
                                            -1 if row['Min_Low_3d'] < 1-eps * row[close] else 0)), axis=1)
        return df

    def get_all_ratios(self, df, exclusion_list):
        feature_list = [col for col in df.columns if col not in exclusion_list]
        ratios = {f"{f1}/{f2}": df[f1] / df[f2] for f1, f2 in combinations(feature_list, 2)}

        return df.assign(**ratios)

    def get_past_prices(self, df, close, n):
        past_prices = {f"Close_{i}": df[close].shift(i) for i in range(1, n)}
        return df.assign(**past_prices)


