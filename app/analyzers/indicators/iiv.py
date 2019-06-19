""" Custom Indicator Increase In  Volume
"""

from scipy import stats
import numpy as np

from analyzers.utils import IndicatorUtils


class IIV(IndicatorUtils):
    def analyze(self, historical_data, signal=['iiv'], hot_thresh=10, cold_thresh=0):
        """Performs an analysis about the increase in volumen on the historical data

        Args:
            historical_data (list): A matrix of historical OHCLV data.
            signal (list, optional): Defaults to iiv. The indicator line to check hot against.
            hot_thresh (float, optional): Defaults to 10. 
            cold_thresh: Unused
            

        Returns:
            pandas.DataFrame: A dataframe containing the indicator and hot/cold values.
        """

        dataframe = self.convert_to_dataframe(historical_data)
        
        z = np.abs(stats.zscore(dataframe['volume']))
        filtered = dataframe.volume[(z < 3)]
        
        previous_mean = filtered.mean()
        
        dataframe[signal[0]] = dataframe['volume'] / previous_mean

        dataframe['is_hot']  = False
        dataframe['is_cold'] = False

        _open, _close = dataframe.iloc[-1]['open'] , dataframe.iloc[-1]['close']

        dataframe.iloc[-1]['is_hot']  = dataframe.iloc[-1][signal[0]] >= hot_thresh and _close > _open

        return dataframe
