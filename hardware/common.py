try:
    import RPi.GPIO as gpio

    ON_PI = True
except (ImportError, RuntimeError):
    ON_PI = False


def cleanup():
    if ON_PI:
        gpio.cleanup()
