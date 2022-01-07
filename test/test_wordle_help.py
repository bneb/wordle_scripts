from wordle_help import filter_words
import unittest

class TestWordleHelp(unittest.TestCase):

    def test_filter_words_returns_no_bad_matches(self):
        hot = '_____'
        warm = {'u':{0}, 'l':{2}, 's':{3}, 'm':{0}}
        cold = set('unlid carse mothy') - set(hot) - set(warm)
        words = 'slamp sleep stamp scamp swamp clamp slaum slare slart'.split(' ')

        expected = []
        actual = filter_words(hot, warm, cold, words)

        self.assertEqual(expected, actual)

