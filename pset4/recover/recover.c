#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");

    if (file == NULL)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //output img declared
    FILE *img = NULL;

    unsigned char buffer[512];
    char filename[8];

    int counter = 0;

    bool writingData = false;

    // it does write to buffer
    while (fread(buffer, 512, 1, file) == 1)
    {
        // checking the first 4 bytes
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (writingData == true)
            {
                fclose(img);
            }
            else
            {
                writingData = true;
            }
            //filename gets renamed (smart trick)
            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");
            counter++;
        };
        // if anything else than first 4 bytes
        if (writingData == true)
        {
            fwrite(&buffer, 512, 1, img);
        }


        //if end of memory card => break

        //check first for blocks for jpg header
        //if so start a new jpg
        //close previous jpg and start a new one
        //if jpg is started and not start of jpg, continue writing

    }


    fclose(file);
    fclose(img);

    return 0;
}
