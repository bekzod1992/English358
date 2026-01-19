"""
Test questions data
"""

from typing import Dict, List, Optional

# Test questions organized by grade and topic
TESTS: Dict[int, Dict[str, List[dict]]] = {
    # 1-4 grades
    1: {
        "alphabet": [
            {
                "question": "Which letter comes after 'A'?",
                "options": {"A": "C", "B": "B", "C": "D", "D": "E"},
                "correct": "B"
            },
            {
                "question": "What letter is this? 🍎 = A____",
                "options": {"A": "Apple", "B": "Ant", "C": "Air", "D": "Art"},
                "correct": "A"
            },
            {
                "question": "Which is a vowel?",
                "options": {"A": "B", "B": "C", "C": "E", "D": "D"},
                "correct": "C"
            },
            {
                "question": "How many letters are in the English alphabet?",
                "options": {"A": "24", "B": "25", "C": "26", "D": "27"},
                "correct": "C"
            },
            {
                "question": "Which letter comes before 'D'?",
                "options": {"A": "E", "B": "C", "C": "B", "D": "A"},
                "correct": "B"
            }
        ],
        "numbers": [
            {
                "question": "What is 'three' in number?",
                "options": {"A": "2", "B": "3", "C": "4", "D": "5"},
                "correct": "B"
            },
            {
                "question": "How do you write '7' in English?",
                "options": {"A": "six", "B": "eight", "C": "seven", "D": "five"},
                "correct": "C"
            },
            {
                "question": "2 + 3 = ?",
                "options": {"A": "four", "B": "five", "C": "six", "D": "three"},
                "correct": "B"
            },
            {
                "question": "What comes after 'nine'?",
                "options": {"A": "eight", "B": "eleven", "C": "ten", "D": "seven"},
                "correct": "C"
            },
            {
                "question": "How many fingers do you have?",
                "options": {"A": "eight", "B": "nine", "C": "ten", "D": "five"},
                "correct": "C"
            }
        ],
        "colors": [
            {
                "question": "What color is the sky?",
                "options": {"A": "red", "B": "green", "C": "blue", "D": "yellow"},
                "correct": "C"
            },
            {
                "question": "What color is grass?",
                "options": {"A": "blue", "B": "green", "C": "red", "D": "white"},
                "correct": "B"
            },
            {
                "question": "🍎 is ___",
                "options": {"A": "yellow", "B": "blue", "C": "red", "D": "green"},
                "correct": "C"
            },
            {
                "question": "The sun is ___",
                "options": {"A": "blue", "B": "yellow", "C": "green", "D": "black"},
                "correct": "B"
            },
            {
                "question": "Snow is ___",
                "options": {"A": "black", "B": "blue", "C": "white", "D": "red"},
                "correct": "C"
            }
        ],
        "family": [
            {
                "question": "'Ona' in English is ___",
                "options": {"A": "father", "B": "mother", "C": "brother", "D": "sister"},
                "correct": "B"
            },
            {
                "question": "'Ota' in English is ___",
                "options": {"A": "mother", "B": "sister", "C": "father", "D": "brother"},
                "correct": "C"
            },
            {
                "question": "My mother's mother is my ___",
                "options": {"A": "sister", "B": "aunt", "C": "grandmother", "D": "mother"},
                "correct": "C"
            },
            {
                "question": "My father's son is my ___",
                "options": {"A": "sister", "B": "brother", "C": "uncle", "D": "cousin"},
                "correct": "B"
            },
            {
                "question": "'Grandparents' means ___",
                "options": {"A": "ota-ona", "B": "aka-uka", "C": "buvi-bobo", "D": "opa-singil"},
                "correct": "C"
            }
        ],
        "fruits": [
            {
                "question": "🍌 is a ___",
                "options": {"A": "apple", "B": "banana", "C": "orange", "D": "grape"},
                "correct": "B"
            },
            {
                "question": "Which fruit is yellow?",
                "options": {"A": "apple", "B": "grape", "C": "lemon", "D": "strawberry"},
                "correct": "C"
            },
            {
                "question": "'Olma' in English is ___",
                "options": {"A": "orange", "B": "apple", "C": "banana", "D": "grape"},
                "correct": "B"
            },
            {
                "question": "Which is NOT a fruit?",
                "options": {"A": "apple", "B": "banana", "C": "carrot", "D": "orange"},
                "correct": "C"
            },
            {
                "question": "'Tarvuz' in English is ___",
                "options": {"A": "melon", "B": "watermelon", "C": "lemon", "D": "orange"},
                "correct": "B"
            }
        ],
        "animals": [
            {
                "question": "🐕 is a ___",
                "options": {"A": "cat", "B": "bird", "C": "dog", "D": "fish"},
                "correct": "C"
            },
            {
                "question": "Which animal can fly?",
                "options": {"A": "dog", "B": "cat", "C": "fish", "D": "bird"},
                "correct": "D"
            },
            {
                "question": "'Mushuk' in English is ___",
                "options": {"A": "dog", "B": "cat", "C": "bird", "D": "mouse"},
                "correct": "B"
            },
            {
                "question": "Which animal lives in water?",
                "options": {"A": "bird", "B": "dog", "C": "fish", "D": "cat"},
                "correct": "C"
            },
            {
                "question": "The king of animals is ___",
                "options": {"A": "elephant", "B": "tiger", "C": "lion", "D": "bear"},
                "correct": "C"
            }
        ]
    },

    # 5-7 grades
    5: {
        "present_simple": [
            {
                "question": "She ___ to school every day.",
                "options": {"A": "go", "B": "goes", "C": "going", "D": "gone"},
                "correct": "B"
            },
            {
                "question": "They ___ football on Sundays.",
                "options": {"A": "plays", "B": "playing", "C": "play", "D": "played"},
                "correct": "C"
            },
            {
                "question": "___ you like pizza?",
                "options": {"A": "Does", "B": "Do", "C": "Is", "D": "Are"},
                "correct": "B"
            },
            {
                "question": "He ___ not speak French.",
                "options": {"A": "do", "B": "does", "C": "is", "D": "are"},
                "correct": "B"
            },
            {
                "question": "My mother ___ delicious food.",
                "options": {"A": "cook", "B": "cooks", "C": "cooking", "D": "cooked"},
                "correct": "B"
            },
            {
                "question": "I ___ wake up early.",
                "options": {"A": "doesn't", "B": "don't", "C": "isn't", "D": "aren't"},
                "correct": "B"
            },
            {
                "question": "___ she live in Tashkent?",
                "options": {"A": "Do", "B": "Is", "C": "Does", "D": "Are"},
                "correct": "C"
            },
            {
                "question": "We ___ English at school.",
                "options": {"A": "studies", "B": "studying", "C": "study", "D": "studied"},
                "correct": "C"
            }
        ],
        "present_continuous": [
            {
                "question": "I ___ a book now.",
                "options": {"A": "read", "B": "reads", "C": "am reading", "D": "reading"},
                "correct": "C"
            },
            {
                "question": "She ___ TV at the moment.",
                "options": {"A": "watches", "B": "is watching", "C": "watch", "D": "watched"},
                "correct": "B"
            },
            {
                "question": "They ___ football right now.",
                "options": {"A": "play", "B": "plays", "C": "playing", "D": "are playing"},
                "correct": "D"
            },
            {
                "question": "___ you studying?",
                "options": {"A": "Do", "B": "Does", "C": "Are", "D": "Is"},
                "correct": "C"
            },
            {
                "question": "He ___ sleeping now.",
                "options": {"A": "isn't", "B": "doesn't", "C": "don't", "D": "aren't"},
                "correct": "A"
            },
            {
                "question": "What ___ you doing?",
                "options": {"A": "do", "B": "does", "C": "is", "D": "are"},
                "correct": "D"
            },
            {
                "question": "The baby ___ crying.",
                "options": {"A": "are", "B": "is", "C": "am", "D": "be"},
                "correct": "B"
            },
            {
                "question": "We ___ not working today.",
                "options": {"A": "is", "B": "am", "C": "are", "D": "be"},
                "correct": "C"
            }
        ],
        "past_simple": [
            {
                "question": "I ___ to school yesterday.",
                "options": {"A": "go", "B": "goes", "C": "went", "D": "going"},
                "correct": "C"
            },
            {
                "question": "She ___ a cake last week.",
                "options": {"A": "make", "B": "makes", "C": "making", "D": "made"},
                "correct": "D"
            },
            {
                "question": "___ you see the movie?",
                "options": {"A": "Do", "B": "Does", "C": "Did", "D": "Was"},
                "correct": "C"
            },
            {
                "question": "They ___ not come to the party.",
                "options": {"A": "do", "B": "did", "C": "was", "D": "were"},
                "correct": "B"
            },
            {
                "question": "He ___ his homework last night.",
                "options": {"A": "do", "B": "does", "C": "did", "D": "doing"},
                "correct": "C"
            },
            {
                "question": "We ___ a great time at the beach.",
                "options": {"A": "have", "B": "has", "C": "had", "D": "having"},
                "correct": "C"
            },
            {
                "question": "She ___ English two years ago.",
                "options": {"A": "study", "B": "studies", "C": "studied", "D": "studying"},
                "correct": "C"
            },
            {
                "question": "I ___ him at the store.",
                "options": {"A": "see", "B": "saw", "C": "seen", "D": "seeing"},
                "correct": "B"
            }
        ],
        "reading": [
            {
                "question": "What does 'skimming' mean?",
                "options": {"A": "Reading every word", "B": "Quick overview", "C": "Reading aloud", "D": "Translating"},
                "correct": "B"
            },
            {
                "question": "'Scanning' is used to ___",
                "options": {"A": "understand everything", "B": "find specific information", "C": "memorize", "D": "translate"},
                "correct": "B"
            },
            {
                "question": "The main idea is usually in the ___",
                "options": {"A": "middle", "B": "end", "C": "first paragraph", "D": "title only"},
                "correct": "C"
            },
            {
                "question": "'Who' is a question word for ___",
                "options": {"A": "place", "B": "time", "C": "person", "D": "reason"},
                "correct": "C"
            },
            {
                "question": "'Where' asks about ___",
                "options": {"A": "time", "B": "person", "C": "reason", "D": "place"},
                "correct": "D"
            }
        ],
        "writing": [
            {
                "question": "A paragraph should start with a ___",
                "options": {"A": "conclusion", "B": "topic sentence", "C": "example", "D": "question"},
                "correct": "B"
            },
            {
                "question": "Which connector shows contrast?",
                "options": {"A": "and", "B": "but", "C": "so", "D": "because"},
                "correct": "B"
            },
            {
                "question": "'First, Then, Finally' show ___",
                "options": {"A": "contrast", "B": "reason", "C": "sequence", "D": "comparison"},
                "correct": "C"
            },
            {
                "question": "The last sentence of a paragraph is ___",
                "options": {"A": "topic sentence", "B": "example", "C": "concluding sentence", "D": "question"},
                "correct": "C"
            },
            {
                "question": "'Because' shows ___",
                "options": {"A": "contrast", "B": "sequence", "C": "reason", "D": "addition"},
                "correct": "C"
            }
        ],
        "speaking": [
            {
                "question": "How do you introduce yourself?",
                "options": {"A": "I am name", "B": "My name is...", "C": "Name I am", "D": "Is my name"},
                "correct": "B"
            },
            {
                "question": "'How old are you?' asks about ___",
                "options": {"A": "name", "B": "place", "C": "age", "D": "hobby"},
                "correct": "C"
            },
            {
                "question": "To ask about hobbies, you say ___",
                "options": {"A": "What is your hobby?", "B": "Who is hobby?", "C": "Where hobby?", "D": "Hobby what?"},
                "correct": "A"
            },
            {
                "question": "'I like + ___' (verb form)",
                "options": {"A": "to go", "B": "going", "C": "go", "D": "Both A and B"},
                "correct": "D"
            },
            {
                "question": "'Nice to meet you' is used when ___",
                "options": {"A": "saying goodbye", "B": "meeting someone new", "C": "asking questions", "D": "apologizing"},
                "correct": "B"
            }
        ]
    },

    # 8-9 grades
    8: {
        "present_perfect": [
            {
                "question": "I ___ never ___ to London.",
                "options": {"A": "have/been", "B": "has/been", "C": "have/be", "D": "has/be"},
                "correct": "A"
            },
            {
                "question": "She ___ here for 5 years.",
                "options": {"A": "live", "B": "lives", "C": "has lived", "D": "living"},
                "correct": "C"
            },
            {
                "question": "___ you ever eaten sushi?",
                "options": {"A": "Do", "B": "Did", "C": "Have", "D": "Has"},
                "correct": "C"
            },
            {
                "question": "He has worked here ___ 2018.",
                "options": {"A": "for", "B": "since", "C": "from", "D": "at"},
                "correct": "B"
            },
            {
                "question": "They have studied English ___ 10 years.",
                "options": {"A": "since", "B": "for", "C": "from", "D": "at"},
                "correct": "B"
            },
            {
                "question": "I have ___ finished my homework.",
                "options": {"A": "yet", "B": "already", "C": "never", "D": "ever"},
                "correct": "B"
            },
            {
                "question": "Have you done it ___?",
                "options": {"A": "already", "B": "just", "C": "yet", "D": "ever"},
                "correct": "C"
            },
            {
                "question": "She has ___ seen that movie.",
                "options": {"A": "yet", "B": "for", "C": "since", "D": "just"},
                "correct": "D"
            }
        ],
        "past_perfect": [
            {
                "question": "When I arrived, the train ___.",
                "options": {"A": "left", "B": "has left", "C": "had left", "D": "leaves"},
                "correct": "C"
            },
            {
                "question": "She ___ dinner before he came.",
                "options": {"A": "finished", "B": "has finished", "C": "had finished", "D": "finishes"},
                "correct": "C"
            },
            {
                "question": "I ___ never seen snow before I went to Russia.",
                "options": {"A": "have", "B": "has", "C": "had", "D": "was"},
                "correct": "C"
            },
            {
                "question": "After he ___ the book, he returned it.",
                "options": {"A": "read", "B": "has read", "C": "had read", "D": "reads"},
                "correct": "C"
            },
            {
                "question": "By the time I woke up, mom ___ breakfast.",
                "options": {"A": "made", "B": "has made", "C": "had made", "D": "makes"},
                "correct": "C"
            }
        ],
        "future": [
            {
                "question": "I think it ___ rain tomorrow.",
                "options": {"A": "will", "B": "is going to", "C": "is", "D": "was"},
                "correct": "A"
            },
            {
                "question": "Look at those clouds! It ___ rain.",
                "options": {"A": "will", "B": "is going to", "C": "is", "D": "was"},
                "correct": "B"
            },
            {
                "question": "I ___ help you with that. (just decided)",
                "options": {"A": "am going to", "B": "will", "C": "am", "D": "would"},
                "correct": "B"
            },
            {
                "question": "We ___ to London next week. (planned)",
                "options": {"A": "will fly", "B": "fly", "C": "are flying", "D": "flew"},
                "correct": "C"
            },
            {
                "question": "She ___ a doctor when she grows up.",
                "options": {"A": "is", "B": "is going to be", "C": "was", "D": "been"},
                "correct": "B"
            }
        ],
        "conditionals": [
            {
                "question": "If you heat water, it ___.",
                "options": {"A": "boils", "B": "will boil", "C": "would boil", "D": "boiled"},
                "correct": "A"
            },
            {
                "question": "If I study, I ___ the exam.",
                "options": {"A": "pass", "B": "will pass", "C": "would pass", "D": "passed"},
                "correct": "B"
            },
            {
                "question": "If I were rich, I ___ a car.",
                "options": {"A": "buy", "B": "will buy", "C": "would buy", "D": "bought"},
                "correct": "C"
            },
            {
                "question": "If it rains, we ___ inside.",
                "options": {"A": "stay", "B": "will stay", "C": "would stay", "D": "stayed"},
                "correct": "B"
            },
            {
                "question": "If I ___ you, I would study harder.",
                "options": {"A": "am", "B": "was", "C": "were", "D": "be"},
                "correct": "C"
            },
            {
                "question": "Water ___ if you heat it to 100°C.",
                "options": {"A": "boils", "B": "will boil", "C": "would boil", "D": "boiling"},
                "correct": "A"
            }
        ],
        "passive": [
            {
                "question": "English ___ worldwide.",
                "options": {"A": "speaks", "B": "is spoken", "C": "spoke", "D": "speaking"},
                "correct": "B"
            },
            {
                "question": "The book ___ by Hemingway.",
                "options": {"A": "wrote", "B": "written", "C": "was written", "D": "write"},
                "correct": "C"
            },
            {
                "question": "The car ___ in Japan.",
                "options": {"A": "made", "B": "is made", "C": "make", "D": "making"},
                "correct": "B"
            },
            {
                "question": "The letter ___ yesterday.",
                "options": {"A": "sent", "B": "is sent", "C": "was sent", "D": "send"},
                "correct": "C"
            },
            {
                "question": "The project ___ next week.",
                "options": {"A": "will finish", "B": "will be finished", "C": "finished", "D": "finishing"},
                "correct": "B"
            },
            {
                "question": "Many houses ___ every year.",
                "options": {"A": "build", "B": "built", "C": "are built", "D": "building"},
                "correct": "C"
            }
        ],
        "reading_vocab": [
            {
                "question": "The prefix 'un-' means ___",
                "options": {"A": "again", "B": "not", "C": "before", "D": "after"},
                "correct": "B"
            },
            {
                "question": "The suffix '-tion' makes a ___",
                "options": {"A": "verb", "B": "adjective", "C": "noun", "D": "adverb"},
                "correct": "C"
            },
            {
                "question": "'Re-' means ___",
                "options": {"A": "not", "B": "again", "C": "before", "D": "opposite"},
                "correct": "B"
            },
            {
                "question": "We ___ a decision. (make/do)",
                "options": {"A": "make", "B": "do", "C": "take", "D": "have"},
                "correct": "A"
            },
            {
                "question": "We ___ homework. (make/do)",
                "options": {"A": "make", "B": "do", "C": "take", "D": "have"},
                "correct": "B"
            }
        ]
    },

    # 10-11 grades
    10: {
        "advanced_grammar": [
            {
                "question": "The man ___ lives next door is a doctor.",
                "options": {"A": "which", "B": "who", "C": "whom", "D": "whose"},
                "correct": "B"
            },
            {
                "question": "The book ___ I bought is interesting.",
                "options": {"A": "who", "B": "whom", "C": "which", "D": "whose"},
                "correct": "C"
            },
            {
                "question": "The girl ___ father is a teacher is my friend.",
                "options": {"A": "who", "B": "which", "C": "whom", "D": "whose"},
                "correct": "D"
            },
            {
                "question": "This is the place ___ I was born.",
                "options": {"A": "which", "B": "who", "C": "where", "D": "when"},
                "correct": "C"
            },
            {
                "question": "I remember the day ___ we first met.",
                "options": {"A": "which", "B": "where", "C": "who", "D": "when"},
                "correct": "D"
            },
            {
                "question": "The man standing there is my uncle. (Full form: The man ___ is standing there)",
                "options": {"A": "which", "B": "who", "C": "whom", "D": "whose"},
                "correct": "B"
            }
        ],
        "conditionals_adv": [
            {
                "question": "If I ___ studied, I would have passed.",
                "options": {"A": "have", "B": "has", "C": "had", "D": "having"},
                "correct": "C"
            },
            {
                "question": "If she had known, she ___ helped.",
                "options": {"A": "will have", "B": "would have", "C": "would", "D": "will"},
                "correct": "B"
            },
            {
                "question": "___ I known, I would have helped. (Inversion)",
                "options": {"A": "If", "B": "Have", "C": "Had", "D": "Would"},
                "correct": "C"
            },
            {
                "question": "If I were taller, I ___ played basketball. (Mixed)",
                "options": {"A": "would", "B": "would have", "C": "will", "D": "will have"},
                "correct": "B"
            },
            {
                "question": "If I had studied medicine, I ___ a doctor now. (Mixed)",
                "options": {"A": "would be", "B": "would have been", "C": "will be", "D": "am"},
                "correct": "A"
            },
            {
                "question": "___ I you, I would study harder. (Inversion)",
                "options": {"A": "Was", "B": "Am", "C": "Were", "D": "Be"},
                "correct": "C"
            }
        ],
        "reported_speech": [
            {
                "question": "'I am happy' → He said he ___ happy.",
                "options": {"A": "is", "B": "was", "C": "were", "D": "be"},
                "correct": "B"
            },
            {
                "question": "'I will come' → She said she ___ come.",
                "options": {"A": "will", "B": "would", "C": "can", "D": "could"},
                "correct": "B"
            },
            {
                "question": "'I have finished' → He said he ___ finished.",
                "options": {"A": "has", "B": "have", "C": "had", "D": "having"},
                "correct": "C"
            },
            {
                "question": "'Where do you live?' → He asked where I ___.",
                "options": {"A": "live", "B": "lives", "C": "lived", "D": "living"},
                "correct": "C"
            },
            {
                "question": "'Open the door' → He told me ___ the door.",
                "options": {"A": "open", "B": "to open", "C": "opening", "D": "opened"},
                "correct": "B"
            },
            {
                "question": "'Don't run' → She told us ___ run.",
                "options": {"A": "don't", "B": "not", "C": "not to", "D": "to not"},
                "correct": "C"
            },
            {
                "question": "'now' changes to ___ in reported speech.",
                "options": {"A": "now", "B": "then", "C": "here", "D": "there"},
                "correct": "B"
            },
            {
                "question": "'today' changes to ___ in reported speech.",
                "options": {"A": "today", "B": "yesterday", "C": "that day", "D": "this day"},
                "correct": "C"
            }
        ],
        "academic_reading": [
            {
                "question": "What does SQ3R stand for? S = ___",
                "options": {"A": "Study", "B": "Survey", "C": "Search", "D": "Scan"},
                "correct": "B"
            },
            {
                "question": "'Inference' means ___",
                "options": {"A": "direct statement", "B": "reading between the lines", "C": "skimming", "D": "scanning"},
                "correct": "B"
            },
            {
                "question": "Academic texts often use ___ voice.",
                "options": {"A": "active", "B": "passive", "C": "future", "D": "present"},
                "correct": "B"
            },
            {
                "question": "'Therefore' shows ___",
                "options": {"A": "contrast", "B": "addition", "C": "result", "D": "example"},
                "correct": "C"
            },
            {
                "question": "'However' shows ___",
                "options": {"A": "result", "B": "addition", "C": "contrast", "D": "example"},
                "correct": "C"
            }
        ],
        "essay": [
            {
                "question": "An essay introduction should end with a ___",
                "options": {"A": "question", "B": "example", "C": "thesis statement", "D": "conclusion"},
                "correct": "C"
            },
            {
                "question": "How many body paragraphs does a standard essay have?",
                "options": {"A": "1", "B": "2-3", "C": "5", "D": "1-2"},
                "correct": "B"
            },
            {
                "question": "'To sum up' is used in the ___",
                "options": {"A": "introduction", "B": "body", "C": "conclusion", "D": "title"},
                "correct": "C"
            },
            {
                "question": "Each body paragraph should start with a ___",
                "options": {"A": "conclusion", "B": "example", "C": "topic sentence", "D": "question"},
                "correct": "C"
            },
            {
                "question": "'On the other hand' shows ___",
                "options": {"A": "addition", "B": "contrast", "C": "result", "D": "sequence"},
                "correct": "B"
            }
        ],
        "listening": [
            {
                "question": "Before listening, you should ___",
                "options": {"A": "panic", "B": "read questions first", "C": "close your eyes", "D": "translate everything"},
                "correct": "B"
            },
            {
                "question": "During listening, you should ___",
                "options": {"A": "write every word", "B": "take short notes", "C": "translate", "D": "stop if you miss something"},
                "correct": "B"
            },
            {
                "question": "Key words help you ___",
                "options": {"A": "translate", "B": "identify main ideas", "C": "memorize", "D": "write faster"},
                "correct": "B"
            },
            {
                "question": "If you miss an answer, you should ___",
                "options": {"A": "stop and think", "B": "go back", "C": "move on", "D": "give up"},
                "correct": "C"
            },
            {
                "question": "Stress and intonation help you understand ___",
                "options": {"A": "spelling", "B": "meaning and emphasis", "C": "grammar", "D": "vocabulary"},
                "correct": "B"
            }
        ]
    }
}

