import random
import interpreter
import math

functions = {
    'Print': {
        'return': 'NoneType',
        'args': ['any']
    },
    'System.Input': {
        'return': 'str',
        'args': ['str']
    },
    'System.Type': {
        'return': 'str',
        'args': ['any']
    }
}

def exec_func(func_name: str, args: list):
    func_name = func_name.replace('TD.', '')
    args_value = [interpreter.get_value(x) for x in args]
    args_type = [interpreter.get_type(x) for x in args]

    if func_name == 'Print':
        for i in args_value:
            print(i.replace('"', '').replace("'", ''))
    elif func_name.startswith('System.'):
        name = func_name.replace('System.', '')
        if name == 'Input':
            return str(input(args_value[0].replace('"', '').replace("'", '')))
        elif name == 'Type':
            return str(args_type[0]) 
        else:
            raise RuntimeError('The specified function doesn\'t exist')
    elif func_name.startswith('Math.'):
        name = func_name.replace('Math.', '')
        if name == 'Random':
            return str(random.random)
        elif name == "Cos":
            return str(math.cos(args_value[0]))
        elif name == "Sin":
            return str(math.sin(args_value[0]))
        elif name == "Tan":
            return  str(math.tan(args_value[0]))   
    else:
        raise RuntimeError('The specified module doesn\'t exist')