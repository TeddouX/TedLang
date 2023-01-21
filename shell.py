import sys
import interpreter
import re

if len(sys.argv) > 1:
    for filename in sys.argv[1:]:
        with open(filename, 'r') as file:
            parsed_file = file.read()
            comments = [x.group() for x in re.finditer(r':/(.*?)\n', parsed_file)]
            for comment in comments:
                parsed_file = parsed_file.replace(comment, '')

            functions = [x.group() for x in re.finditer(r'func((.\s*?)*?)end', parsed_file)]
            for function in functions:
                parsed_file = parsed_file.replace(function, '')
                interpreter.prepare_functions(function.replace('\n', ''))

            while '; ' in parsed_file:
                parsed_file = parsed_file.replace('; ', ';')
            parsed_file = parsed_file.split(';')

            parsed_file = parsed_file[:-1]

            for line in parsed_file:
                interpreter.exec_line(line)
else:
    is_running = True
    while is_running:
        code = input('>> ')
        if code == 'QUIT':
            is_running = False
        else:
            interpreter.exec_line(code)
