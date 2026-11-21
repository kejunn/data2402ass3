import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations, combinations_with_replacement


class RaceSimulator:
    """
    Simulates an F1 race strategy by calculating the time added
    from tire degradation and pit stops.
    """
    LAPS = 60
    PIT_STOP_TIME = 25
    NUM_OF_STINTS = 3
    
    def __init__(self):
        """
        Initialize the simulator and store tire data.
        """
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
        # add validation check
        if len(stint_lengths) != self.NUM_OF_STINTS or len(tire_types) != self.NUM_OF_STINTS:
            raise ValueError('A strategy needs 3 stints (2 pit stops) with one tire each.')

        for n in stint_lengths:
            if int(n) != n or n < 1:
                raise ValueError('Each stint leangth must be an integer with at least 1 lap.')

        if sum(stint_lengths) != self.LAPS:
            raise ValueError('Stint lengths must add up to 60 total laps.')

        for tire in tire_types:
            if tire not in self.tires.index:
                raise ValueError('Tire is not one of the three tire types.')

        if len(set(tire_types)) < 2:
            raise ValueError('Minimum two tire types must be used.')
            
        stints = []

        for stint_number, (length, tire) in enumerate(zip(stint_lengths, tire_types), start=1):
            tire_specs = self.tires.loc[tire] # select by row label
            # one dataframe for each stint
            stint = pd.DataFrame(
                {
                    'age': np.arange(length)
                }
            )
            # add the tire time and pit stop times to dataframe
            stint['tire_time'] = self.tire_time(stint['age'], tire_specs['Tmin'], tire_specs['Tmax'], tire_specs['alpha'], tire_specs['beta'])

            # add pit stop time - number greater than 0 means 2nd and 3rd stints and each pit lap starts at 0 again
            stint['pit_time'] = np.where((stint['age'] == 0) & (stint_number > 1), self.PIT_STOP_TIME, 0)

            stints.append(stint)

        # three stint dataframes
        race = pd.concat(stints, ignore_index=True) # returns dataframe, brand new index labels from 0-59
        race['lap_time'] = race['tire_time'] + race['pit_time']

        return float(np.sum(race['lap_time']))


def plot_tires(simulator):
    """
    Plot tire degradation curves for all tire compounds.

    Parameters:
        simulator: A RaceSimulator object containing tire data.

    Returns:
        None.
    """
    ages = np.arange(0, simulator.LAPS + 1)
    for tire in simulator.tires.index:
        tire_specs = simulator.tires.loc[tire]
        plt.plot(ages, simulator.tire_time(ages, tire_specs['Tmin'], tire_specs['Tmax'], tire_specs['alpha'], tire_specs['beta']), label=tire)

    plt.xlabel = ('Tire Age')
    plt.ylabel = ('Tire Time Added / Lap')
    plt.title('Tire Degradation')
    plt.legend()
    plt.show()


def find_best_strategy(simulator):
    """
    Test all valid race strategies and find the one
    with the minimum total time added.

    Parameters:
        simulator: A RaceSimulator object.

    Returns:
        The strategy with the lowest total tire and pit time.
    """
    laps = simulator.LAPS
    tires = list(simulator.tires.index)

    # order matters for strategies, can repeat but minimum 2 tires, get every possible tire type order
    tire_orders = []
    for a in tires:
        for b in tires:
            for c in tires:
                if len({a, b, c}) >= 2:
                    tire_orders.append((a, b, c))

    best = None
    # pit laps = first lap of stints 2 and 3. each stint >= 1 lap. pit stop at lap 1 would mean zero laps for stint 1, size of each combination is 2
    for pit1, pit2 in combinations(range(2, laps + 1), 2):
        stint_lengths = (pit1 - 1, pit2- pit1, laps - pit2 + 1)
        for tire_order in tire_orders:
            total_time = simulator.simulate(stint_lengths, tire_order)
            if best is None or total_time < best['total_time']:
                best = {
                    'pit_laps': (pit1, pit2),
                    'stint_lengths': stint_lengths,
                    'tire_types': tire_order,
                    'total_time': total_time
                }

    return best

def main():
    simulator = RaceSimulator()
    plot_tires(simulator)
    total_time_added = simulator.simulate((14, 8, 38), ('Soft', 'Medium', 'Hard'))
    print(total_time_added)
    print(find_best_strategy(simulator))

if __name__ == '__main__':
    main()