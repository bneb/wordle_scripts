from nltk import download
from nltk.corpus import brown
from wordle import PATH

def main():
    print('downloading brown')
    download('brown')
    print(' - done')

    print('preparing word list')
    data = {w.lower() for w in brown.words() if len(w) == 5 and w.islower()}
    print(' - done')

    print(f'writing to {PATH}')
    with open(PATH, 'w') as f: f.write('\n'.join(data))
    print(' - done')


if __name__ == '__main__':
    main()
