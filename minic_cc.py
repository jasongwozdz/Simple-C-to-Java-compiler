from argparse import ArgumentParser
from minic_lex import lexer
from minic_frontend import parser
from minic_state import state
from minic_cc_codegen import walk as codegen
from minic_cc_output import output
from grammar_stuff import dump_AST

def cc(input_stream, output_file_name):

    # initialize the state object
    state.initialize()

    # build the AST
    parser.parse(input_stream, lexer=lexer)

    # generate the list of instruction tuples
    instr_stream = codegen(state.AST)
    # output the instruction stream
    bytecode = output(instr_stream, output_file_name)

    return bytecode 

if __name__ == "__main__":
    # parse command line args
    aparser = ArgumentParser()
    aparser.add_argument('input', metavar='output_file_name', help='.class file name')
    

    args = vars(aparser.parse_args())

    f = open(args['input'], 'r')
    input_stream = f.read()
    f.close()

    # run the compiler
    bytecode = cc(input_stream=input_stream)

    if not args['o']:
        print(bytecode)

    else:
        f = open(args['o'], 'w')
        print(args[0])
        f.close()
