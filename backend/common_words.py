# These are common words that can be ignored because they are not listed in the database.

common_words = ['a', 'ah', 'about', 'above', 'across', 'after', 'again', 'ago', 'all', 'along', 'already', 'always', 'am', 'among', 'an', 'and', 'another', 'any', 'anyone', 'anything', 'are', 'around', 'as', 'at', 'away', 'be', 'been', 'before', 'began', 'behind', 'below', 'besides', 'best', 'better', 'between', 'both', 'but', 'by', 'came', 'can\'t', 'colour', 'course', 'did', 'done', 'down', 'each', 'early', 'either', 'else', 'enough', 'even', 'ever', 'every', 'everyone', 'everybody', 'except', 'extremely', 'false', 'far', 'fast', 'few', 'for', 'from', 'front', 'further', 'goodbye', 'half', 'he', 'hello', 'her', 'here', 'hers', 'him', 'his', 'how', 'i', 'if', 'in', 'inside', 'into', 'is', 'it', 'its', 'just', 'kept', 'la', 'last', 'lately', 'left', 'less', 'long', 'lot', 'lower', 'mah', 'many', 'mark', 'me', 'more', 'most', 'much', 'my', 'near', 'nearly', 'neighbour', 'neither', 'never', 'next', 'no', 'none', 'nor', 'not', 'nothing', 'now', 'of', 'off', 'often', 'oh', 'on', 'only', 'ooh', 'oooh', 'or', 'our', 'out', 'outside', 'over', 'own', 'per', 'please', 'plenty', 'plowmen', 'probably', 'quite', 'rah', 'really', 'ro', 'said', 'same', 'several', 'she', 'should', 'since', 'so', 'some', 'somebody', 'someone', 'something', 'sometimes', 'soon', 'spoke', 'still', 'such', 'sudden', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'this', 'though', 'through', 'to', 'today', 'together', 'tomorrow', 'tonight', 'too', 'true', 'twice', 'under', 'until', 'up', 'us', 'usually', 'very', 'was', 'we', 'were', 'well', 'went', 'what', 'when', 'where', 'which', 'while', 'who', 'why', 'with', 'without', 'worth', 'yesterday', 'yet', 'you', 'your', 'zero']

# Adding additional words:
# ah, among, be, been, began, came, did, done, kept, la, mah, oh, ooh, oooh, plowmen, rah, ro, said, somebody, spoke, them, there, they, through, us, we, went, worth


# TODO:
# Need to remove -ing, -ly suffixes. (But only some of them..)
# ie: act is a valid word, but actting is not.
# ie: drive is a valid word, but driving is not.
# ie: false is a valid word, but falsely is not.
# ie: fool is a valid word, but fooling is not.
# ie: get is a valid word, but getting and gets is not.
# ie: kind is a valid word, but kindly is not.
# ie: make is a valid word, but making is not.
# ie: talk is a valid word, but talking is not.
# ie: try is a valid word, but trying is not.
# ie: watch, watching
# ie: yell, yelling

# Need to convert Canadian spelling to American. 
# ie: color is a valid word, but colour is not.
# ie: gray is a valid word, but grey is not.

# Plurals need to be shortened. 
# ie: fear is a valid word, but fears is not. 
# ie: life is a valid word, but life's is not. 
# ie: prince is a valid word, but princes is not. 
# ie: rider is a valid word, but rider is not.
# ie: servant is a valid word, but servant is not.
# ie: thing is a valid word, but things is not.
# ie: woman is a valid word, but women is not.
# ie: businessman is a valid word, but businessmen is not.
# edge: there, theres, and there's are not valid words.
# edge: that, that's are not valid words.

# Need to remove contractions.
# contractions = ["aren't", "can't", "couldn't", "didn't", "doesn't", "don't", "hadn't", "hasn't", "haven't", "he'd", "he'll", "he's", "I'd", "I'll", "I'm", "I've", "isn't", "let's", "mightn't", "mustn't", "shan't", "she'd", "she'll", "she's", "shouldn't", "that's", "there's", "they'd", "they'll", "they're", "they've", "we'd", "we're", "we've", "weren't", "what'll", "what're", "what's", "what've", "where's", "who's", "who'll", "who're", "who's", "who've", "won't", "wouldn't", "you'd", "you'll", "you're", "you've"]
# edge: could is not valid word.
# edge: it and it's are not valid words.
# edge: we, we're, we've are not valid words.
# edge: you, you're are not valid words.

# Need to remove slang.
# cuz, gonna, huh, uh, why'd

# Maybe remove duplicate characters. (What does this mean?)