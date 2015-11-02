import itertools
import re
import shutil

from run_case import *
from tokenizer import *

def reduce_failing_case(reduce_path, test_case, fail_msg):
    assert(fail_msg != '')
    res = delta_debug(reduce_path, test_case, fail_msg, 2)
    return res

def delta_debug(reduce_path, test_case, fail_msg, grain):
    print 'CALLED DDMIN'
    print test_case.text
    print 'grain = ', str(grain)
    subsets = split_into_subsets(test_case, grain)
    print '# subsets = ', str(len(subsets))
    print 'ALL SUBSETS'
    for subset in subsets:
        print 'SUBSET'
        print_tokens(subset)
    fail_subset = first_failing_case(reduce_path, test_case.name, subsets, fail_msg)

    if not fail_subset is None:
        print 'SUBSET FAIL'
        new_case = TestCase(test_case.name, untokenize(fail_subset))
        return delta_debug(reduce_path, new_case, fail_msg, 2)

    test_tokens = tokenize(test_case.text)
    test_size = len(test_tokens)    
    subset_comps = subset_complements(test_tokens, subsets)
    fail_complement = first_failing_case(reduce_path, test_case.name, subset_comps, fail_msg)
    
    if not fail_complement is None:
        print 'COMPLEMENT FAIL'
        print 'test_size', str(test_size)
        new_case = TestCase(test_case.name, untokenize(fail_complement))
        print new_case.text
        new_grain = max(grain - 1, 2)
        print 'grain', str(new_grain)
#        return new_case
        return delta_debug(reduce_path, new_case, fail_msg, new_grain)

    print 'test_size = ', str(test_size)
    print 'grain = ', str(grain)
    if grain < test_size:
        print 'INCREASE GRAIN'
        new_grain = min(test_size, 2*grain)
        return delta_debug(reduce_path, test_case, fail_msg, new_grain)

    print 'DELTA IS DONE'
    return test_case

def split_into_subsets(test_case, grain):
    tokens = tokenize(test_case.text)
    size = len(tokens) / grain
    assert(size != 0)
    return list(split_seq(tokens, size))

def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))

def subset_complements(tokens, subsets):
    complements = []
    for subset in subsets:
        complements.append(complement(tokens, subset))
    return complements

def complement(tokens, subset):
    assert(subset != [])
    startLoc = sublist_exists(tokens, subset)
    if startLoc == 0:
#        print 'Start location is zero'
        complement = tokens[len(subset):]
    else:
        complement = tokens[0:startLoc] + tokens[startLoc + len(subset):]    
    # print 'TEST COMPLEMENT'
    # print 'Tokens'
    # print_tokens(tokens)
    # print 'Subset'
    # print_tokens(subset)
    # print 'Complement'
    # print_tokens(complement)
    return complement

def print_tokens(tokens):
    for token in tokens:
        print token.string

def same_tokens(l, r):
    if len(l) != len(r):
        return False
    for i in xrange(len(l)):
        if l[i].string != r[i].string:
            return False
    return True
    
def sublist_exists(tokens, sublist):
    for i in range(len(tokens)-len(sublist)+1):
#        print_tokens(sublist)
#        print_tokens(tokens[i:i+len(sublist)])
        if same_tokens(sublist, tokens[i:i+len(sublist)]):
            return i
    print 'tokens'
    print_toks(tokens)
    print 'Sublist'
    print_toks(sublist)
    assert(False)

def first_failing_case(reduce_path, name, subsets, fail_msg):
    for subset in subsets:
        shutil.rmtree(reduce_path)
        res = run_test(reduce_path, TestCase(name, untokenize(subset)))
        if res == fail_msg:
            return subset
    return None

