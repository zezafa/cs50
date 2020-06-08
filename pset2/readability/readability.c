#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    string text = get_string("Text: ");
    long i = 0;
    long letters = 0;
    long words = 1; //we assume to always receive a word to begin with
    long sentences = 0; //we assume sentence to end with . ! ? (46, 33, 63)

    while (text[i] != '\0')
    {
        //printf("%c\n", text[letters]);

        //see ascii table
        if (((int) text[i] >= 65 && (int) text[i] <= 90) || ((int) text[i] >= 97 && (int) text[i] <= 122))
        {
            letters++;
        }
        //space is 32 in ascii
        if ((int) text[i] == 32)
        {
            words++;
        }

        if ((int) text[i] == 46 || (int) text[i] == 33 || (int) text[i] == 63)
        {
            sentences++;
        }

        i++;
    }
    //printf("%li letter(s)\n", letters);
    //printf("%li word(s)\n", words);
    //printf("%li sentence(s)\n", sentences);

    float index = 0.0588 * (letters / (float) words * 100.0) - 0.296 * (sentences / (float) words * 100.0) - 15.8;

    if (index < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
        return 0;
    }
    printf("Grade %.0lf\n", round(index));

}