# These are common words that can be ignored because they are not listed in the database.

common_words = ['a', 'ah', 'about', 'above', 'across', 'after', 'again', 'ago', 'all', 'along', 'already', 'always', 'am', 'an', 'and', 'another', 'any', 'anyone', 'anything', 'are', 'around', 'as', 'at', 'away', 'be', 'before', 'behind', 'below', 'besides', 'best', 'better', 'between', 'both', 'but', 'by',   'can\'t',   'colour', 'course', 'down', 'each', 'early', 'either', 'else', 'enough', 'even', 'ever', 'every', 'everyone', 'everybody', 'except', 'extremely', 'false', 'far', 'fast', 'few', 'for', 'from', 'front', 'further', 'goodbye', 'half', 'he', 'hello', 'her', 'here', 'hers', 'him', 'his', 'how', 'i', 'if', 'in', 'inside', 'into', 'is', 'it', 'its', 'just', 'kept', 'la', 'last', 'lately', 'left', 'less', 'long', 'lot', 'lower', 'mah', 'many', 'mark', 'me', 'more', 'most', 'much', 'my', 'near', 'nearly', 'neighbour', 'neither', 'never', 'next', 'no', 'none', 'nor', 'not', 'nothing', 'now', 'of', 'off', 'often', 'oh', 'on', 'only', 'ooh', 'oooh', 'or', 'our', 'out', 'outside', 'over', 'own', 'per', 'please', 'plenty', 'probably', 'quite', 'rah', 'really', 'ro', 'said', 'same', 'several', 'she', 'should', 'since', 'so', 'some', 'someone', 'something', 'sometimes', 'soon', 'still', 'such', 'sudden', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'this', 'though', 'through', 'to', 'today', 'together', 'tomorrow', 'tonight', 'too', 'true', 'twice', 'under', 'until', 'up', 'usually', 'very', 'was', 'we', 'were', 'well', 'what', 'when', 'where', 'which', 'while', 'who', 'why', 'with', 'without', 'yesterday', 'yet', 'you', 'your', 'zero']

# Adding additional words:
# ah, be, kept, la, mah, oh, ooh, oooh, rah, ro, said, them, they, through


# TODO:
# Need to remove special characters, punctuation.

# Need to remove -ing, -ly suffixes. (But only some of them..)

# Need to convert Canadian spelling to American. 
# ie: color is a valid word, but colour is not.
# ie: gray is a valid word, but grey is not.

# Plurals need to be shortened. 
# ie: prince is a valid word, but princes is not. 
# ie: rider is a valid word, but rider is not.
# ie: servant is a valid word, but servant is not.
# ie: woman is a valid word, but women is not.

# Need to remove contractions.
# contractions = ["aren't", "can't", "couldn't", "didn't", "doesn't", "don't", "hadn't", "hasn't", "haven't", "he'd", "he'll", "he's", "I'd", "I'll", "I'm", "I've", "isn't", "let's", "mightn't", "mustn't", "shan't", "she'd", "she'll", "she's", "shouldn't", "that's", "there's", "they'd", "they'll", "they're", "they've", "we'd", "we're", "we've", "weren't", "what'll", "what're", "what's", "what've", "where's", "who's", "who'll", "who're", "who's", "who've", "won't", "wouldn't", "you'd", "you'll", "you're", "you've"]

# Maybe remove duplicate characters. (What does this mean?)