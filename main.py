from machine import Pin, SPI
import time
import framebuf
from ili9341 import ILI9341
import keypad

import wifi_app
import storage_app
import diag_app
import battery_app

# --- HARDWARE CONFIG ---
spi = SPI(0, baudrate=40000000, sck=Pin(18), mosi=Pin(19))
cs = Pin(17, Pin.OUT)
dc = Pin(20, Pin.OUT)
rst = Pin(21, Pin.OUT)

display = ILI9341(spi, cs, dc, rst, width=240, height=320)

BLACK = 0x0000
GREEN = 0xE007 

def draw_char(char, x, y, color):
    tiny_ram = bytearray(8 * 8 * 2) 
    tiny_fb = framebuf.FrameBuffer(tiny_ram, 8, 8, framebuf.RGB565)
    tiny_fb.fill(BLACK)
    tiny_fb.text(char, 0, 0, color)
    display.draw_tiny_buffer(tiny_ram, x, y, 8, 8)

def print_line(text, y_pos):
    for i, char in enumerate(text):
        if 10 + (i * 10) < 220:
            draw_char(char, 10 + (i * 10), y_pos, GREEN)

def clear_terminal_area():
    slice_w = 230
    slice_h = 10
    slice_ram = bytearray(slice_w * slice_h * 2) 
    for y_offset in range(75, 305, slice_h):
        display.draw_tiny_buffer(slice_ram, 5, y_offset, slice_w, slice_h)

def render_mode_status(status_char):
    draw_char(status_char, 220, 295, GREEN)

def boot_sequence():
    display.fill(BLACK)
    display.text("KERNEL CORE", 10, 15, GREEN)
    display.text("===========", 10, 27, GREEN)
    display.text("[+] NODE ONLINE", 10, 50, GREEN)
    display.rect(2, 2, 236, 316, GREEN)
    display.show()

# --- INITIALIZATION ---
boot_sequence()
cursor_x = 10
cursor_y = 80
draw_char(">", cursor_x, cursor_y, GREEN)
cursor_x += 15

input_buffer = ""
text_buffer = ""
target_filename = ""
sys_state = "COMMAND"  
render_mode_status("W")

last_key = None
last_clock_update = 0

