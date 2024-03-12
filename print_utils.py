import numpy as np
import pandas as pd 


def _process_list(info, prefix):
    if not isinstance(info, str):
        info = info.__str__()

    info_list = info.split('\n')
    if len(info_list) > 1:
        lines = []
        for it in info_list:
            lines.append(prefix + it)
        print('\n'.join(lines))
    else:
        print(prefix + info)


def part_print(info):
    print('='*4, info, '='*4)
    
    
def print_h1(info):
    _process_list(info, '- ')
    
    
def print_h2(info):
    _process_list(info, ' * ')
    
    
def print_h3(info):
    _process_list(info, '  + ')
    
    
def print_h4(info):
    _process_list(info, '   ~ ')


if __name__ == "__main__":
    arr = np.array([1,2,3,3,3,1])
    df = pd.DataFrame(arr)

    part_print('Label Distribution Check')
    print_h1('y train check')
    print_h2(df.value_counts())
    print_h3('label 1 cnt valid')
    print_h3('label 2 cnt valid')

    print_h1('y valid check')
    print_h2(df.value_counts())
    print_h3('label 1 cnt valid')
    print_h3('label 2 cnt valid')

    print_h1('y test check')
    print_h2(df.value_counts())
    print_h3('label 1 cnt valid')
    print_h3('label 2 cnt valid')