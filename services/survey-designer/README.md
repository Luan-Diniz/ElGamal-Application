Survey Designer is the one supposed to send a survey to the Survey Handler, and
, at some point, ask for the answer.

The created survey should be at survey.json and must respect the following
structure:
    {
    "TextQuestion1" : [1, "average"],
    "TextQuestion2" : [2, "text"],
    "TextQuestion3" : [3, "multiple choice" ,
            {
                "a" : ["ChoiceText1", 3],
                "b" : ["ChoiceText2", 5],
                "c" : ["ChoiceText3", 7]
            }
        ]
    }   

There are three types of question that you can put in a survey:
    Average:
            The workers will answer with a number, and the result will be the
        calculated average of the answers.
    Text: 
            The answer of that question is a string. The answers should be shuffled
        by the Survey Handler.
    Multiple Choice:
            Here, the workers will have some options and will choose one of them.
            Every single option should be an unique prime associated to it.
            The product of these primes will be calculated with all the answers,
        then the Survey Designer will calculate how many time each options was
        chose.

Note that every question has a id that identifies it, like in 
"TextQuestion1" : [1, "average"], 1 is it id. Do note confuse this number with
the prime one associated in every alternative of a multiple choice question!




    