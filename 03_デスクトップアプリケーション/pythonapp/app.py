import os.path as osp
import sys
import csv

if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print('Usage: python {} [textfile]'.format(sys.argv[0]))
        exit()
    
    print('Hello Python')

    input_file = sys.argv[1]
    if not osp.exists(input_file):
        print('No such file: {}'.format(input_file))
        exit()

    output_file = osp.join(osp.dirname(input_file), 'result.csv')
    with open(input_file, 'r') as rf:
        with open(output_file, 'w') as wf:
            reader = csv.reader(rf)
            writer = csv.writer(wf)
            for row in reader:
                list = [ int(elm) for elm in row ]
                writer.writerow([sum(list)])
    
    print('Successfully generated results: {}'.format(output_file))