# -*- coding: utf-8 -*-
import subprocess
import re
import argparse


class SimpleMenu(object):
    def __init__(self):
        pass

    def select(self, candidates, title=None):
        idx_width = len(str(len(candidates) - 1))
        menu_width = 50
        print('')
        if(title):
            titlestr = ('=' * 15) + ' {} '.format(title) + ('=' * 15)
            print(titlestr)
            menu_width = len(titlestr)

        for i, candidate in enumerate(candidates):
            print('[{:>{idx_width}}]: {}'.format(i, candidate, idx_width=idx_width))
        print('-' * menu_width)
        print('select: ', end='')
        inputstr = input()
        m = re.match(r'(?P<idx>\d+)', inputstr)
        if(m):
            return int(m.group('idx'))
        else:
            None

class InteractiveGtest(object):

    def __init__(self, gtest_path):
        self._gtest = gtest_path
        self._RGX_TESTCASE = re.compile(r'(?P<testcase>.+)\.')
        self._RGX_TESTNAME = re.compile(r'  (?P<testname>.+)')
        self._testlist = self.__make_testlist()

    def start(self):
        menu = SimpleMenu()
        while(True):
            # Testcaseの選択
            selected_testcase = self.__select_testcase(menu)
            if(selected_testcase is None):
                break 
            elif(selected_testcase == '*'):
                self.__execute_selected_test(selected_testcase)
            else:
                while(True):
                    # Testnameの選択
                    selected_testname = self.__select_testname(menu, selected_testcase)
                    if(selected_testname is None):
                        break 
                    else:
                        self.__execute_selected_test("{}.{}".format(selected_testcase, selected_testname))

    
    def __select_testcase(self, menu):
        # 先頭に全部実行の'* 'を追加する
        testcases = ['*'] + list(self._testlist.keys())
        while(True):
            selected = menu.select(testcases, title='select testcase')
            if(selected is None):
                return None 
            else:
                # 範囲外Idxだった場合、再度メニュー表示する
                if(selected < len(testcases)):
                    return testcases[selected]

    def __select_testname(self, menu, testcase):
        # Testcaseと違い、Testnameは中身が1つだろうと0だろうとMenuを表示する
        # 先頭に全部実行の'*'を追加する
        testnames = ['*'] + list(self._testlist[testcase])
        while(True):
            selected = menu.select(testnames, title='select testname')
            if(selected is None):
                return None
            else:
                # 範囲外Idxだった場合、再度メニュー表示する
                if(selected < len(testnames)):
                    return testnames[selected] 

    def __execute_selected_test(self, selected_test):
        options = ['--gtest_filter={}'.format(selected_test)]
        self.__execute_gtest(options, disp=True)


    def __make_testlist(self):
        output, returncode = self.__execute_gtest(['--gtest_list_tests'], disp=False)
        if(returncode != 0): raise 
        # 1行目は"Running main() from ..." 
        testlist = {}
        testcase = None
        for line in output[1:]:
            line = line.rstrip()
            m = re.match(self._RGX_TESTCASE, line)
            if(m):
                testcase = m.group('testcase')
                testlist[testcase] = []
                continue
            m = re.match(self._RGX_TESTNAME, line)
            if(m):
                testlist[testcase].append(m.group('testname'))
                continue
        return testlist

    def __execute_gtest(self, options, disp=True):
        cmd = [self._gtest, '--gtest_color=yes'] + options
        output = []
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            if(disp): print(line, end='')  # 標準出力を画面に表示
            output.append(line)
        process.stdout.close()
        returncode = process.wait()
        return output, returncode

def get_argparse():
    parser = argparse.ArgumentParser(description='This is an interactive, simple and quick test selector for GoogleTest.') 
    parser.add_argument('gtest', help='Executable file path of GoogleTest.')
    return parser

if __name__ == "__main__":
    args = get_argparse().parse_args()
    InteractiveGtest(args.gtest).start()