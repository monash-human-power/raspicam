#include <pigpio.h>
#include <stdio.h>

#define DATAX0 0x32
#define READ_BIT 0x80   // 0b10000000

int readBytes(int handle, char *data, int count)
{
    data[0] |= READ_BIT;
    return spiXfer(handle, data, data, count);
}

int main()
{
    int LSM6DS3;
    char data[7];
    const int baud = 5000000;  // SPI baudrate
    int count=0;

    if (gpioInitialise() < 0)
    {
        printf("\nFailed to initialize GPIO!\n\n");
        return 1;
    }

    LSM6DS3 = spiOpen(0, baud, 3);
    if (LSM6DS3 < 0)
    {
        printf("spiOpen Failed.\n\n");
    }

    data[0]=DATAX0;
    count=spiXfer(LSM6DS3,data,data,7);
    //data[0]=WHO_AM_I;
    //count = readBytes(LSM6DS3, data, 1);

    printf("\n%d bytes were transferred\n\n",count);
    printf("data was %d %d %d %d %d %d %d %d\n\n",data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]);

    return 1;
}
