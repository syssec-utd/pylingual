from time import perf_counter
import unittest
from featurize import get_text_length
from datalabs import load_dataset

class MyTestCase(unittest.TestCase):

    def test_Data_featurize(self):
        dataset = load_dataset('ag_news')
        one_start = perf_counter()
        res = dataset['train'].apply(get_text_length, mode='memory', num_proc=1)
        one_end = perf_counter()
        print('One proc: ' + str(one_end - one_start))
if __name__ == '__main__':
    unittest.main()