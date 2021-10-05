# Phonetizer basics

## Introduction
Phonetizer basics provides a set of tools to build a python phonetizer for your language.
It was developed by Lo Congrès (https://locongres.org) among a set of tools to build datas for NLP applications for poorly endowed languages.


## How to use ?
First, you need to adapt the functions in functions.py to your language. Every place you need to do ajustments is marked with the mention "----> to complete". Mostly, you have to translate the vocabulary lists and add rules to transcribe words into International Phonetic Alphabet in your language.

If you want, you can complete the exceptions.csv file with words whose pronunciation deviates from the general rule. Then, you need to update the exception file with the command python3 picklize_exceptions.py.

You can then use the functions from the functions.py file in your own programs (see a description of these functions in the file).
