from grammar_stuff import assert_match
from minic_state import state

frame_size = None
line_number= 0

curr_var = 0

endline = []
#########################################################################
def push_args(args):
    # args can either be a ('seq', item, rest) node or a ('nil',) node.

    if args[0] == 'nil':
        return []

    else:
        # unpack the args
        (SEQ, exp_tree, rest) = args
        
        code = push_args(rest)
        
        (ecode, eloc) = walk(exp_tree)
        
        code += ecode
        code += [('pushv', eloc)]
        
        return code

#########################################################################
def pop_args(args):
    # args can either be a ('seq', item, rest) node or a ('nil',) node.

    if args[0] == 'nil':
        return []

    else:
        # unpack the args
        (SEQ, _, rest) = args
        
        code = pop_args(rest)
        code += [('popv',)]
        
        return code

#########################################################################
def init_formal_args(formal_args, ix, frame_size):
    # formal_args can either be a ('seq', item, rest) node or a ('nil',) node.
    
    if formal_args[0] == 'nil':
        return []

    else:
        # unpack the args
        (SEQ, sym, rest) = formal_args

        offset = str((0 if not ix else -ix) - frame_size - 1)
        code = [('store', sym, '%tsx['+offset+']')]
        
        return code + init_formal_args(rest, ix+1, frame_size)

#########################################################################
# node functions
#########################################################################
def seq(node):

    (SEQ, s1, s2) = node
    assert_match(SEQ, 'seq')
    stmt = walk(s1)
    lst = walk(s2)
    return stmt + lst

#########################################################################
def nil(node):
    
    (NIL,) = node
    assert_match(NIL, 'nil')
    
    return []
    

#########################################################################
def assign_stmt(node):
    global line_number
    global curr_var
    (ASSIGN, name, return_type, exp) = node
    assert_match(ASSIGN, 'decl')
    (data_type, code) = walk(exp)
    state.symbol_table.declare_scalar(name, return_type[0], data_type)
    (SCALAR, data_type, var_num) = state.symbol_table.lookup_sym(name)
    if(data_type == 'integer'):
        code += [[line_number, "istore",var_num]]
        line_number += 1
    elif(data_type =='float'):
        code += [[line_number,"fstore", var_num]]
        line_number += 1

    return code


#########################################################################
def print_stmt(node):
    global line_number
    (PRINT, exp) = node
    assert_match(PRINT, 'print')
    orig_line_number = line_number
    line_number += 3 #add line number for get static +3 because get static is 3 bytes
    (data_type, return_code) = walk(exp)

    code = [[orig_line_number, "getstatic",data_type]]  # need to getstatic before adding print variable to stack
    code += return_code 

    if(data_type == 'integer'):
        code += [[line_number, 'INVOKEINVOKEVIRTUAL java/io/PrintStream.println (I)V', 'integer']] 
        line_number += 3 #invokevirtual is also 3 bytes so increase linenumber by 3
    elif(data_type == 'float'):
        code += [[line_number, 'INVOKEVIRTUAL java/io/PrintStream.println (F)V', 'float']]
        line_number += 3 #invokevirtual is also 3 bytes so increase linenumber by 3
    elif(data_type == 'string'):
        code += [[line_number, 'INVOKEVIRTUAL java/io/PrintStream.println (Ljava/lang/String;)V', 'string']]
        line_number += 3 #invokevirtual is also 3 bytes so increase linenumber by 3
    return code


def for_stmt(node):
    global line_number
    global endline
    start_line = line_number
    (FOR, init_value, condition, endloop, block_stmt) = node
    assert_match(FOR, 'for')
    code = []
    init_code = walk(init_value)
    #code += cond_code
    end_code = walk(endloop)
    block_code = walk(block_stmt)
    goto_code = [[line_number, "goto", start_line]]
    line_number += 3
    endline += [line_number]
    (data_type, cond_code) = walk(condition)
    code += init_code 
    code += cond_code  
    code += end_code[1] 
    code += block_code 
    code += goto_code
    return code

#########################################################################
def if_stmt(node):

    try: # try the if-then pattern
        (IF, cond, s1, (NIL,)) = node
        assert_match(IF, 'if')
        assert_match(NIL, 'nil')
    
    except ValueError: # pattern didn't match
        # try the if-then-else pattern
        (IF, cond, s1, s2) = node
        assert_match(IF, 'if')
        
        else_label = label()
        end_label = label()
        (cond_code, cond_loc) = walk(cond)
        stmt1_code = walk(s1)
        stmt2_code = walk(s2)

        code = cond_code
        code += [('jumpF', cond_loc, else_label)]
        code += stmt1_code
        code += [('jump', end_label)]
        code += [(else_label + ':',)]
        code += stmt2_code
        code += [(end_label + ':',)]
        code += [('noop',)]

        return code

    else:
        end_label = label()
        (cond_code, cond_loc) = walk(cond)
        stmt1_code = walk(s1)

        code = cond_code
        code = [('jumpF', cond_loc, end_label)]
        code += stmt1_code
        code += [(end_label + ':',)]
        code += [('noop',)]

        return code

