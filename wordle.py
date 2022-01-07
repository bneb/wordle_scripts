from collections import Counter
from itertools import permutations
from math import log

PATH = './five_letter_words.txt'


def main():
    print('\nThis may take a moment...\n')

    words = get_words()
    letter_pos, pair_freq = get_letter_pos_freq_and_pair_freq(words)
    freq_means = get_frequency_means(words)
    ranked_letters = get_ranked_letters(freq_means)
    top17 = set(ranked_letters[:17])

    combos = get_combos(top17, words, freq_means, letter_pos, pair_freq)
    top_score = combos[0][0]

    print('best first three guesses:')
    for score, w1, w2, w3 in combos[:10]:
        print(f'  {score/top_score:.3f} :: 1) {w1} 2) {w2} 3) {w3}')


def get_letter_frequency(words):
    return Counter(l for w in words for l in w)


def get_words():
    with open(PATH, 'r') as f:
        return {w.strip() for w in f.read().split('\n')}


def get_letter_pos_freq_and_pair_freq(words):
    '''Returns the modal position of each letter.'''
    letter_pos = dict()
    pair_freq = Counter()

    for w in words:
        for i, l in enumerate(w):
            pair = ('', l) if i == 0 else (w[i-1], l)
            pair_freq.update([pair])

            letter_pos[l] = letter_pos.get(l, Counter())
            letter_pos[l].update([i])

    return letter_pos, pair_freq


def get_frequency_means(words):
    overall_freq = get_letter_frequency(words)
    unique_freq = get_letter_frequency([set(w) for w in words])

    freq_means = dict()

    for l, ufreq in unique_freq.items():
        ofreq = overall_freq[l]
        # use harmonic mean here to weight letter
        mean = (2 * ufreq * ofreq) / (ufreq + ofreq)
        freq_means[l] = mean

    return freq_means


def get_ranked_letters(freq_means):
    ranked_letters = [k for k, v in sorted(
        freq_means.items(),
        key=lambda p: p[1],
        reverse=True)]

    return ranked_letters


def score(words, freq_means, letter_pos, pair_freq):
    score = 0

    for i, l in enumerate(words):
        freq_score = freq_means[l]
        pos_score = letter_pos[l][i]
        pair_score = 1 if i%5 == 0 else pair_freq[(words[i-1], l)]
        word_order_score = 1/(1+i//5)
        score += log(freq_score) * log(pos_score + pair_score) * word_order_score

    return score


def get_combos(top17, words, freq_means, letter_pos, pair_freq):
    combos = []

    for c in permutations(top17, 5):
        w1 = ''.join(c)
        if w1 not in words or 'e' not in c or 'u' in c: continue

        for d in permutations(top17 - set(c), 5):
            w2 = ''.join(d)
            if w2 not in words: continue

            for e in permutations(top17 - set(c) - set(d), 5):
                w3 = ''.join(e)
                if w3 not in words: continue

                combo_score = score(w1+w2+w3, freq_means, letter_pos, pair_freq)
                combos.append((combo_score, w1, w2, w3))

    return sorted(combos, reverse=True)


if __name__ == '__main__':
    main()
