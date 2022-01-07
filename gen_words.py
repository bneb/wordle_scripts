from nltk import download
from nltk.corpus import brown

WORD_FILE_PATH = './five_letter_words.txt'


def main():
    print('downloading brown')
    download('brown')
    print(' - done')
    print('preparing word list')
    words = {w.lower() for w in brown.words() if len(w) == 5 and w.isalpha()}
    print(' - done')
    print(f'writing to {WORD_FILE_PATH}')
    with open(WORD_FILE_PATH, 'w') as f: f.write('\n'.join(words))
    print(' - done')


if __name__ == '__main__':
    main()
