import parser
import tedlang

import re

variables = {}
functions = {}

# TYPES
INT = 'int'
FLOAT = 'float'
STR = 'str'
BOOL = 'bool'
NONE = 'NoneType'

def string(code: str):
    code = code.strip()
    if 'f"' or "f'" in code:
        for x in re.finditer(r'{(.*?)}', code):
            var_name = x.group().replace('{', '').replace('}', '')
            code = code.replace(x.group(), get_value(var_name))
        return code.replace('f"', '"').replace("f'", "'")
    return code

def exec_func(func_name: str, args: list[str]):
    func_content: list[str] = functions[func_name]['content']
    given_args_type = [get_type(x.strip()) for x in args]
    given_args_value = [get_value(x.strip()) for x in args]
    func_args_type = [functions[func_name]['args'][x]['type'] for x in range(len(functions[func_name]["args"]))]
    func_args_name = [functions[func_name]['args'][x]['name'] for x in range(len(functions[func_name]["args"]))]

    for i in range(len(func_args_type)):
        if given_args_type[i] != func_args_type[i] and given_args_type[i] != 'ID':
            raise RuntimeError(f'Cannot execute function {func_name} that has args {func_args_type} with args {given_args_type}')

    for i in range(len(func_args_name)):
        func_content.insert(0, f'var {func_args_name[i]} = {given_args_value[i]}')

    for i in func_content:
        if bool(re.match(r'return(.*?)', i)):
            return_value =  get_value(i.replace('return', '').strip())
            for j in func_args_name:
                del variables[j]
            return return_value
        else:
            exec_line(i)
    
    for j in func_args_name:
        del variables[j]

    return NONE

def exec_if(ifstr: str):
    if_conditions = ifstr[ifstr.index('if')+2:ifstr.index(':')].strip()

def is_tedlang(func: str):
    try: return True if func[:func.index('(')].replace('TD.', '') in tedlang.functions else False
    except: return False

def var_exists(var: str):
    try: return var[:var.index('=')].strip() in variables
    except: return True if var in variables else False

def func_exists(func: str):
    try: return func[:func.index('(')].strip() in functions
    except: return False


def get_type(word: str):
    if var_exists(word):
        return variables[word]['type']
    elif is_tedlang(word):
        return tedlang.functions[word[:word.index('(')].strip().replace('TD.', '')]['return']
    return parser.tokenize(word)[0]

def get_value(word: str):
    if var_exists(word):
        return variables[word]['value']
    elif is_tedlang(word):
        try: 
            args = word[word.index('(')+1:word.rindex(')')]
            args = re.split(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)", args)
        except ValueError: raise RuntimeError('Missing parenthesis in function call')

        func_name = word[:word.index('(')].replace('TD.', '').strip()

        if not func_name in tedlang.functions: 
            raise RuntimeError(f'TD.{func_name} doesn\'t exist in TedLang')
            raise RuntimeError('Cannot call function with return outside of variable declaration')   
        if len(tedlang.functions[func_name]['args']) != len(args):
            raise RuntimeError(f'Cannot call function that has {len(tedlang.functions[func_name]["args"])} arguments with {len(args)} arguments')
        
        for i in range(len(args)):
            if get_type(args[i]) != tedlang.functions[func_name]['args'][i] and tedlang.functions[func_name]['args'][i] != 'any': 
                raise RuntimeError(f'Argument for function {func_name} must be {tedlang.functions[func_name]["args"]}')

        return tedlang.exec_func(func_name, args)
    elif func_exists(word):
        try: 
            args = word[word.index('(')+1:word.rindex(')')]
            args = re.split(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)", args)
        except ValueError: raise RuntimeError('Missing parenthesis in function call')

        func_name = word[:word.index('(')].replace('TD.', '').strip()  
        if len(functions[func_name]['args']) != len(args):
            raise RuntimeError(f'Cannot execute function that has {len(functions[func_name]["args"])} arguments with {len(args)} arguments')

        return exec_func(func_name, args)
    elif get_type(word) == STR:
        return string(word)
    
    return word 

def exec_line(line: str):
    line = line.strip()

    if line[0:3] == 'var':
        var = line.replace('var', '')
        try: var_name = var[:var.index('=')].strip()
        except ValueError: raise RuntimeError('Missing "=" in variable declaration')

        var_value = var[var.index('=')+1:].strip()

        variables[var_name] = {
            'value': get_value(var_value),
            'type': get_type(var_value)
        }
        return
    if is_tedlang(line):
        try: 
            args = line[line.index('(')+1:line.rindex(')')]
            args = re.split(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)", args)
        except ValueError: raise RuntimeError('Missing parenthesis in function call')

        func_name = line[:line.index('(')].replace('TD.', '').strip()


        if not func_name in tedlang.functions: 
            raise RuntimeError(f'TD.{func_name} doesn\'t exist in TedLang')
        if tedlang.functions[func_name]['return'] != NONE: 
            raise RuntimeError('Cannot call function with return outside of variable declaration')   
        if len(tedlang.functions[func_name]['args']) != len(args):
            raise RuntimeError(f'Cannot call function that has {len(tedlang.functions[func_name]["args"])} arguments with {len(args)} arguments')
        
        for i in range(len(args)):
            if get_type(args[i]) != tedlang.functions[func_name]['args'][i] and tedlang.functions[func_name]['args'][i] != 'any': 
                raise RuntimeError(f'Argument for function {func_name} must be {tedlang.functions[func_name]["args"]}')

        tedlang.exec_func(func_name, args)

        return
    try:
        if var_exists(line):
            try: var_name = line[:line.index('=')].strip()
            except ValueError: raise RuntimeError('Missing "=" in variable redeclaration')

            new_value = line[line.index('=')+1:].strip()
            new_value = get_value(new_value)

            if get_type(new_value) == variables[var_name]['type']:
                variables[var_name]['value'] = new_value
            else:
                raise RuntimeError(f'Cannot convert type "{variables[var_name]["type"]}" to type "{get_type(new_value)}"')
            return
    except ValueError: pass
    if func_exists(line):
        try: 
            args = line[line.index('(')+1:line.rindex(')')]
            args = re.split(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)", args)
        except ValueError: raise RuntimeError('Missing parenthesis in function call')

        func_name = line[:line.index('(')].replace('TD.', '').strip()  
        if len(functions[func_name]['args']) != len(args):
            raise RuntimeError(f'Cannot execute function that has {len(functions[func_name]["args"])} arguments with {len(args)} arguments')

        func_return = exec_func(func_name, args)
        if func_return != NONE:
            raise RuntimeError('Canot execute function with a return ouside of a variable declaration')
        else: return

def prepare_functions(func: str):
    func = func.replace('func', '').replace('end', '')
    try: 
        func_name = func[:func.index('(')].strip() 
        func_args = func[func.index('(')+1:func.index(')')].split(',')
    except ValueError: raise RuntimeError('Missing parenthesis in function declaration')
    
    func_content = func[func.index(':')+1:].strip().split(';')[:-1] # [:-1] to remove one index of the array else it will have an empty index
    func_content = list(map(str.strip, func_content))

    if func_args == ['']: args = NONE
    else:
        func_args_name = [x[:x.index('$')].strip() for x in func_args]
        func_args_type = [x[x.index('$')+1:].strip() for x in func_args]
        args = []
        for x in range(len(func_args_name)):
            args.append({'name': func_args_name[x], 'type': func_args_type[x]})

    functions[func_name] = {
        'args': args,
        'content': func_content,
    }