# Copy tests for similar grades
for grade in [2, 3, 4]:
    TESTS[grade] = TESTS[1].copy()

for grade in [6, 7]:
    TESTS[grade] = TESTS[5].copy()

for grade in [9]:
    TESTS[grade] = TESTS[8].copy()

for grade in [11]:
    TESTS[grade] = TESTS[10].copy()


# IELTS Tests
IELTS_TESTS: Dict[str, List[dict]] = {
    "reading": [
        {
            "question": "In IELTS Reading, you have ___ minutes.",
            "options": {"A": "30", "B": "45", "C": "60", "D": "90"},
            "correct": "C"
        },
        {
            "question": "IELTS Reading has ___ sections.",
            "options": {"A": "2", "B": "3", "C": "4", "D": "5"},
            "correct": "B"
        },
        {
            "question": "'Skimming' is best for finding ___",
            "options": {"A": "specific details", "B": "main ideas", "C": "numbers", "D": "names"},
            "correct": "B"
        },
        {
            "question": "'Scanning' is best for finding ___",
            "options": {"A": "main ideas", "B": "author's opinion", "C": "specific information", "D": "conclusions"},
            "correct": "C"
        },
        {
            "question": "In True/False/Not Given questions, 'Not Given' means ___",
            "options": {"A": "the answer is false", "B": "information is not in the text", "C": "the answer is true", "D": "you should guess"},
            "correct": "B"
        },
        {
            "question": "How many questions are in IELTS Reading?",
            "options": {"A": "30", "B": "35", "C": "40", "D": "45"},
            "correct": "C"
        },
        {
            "question": "Which is a good strategy for matching headings?",
            "options": {"A": "Read the whole text first", "B": "Match easiest paragraphs first", "C": "Guess randomly", "D": "Skip difficult ones"},
            "correct": "B"
        },
        {
            "question": "For 'complete the sentence' questions, answers should be ___",
            "options": {"A": "your own words", "B": "grammatically correct with the sentence", "C": "as long as possible", "D": "in capital letters"},
            "correct": "B"
        },
        {
            "question": "In IELTS Academic Reading, texts are from ___",
            "options": {"A": "newspapers only", "B": "academic sources", "C": "fiction books", "D": "social media"},
            "correct": "B"
        },
        {
            "question": "You should spend about ___ minutes per passage.",
            "options": {"A": "10", "B": "15", "C": "20", "D": "30"},
            "correct": "C"
        }
    ]
}


