import Reactor_Object
import Unit_Object
import Turbine_Object
from time import sleep


reactor = Reactor_Object.Reactor(100)
turbine = Turbine_Object.Turbine()
unit = Unit_Object.Unit()
turbine.valve_open(7100)
turbine.valve_setpoint(40)
turbine.refresh(pressure=7100)

while True:
    print(f"Power : {unit.thermal_power() * 100}")
    print(f"Period : {unit.period()}")
    print(f"Pressure : {unit.reactor.pressure}")
    print(f"Temp : {unit.temperature()}")
    print(f"Water : {unit.reactor.water_amount}")
    
    print("\n")
    unit.__debug_raise__()
    unit.refresh()
    unit.fast_refresh()
    unit.main_valve(True)
    unit.set_valve(40)
    unit.feed_pump1_set(100)
    sleep(1)