import os
import unittest

DIR_EXAMPLES = 'examples'


class TestExamples(unittest.TestCase):
    def test_examples(self):
        for file_only in os.listdir(DIR_EXAMPLES):
            file = os.path.join(DIR_EXAMPLES, file_only)
            if file[:7] != 'example' or file[-3:] != '.py':
                continue
            os.system(f'python3 {file}')
