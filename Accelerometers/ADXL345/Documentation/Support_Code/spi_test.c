#include <pigpio.h>
#include <stdio.h>

#define DATAX0 0x32
#define DATA_FORMAT     0x31    // Data_Format register address (influences 3 or 4 wire SPI, +-2g, +-4g, +-8g, +-16g)
#define BW_RATE         0x2C    // BW_Rate register address (influences ODR)
#define POWER_CTL       0x2D    // Power_CTL register address (influences Auto-sleep, Standby, Sleep, Wakup functions)
#define FORMAT_CONTENTS 0x0B    // bits to write to data format register = +/- 16g range, 13-bit resolution (p. 26 of ADXL345 datasheet)
#define BW_CONTENTS     0x0F    // Normal operation, 3200Hz
#define POWER_CONTENTS  0x08    // Measurement mode, 2Hz readings in sleep mode
#define READ_BIT 0x80   // 0b10000000
#define MULTI_BIT 0x40

int readBytes(int handle, char *data, int count) {
    data[0] |= READ_BIT;
    if (count > 1) data[0] |= MULTI_BIT;
    return spiXfer(handle, data, data, count);
}

int main()
{
    int ADXL345;
    char data[7];
    const int baud = 5000000;  // SPI baudrate
    int count=0;

    if (gpioInitialise() < 0)
    {
        printf("\nFailed to initialize GPIO!\n\n");
        return 1;
    }

    ADXL345 = spiOpen(0, baud, 3);
    if (ADXL345 < 0)
    {
        printf("spiOpen Failed.\n\n");
    }

    // Write to BW_RATE Register
    data[0] = BW_RATE | MULTI_BIT;
    data[1] = BW_CONTENTS;
    spiWrite(ADXL345, data, 2);
    printf("\nADXL345=%d,data[0]=%x,data[1]=%x\n\n",ADXL345,data[0],data[1]);

    // Write to DATA_FORMAT Register
    data[0] = DATA_FORMAT | MULTI_BIT;
    data[1] = FORMAT_CONTENTS;
    spiWrite(ADXL345, data, 2);
    printf("ADXL345=%d,data[0]=%x,data[1]=%x\n\n",ADXL345,data[0],data[1]);

    // Write to POWER_MODE Register
    data[0] = POWER_CTL | MULTI_BIT;
    data[1] = POWER_CONTENTS;
    spiWrite(ADXL345, data, 2);
    printf("ADXL345=%d,data[0]=%x,data[1]=%x\n\n",ADXL345,data[0],data[1]);

    data[0]=DATAX0;
    data[0] |= MULTI_BIT;
    count=spiXfer(ADXL345,data,data,7);
    //data[0]=WHO_AM_I;
    //count = readBytes(LSM6DS3, data, 1);

    printf("\n%d bytes were transferred\n\n",count);
    printf("data was %x %x %x %x %x %x %x %x\n\n",data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]);

    return 1;
}
