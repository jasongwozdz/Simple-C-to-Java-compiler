def _id(a):
    'identity function for type conversions'
    return a

_promote_table = {
  'string'    : {'string': 'string', 'float': 'string', 'integer': 'string',  'array-type': 'string',     'void': 'None'},
  'float'     : {'string': 'string', 'float': 'float',  'integer': 'float',   'array-type': 'None',       'void': 'None'},
  'integer'   : {'string': 'string', 'float': 'float',  'integer': 'integer', 'array-type': 'None',         'void': 'None'},
  'array-type': {'string': 'string', 'float': 'None',   'integer': 'None',    'array-type': 'array-type', 'void': 'None'},
  'void'      : {'string': 'None',   'float': 'None',   'integer': 'None',    'array-type': 'None',       'void': 'void'},
}

_conversion_table = {
  'string'    : {'string': str,  'float': str,   'integer': str,   'array-type': str,  'void': None},
  'float'     : {'string': str,  'float': float, 'integer': float, 'array-type': None, 'void': None},
  'integer'   : {'string': str,  'float': float, 'integer': int,   'array-type': None, 'void': None},
  'array-type': {'string': str,  'float': None,  'integer': None,  'array-type': _id,  'void': None},
  'void'      : {'string': None, 'float': None,  'integer': None,  'array-type': None, 'void': _id},
}

_safe_assign_table = {
  'string' :    {'string': True,  'float': True,  'integer': True,  'array-type': True,  'void': False},
  'float'  :    {'string': False, 'float': True,  'integer': True,  'array-type': False, 'void': False},
  'integer':    {'string': False, 'float': False, 'integer': True,  'array-type': False, 'void': False},
  'array-type': {'string': False, 'float': False, 'integer': False, 'array-type': True,  'void': False},
  'void'   :    {'string': False, 'float': False, 'integer': False, 'array-type': False, 'void': False},
}

def promote(type1, type2):
    return (_promote_table.get(type1[0]).get(type2[0]),)

def conversion_fun(ltype, rtype):
    return _conversion_table.get(ltype[0]).get(rtype[0])

def safe_assign(ltype, rtype):
        return _safe_assign_table.get(ltype[0]).get(rtype[0])

def is_primitive(type):
    return type[0] in ['integer', 'float', 'string']

def cast_string(to_data_type, string_arg):
    try:
        if to_data_type[0] == 'integer':
            return (('integer',), int(string_arg))
        elif to_data_type[0] == 'float':
            return (('float',), float(string_arg))
        elif to_data_type[0] == 'string':
            return (('string',), string_arg)
    except ValueError:
        raise ValueError(\
            "value {} not supported for type {}"\
            .format(string_arg, to_data_type))
    else:
        raise ValueError(\
            "type {} and not supported in 'cast_string'"\
            .format(to_data_type))
