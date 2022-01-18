import argparse

# Create the parser and add arguments
parser = argparse.ArgumentParser(description='Read a file')
parser.add_argument('filename', help="file to read")
parser.add_argument('--limit', '-l', type=int, help='the number of lines to read')
parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0')

args = parser.parse_args()

with open(args.filename) as f:
    lines = f.readlines()
    lines.reverse()

    if args.limit:
        lines = lines[:args.limit]
    for line in lines:
        # print(line.strip()[::-1])
        print(line)
        
        

# parse the arguments

# read the file, reverse the contents and print