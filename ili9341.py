import time
import ustruct
import framebuf

class ILI9341:
    def __init__(self, spi, cs, dc, rst, width=240, height=320):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.width = width
        self.height = height
        
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=1)
        
        self.reset()
        self.init()
        
        self.buffer = bytearray(self.width * self.height * 2)
        self.fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.RGB565)

    def write_cmd(self, cmd):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, data):
        self.cs(0)
        self.dc(1)
        self.spi.write(data)
        self.cs(1)

    def reset(self):
        self.rst(0)
        time.sleep_ms(50)
        self.rst(1)
        time.sleep_ms(50)

    def init(self):
        self.write_cmd(0x01)
        time.sleep_ms(150)
        self.write_cmd(0x11)
        time.sleep_ms(255)
        self.write_cmd(0x3A)
        self.write_data(bytearray([0x55])) 
        self.write_cmd(0x36)
        self.write_data(bytearray([0x48])) 
        self.write_cmd(0x29)

    def fill(self, color):
        self.fb.fill(color)
        
    def text(self, text, x, y, color):
        self.fb.text(text, x, y, color)
        
    def rect(self, x, y, w, h, color):
        self.fb.rect(x, y, w, h, color)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(ustruct.pack(">HH", 0, self.width - 1))
        self.write_cmd(0x2B)
        self.write_data(ustruct.pack(">HH", 0, self.height - 1))
        self.write_cmd(0x2C)
        self.cs(0)
        self.dc(1)
        self.spi.write(self.buffer)
        self.cs(1)
        
    def draw_tiny_buffer(self, tiny_buffer, x, y, w, h):
        self.write_cmd(0x2A) 
        self.write_data(ustruct.pack(">HH", x, x + w - 1))
        self.write_cmd(0x2B) 
        self.write_data(ustruct.pack(">HH", y, y + h - 1))
        self.write_cmd(0x2C) 
        self.cs(0)
        self.dc(1)
        self.spi.write(tiny_buffer)
        self.cs(1)