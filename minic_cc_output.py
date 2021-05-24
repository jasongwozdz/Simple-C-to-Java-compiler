import struct
from minic_state import state

stringconst = 0

entrynum = 0

PRINT_INT_LOCATION = 0

constpool = 0

Classname = "Output"

CODE_SIZE = 13

max_stack = 0

max_vars = 1

const_pool_line = 1 #keeps track of const pool line to help with linking const pool variables

printstream_loc = None

float_dict = {}

PRINT_FLOAT_LOCATION = None

PRINT_STRING_LOCATION = None

#########################################################################
def output(instr_stream, classname):
    global Classname
    Classname = classname
    global entrynum
    global const_pool_line

    java_lang_object = None
    java_io_printstream = None

    f = open(Classname+".class", "wb")
    output_stream = ''
    # f.write(b'\xca\xfe\xba\xbe\x00\x00\x00\x34') #magic number

    # constpool = bytearray(b'\xca\xfe\xba\xbe\x00\x00\x00\x34\x00') #const pool
    # constpool.append(entrynum+1)

    #class name
    b = bytearray(b'\x07\x00')  #line 1
    b.append(const_pool_line + 1)
    # f.write(b)
    entrynum += 2
    const_pool_line += 1

    b += bytearray(b'\x01\x00') #line 2
    b.append(len(Classname))
    b += Classname.encode()
    const_pool_line += 1
    # f.write(b)

    #java/lang/object
    b += bytearray(b'\x07\x00')
    b.append(const_pool_line + 1)
    # f.write(b)
    entrynum += 2
    java_lang_object = const_pool_line
    const_pool_line += 1

    b += b'\x01\x00\x10\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x4f\x62\x6a\x65\x63\x74'
    # f.write(b'\x01\x00\x10\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x4f\x62\x6a\x65\x63\x74')
    const_pool_line += 1
    
    
    #java/lang/system
    b += bytearray(b'\x07\x00')
    b.append(const_pool_line + 1)
    # f.write(b)
    entrynum += 2
    java_lang_system = const_pool_line
    const_pool_line += 1

    b += b'\x01\x00\x10\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x53\x79\x73\x74\x65\x6d'
    const_pool_line += 1
    # f.write(b'\x01\x00\x10\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x53\x79\x73\x74\x65\x6d')

    #java/io/printstream
    b += bytearray(b'\x07\x00')
    b.append(const_pool_line + 1)
    entrynum += 2
    java_io_printstream = const_pool_line
    const_pool_line += 1

    b += b'\x01\x00\x13\x6a\x61\x76\x61\x2f\x69\x6f\x2f\x50\x72\x69\x6e\x74\x53\x74\x72\x65\x61\x6d'
    # f.write(b'\x01\x00\x13\x6a\x61\x76\x61\x2f\x69\x6f\x2f\x50\x72\x69\x6e\x74\x53\x74\x72\x65\x61\x6d')
    const_pool_line += 1

    b += b'\x01\x00'
    b.append(len("StackMapTable"))
    b +=  "StackMapTable".encode()
    entrynum += 1
    const_pool_line += 1


    #float info
    if(state.floats != None):
        for fl in state.floats:
            b += add_float_info(fl)

    if(state.strings != None):
        for s1 in state.strings:
            b+= add_string_info(s1)

    #b += add_string_info("dog")

    #Function Name
    # b = add_stringconst('dog',f,b)
    b = add_stringconst("main", f, b)

    #java/lang/System.out:Ljava/io/PrintStream;
    global printstream_loc
    printstream_loc = const_pool_line
    b += bytearray(b'\x09\x00')
    b.append(java_lang_system)
    b += b'\x00'
    b.append(const_pool_line + 1)
    #entrynum += 2
    const_pool_line += 1

    #out:Ljava/io/PrintStream;
    b += b'\x0c\x00'
    b.append(const_pool_line + 1)
    b += b'\x00'
    b.append(const_pool_line + 2)
    const_pool_line += 1
    #entrynum += 2

    b += b'\x01\x00\x03\x6f\x75\x74' #out
    const_pool_line += 1
    b += b'\x01\x00\x15\x4c\x6a\x61\x76\x61\x2f\x69\x6f\x2f\x50\x72\x69\x6e\x74\x53\x74\x72\x65\x61\x6d\x3b' #Ljava/io/PrintStream;
    const_pool_line += 1
    # f.write(b)

    #java/io/PrintStream.println:(I)V
    global PRINT_INT_LOCATION
    PRINT_INT_LOCATION = const_pool_line
    b += bytearray(b'\x0a\x00')
    b.append(java_io_printstream)
    b += b'\x00'
    b.append(const_pool_line + 1)
    #entrynum += 2
    const_pool_line += 1

    b += b'\x0c\x00'
    b.append(const_pool_line + 1)
    b += b'\x00' #println:(I)V
    b.append(const_pool_line + 2)
    #entrynum += 2
    const_pool_line += 1

    b += b'\x01\x00\x07\x70\x72\x69\x6e\x74\x6c\x6e' #utf8 println
    const_pool_line += 1

    b += b'\x01\x00\x04' #utf8 (I)V
    b += '(I)V'.encode()
    const_pool_line += 1


    #print/io/PrintStream.println:():(F)V
    global PRINT_FLOAT_LOCATION
    PRINT_FLOAT_LOCATION = const_pool_line
    b += bytearray(b'\x0a\x00')
    b.append(java_io_printstream)
    b += b'\x00'
    b.append(const_pool_line + 1)
    #entrynum += 2
    const_pool_line += 1

    b += b'\x0c\x00'
    b.append(const_pool_line + 1)
    b += b'\x00' #println:(I)V
    b.append(const_pool_line + 2)
    #entrynum += 2
    const_pool_line += 1

    b += b'\x01\x00\x07\x70\x72\x69\x6e\x74\x6c\x6e' #utf8 println
    const_pool_line += 1
    #utf8 (F)V
    b+= b'\x01\x00'
    b.append(len('(F)V'))
    b += '(F)V'.encode()
    const_pool_line += 1

    #print/io/PrintStream.println:():(Ljava/lang/String;)V
    global PRINT_STRING_LOCATION
    PRINT_STRING_LOCATION = const_pool_line
    b += bytearray(b'\x0a\x00')
    b.append(java_io_printstream)
    b += b'\x00'
    b.append(const_pool_line + 1)
    #entrynum += 2
    const_pool_line += 1

    b += b'\x0c\x00'
    b.append(const_pool_line + 1)
    b += b'\x00' #println:(I)V
    b.append(const_pool_line + 2)
    #entrynum += 2
    const_pool_line += 1

    b += b'\x01\x00\x07\x70\x72\x69\x6e\x74\x6c\x6e' #utf8 println
    const_pool_line += 1
    #utf8 (F)V
    b+= b'\x01\x00'
    b.append(len('(Ljava/lang/String;)V'))
    b += '(Ljava/lang/String;)V'.encode()
    const_pool_line += 1
    

    constpool = bytearray(b'\xca\xfe\xba\xbe\x00\x00\x00\x34\x00') #Magic number
    constpool.append(const_pool_line+3)
    f.write(constpool)
    f.write(b)

    #MAIN code (dosent add to constant pool size)
    b = bytearray(b'\x01\x00\x04\x6d\x61\x69\x6e') #utf8 main
    main_loc = const_pool_line
    const_pool_line += 1
    b += b'\x01\x00\x16\x28\x5b\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x53\x74\x72\x69\x6e\x67\x3b\x29\x56' #utf8 ([Ljava/lang/String;)V
    const_pool_line += 1
    b += b'\x01\x00\x04\x43\x6f\x64\x65' #utf8 Code
    code_loc = const_pool_line


    f.write(b)

    f.write(b'\x00\x21\x00\x01\x00\x03\x00\x00\x00\x00')

    #Method info
    f.write(b'\x00\x01') #num of methods


    #machine code
    code = bytearray()
    #machine code instructions
    #code += b'\xb2\x00\x0b'
    for instr in instr_stream:
        print(instr)
        code = machincode_fun[instr[1]](instr[2], code)

    code += b'\xb1' #return

    
    global CODE_SIZE
    global max_stack
    CODE_SIZE = len(code)

    b = bytearray(b'\x00\x09')  # public static
    b+= b'\x00'
    b.append(main_loc)
    #b+= b'\x14'
    b += b'\x00'
    b.append(main_loc + 1)
    #b+= b'\x15' # main
    b+= b'\x00\x01' # attribute size
    b+= b'\x00' # code attribute(index of Code in constant pool)
    b.append(code_loc)
    b+= b'\x00\x00\x00' # code attribute size = size of code + 12
    b.append(CODE_SIZE + 12)
    b+= b'\x00'
    b.append(max_stack)
    b+=b'\x00' # Max stack size, max local var size
    b.append(max_vars) 
    b+= b'\x00\x00\x00' # Size of code
    b.append(CODE_SIZE)

    f.write(b)
    #f.write(byte_goto(13,bytearray()))
    #max_stack += 1
    f.write(code)
    
    #end of machine code
    f.write(b'\x00\x00\x00\x00')

    f.write(b'\x00\x00')

    return output_stream