# CEFR Tests
CEFR_TESTS: Dict[str, List[dict]] = {
    "a1": [
        {
            "question": "Hello! My name ___ John.",
            "options": {"A": "am", "B": "is", "C": "are", "D": "be"},
            "correct": "B"
        },
        {
            "question": "I ___ from Uzbekistan.",
            "options": {"A": "is", "B": "are", "C": "am", "D": "be"},
            "correct": "C"
        },
        {
            "question": "___ is your name?",
            "options": {"A": "Who", "B": "What", "C": "Where", "D": "When"},
            "correct": "B"
        },
        {
            "question": "She ___ a student.",
            "options": {"A": "am", "B": "are", "C": "is", "D": "be"},
            "correct": "C"
        },
        {
            "question": "They ___ teachers.",
            "options": {"A": "is", "B": "am", "C": "are", "D": "be"},
            "correct": "C"
        },
        {
            "question": "I have ___ apple.",
            "options": {"A": "a", "B": "an", "C": "the", "D": "-"},
            "correct": "B"
        },
        {
            "question": "This is ___ book.",
            "options": {"A": "a", "B": "an", "C": "the", "D": "-"},
            "correct": "A"
        },
        {
            "question": "___ are you? - I'm fine.",
            "options": {"A": "What", "B": "Who", "C": "How", "D": "Where"},
            "correct": "C"
        }
    ],
    "a2": [
        {
            "question": "She ___ to school every day.",
            "options": {"A": "go", "B": "goes", "C": "going", "D": "gone"},
            "correct": "B"
        },
        {
            "question": "I ___ TV yesterday.",
            "options": {"A": "watch", "B": "watches", "C": "watched", "D": "watching"},
            "correct": "C"
        },
        {
            "question": "He can ___ English.",
            "options": {"A": "speaks", "B": "spoke", "C": "speaking", "D": "speak"},
            "correct": "D"
        },
        {
            "question": "There ___ a book on the table.",
            "options": {"A": "is", "B": "are", "C": "am", "D": "be"},
            "correct": "A"
        },
        {
            "question": "She is ___ than her sister.",
            "options": {"A": "tall", "B": "taller", "C": "tallest", "D": "more tall"},
            "correct": "B"
        },
        {
            "question": "I ___ like coffee.",
            "options": {"A": "doesn't", "B": "don't", "C": "isn't", "D": "aren't"},
            "correct": "B"
        },
        {
            "question": "___ you play tennis?",
            "options": {"A": "Does", "B": "Do", "C": "Is", "D": "Are"},
            "correct": "B"
        },
        {
            "question": "We are going ___ the cinema.",
            "options": {"A": "at", "B": "in", "C": "to", "D": "on"},
            "correct": "C"
        }
    ],
    "b1": [
        {
            "question": "I have ___ to Paris twice.",
            "options": {"A": "be", "B": "been", "C": "being", "D": "was"},
            "correct": "B"
        },
        {
            "question": "If it rains, I ___ stay home.",
            "options": {"A": "would", "B": "will", "C": "am", "D": "was"},
            "correct": "B"
        },
        {
            "question": "She ___ here since 2020.",
            "options": {"A": "live", "B": "lives", "C": "has lived", "D": "lived"},
            "correct": "C"
        },
        {
            "question": "The book ___ by many people.",
            "options": {"A": "read", "B": "reads", "C": "is read", "D": "reading"},
            "correct": "C"
        },
        {
            "question": "I used to ___ early when I was young.",
            "options": {"A": "waking", "B": "woke", "C": "wake", "D": "woken"},
            "correct": "C"
        },
        {
            "question": "He asked me ___ I was from.",
            "options": {"A": "what", "B": "where", "C": "who", "D": "which"},
            "correct": "B"
        },
        {
            "question": "I wish I ___ more money.",
            "options": {"A": "have", "B": "has", "C": "had", "D": "having"},
            "correct": "C"
        },
        {
            "question": "The man ___ car was stolen called the police.",
            "options": {"A": "who", "B": "which", "C": "whose", "D": "whom"},
            "correct": "C"
        }
    ],
    "b2": [
        {
            "question": "If I had studied, I ___ passed the exam.",
            "options": {"A": "will have", "B": "would have", "C": "would", "D": "will"},
            "correct": "B"
        },
        {
            "question": "He told me that he ___ the movie.",
            "options": {"A": "saw", "B": "see", "C": "had seen", "D": "has seen"},
            "correct": "C"
        },
        {
            "question": "By the time I arrived, the train ___.",
            "options": {"A": "left", "B": "has left", "C": "had left", "D": "leaves"},
            "correct": "C"
        },
        {
            "question": "She suggested ___ to the beach.",
            "options": {"A": "go", "B": "going", "C": "to go", "D": "went"},
            "correct": "B"
        },
        {
            "question": "I'd rather you ___ me the truth.",
            "options": {"A": "tell", "B": "told", "C": "telling", "D": "to tell"},
            "correct": "B"
        },
        {
            "question": "___ had I arrived than it started to rain.",
            "options": {"A": "Hardly", "B": "No sooner", "C": "Scarcely", "D": "Barely"},
            "correct": "B"
        },
        {
            "question": "Not only ___ she smart, but also hardworking.",
            "options": {"A": "is", "B": "was", "C": "does", "D": "did"},
            "correct": "A"
        },
        {
            "question": "It's high time we ___ home.",
            "options": {"A": "go", "B": "went", "C": "going", "D": "gone"},
            "correct": "B"
        }
    ],
    "c1": [
        {
            "question": "___ I known, I would have helped.",
            "options": {"A": "If", "B": "Have", "C": "Had", "D": "Should"},
            "correct": "C"
        },
        {
            "question": "Under no circumstances ___ leave early.",
            "options": {"A": "you should", "B": "should you", "C": "you would", "D": "would you"},
            "correct": "B"
        },
        {
            "question": "It was John ___ broke the window.",
            "options": {"A": "which", "B": "who", "C": "whom", "D": "whose"},
            "correct": "B"
        },
        {
            "question": "Not until midnight ___ he arrive.",
            "options": {"A": "does", "B": "did", "C": "had", "D": "has"},
            "correct": "B"
        },
        {
            "question": "Seldom ___ such beauty.",
            "options": {"A": "I have seen", "B": "have I seen", "C": "I saw", "D": "saw I"},
            "correct": "B"
        },
        {
            "question": "___ it not for your help, I would have failed.",
            "options": {"A": "Was", "B": "Were", "C": "Had", "D": "If"},
            "correct": "B"
        },
        {
            "question": "So tired ___ that I fell asleep immediately.",
            "options": {"A": "I was", "B": "was I", "C": "I am", "D": "am I"},
            "correct": "B"
        },
        {
            "question": "Little ___ he know what awaited him.",
            "options": {"A": "do", "B": "does", "C": "did", "D": "had"},
            "correct": "C"
        }
    ],
    "c2": [
        {
            "question": "Be that as it ___, we must continue.",
            "options": {"A": "may", "B": "might", "C": "can", "D": "could"},
            "correct": "A"
        },
        {
            "question": "He speaks English as if he ___ a native speaker.",
            "options": {"A": "is", "B": "was", "C": "were", "D": "be"},
            "correct": "C"
        },
        {
            "question": "___ though he tried, he couldn't succeed.",
            "options": {"A": "Try", "B": "Tried", "C": "Trying", "D": "To try"},
            "correct": "A"
        },
        {
            "question": "Come ___ may, I'll be there.",
            "options": {"A": "which", "B": "what", "C": "that", "D": "who"},
            "correct": "B"
        },
        {
            "question": "He is, ___ it were, a walking dictionary.",
            "options": {"A": "so", "B": "as", "C": "if", "D": "like"},
            "correct": "B"
        },
        {
            "question": "The more you practice, ___.",
            "options": {"A": "better you get", "B": "the better you get", "C": "you get better", "D": "the best you get"},
            "correct": "B"
        },
        {
            "question": "Suffice ___ to say, he was not pleased.",
            "options": {"A": "this", "B": "that", "C": "it", "D": "which"},
            "correct": "C"
        },
        {
            "question": "___ having finished the work, he went home.",
            "options": {"A": "On", "B": "In", "C": "At", "D": "By"},
            "correct": "A"
        }
    ]
}


def get_test_questions(grade: int, topic: str) -> Optional[List[dict]]:
    """Get test questions for grade and topic"""
    if grade in TESTS and topic in TESTS[grade]:
        return TESTS[grade][topic]
    return None


def get_ielts_test(test_type: str) -> Optional[List[dict]]:
    """Get IELTS test questions"""
    return IELTS_TESTS.get(test_type)


def get_cefr_test(level: str) -> Optional[List[dict]]:
    """Get CEFR test questions"""
    return CEFR_TESTS.get(level)
