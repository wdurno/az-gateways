from flask import Flask, jsonify 
from waitress import serve 
import argparse 

parser = argparse.ArgumentParser(description='a simple back-end service') 
parser.add_arugment('--port', dest='port', required=False, default=80, help='which port to list to')

app = Flask(__name__) 

@app.route('/', defaults={'path': ''}) 
@app.route('/<path:path>') 
def index(path): 
    return jsonify({'path': path}) 

def __format_args(args):
    '''Casts `args` into correct formats.
    Returns updated `args`.
    '''
    args.port = int(args.port) 
    return args

if __name__ == '__main__':
    ## get args 
    args = parser.parse_args() 
    args = __format_args(args) 
    serve(app, host='0.0.0.0', port=args.port) 
