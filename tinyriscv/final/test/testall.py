import os
import subprocess
import sys


# 找出path目录下的所有bin文件
def list_binfiles(path):
    files = []
    list_dir = os.walk(path)
    for maindir, subdir, all_file in list_dir:
        for filename in all_file:
            apath = os.path.join(maindir, filename)
            if apath.endswith('.bin'):
                files.append(apath)

    return files

# 主函数
def main():
    bin_files = list_binfiles(r'test/isa/generated')

    anyfail = False

    # 对每一个bin文件进行测试
    for file in bin_files:
        cmd = r'python test/testbench.py' + ' ' + file + ' ' + f'test/inst/{os.path.basename(file)}_inst.data'
        f = os.popen(cmd)
        r = f.read()
        f.close()
        if (r.find('TEST_PASS') != -1):
            idx = r.find('time: ')
            t = r[idx + 6: idx + 15]
            print(file + '   ' + f'time: {t}' + '    PASS')
        else:
            print(file + '    !!!FAIL!!!')
            anyfail = True
            # break

    if (anyfail == False):
        print('Congratulation, All PASS...')


if __name__ == '__main__':
    sys.exit(main())
    # main()
