#include <pigpio.h>
#include <stdio.h>

#define WHO_AM_I 0x0f
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

    //count=spiXfer(LSM6DS3,WHO_AM_I,result,1);
    data[0]=WHO_AM_I;
    count = readBytes(LSM6DS3, data, 1);

    printf("%d bytes were transferred",count);

    if(data[1]==0x69)
    {
        printf("\nCommunication Successful!\n\n");
    }
    return 1;
}
