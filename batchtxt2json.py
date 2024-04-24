import os
import argparse
import scripts.txt2json
import re
import sys




META_REGEX = re.compile(r'([\w]+)\s*\:\s*(.*)')
HEADER_REGEX = re.compile(r'([\w]+)(?:\[([^\]]+)\])?')
BOOL_PATTERN = {'false': False, 'true': True}

parser = argparse.ArgumentParser()
parser.add_argument('dir', help="Input file directory for PQC text format.")
args = parser.parse_args()
directory = args.dir
print('directory',directory)


for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        f_path = os.path.join(directory,filename)
        o_path = f_path.split('.')
        o_path = str(o_path[0]) + '.json'
        with open(f_path, 'r') as f:
            data = scripts.txt2json.load_text(f)
        
        with open(o_path, 'w') as o:
            scripts.txt2json.to_json(data, o)
        
    
