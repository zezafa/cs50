// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 27;

// Hash table
node *table[N];

// Number of words in dictionary
int count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //remember to make lower-cased version of the word
    char tmp[LENGTH + 1];
    int len = strlen(word);
    for (int i = 0; i < len; i++)
    {
        tmp[i] = tolower(word[i]);
    }
    tmp[len] = '\0';

    // hash word to obtain a hash value
    int index = hash(word);

    // access linked list at that index in the hash table
    node *cursor = table[index];

    // traverse linked list, looking for the word
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, tmp) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
// Hash function from edouardjamin github's page.
unsigned int hash(const char *word)
{
    int index = 0;

    // find sum of all ascii values
    for (int i = 0; word[i] != '\00'; i++)
    {
        // make upper letters to lower
        index += tolower(word[i]);
    }
    // So it does not overflow hash table size
    return index % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //printf("yes");
    // Open dictionary file
    FILE *dict = fopen(dictionary, "r");

    if (dict == NULL)
    {
        // speller.c prints error message;
        return 1;
    }

    // Read strings from file one at a time
    char readword[LENGTH + 1];
    int index = 0;

    while (fscanf(dict, "%s\n", readword) != EOF)
    {
        // Create a new node for each word
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return 1;
        }

        //n->word = malloc(sizeof(char) * (LENGTH + 1));

        strcpy(n->word, readword);

        // Hash word to obtain a hash value
        index = hash(readword);

        // Insert node into hash table at that location
        // If first object
        if (table[index] == NULL)
        {
            table[index] = n;
            n->next = NULL;
        }
        // if not first object
        else
        {
            n->next = table[index];
            table[index] = n;
        }

        count++;

    }

    fclose(dict);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // count logic is in load function
    return count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // searched after malloc and freed memory
    // remembered to iterate through
    node *cursor;
    node *tmp;

    for (int i = 0; i < N; i++)
    {
        cursor = table[i];
        tmp = cursor;

        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }

        table[i] = NULL;

    }

    return true;
}
