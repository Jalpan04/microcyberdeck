import network

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