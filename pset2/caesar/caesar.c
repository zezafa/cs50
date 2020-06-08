#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char *argv[])
{
    if (argc == 2)
    {
        int j = 0;
        while (argv[1][j] != '\0')
        {
            if (argv[1][j] < 48 || argv[1][j] > 57)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
            j++;
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int k = atoi(argv[1]);
    //printf("%i\n", k);


    string pt = get_string("plaintext: ");


    //ciphertext part
    int j = 0;
    printf("ciphertext: ");
    while (pt[j] != '\0')
    {
        char c = pt[j];
        char sC = pt[j]; //secret char

        //upper case
        if (c >= 65 && c <= 90)
        {
            sC = ((c - 65) + k) % 26 + 65;
        }

        //lower case
        if (c >= 97 && c <= 122)
        {
            sC = ((c - 97) + k) % 26 + 97;
        }

        //print one char at the time
        printf("%c", sC);
        j++;
    }
    printf("\n");
    return 0;
}