def add_stringconst(instr, f, b):
    global entrynum
    global const_pool_line
    b += bytearray(b'\x08\x00')
    b.append(const_pool_line + 1)
    # f.write(b)
    entrynum += 2
    b += bytearray(b'\x01\x00')
    b.append(len(instr))
    # f.write(b)
    b+=(instr.encode())
    const_pool_line += 2
    return b
    # f.write(instr.encode())

def add_float_info(value):
    global const_pool_line
    global float_dict
    float_dict[value] = const_pool_line

    const_pool_line += 1
    #need to convert to a 4 byte ieee754 standard float
    buf = struct.pack(">f", value)
    f = ''.join("%x" % ord(c) for c in struct.unpack(">4c", buf) )
    a = bytearray.fromhex(f)
    b = bytearray(b'\x04')
    b += a
    return b

def add_string_info(value):
    global const_pool_line
    global float_dict
    float_dict[value] = const_pool_line
    b = bytearray(b'\x08\x00')
    b.append(const_pool_line + 1)
    
    #add utf8 constant of string
    const_pool_line += 1
    b += b'\x01\x00'
    b.append(len(value))
    b += value.encode()
    const_pool_line += 1
    return b


def byte_iconst(value, b):
    global max_stack
    max_stack += 1
    ints = {
        0 : b'\x03',
        1 : b'\x04',
        2 : b'\x05',
        3 : b'\x06',
        4 : b'\x07',
        5 : b'\x08'
    }
    b += ints[value]
    return b

