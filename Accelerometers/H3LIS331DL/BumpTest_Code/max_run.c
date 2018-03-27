#include <stdio.h>
#include <pigpio.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>

#define READ_BIT      0x80
#define MULTI_BIT     0x40
#define CTRL_REG1   0x20
#define CTRL_REG4   0x23
#define DATAX0      0x28
#define CTRL_REG1_CONTENTS 0b00111111   // Normal Mode, 1000Hz ODR, Enable axes
#define CTRL_REG4_CONTENTS 0b00000000   // +-100g (change bits 2/3 - 00 = 100g, 01 = 200g, 11 = 400g)

int readBytes(int handle, char *data, int count) {
    data[0] |= READ_BIT;
    if (count > 1) data[0] |= MULTI_BIT;
    return spiXfer(handle, data, data, count);
}

int writeBytes(int handle, char *data, int count) {
    if (count > 1) data[0] |= MULTI_BIT;
    return spiWrite(handle, data, count);
}

int main(int argc, char *argv[])
{
    int bytes, h;
    int16_t x, y, z;
    double rt, rx, ry, rz;
    const double accConversion = 2 * 100.0 / 65536.0;
    const int speedSPI = 2000000;
    char data[7];
    double tStart, t;
    int ODR = 1000;
    double delay = 1.0 / ODR;

    h = spiOpen(0, speedSPI, 3);
    data[0] = CTRL_REG1;
    data[1] = CTRL_REG1_CONTENTS;
    writeBytes(h, data, 2);
    data[0] = CTRL_REG4;
    data[1] = CTRL_REG4_CONTENTS;

    tStart = time_time();
    while (1)
    {
        data[0] = DATAX0;
        bytes = readBytes(h, data, 7);
        if (bytes == 7)
        {
            x = (data[2]<<8)|data[1];
            rx = x * accConversion;
            y = (data[4]<<8)|data[3];
            ry = y * accConversion;
            z = (data[6]<<8)|data[5];
            rz = z * accConversion;
            t = time_time() - tStart;

            printf("\n");
            if ((x > 30) | (y > 30) | (z > 30))
            {
                printf("t = %.2f\tx = %.2f\ty = %.2f\tz = %.2f\n", t, rx, ry, rz);
            }
        }
        time_sleep(delay);  // pigpio sleep is accurate enough for console output, not necessary to use nanosleep
    }
    gpioTerminate();
