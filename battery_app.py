from machine import ADC

bat_adc = ADC(26)

def run_battery_gauge(print_line_func, start_y):
    current_y = start_y
    print_line_func("BATTERY TELEMETRY:", current_y)
    
    raw_value = bat_adc.read_u16()
    pin_voltage = raw_value * (3.3 / 65535)
    battery_voltage = pin_voltage * 2
    
    if battery_voltage >= 4.2:
        percentage = 100.0
    elif battery_voltage <= 3.2:
        percentage = 0.0
    else:
        percentage = ((battery_voltage - 3.2) / (4.2 - 3.2)) * 100
        
    current_y += 15
    print_line_func(f"CELL VOLTS: {battery_voltage:.2f} V", current_y)
    current_y += 15
    print_line_func(f"CAPACITY  : {percentage:.1f} %", current_y)
    
    return current_y