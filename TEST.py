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

stop = False


while not stop:
    print(f"Power : {unit.thermal_power() * 100}")
    print(f"Period : {unit.period()}")
    print(f"Pressure : {unit.reactor.pressure}")
    print(f"Temp : {unit.temperature()}")
    print(f"Water : {unit.reactor.water_amount}")
    print(f"Steam : {unit.reactor.steam_amount}")
    print(f"RPM : {unit.turbine.get_rpm()}")
    if unit.temperature() > 150:
        stop = True
    
    if stop:
        unit.__debug_raise__(0)
    else:
        unit.__debug_raise__()
    unit.refresh()
    unit.fast_refresh()
    sleep(1)
    print("\n")