while True:
    current_millis = time.ticks_ms()
    
    if time.ticks_diff(current_millis, last_clock_update) > 500:
        total_seconds = current_millis // 1000
        sim_seconds = total_seconds % 60
        sim_minutes = (total_seconds // 60) % 60
        sim_hours = ((total_seconds // 3600) % 12) or 12
        period = "AM" if (total_seconds // 3600) % 24 < 12 else "PM"
        time_str = f"{sim_hours:02d}:{sim_minutes:02d}:{sim_seconds:02d} {period}"
        for idx, character in enumerate(time_str):
            draw_char(character, 140 + (idx * 8), 15, GREEN)
        last_clock_update = current_millis

    key = keypad.scan()
    
    if key != last_key:
        if key is not None:
            
            # --- STATE: FILENAME ASSIGNMENT (WRITE) ---
            if sys_state == "FILENAME_SET":
                if key == 'A': 
                    if input_buffer.strip() == "":
                        target_filename = "notes.txt"
                    else:
                        target_filename = input_buffer.strip()
                    
                    input_buffer = ""
                    sys_state = "TEXT"
                    render_mode_status("I")
                    cursor_y += 15
                    print_line("ENTER TEXT BODY...", cursor_y)
                    cursor_y += 15
                    draw_char("+", 10, cursor_y, GREEN)
                    cursor_x = 25
                elif key == 'B' and len(input_buffer) > 0:
                    input_buffer = input_buffer[:-1]
                    cursor_x -= 10
                    draw_char(" ", cursor_x, cursor_y, GREEN)
                elif key != 'C' and key != 'D' and key != '#':
                    if cursor_x < 220:
                        input_buffer += key
                        draw_char(key, cursor_x, cursor_y, GREEN)
                        cursor_x += 10

            # --- STATE: FILENAME ASSIGNMENT (READ) ---
            elif sys_state == "FILENAME_READ":
                if key == 'A':
                    read_target = input_buffer.strip() if input_buffer.strip() != "" else "notes.txt"
                    input_buffer = ""
                    cursor_y += 15
                    cursor_y = storage_app.run_read_notes(print_line, cursor_y, read_target)
                    
                    sys_state = "COMMAND"
                    render_mode_status("W")
                    cursor_x = 10
                    cursor_y += 15
                    if cursor_y > 270: clear_terminal_area(); cursor_y = 80
                    draw_char(">", cursor_x, cursor_y, GREEN)
                    cursor_x += 15
                elif key == 'B' and len(input_buffer) > 0:
                    input_buffer = input_buffer[:-1]
                    cursor_x -= 10
                    draw_char(" ", cursor_x, cursor_y, GREEN)
                elif key != 'C' and key != 'D' and key != '#':
                    if cursor_x < 220:
                        input_buffer += key
                        draw_char(key, cursor_x, cursor_y, GREEN)
                        cursor_x += 10

            # --- STATE: TEXT BODY EDITING MODE ---
            elif sys_state == "TEXT":
                if key == '#': 
                    cursor_y += 15
                    cursor_y = storage_app.run_save_note(print_line, cursor_y, target_filename, text_buffer)
                    text_buffer = ""
                    sys_state = "COMMAND"
                    render_mode_status("W")
                    
                    cursor_x = 10
                    cursor_y += 15
                    if cursor_y > 270: clear_terminal_area(); cursor_y = 80
                    draw_char(">", cursor_x, cursor_y, GREEN)
                    cursor_x += 15
                elif key == 'A':  
                    cursor_x = 10
                    cursor_y += 15
                    if cursor_y > 270: clear_terminal_area(); cursor_y = 80
                    draw_char("+", cursor_x, cursor_y, GREEN)
                    cursor_x += 15
                elif key == 'B':  
                    if len(text_buffer) > 0:
                        text_buffer = text_buffer[:-1]
                        cursor_x -= 10
                        draw_char(" ", cursor_x, cursor_y, GREEN)
                elif key == 'D':  
                    text_buffer += " "
                    draw_char(" ", cursor_x, cursor_y, GREEN)
                    cursor_x += 10
                elif key != 'C':  
                    if cursor_x < 220:
                        text_buffer += key
                        draw_char(key, cursor_x, cursor_y, GREEN)
                        cursor_x += 10

            # --- STATE: STANDARD COMMAND MODE ---
            elif sys_state == "COMMAND":
                if key == 'A': 
                    cursor_y += 15
                    if cursor_y > 270: clear_terminal_area(); cursor_y = 80
                    
                    if input_buffer == "11":
                        cursor_y = wifi_app.run_wifi_scan(print_line, cursor_y)
                    elif input_buffer == "22":
                        cursor_y = diag_app.run_diagnostics(print_line, cursor_y)
                    elif input_buffer == "02":
                        cursor_y = battery_app.run_battery_gauge(print_line, cursor_y)
                    elif input_buffer == "55":
                        sys_state = "FILENAME_READ"
                        input_buffer = ""
                        clear_terminal_area()
                        cursor_y = 80
                        print_line("READ FILE NAME?", cursor_y)
                        cursor_y += 15
                        draw_char("?", 10, cursor_y, GREEN)
                        cursor_x = 25
                    elif input_buffer == "77":
                        cursor_y = diag_app.run_help_index(print_line, cursor_y)
                    elif input_buffer == "1":  
                        sys_state = "FILENAME_SET"
                        input_buffer = ""
                        clear_terminal_area()
                        cursor_y = 80
                        print_line("NAME YOUR FILE:", cursor_y)
                        cursor_y += 15
                        draw_char("?", 10, cursor_y, GREEN)
                        cursor_x = 25
                    elif input_buffer == "":
                        print_line("ERROR: NO INPUT", cursor_y)
                    else:
                        print_line("UNKNOWN COMMAND", cursor_y)
                    
                    if sys_state == "COMMAND":
                        input_buffer = ""
                        cursor_x = 10
                        cursor_y += 15
                        if cursor_y > 270: clear_terminal_area(); cursor_y = 80
                        draw_char(">", cursor_x, cursor_y, GREEN)
                        cursor_x += 15

                elif key == 'B':  
                    if len(input_buffer) > 0:
                        input_buffer = input_buffer[:-1]
                        cursor_x -= 10
                        draw_char(" ", cursor_x, cursor_y, GREEN)
                elif key == 'C':  
                    clear_terminal_area()
                    input_buffer = ""
                    cursor_x = 10
                    cursor_y = 80
                    draw_char(">", cursor_x, cursor_y, GREEN)
                    cursor_x += 15
                elif key == 'D':  
                    input_buffer += " "
                    draw_char(" ", cursor_x, cursor_y, GREEN)
                    cursor_x += 10
                elif key != '#':  
                    if cursor_x < 220:
                        input_buffer += key
                        draw_char(key, cursor_x, cursor_y, GREEN)
                        cursor_x += 10

        last_key = key
        time.sleep(0.01)