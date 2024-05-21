from hdlConvertorAst.hdlAst import HdlValueId, HdlOp, HdlOpType, HdlTypeAuto
import re

PRIMITIVE_TYPES = (
    HdlValueId("reg"),
    HdlValueId("wire"),
    HdlValueId("bit"),
    HdlValueId("logic"),
    HdlValueId("signed"),
    HdlValueId("unsigned"),
    HdlTypeAuto,
)

NULL = HdlValueId("null")


def collect_array_dims(t):
    array_dim = []
    while isinstance(t, HdlOp) and t.fn == HdlOpType.INDEX:
        assert len(t.ops) <= 2
        if len(t.ops) == 2:
            d = t.ops[1]
        else:
            d = None
        array_dim.append(d)
        t = t.ops[0]
    array_dim.reverse()
    return t, array_dim


def get_wire_t_params(t):
    """
    wire/reg type is actually stored as: t#(width, is_signed)
    This function extracts t, width, is_signed and potential array dimmensions
    if this type is an array.
    """
    t, array_dim = collect_array_dims(t)

    if t in PRIMITIVE_TYPES:
        is_signed = None
        if t == HdlValueId("signed"):
            is_signed = True
        elif t == HdlValueId("unsigned"):
            is_signed = False
        return t, None, is_signed, array_dim

    # 1b scala
    if not isinstance(t, HdlOp) or t.fn != HdlOpType.PARAMETRIZATION or len(t.ops) != 3:
        return None

    if t.ops[0] not in PRIMITIVE_TYPES:
        return None

    t, width, is_signed = t.ops
    if width == NULL:
        width = None
    if is_signed is None:
        is_signed = None
    else:
        is_signed = bool(is_signed)

    return t, width, is_signed, array_dim


global_module_dict = {}
cur_module = None
mp = {}

def set_cur_module(module):
    global global_module_dict
    global cur_module
    cur_module = module
    if module not in global_module_dict.keys():
        global_module_dict[cur_module] = {}

def set_mapping(inst, module):
    global mp
    mp[inst] = module
    mp[module] = module


def save_port_dims(port, width, dims):
    global global_module_dict
    global cur_module
    global_module_dict[cur_module][port] = (width, dims)

def search_from_dict(port) -> int:
    """
    Arguments:
        port {str}

    Returns:
        int -- the dimension(s) of the port
    """
    global global_module_dict
    global cur_module
    if port not in global_module_dict[cur_module].keys():
        raise AssertionError(f"the key {port} does not exists")
    return global_module_dict[cur_module][port]

def split_function_name_and_args(input_str):
    match = re.match(r'(\w+)\((.*?)\)', input_str)
    if match:
        function_name = match.group(1)
        args_str = match.group(2).strip()

        args = [arg.strip() for arg in args_str.split(',') if arg.strip()]

        return function_name, args
    else:
        raise ValueError("invalid function format")

def split_variable_and_slice(input_str):
    match = re.match(r'(\w+)\[(.*)\]', input_str)
    if match:
        array_name = match.group(1)
        index_str = match.group(2)

        index_parts = re.split(r'\]\s*\[', index_str)
        index_parts = [part for part in index_parts if part]

        return array_name, index_parts
    else:
        raise ValueError("invalid array format")

def filter_(s):
    # variable
    var_name_pattern = re.compile(r'^[a-zA-Z_]\w*$')
    # function
    # function_pattern = re.compile(r'^[a-zA-Z_]\w*(\([a-zA-Z0-9_, ]*\))?$')
    # array
    # part_select_pattern = re.compile(r'^[a-zA-Z_]\w*(\[\d+(:\d+)?\])?(\[\d+(:\d+)?\])?$')

    array = []

    if re.match(var_name_pattern, s):
        return "var", s
    elif '(' in s:
        name, args = split_function_name_and_args(s)
        return "func", name, args
    elif '[' in s:
        variable_name, slice_str = split_variable_and_slice(s)
        return "array", variable_name, slice_str

    raise ValueError(f"invalid format: {s}")


def extract_numbers(s):
    pattern = r'(\d+):(\d+)'
    matches = re.findall(pattern, s)
    return matches[0]


def get_width_msg(port):
    assert type(port) == str, f"type error: {type(port)}"
    if ':' in port:
        a, b = port.split(':')
        return f"{a} - {b} + 1"
    else:
        return '1'

def extract_last_bracket_content(input_string):
    matches = re.findall(r'\[(.*?)\]', input_string)
    if matches:
        return matches[-1]
    else:
        return None
