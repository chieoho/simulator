"""
This file is used to run the simulation. It is used to test the simulation.
"""
from simulator.simulation import start_simulation

def simulation_test():
    """
    Test the simulation
    """
    test_device_list = range(1, 10001)
    start_simulation(test_device_list)

if __name__ == "__main__":
    simulation_test()
