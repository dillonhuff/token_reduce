from os.path import *

from delta_debugger import *
from run_case import *
from test_case import *

failing_test_dir = '/Users/dillon/PythonWorkspace/token_reduce/dummy'
failing_test_name = 'test_0.cc'
failing_test_path = join(failing_test_dir, failing_test_name)
reduce_dir = './suites'

def main():
    failing_case_str = open(failing_test_path, 'r').read()
    case = TestCase(failing_test_name, failing_case_str)
    fail_msg = run_test(reduce_dir, case)
    print 'INITIAL FAIL MSG:', fail_msg
    min_case = reduce_failing_case(reduce_dir, case, fail_msg)
    print min_case.text

if __name__ == "__main__":
    main()
