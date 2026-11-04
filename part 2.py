import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations, combinations_with_replacement


class RaceSimulator:
    """
    Simulates an F1 race strategy by calculating the time added
    from tire degradation and pit stops.
    """

    def __init__(self):
        """
        Initialize the simulator and store tire data.
        """
        LAPS = 60
        PIT_STOP_TIME = 25
        NUM_OF_STINTS = 3

        def __init__(self):
            self.tires = pd.DataFrame(
                {
                    'Tmin': [0, 1, 2],
                    'Tmax': [10, 10, 10],
                    'alpha': [1 / 2, 1 / 4, 1 / 16],
                    'beta': [15, 25, 55]
                },
                index = ['Soft', 'Medium', 'Hard']
            )

    def tire_time(self, age, Tmin, Tmax, alpha, beta):
        """
        Calculate the time added due to tire degradation.

        Parameters:
            age: Tire age in laps.
            Tmin: Minimum time added by the tire.
            Tmax: Maximum time added by the tire.
            alpha: Tire degradation rate parameter.
            beta: Tire degradation midpoint parameter.

        Returns:
            Tire time added for the given tire age.
        """
        return Tmin + ((Tmax - Tmin) / (1 + np.exp(-alpha * (age - beta))))


    def simulate(self, stint_lengths, tire_types):
        """
        Simulate a complete race strategy.

        Parameters:
            stint_lengths: Length of each race stint.
            tire_types: Tire compound used for each stint.

        Returns:
            Total time added from tire degradation and pit stops.
        """
        stints = []

        for number, (length, tire) in enumerate(zip(stint_lengths, tire_types)):
            tire_params = self.tires.loc[tire]
            # one dataframe for each stint
            stint = pd.DataFrame(
                {
                    'age': np.arange(length)
                }
            )
            # add the tire time and pit stop times to dataframe
            stint['tire_time'] = self.tire_time(stint['age'], tire_params['Tmin'], tire_params['Tmax'], tire_params['alpha'], tire_params['beta'])

            # add pit stop time - number greater than 0 means 2nd and 3rd stints
            stint['pit_time'] = np.where((stint['age'] == 0) & (number > 0), self.PIT_STOP_TIME, 0)

            stints.append(stint)

        race = pd.concat(stints, ignore_index=True)
        race['lap_time'] = race['tire_time'] + race['pit_time']
        return float(race['lap_time'].sum())






def plot_tires(simulator):
    """
    Plot tire degradation curves for all tire compounds.

    Parameters:
        simulator: A RaceSimulator object containing tire data.

    Returns:
        None.
    """
    pass


def find_best_strategy(simulator):
    """
    Test all valid race strategies and find the one
    with the minimum total time added.

    Parameters:
        simulator: A RaceSimulator object.

    Returns:
        The strategy with the lowest total tire and pit time.
    """
    pass