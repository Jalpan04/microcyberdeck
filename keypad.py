from machine import Pin

MATRIX = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

row_pins = [Pin(i, Pin.OUT) for i in range(2, 6)]
col_pins = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in range(6, 10)]

def scan():
    for row in range(4):
        row_pins[row].value(1) 
        for col in range(4):
            if col_pins[col].value() == 1: 
                row_pins[row].value(0)
                return MATRIX[row][col]
        row_pins[row].value(0)
    return None