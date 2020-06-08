#readability.py - asks for text input and then calculates Coleman-Liau index (readability index)

from cs50 import get_string

text = get_string("Text: ")

letters = 0
words = 1
sentences = 0

for i, value in enumerate(text):
    if value.isalpha():
        letters += 1
    elif ord(value) == 32:
        words += 1
    elif (ord(value) == 46 or ord(value) == 33 or ord(value) == 63):
        sentences += 1

index = (0.0588 * letters / words * 100) - (0.296 * sentences / words * 100) - 15.8
print(letters)
print(words)
print(sentences)

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print ("Grade 16+")
else:
    print(f"Grade {int(round(index))}")