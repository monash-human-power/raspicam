

// =========================== PROGRAM SETUP =================================

#include <stdio.h>
#include <pigpio.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <time.h>

// KEY ACCELEROMETER INFORMATION
// - 3.9mg/LSB resolution
// - Measurement +-2g (10 bits), +-4g (11 bits), +-8g (12 bits), +-16g (13 bits)
// - Use of the 3200 Hz and 1600 Hz output data rates is only recommended with SPI communication rates greater than or equal to 2 MHz
// - The 800 Hz output data rate is recommended only for communication speeds greater than or equal to 400 kHz

// ACCELEROMETER REGISTERS
#define DATA_FORMAT     0x31    // Data_Format register address (influences 3 or 4 wire SPI, +-2g, +-4g, +-8g, +-16g)
#define BW_RATE         0x2C    // BW_Rate register address (influences ODR)
#define POWER_CTL       0x2D    // Power_CTL register address (influences Auto-sleep, Standby, Sleep, Wakup functions)
#define DATAX0          0x32    // Start address for reading accelerometer registers
double fs = 3200;
double t = 2;

// ACCELEROMETER SETTINGS
#define FORMAT_CONTENTS 0x0B    // bits to write to data format register = +/- 16g range, 13-bit resolution (p. 26 of ADXL345 datasheet)
#define BW_CONTENTS     0x0F    // Normal operation, 3200Hz
#define POWER_CONTENTS  0x08    // Measurement mode, 2Hz readings in sleep mode

// SPI COMMUNICATION BYTES
#define MULTI_BIT       0x40    // SPI multi-bit communication
#define READ_BIT        0x80
const double accConversion = 2 * 16.0 / 8192.0;  // +/- 16g range, 13-bit resolution (2^13 = 8192)
const int coldStartSamples = 2;  // number of samples to be read before outputting data to console (cold start delays)
const double coldStartDelay = 0.1;  // time delay between cold start reads
const int speedSPI = 5000000;  // SPI communication speed, bps

// SPI FUNCTIONS
int readBytes(int handle, char *data, int count) {
    data[0] |= READ_BIT;
    if (count > 1) data[0] |= MULTI_BIT;
    return spiXfer(handle, data, data, count);
}

int writeBytes(int handle, char *data, int count) {
    if (count > 1) data[0] |= MULTI_BIT;
    return spiWrite(handle, data, count);
}

/*void sigintHandler(int sig_num)
{
     //Reset handler to catch SIGINT next time.
       //Refer http://en.cppreference.com/w/c/program/signal
    signal(SIGINT, sigintHandler);
    printf("\n Terminating after Ctr C \n");
    fflush(stdout);
    exit(0);
}*/

// =========================== FUNCTION MAIN =================================
int main(int argc, char const *argv[])
{
    //char save_dir[256] = "/Desktop/text.txt";
    FILE *f;
    //f = fopen("text.txt", "w");
    //fprintf(f, "time, x, y, z\n");
    //int samples = fs * t;
    double tStart;
    //signal(SIGINT, sigintHandler);

    // SPI Variables
    int i;
    int success = 1;
    char data[7];
    int ADXL345, bytes;

    int16_t x, y, z;

    char filename[40];
    struct tm *timenow;
    time_t now = time(NULL);
    printf("the current time is %s",time_t)
    sprintf(filename, "%H", (int)now);
    //strftime(filename, "/home/pi/Documents/MHP_raspicam/Accelerometers/ADXL345/BumpTest_Code/%d.txt", (int)now);
    f = fopen(filename,"w");

    // Intialize gpio pins
    if (gpioInitialise() < 0)
    {
        printf("Failed to initialize GPIO!");
        return 1;
    }

    // -------------------------- SET UP SPI DEVICE --------------------------

    // Define new spi device
    ADXL345 = spiOpen(0, speedSPI, 3);

    // Write to BW_RATE Register
    data[0] = BW_RATE;
    data[1] = BW_CONTENTS;
    writeBytes(ADXL345, data, 2);

    // Write to DATA_FORMAT Register
    data[0] = DATA_FORMAT;
    data[1] = FORMAT_CONTENTS;
    writeBytes(ADXL345, data, 2);

    // Write to POWER_MODE Register
    data[0] = POWER_CTL;
    data[1] = POWER_CONTENTS;
    writeBytes(ADXL345, data, 2);

    // --------------------------- INITIALIZE READ ---------------------------

    // Find delay between samples
    double delay = 1.0 / fs;

    // Need a warm up segment to initialize readings
    for (i = 0; i < coldStartSamples; i++) {
        data[0] = DATAX0;
        bytes = readBytes(ADXL345, data, 7);
        if (bytes != 7) {
            success = 0;
        }
        time_sleep(coldStartDelay);
    }

    // --------------------------- READ DATA ---------------------------

    // Set start time
    tStart = time_time();

    // Begin reads
    //for (i = 0; i < samples; i++)
    while(1)
    {
        // Read bytes
        data[0] = DATAX0;
        bytes = readBytes(ADXL345, data, 7);

        // Process bytes on last read
        if (bytes == 7)
        {
            x = (data[2]<<8)|data[1];
            y = (data[4]<<8)|data[3];
            z = (data[6]<<8)|data[5];
            t = time_time() - tStart;
            //printf("time = %.3f, x = %.3f, y = %.3f, z = %.3f\n",
                   t, x * accConversion, y * accConversion, z * accConversion);
            fprintf(f, "%.5f, %.5f, %.5f, %.5f \n", t, x * accConversion, y * accConversion, z * accConversion);
        }
        else
        {
            success = 0;
        }

        time_sleep(delay);  // pigpio sleep is accurate enough for console output, not necessary to use nanosleep
    }

    // End read
    fclose(f);
    gpioTerminate();

    // Check for error state
    if (success == 0) {
        printf("Error occurred!");
        return 1;
    }

    return 0;
}
