#!/usr/bin/env python3


class colours(object):
    '''Colors class:reset all colors with colors.reset; two
    sub classes fg for foreground
    and bg for background; use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold'''
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

# 4 bit colour (16 colours)
    class fg(object):
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
        white = '\033[97m'

    class bg(object):
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'
        darkgrey = '\033[100m'
        lightred = '\033[101m'
        lightgreen = '\033[102m'
        yellow = '\033[103m'
        lightblue = '\033[104m'
        pink = '\033[105m'
        lightcyan = '\033[106m'
        white = '\033[107m'

# 8 bit colour (255 colours):
    @staticmethod
    def fg8bit(n:int) -> str:
        if (n not in range(255)):
            errorMessage = "Value out of range: 0-255"
            raise ValueError(errorMessage)
        return '\033[38;5;%im' % (n)
    
    @staticmethod
    def bg8bit(n:int) -> str:
        if (n not in range(255)):
            errorMessage = "Value out of range: 0-255"
            raise ValueError(errorMessage)
        return '\033[48;5;%im' % (n)

# 16 bit colour (65,536 colours)
    @staticmethod
    def fgrgb(red:int, green:int, blue:int):
        if (red not in range(256)):
            errorMessage = "Red value out of range: 0-255"
            raise ValueError(errorMessage)
        if (green not in range(256)):
            errorMessage = "Green value out of range: 0-255"
            raise ValueError(errorMessage)
        if (blue not in range(256)):
            errorMessage = "Blue value out of range: 0-255"
            raise ValueError(errorMessage)
        return '\033[38;2;%i;%i;%im' % (red, green, blue)
    @staticmethod
    def bgrgb(red:int, green:int, blue:int):
        if (red not in range(256)):
            errorMessage = "Red value out of range: 0-255"
            raise ValueError(errorMessage)
        if (green not in range(256)):
            errorMessage = "Green value out of range: 0-255"
            raise ValueError(errorMessage)
        if (blue not in range(256)):
            errorMessage = "Blue value out of range: 0-255"
            raise ValueError(errorMessage)
        return '\033[48;2;%i;%i;%im' % (red, green, blue)

if __name__ == '__main__':
# 4 bit colour:
    print(colours.fg.red, "This", " is", colours.bg.darkgrey, " a", colours.strikethrough, " test", colours.reset)
# 8 bit colour:
    print(colours.fg8bit(9), "This", colours.reset, " is ", colours.bg8bit(213), "a test", colours.reset)
# 16 bit colour:
    print(colours.fgrgb(255,0,0), "This", colours.reset, " is ", colours.bgrgb(0, 255, 0), colours.underline, " a test", colours.reset)
    exit(0)