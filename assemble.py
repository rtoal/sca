import sys

instructions = 'LOAD STORE IN OUT ADD SUB MUL DIV MOD AND OR XOR JUMP JZ JLZ JGZ'.split()

address = {}
current_address = 0

def assemble_label(words):
    address[words[0][:-1]] = current_address
    return assemble(words[1:])

def assemble_number(words):
    if len(words) > 1 and not words[1].startswith(';'):
        raise ValueError('Extra stuff on line')
    global current_address
    current_address += 1
    return hex(int(words[0]))[2:].zfill(8)

def get_operand(word):
    if word.isdigit():
        return int(word)
    if word.isalpha():
        return address[word]
    raise ValueError('Argument must be a number or label')

def ensure_only_one_operand(words):
    if len(words) == 1:
        raise ValueError('No operand to instruction')
    if len(words) > 2 and not words[2].startswith(';'):
        raise ValueError('Extra stuff on line')

def assemble_instruction(words):
    ensure_only_one_operand(words)
    operand = get_operand(words[1])
    if operand >= 2 ** 28:
        raise ValueError('Operand too large')
    opcode = hex(instructions.index(words[0]))[2:]
    operand_in_hex = hex(operand)[2:].zfill(7)
    global current_address
    current_address += 1
    return f'{opcode}{operand_in_hex}'

def assemble(words):
    if not words:
        return ''
    elif words[0].startswith(';'):
        return ''
    elif words[0].endswith(':'):
        return assemble_label(words)
    elif words[0].isdigit():
        return assemble_number(words)
    elif words[0] in instructions:
        return assemble_instruction(words)
    raise ValueError('Illegal syntax')

try:
    for line in sys.stdin:
        machine_code = assemble(line.rstrip().upper().split())
        if machine_code:
            print(machine_code)
except ValueError as e:
    print(e)