def byte_bipush(value, b):
    global max_stack
    max_stack += 1
    b += b'\x10'
    b.append(value)
    return b

def byte_sipush(value, b):
    global max_stack
    max_stack += 1
    b+= b'\x11'
    b.append(value)
    return b


def handlePrint(data_type, b):
    global max_stack
    max_stack += 1
    # b[len(b)-1:len(b)-1] =  b'\xb2\x00\x0b'# get out from static pool and insert infront of code before last
    b += b'\xb6\x00'
    print_stmt = {
        'integer' : PRINT_INT_LOCATION,
        'float' : PRINT_FLOAT_LOCATION,
        'string' : PRINT_STRING_LOCATION
    }
    b.append(print_stmt[data_type])
    #b += b'\xb2\x00\x0b'
    return b

def byte_iadd(data_type, b):
    global max_stack
    max_stack += 1
    b += b'\x60'
    return b

def byte_imul(data_type, b):
    global max_stack
    max_stack += 1
    b.append(104)
    return b

def byte_idiv(data_type, b):
    global max_stack
    max_stack += 1
    b.append(108)
    return b

def byte_isub(data_type, b):
    global max_stack
    max_stack += 1
    b.append(100)
    return b

def byte_istore_(value, b):
    global max_vars
    max_vars += 1
    vals = {
        0 : b'\x3b',
        1 : b'\x3c',
        2 : b'\x3d',
        3 : b'\x4d'
    }
    if value in vals:
        b += vals[value]
    else:
        b+= b'\x36'
        b.append(value)
    return b

