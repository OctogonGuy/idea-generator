"""
File: util.py
Author: Alex Gill
A utility file for the random sentence generator program.
"""
import string

def readIdeaFile(filename):
    """Reads a file and returns a list of all non-empty lines"""
    # Open the file
    file = open(filename, 'r', encoding='utf-8')

    # Read the titles
    titles = []
    for line in file:
        line = line.strip()
        line = line.replace('\\n', '\n')
        if line != '' and line[0:2] != '//':
            titles.append(line)

    # Close the file
    file.close()

    # Return the contents
    return titles


def readWordFile(filename):
    """Reads a file and returns a list of dictionaries with 'singular'
    and 'plural' entries if two or simply strings if one."""
    # Open the file
    file = open(filename, 'r', encoding='utf-8')

    # Read the words
    words = []
    for line in file:
        w = line.strip().split(',')
        if len(w) >= 2:
            words.append({"singular":w[0], "plural":w[1]})
        else:
            words.append(w[0])

    # Close the file
    file.close()

    # Return the contents
    return words


class TopicFormatter(string.Formatter):
    def format_field(self, value, format_spec):
        """Formats the idea titles"""

        if isinstance(value.word, str):

            # is/are
            if format_spec.endswith('is/are'):
                if value.number == 'singular':
                    value = 'is'
                else:
                    value = 'are'
            
            # has/have
            elif format_spec.endswith('has/have'):
                if value.number == 'singular':
                    value = 'has'
                else:
                    value = 'have'

            # a/an
            elif format_spec.endswith('a/an'):
                if value.word[0].lower == 'a' or \
                   value.word[0].lower == 'e' or \
                   value.word[0].lower == 'i' or \
                   value.word[0].lower == 'o' or \
                   value.word[0].lower == 'u':
                    value = 'an'
                else:
                    value = 'a'

            # singular version of topic
            elif format_spec.endswith('s'):
                value = value.singular
            
            # plural version of topic
            elif format_spec.endswith('p'):
                value = value.plural

            else:
                value = value.word
        else:
            value = value.word
        
        return super(TopicFormatter, self).format(value, format_spec)
    

class Topic():
    """Topic class"""
    def __init__(self, singular, plural, number):
        self.singular = singular[0].upper() + singular[1:]
        self.plural = plural[0].upper() + plural[1:]
        self.number = number
        if number == 'singular':
            self.word = self.singular
        else:
            self.word = self.plural