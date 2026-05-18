import time
from machine import ADC

temp_sensor = ADC(4)

def run_diagnostics(print_line_func, start_y):
    current_y = start_y
    print_line_func("DIAGNOSTICS PROTOCOL:", current_y)
    reading = temp_sensor.read_u16() * (3.3 / 65535)
    temperature = 27 - (reading - 0.706) / 0.001721
    current_y += 15
    print_line_func(f"CPU TEMP : {temperature:.1f} C", current_y)
    current_y += 15
    print_line_func(f"UPTIME   : {time.ticks_ms() // 1000}s RUNTIME", current_y)
    return current_y

def run_help_index(print_line_func, start_y):
    current_y = start_y
    print_line_func("COMMAND REGISTRY:", current_y)
    current_y += 15
    print_line_func("11 -> WI-FI MESH SCAN", current_y)
    current_y += 15
    print_line_func("22 -> TELEMETRY DIAGS", current_y)
    current_y += 15
    print_line_func("02 -> BATTERY TELEMETRY", current_y)
    current_y += 15
    print_line_func("1  -> ENTER TEXT MODE", current_y)
    current_y += 15
    print_line_func("55 -> DUMP FILE CACHE", current_y)
    return current_y