def byte_iload_(value, b):
    global max_stack
    max_stack += 1
    vals = {
        0 : b'\x1a',
        1 : b'\x1b',
        2 : b'\x1c',
        3 : b'\x1d'
    }
    b += vals[value]
    return b

def byte_static(value, b):
    b+=b'\xb2\x00'
    b.append(printstream_loc)
    #\x0c'
    return b


def byte_if(value, b):
    # vals = {
    #     'if_icmpgt' : b'\xa3',
    #     'if_icmpeq' : b'\x9f'
    # }
    b += b'\xa3\x00'
    b.append(value)
    return b
    
def byte_goto(value, b):
    b += b'\xa7'
    print(struct.pack('>H', value))
    b += struct.pack('>H', 1)
    return b

def byte_ldc(value, b):
    global max_stack
    max_stack += 1
    b += b'\x12'
    b.append(float_dict[value])
    return b

def byte_fstore(value, b):
    global max_vars
    max_vars += 1
    b += b'\x38'
    b.append(value)
    return b

def byte_fload(value, b):
    b += b'\x17'
    b.append(value)
    return b

def byte_fadd(value, b):
    global max_stack
    max_stack += 1
    b.append(98)
    return b

def byte_fsub(value, b):
    global max_stack
    max_stack += 1
    b.append(102)
    return b

def byte_fmul(value, b):
    global max_stack
    max_stack += 1
    b.append(106)
    return b

def byte_fdiv(value, b):
    global max_stack
    max_stack += 1
    b.append(110)
    return b

machincode_fun = {
    'iconst_' : byte_iconst,
    'bipush' : byte_bipush,
    'sipush' : byte_sipush,
    'INVOKEINVOKEVIRTUAL java/io/PrintStream.println (I)V' : handlePrint,
    'INVOKEVIRTUAL java/io/PrintStream.println (F)V' : handlePrint,
    'INVOKEVIRTUAL java/io/PrintStream.println (Ljava/lang/String;)V' : handlePrint,
    'iadd' : byte_iadd,
    'istore' : byte_istore_,
    'idiv' : byte_idiv,
    'imul' : byte_imul,
    'isub'  : byte_isub,
    'iload' : byte_iload_,
    'fload' : byte_fload,
    'getstatic' : byte_static,
    'if_icmpgt' : byte_if,
    'goto'  : byte_goto,
    'ldc'  : byte_ldc,
    'fstore' : byte_fstore,
    'fadd' : byte_fadd,
    'fsub' : byte_fsub,
    'fmul' : byte_fmul,
    'fdiv' : byte_fdiv
}

def initglobalvars():
    global stringconst
    stringconst = 0
    global entrynum
    entrynum = 0
    global PRINT_INT_LOCATION
    PRINT_INT_LOCATION = 0
    global constpool 
    constpool = 0
    global Classname 
    Classname = "Output"
    global CODE_SIZE 
    CODE_SIZE = 0
    global max_stack 
    max_stack = 1
    global max_vars
    max_vars = 1
    global const_pool_line
    const_pool_line = 1 #keeps track of const pool line to help with linking const pool variables
    global printstream_loc
    printstream_loc = None
    global float_dict
    float_dict = {}
    global PRINT_FLOAT_LOCATION
    PRINT_FLOAT_LOCATION = None
    global PRINT_STRING_LOCATION
    PRINT_STRING_LOCATION = None
