#include <pigpio.h>
#include <stdio.h>
#include <stdlib.h>

int main()
{
    int pin = 4;
    int fs = 4000;
    int t = 20;	// length of run in seconds
    int screen = 0;
    int samples = fs*t;

    int i;
    int *p;
    p = malloc(samples*sizeof(int));

    gpioInitialise();
    gpioSetPullUpDown(pin,PI_PUD_UP);

    printf("\nStarting run....");

    for(i = 0; i < samples; i++)
    {
	if(screen)
	{
	    printf("\n%d",gpioRead(pin));
	}
	else
	{
	    p[i] = gpioRead(pin);
	}
	time_sleep(0.00025);
    }

    printf("\nWriting to file....\n\n");

    FILE *f;
    f = fopen("speed.csv","w");
    for(i = 0; i < samples; i++)
    {
	fprintf(f,"\n%d",p[i]);
    }
    fclose(f);
}
