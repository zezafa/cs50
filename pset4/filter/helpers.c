#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            float ave = (image[y][x].rgbtRed + image[y][x].rgbtGreen + image[y][x].rgbtBlue) / 3.0;
            image[y][x].rgbtRed = round(ave);
            image[y][x].rgbtGreen = round(ave);
            image[y][x].rgbtBlue = round(ave);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            int newRed = round(0.393 * image[y][x].rgbtRed + 0.769 * image[y][x].rgbtGreen + 0.189 * image[y][x].rgbtBlue);
            int newGreen = round(0.349 * image[y][x].rgbtRed + 0.686 * image[y][x].rgbtGreen + 0.168 * image[y][x].rgbtBlue);
            int newBlue = round(0.272 * image[y][x].rgbtRed + 0.534 * image[y][x].rgbtGreen + 0.131 * image[y][x].rgbtBlue);

            if (newRed > 255)
            {
                newRed = 255;
            }

            if (newGreen > 255)
            {
                newGreen = 255;
            }

            if (newBlue > 255)
            {
                newBlue = 255;
            }

            image[y][x].rgbtRed = newRed;
            image[y][x].rgbtGreen = newGreen;
            image[y][x].rgbtBlue = newBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //RGBTRIPLE(*revImage)[width] = image;

    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < round(width / 2.0); x++)
        {
            // Swap the constructs.
            RGBTRIPLE temp;
            temp = image[y][x];
            image[y][x] = image[y][width - (x + 1)];
            image[y][width - (x + 1)] = temp;
            //image[y][x] = revImage[y][width-x];
            //image[y][width / 2 + x] = image[y][x];
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    //Copy contents of the image to copy image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    //Count average value of 9 px
    int tempRed = 0;
    int tempGreen = 0;
    int tempBlue = 0;
    int count = 0;
    //Iterate pixels
    //printf("test");
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Reset values
            tempRed = 0;
            tempGreen = 0;
            tempBlue = 0;
            count = 0;
            //printf("i is %i", i);
            //Iterate 9 pixels around sel. pixel
            for (int bi = i - 1; bi < i + 2 && bi < height; bi++)
            {
                if (bi < 0)
                {
                    continue;
                }
                for (int bj = j - 1; bj < j + 2 && bj < width; bj++)
                {
                    if (bj < 0)
                    {
                        continue;
                    }
                    tempRed += image[bi][bj].rgbtRed;
                    tempGreen += image[bi][bj].rgbtGreen;
                    tempBlue += image[bi][bj].rgbtBlue;
                    count++;
                }
            }

            //Find average color of those 9 pixels
            copy[i][j].rgbtRed = round(tempRed / (float) count);
            copy[i][j].rgbtGreen = round(tempGreen / (float) count);
            copy[i][j].rgbtBlue = round(tempBlue / (float) count);
        }
    }

    //Copy contents of the copy image to image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }

    return;
}
