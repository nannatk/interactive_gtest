# interactive_gtest

This is an interactive, simple and quick test selector for [GoogleTest](https://github.com/google/googletest).

## Guide

This was developed to make it as simple and fast as possible in test-driven development, and to pick and choose some of the GoogleTest tests to run.

Developers can execute any test by numerically selecting the listed tests. It will be faster to see.

This example runs [GoogleTest's sample1_unittest](https://github.com/google/googletest/blob/main/googletest/samples/sample1_unittest.cc) and selects `FactorialTest.Zero`.

```sh
nannatk@DESKTOP:~/interactive_gtest$ python3 interactive_gtest.py ./sample1_unittest 

=============== select testcase ===============
[0]: *
[1]: FactorialTest
[2]: IsPrimeTest
-----------------------------------------------
select: 1

=============== select testname ===============
[0]: *
[1]: Negative
[2]: Zero
[3]: Positive
-----------------------------------------------
select: 2
Running main() from /home/nannatk/workspace/googletest/googletest/src/gtest_main.cc
Note: Google Test filter = FactorialTest.Zero
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from FactorialTest
[ RUN      ] FactorialTest.Zero
[       OK ] FactorialTest.Zero (0 ms)
[----------] 1 test from FactorialTest (0 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (0 ms total)
[  PASSED  ] 1 test.

=============== select testname ===============
[0]: *
[1]: Negative
[2]: Zero
[3]: Positive
-----------------------------------------------
select: 
```

## Getting Started

The tool is written in pure Python and does not depend on any other libraries. The following versions of Python are guaranteed to work.

- Python 3.10.12

When the GoogleTest executable file is passed as an argument and invoked, a menu is displayed. Enter the number corresponding to the test you wish to run and press `Enter` to select it.

`0` is a `*` designation that always executes all the displayed tests.

If you press `Enter` without entering anything, the menu will return to one level up, i.e., test case selection.