from collections import Counter
from itertools import permutations
from math import exp

# I scraped a website and saved data to the file below.
# One could also use nltk which might be easier /shrug.
with open('5letterwords.txt', 'r') as f:
    words = {w.strip() for w in f.read().split('\n')}

# counts a letter per occurance in all words
overall_freq = Counter(c for w in words for c in w)

# counts a letter once per word (added -> a, d, e)
unique_freq = Counter([c for w in words for c in set(w)])

letter_pos = dict()
for w in words:
    for i, l in enumerate(w):
        letter_pos[l] = letter_pos.get(l, []) + [i]

letter_pos = {k: sum(v)/len(v) for k, v in letter_pos.items()}

# use harmonic mean here to weight letter
freq_means = dict()
for l, ufreq in unique_freq.items():
  ofreq = overall_freq[l]
  mean = (2 * ufreq * ofreq) / (ufreq + ofreq)
  freq_means[l] = mean

ranked_letters = [k for k, v in sorted(
    freq_means.items(),
    key=lambda p: p[1],
    reverse=True)]

top15 = set(ranked_letters[:15])

def score(word1, word2, word3):
    score = 0
    for i, l in enumerate(word1 + word2 + word3):
        letter_score = freq_means[l]
        scalar = exp(-i//5 - abs(i%5 - letter_pos[l]))
        score += letter_score * scalar
    return score

combos = []
for c in permutations(top15, 5):
    w1 = ''.join(c)
    if w1 not in words or 'e' not in c or 'u' in c: continue

    for d in permutations(top15 - set(c), 5):
        w2 = ''.join(d)
        if w2 not in words: continue

        for e in permutations(top15 - set(c) - set(d), 5):
            w3 = ''.join(e)
            if w3 not in words: continue

            combo_score = score(w1,w2,w3)
            combos.append((combo_score, w1, w2, w3))

# combinations of 5 letter words descending by score.
combos = sorted(combos)[::-1]
top_score = combos[0][0]

print('top 10 first-three-guesses:')
for score, w1, w2, w3 in combos[:10]:
    print(f'{score/top_score:.3f} :: 1) {w1} 2) {w2} 3) {w3}')

