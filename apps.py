import time
import network
from machine import ADC

temp_sensor = ADC(4)

def run_wifi_scan(print_line_func, start_y):
    current_y = start_y
    print_line_func("SCANNING MESH...", current_y)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()
    current_y += 15
    if not networks:
        print_line_func("NO NETWORKS FOUND", current_y)
        return current_y
    print_line_func("SSID       | RSSI", current_y)
    current_y += 15
    print_line_func("------------------", current_y)
    for net in networks[:4]:
        current_y += 15
        ssid = net[0].decode('utf-8')[:10]
        rssi = str(net[3])
        print_line_func(f"{ssid:<10} | {rssi}dBm", current_y)
    return current_y

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

def run_save_note(print_line_func, start_y, text_to_save):
    current_y = start_y
    if not text_to_save.strip():
        print_line_func("ABORTED: BUFFER EMPTY", current_y)
        return current_y
    try:
        with open("notes.txt", "a") as f:
            f.write(text_to_save + "\n")
        print_line_func("LOG SECURED TO DISK", current_y)
    except Exception as e:
        print_line_func("FS WRITE ERROR", current_y)
    return current_y

def run_read_notes(print_line_func, start_y):
    current_y = start_y
    print_line_func("READING SAVED LOGS:", current_y)
    try:
        with open("notes.txt", "r") as f:
            lines = f.readlines()
        if not lines:
            current_y += 15
            print_line_func("NO RECORDS FOUND", current_y)
            return current_y
        for line in lines[-4:]:
            current_y += 15
            print_line_func(line.strip(), current_y)
    except Exception as e:
        current_y += 15
        print_line_func("NO FILE DISCOVERED", current_y)
    return current_y

def run_help_index(print_line_func, start_y):
    current_y = start_y
    print_line_func("COMMAND REGISTRY:", current_y)
    current_y += 15
    print_line_func("11 -> WI-FI MESH SCAN", current_y)
    current_y += 15
    print_line_func("22 -> TELEMETRY DIAGS", current_y)
    current_y += 15
    print_line_func("44 -> ENTER TEXT MODE", current_y)
    current_y += 15
    print_line_func("55 -> DUMP FILE CACHE", current_y)
    return current_y