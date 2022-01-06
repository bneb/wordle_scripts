from ast import literal_eval
from collections import Counter
from math import exp

HOT_CHARS = set('_abcdefghijklmnopqrstuvwxyz')


def main():
    with open('5letterwords.txt', 'r') as f:
        words = {w.strip() for w in f.read().strip().split('\n')}

    freq = Counter([l for w in words for l in w])
    hot = get_hot()
    warm = get_warm()
    cold = get_cold()
    cold -= set(hot)
    cold -= set(warm)

    guesses = get_next_guess(hot, warm, cold, words, freq)
    print('\nThe next best guesses are:')
    for score, guess in guesses[:-10:-1]:
        print(f'  - {score = :.2f} :: {guess = }')


def get_hot():
    print('\nenter in the partially filled target. example: f_nny:')
    found = False

    while not found:
        hot = input('  -> ')
        found = (len(hot) == 5 and set(hot).issubset(HOT_CHARS))
        if not found:
            print('  invalid. try again.')

    return hot


def get_warm():
    print('\nenter in the dict of partial matches to guessed positions.')
    print('  example: {"a":{1, 2}, "b":{4}}')
    warm = None

    while warm is None:
        try: warm = literal_eval(input('  -> ').strip())
        except: print('  invalid. try again.')

    return warm


def get_cold():
    print('\nenter in the set of non-matches. example: {"a", "b"}')
    cold = None

    while cold is None:
        try: cold = literal_eval(input('  -> ').strip())
        except: print('  invalid. try again.')

    return cold


def get_next_guess(hot, warm, cold, words, freq):
    '''Given letters placed, unplaced, or not in the target, return a guess.
    @param hot: an array of letters in their correct placement
    @param warm: a map of letters to their incorrectly guessed positions
    @param cold: a set of letters that are not in the target
    @returns a five letter guess for the next round
    '''
    filtered = filter_words(hot, warm, cold, words)
    letter_pos = get_avg_letter_position(filtered)
    ranked = score_all(filtered, freq, letter_pos)

    return ranked


def score_all(words, freq, letter_pos):
    '''Return score-word-pairs in ascending order by score.'''
    return sorted([(score(w, freq, letter_pos), w) for w in words])


def score(word, freq, letter_pos):
    '''Score a word based on the letter frequencies and position matching.
    @param word: the word to score
    @param freq: a map of the frequency of letters across the corpus.
    @param letter_pos: a map of a letter to average position in eligible words.
    @returns a score for the provided word
    '''
    score = 0

    for i, l in enumerate(word):
        letter_freq = freq[l]
        scalar = exp(-letter_pos[l])
        score += letter_freq * scalar

    return score


def get_avg_letter_position(words):
    letter_pos = dict()

    for w in words:
        for i, l in enumerate(w):
            letter_pos[l] = letter_pos.get(l, []) + [i]

    return {k: sum(v)/len(v) for k, v in letter_pos.items()}


def filter_words(hot, warm, cold, words):
    '''Limit the search space based on letter categories.
    @param hot: an array of letters in the correct placement.
    @param warm: a map of letters to the set of incorrectly guessed positions.
    @param cold: a set of letters that are not in the target.
    '''
    filtered = []
    found = False

    for word in words:
        found = True
        for i, l in enumerate(word):
            if l in cold:
                found = False
                break
            if hot[i] not in ('_', l):
                found = False
                break
            if i in warm.get(l,set()):
                found = False
                break
            if not all([w in word for w in warm]):
                found = False
                break

        if found:
            filtered.append(word)

    return filtered


def get_overall_freq(words):
    '''Return the frequency of all letters over all words.'''
    return Counter(c for w in words for c in w)


def get_words():
    with open('5letterwords.txt', 'r') as f:
        return {w.strip() for w in f.read().split('\n')}


if __name__ == '__main__':
    main()
