

// =========================== PROGRAM SETUP =================================

#include <stdio.h>
#include <pigpio.h>

// ACCELEROMETER REGISTERS
#define CTRL1_XL        0x10    // Linear acceleration sensor control register 1
#define DATAX0          0x28    // Start address for reading accelerometer registers

// ACCELEROMETER SETTINGS
#define CTRL1_XL_CONTENTS   0xA4    // +/-16 g, 6667 Hz

// SPI COMMUNICATION BYTES
#define MULTI_BIT       0x40    // SPI multi-bit communication
#define READ_BIT        0x80
const int coldStartSamples = 2;  // number of samples to be read before outputting data to console (cold start delays)
const double coldStartDelay = 0.1;  // time delay between cold start reads
const int speedSPI = 5000000;  // SPI communication speed, bps

// =========================== FUNCTION MAIN =================================
int main(int argc, char const *argv[])
{
    // SPI Variables
    int i;
    char data[7];
    int LSM6DS3, bytes;

    // Intialize gpio pins
    if (gpioInitialise() < 0)
    {
        printf("Failed to initialize GPIO!");
        return 1;
    }

    // -------------------------- SET UP SPI DEVICE --------------------------

    // Define new spi device
    LSM6DS3 = spiOpen(0, speedSPI, 3);
    printf("LSM6DS3=%d",LSM6DS3);

    // Write to BW_RATE Register
    data[0] = BW_RATE | MULTI_BIT;
    data[1] = BW_CONTENTS;
    spiWrite(LSM6DS3, data, 2);
    printf("LSM6DS3=%d,data[0]=%d,data[1]=%d\n\n",LSM6DS3,data[0],data[1]);

    // Write to DATA_FORMAT Register
    data[0] = DATA_FORMAT | MULTI_BIT;
    data[1] = FORMAT_CONTENTS;
    spiWrite(LSM6DS3, data, 2);
    printf("LSM6DS3=%d,data[0]=%d,data[1]=%d\n\n",LSM6DS3,data[0],data[1]);

    // Write to POWER_MODE Register
    data[0] = POWER_CTL | MULTI_BIT;
    data[1] = POWER_CONTENTS;
    spiWrite(LSM6DS3, data, 2);
    printf("LSM6DS3=%d,data[0]=%d,data[1]=%d\n\n",LSM6DS3,data[0],data[1]);

    // --------------------------- INITIALIZE READ ---------------------------

    // Need a warm up segment to initialize readings
    for (i = 0; i < coldStartSamples; i++) {
        data[0] = DATAX0 | MULTI_BIT | READ_BIT;
        bytes = spiXfer(LSM6DS3, data, data, 7);
        printf("bytes = %d,data was %x %x %x %x %x %x %x %x\n\n",bytes,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]);
        time_sleep(coldStartDelay);
    }

    // --------------------------- READ DATA ---------------------------

    data[0] = DATAX0 | MULTI_BIT | READ_BIT;
    bytes = spiXfer(LSM6DS3, data, data, 7);
    printf("bytes=%d,data was %x %x %x %x %x %x %x %x\n\n",bytes,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]);

    // Process bytes on last read
    if (bytes == 7)
    {
        printf("Success!\n\n");
    }
    else
    {
        printf("Error!\n\n");
    }

    gpioTerminate();

    return 0;
}
