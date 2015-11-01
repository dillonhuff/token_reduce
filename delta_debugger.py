from run_case import *
from tokenizer import *

def reduce_failing_case(reduce_path, test_case, fail_msg):
    assert(fail_msg != '')
    res = delta_debug(reduce_path, test_case, fail_msg, 2)
    return test_case

def delta_debug(reduce_path, test_case, fail_msg, grain):
    test_tokens = tokenize(test_case.text)
    fail_subset = failing_subset(reduce_path, test_case.name, test_tokens, fail_msg, grain)
    return test_case
