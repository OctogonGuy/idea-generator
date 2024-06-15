"""
Program: idea.py
Author: Alex Gill
Generates titles from user-given topics.
"""
from util import readIdeaFile, readWordFile, TopicFormatter, Topic
import random

TWO_CHANCE = 0.16
THREE_CHANCE = 0.04
one_titles = readIdeaFile("resources\\titles\\one_topic_titles.txt")
two_titles = readIdeaFile("resources\\titles\\two_topic_titles.txt")
three_titles = readIdeaFile("resources\\titles\\three_topic_titles.txt")
nouns_usually_plural = readWordFile("resources\\words\\noun.csv")
nouns_usually_singular = readWordFile("resources\\words\\noun_usually_uncountable.csv")
nouns_usually_singular += readWordFile("resources\\words\\noun_countable_and_uncountable.csv")
nouns_always_plural = readWordFile("resources\\words\\noun_pluralia_tantum.csv")
nouns_always_singular = readWordFile("resources\\words\\noun_uncountable.csv")
nouns_always_singular += readWordFile("resources\\words\\noun_non_attested.csv")


def main():
    """Test the module"""
    
    # Make sure all titles are acceptable
    subjects = list(setOfSubjects("octopus, deer, abolitionism"))
    fmt = TopicFormatter()
    for title in one_titles:
        fmt.format(title, random.choice(subjects))
    print("Check 1 passed")
    for title in two_titles:
        fmt.format(title, random.choice(subjects), random.choice(subjects))
    print("Check 2 passed")
    for title in three_titles:
        fmt.format(title, random.choice(subjects), random.choice(subjects), random.choice(subjects))
    print("Check 3 passed")

    # Get subjects from user
    subjects = setOfSubjects(input("What subject(s) would you like to generate ideas for?\n" + 
                    "(Enter one or more nouns separated by commas): "))
    
    # Get number of titles to generate from user
    number = int(input("How many? "))
    
    # Generate titles
    for i in range(number):
        print(generateTitle(subjects))



def generateTitle(subjects):
    """Generates an idea"""

    randomNumber = random.random()
    fmt = TopicFormatter()

    # Create a copy of subjects as to not permanently remove any
    subjectsCopy = subjects.copy()
    
    # Generate a title with three subjects
    if len(subjects) >= 3 and randomNumber < THREE_CHANCE:

        title = fmt.format(random.choice(three_titles), removeRandom(subjectsCopy), removeRandom(subjectsCopy), removeRandom(subjectsCopy))
    
    # Generate a title with two subjects
    elif len(subjects) >= 2 and randomNumber < TWO_CHANCE + THREE_CHANCE:
        title = fmt.format(random.choice(two_titles), removeRandom(subjectsCopy), removeRandom(subjectsCopy))
    
    # Generate a title with one subject
    else:
        title = fmt.format(random.choice(one_titles), removeRandom(subjectsCopy))
    
    return title



def setOfSubjects(subjectsText):
    """Converts a string with subjects separated by commas into a set
    with each subject."""
    subjectsSet = set() # (for no duplicate values)
    subjectsList = subjectsText.split(',')
    for i in range(len(subjectsList)):
        subjectsSet.add(findWordForm(subjectsList[i].strip()))
    return subjectsSet



def removeRandom(data):
    """Removes and returns a random item from a data structure."""
    item = random.choice(list(data))
    data.remove(item)
    return item



def findWordForm(word):
    """Finds the singular and plural forms of a noun. Returns the
    preffered form as well as an 's' for singular or 'p' for plural."""
    for noun in nouns_usually_plural:
        if noun['singular'] == word or noun['plural'] == word:
            return Topic(noun['singular'], noun['plural'], 'plural')
    for noun in nouns_usually_singular:
        if noun['singular'] == word or noun['plural'] == word:
            return Topic(noun['singular'], noun['plural'], 'singular')
    for noun in nouns_always_plural:
        if noun == word:
            return Topic(noun, noun, 'plural')
    for noun in nouns_always_singular:
        if noun == word:
            return Topic(noun, noun, 'singular')
    
    # Default to singular
    return Topic(word, word, 'singular')



if __name__ == '__main__':
    main()