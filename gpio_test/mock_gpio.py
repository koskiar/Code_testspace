class GPIO:
    BCM = IN = OUT = PUD_UP = None

    @staticmethod
    def setmode(mode): pass

    @staticmethod
    def setup(pin, mode, pull_up_down=None): pass

    @staticmethod
    def input(pin): return 0

    @staticmethod
    def cleanup(): pass