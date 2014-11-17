LangGrind
=========

Toolkit to aid all the grindy parts of learning new languages. Keep track of
personal progress and identify areas to spend more time on. Language aquisition
software is a generally a joke, thus this project is not meant to provide
direct means for language aquisition, but to provide efficient memorization
exercises with progress markers and gamification.

tl;dr fun exercises with minimal critical thinking.


Current Status
--------------

Work is being put into structuring vocabulary data into logical formats. Data
entry is a butt. Grammar classes are still being figured out, but some useful
data can be found in data/


Exercises
---------
* Vocabulary
* Verb conjugation
* Sentance constructions


Language Support
----------------
* Korean for English speakers


Data Formats
------------

Vocabulary format:
    
    {
      <TERM>: {
        "data": {
          "definitions": [
            [
              <definition list 1>
            ],
            [
              <definition list 2>
            ],
            .
            .
            .
          ],
          "metadata": {
            "chapter": "<chapter no.>",
            "section": "<main|aux>",
            "classes": [
              <grammar class1>,
              <grammar class2>,
              .
              .
              .
            ],
          }
        }
      },
      .
      .
      .
    }

raw txt format:

    Chapter <no.> - <main text|aux vocab>
        <term1>; <csv definitions1>
        <term2>; <csv definitions2>
        .
        .
        .
    
    Chapter <no.> - <main text|aux vocab>
        .
        .
        .

    .
    .
    .

txt to json format:

    [
     {
       "class": [],
       "definitions": [
         "three"
       ],
       "section": {
         "chapter": 8,
         "part": "text"
       },
       "term": "\uc138"
     },
     .
     .
     .
   ]