#########################################################################
def block_stmt(node):

    (BLOCK, s) = node
    assert_match(BLOCK, 'block')

    state.symbol_table.push_scope()
    code = walk(s)
    state.symbol_table.pop_scope()

    
    return code

#########################################################################
def binop_exp(node):
    global line_number
    code = []
    (OP, c1, c2) = node
    if OP not in ['+', '-', '*', '/']:
        raise ValueError("pattern match failed on " + OP)
    
    (data_type1, code1) = walk(c1)
    (data_type2, code2) = walk(c2)
    code += code1
    code += code2
    if(data_type1 == data_type2 == 'integer'):
        op = {
            '+' : 'iadd', 
            '-' : 'isub', 
            '*' : 'imul',
            '/' : 'idiv'
        }
    elif(data_type1 == data_type2 == 'float'):
            op = {
            '+' : 'fadd', 
            '-' : 'fsub', 
            '*' : 'fmul',
            '/' : 'fdiv'
        }
    else:
        raise TypeError("wrong datatype expected ",data_type1," but got ", data_type2)
        
    code += [[line_number, op[OP], OP]]
    line_number += 1
    return (data_type1, code) 

def logic_exp(node):
    global line_number
    code = []
    (OP, c1, c2) = node
    if OP not in ['==', '<=']:
        raise ValueError("pattern match failed on " + OP)
    ops = {
        '==' : "if_icmpne",
        '<=' : "if_icmpgt"   
        }
    
    (data_type1, code1) = walk(c1)
    (data_type2, code2) = walk(c2)
    if(data_type1 == data_type2 == "integer"):
        code += code1
        code += code2
        code += [[line_number, ops[OP], endline[len(endline)-1]]]
        line_number += 3

    return (data_type1, code) 


def val_exp(node):
    (VAL, data_type, value) = node
    assert_match(VAL, 'val')
    (data_type, code) = walk((data_type[0], value)) 
    return (data_type, code)


#########################################################################
def integer_exp(node):
    global line_number
    (INTEGER, value) = node
    assert_match(INTEGER, 'integer')
    code = []
    if(value <= 5 and value >= 0):
        code += [[line_number,"iconst_",value]]
        line_number += 1
    elif(value > 127): #if value is too large then need to use sipush since bipush only uses one byte
        code += [[line_number, "sipush", value]]
        line_number += 1
    else:
        code += [[line_number, 'bipush', value]]
        line_number += 2
    
    return (INTEGER, code)

def float_exp(node):
    global line_number
    (FLOAT, value) = node
    assert_match(FLOAT, 'float')
    code = [[line_number,'ldc',value]]
    line_number += 2 #ldc is 2 bytes
    state.floats.append(value)
    return (FLOAT, code)

def string_exp(node):
    global line_number
    (FLOAT, value) = node
    assert_match(FLOAT, 'string')
    code = [[line_number,'ldc',value]]
    line_number += 2 #ldc is 2 bytes
    state.strings.append(value)
    return (FLOAT, code)



#########################################################################
def id_exp(node):
    global curr_var
    global line_number
    (ID, name) = node
    assert_match(ID, 'id')
    code = []
    (scalar, data_type, var_num) = state.symbol_table.lookup_sym(name)
    curr_var = var_num
    if(data_type == 'integer'):
        code += [[line_number,'iload',var_num]]
        line_number += 1
    elif(data_type == 'float'):
        code += [[line_number, 'fload',var_num]]
        line_number += 1

    
    return (data_type, code)


#########################################################################
# walk
#########################################################################
def walk(node):
    node_type = node[0]
    
    if node_type in dispatch_dict:
        node_function = dispatch_dict[node_type]
        return node_function(node)
    
    else:
        raise ValueError("walk: unknown tree node type: " + node_type)

# a dictionary to associate tree nodes with node functions
dispatch_dict = {
    'seq'     : seq,
    'nil'     : nil,
    'decl'    : assign_stmt,
    'print'     : print_stmt,
    'for'     : for_stmt,
    'if'      : if_stmt,
    'block'   : block_stmt,
    'val'     : val_exp,
    'integer' : integer_exp,
    'float'   : float_exp,
    'string'  : string_exp,
    'id'      : id_exp,
    '+'       : binop_exp,
    '-'       : binop_exp,
    '*'       : binop_exp,
    '/'       : binop_exp,
    '=='      : logic_exp,
    '<='      : logic_exp

}

#########################################################################
label_id = 0

def label():
    global label_id
    s =  'L' + str(label_id)
    label_id += 1
    return s

#########################################################################

