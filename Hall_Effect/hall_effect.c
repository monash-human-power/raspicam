#include <pigpio.h>

int main()
{
    if (gpioInitialise() < 0)
    {
        printf("Failed to initialize GPIO!");
        return 1;
    }

    void aFunction(int gpio, int level, uint32_t tick)
    {
       printf("GPIO %d became %d at %d", gpio, level, tick);
    }

    // call aFunction whenever GPIO 4 changes state

    gpioSetAlertFunc(4, aFunction);

    gpioTerminate();

    return 1;
}
