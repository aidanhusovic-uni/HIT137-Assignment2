from pathlib import Path 
import math # import the maths module - used to check if the result is a complex number or not finite.

project = Path(__file__).resolve().parent

input_path = project/'input.txt'


def token(text): # Convert the string of text into a list of tokens.
    
    tokens = []
    i = 0

    while i < len(text): # Keep looping until the end of the text is reached.
        char = text[i]
        
        if char.isspace(): # Ignore spaces between tokens.
            i += 1
            continue

        if char.isdigit(): # check if the character is a digit. If it is, then it is the start of a number token.
            start = i

            while i < len(text) and text[i].isdigit(): # Keep looping until the end of the text is reached or a non-digit character is found.
                i += 1

            if i < len(text) and text[i] == ".": # check if the next character is a decimal point. If it is, then it is the start of a decimal number token.
                i += 1

                if i >= len(text) or not text[i].isdigit(): # check if the next character is a digit. If it is not, then it is an invalid number token.
                    raise ValueError("Invalid number")

                while i < len(text) and text[i].isdigit():
                    i += 1

            num_text = text[start:i] # Takes the string betweeen the start and end of the number token and assigns it to a variable.
            tokens.append(("NUM", num_text, float(num_text)))
            continue

        if char in "+-*/%^": # Check if the character is an operator. If it is, then it is an operator token.
            tokens.append(("OP", char, None)) 
            i += 1
            continue

        if char == "(": # Check if the character is an opening parenthesis. If it is, then it is a left parenthesis token.
            tokens.append(("LPAREN", char, None))
            i += 1
            continue

        if char == ")": # Check if the character is a closing parenthesis. If it is, then it is a right parenthesis token.
            tokens.append(("RPAREN", char, None))
            i += 1
            continue

        raise ValueError("Invalid character") # raise an error if not defined.

    tokens.append(("END", "", None)) # This is used to signal the end of the input to the parser.
    return tokens

# print(token("2(4+2)")) # This was a test

def tokens_text(tokens): #Convert the token list into the output string.
    parts = []

    for token_type, num_text, _ in tokens:
        if token_type == "END": # if the token type is "END", then it is the end of the input. Append "[END]" to the list.
            parts.append("[END]")
        else:
            parts.append(f"[{token_type}:{num_text}]") # if the token type is not "END", then append the token type and the number text to the parts list.

    return " ".join(parts) # return the parts list as a string, with each part separated by a space.




def current(state): #Return the parser's current token.
    return state["tokens"][state["pos"]]


def advance_token(state): # Save the current token and advance the parser to the next token.
    token = current(state)
    state["pos"] += 1
    return token




def parse_primary(state): # Parse numbers and parenthesised expressions.
    token = current(state)

    if token[0] == "NUM": # if the current token is a number, then advance the token and return a tuple representing the number, with the token type and the number value.
        advance_token(state)
        return ("num", token[2])

    if token[0] == "LPAREN": # if the current token is a left parenthesis, then advance the token and parse the expression inside the parentheses.
        advance_token(state)

        if current(state)[0] == "RPAREN": # if the current token is a right parenthesis, then raise an error because there is nothing inside the parentheses.
            raise ValueError("Empty parentheses")

        expression = parse_expression(state)

        if current(state)[0] != "RPAREN": # if the current token is not a right parenthesis, then raise an error because there is a missing closing parenthesis.
            raise ValueError("Missing closing parenthesis")

        advance_token(state) 
        return expression # return the expression inside the parentheses.

    raise ValueError("Expected number or opening parenthesis") # raise an error if the current token is not a number or a left parenthesis.


def parse_power(state): # Parse Exponents left to right.
    left = parse_primary(state)

    if current(state)[0] == "OP" and current(state)[1] == "^": # if the current token is an operator and the operator is in the 1st postition, then it is an exponentiation. Advance the token and parse the next as the right digit of the exponentiation.
        advance_token(state)
        right = parse_unary(state)
        return ("bin", "^", left, right) # return a tuple representing the exponentiation operation, with the left digit, operator, and right digit.

    return left # return the left side of the expression.


def parse_unary(state): # Parse unary - (negation) and forbid unary +.
    token = current(state)

    if token[0] == "OP" and token[1] == "-": # if the current token is an operator and the operator is a minus sign, then it is a unary negation. Advance the token and parse the next as the operation of the negation.
        advance_token(state)
        operand = parse_unary(state)
        return ("neg", operand)

    if token[0] == "OP" and token[1] == "+": # Disallow unary + (e.g. +3 or +(-2)).
        raise ValueError("Unary plus is not supported")

    return parse_power(state)


def auto_multi_start(state): # eg. 2(4+2) or (2+3)(4+5) or 2(3)(4) or (2+3)4
    token_now = current(state)

    if token_now[0] == "LPAREN":   # A factor followed by "(" means auto multiplication.
        return True

    if token_now[0] == "NUM" and state["pos"] > 0: # if the current token is a number and the position is greater than 0, then check if the previous token is a right parenthesis. If it is, then it is an auto multiplication.
        previous = state["tokens"][state["pos"] - 1]

        if previous[0] == "RPAREN":
            return True # return True if there is an auto multiplication.

    return False # Return False if there is no auto multiplication.


def parse_mul_div_mod(state): # Parse *, /, %, and auto multiplication left-to-right.
    left = parse_unary(state)

    while True:
        token = current(state)

        if token[0] == "OP" and token[1] in "*/%": # if the current token is an operator and the operator continue parsing.
            op = advance_token(state)[1]
            right = parse_unary(state)
            left = ("bin", op, left, right)
            continue

        if auto_multi_start(state): # if the current token is a left parenthesis or a number and the previous token is a right parenthesis, then it is an auto multiplication.
            right = parse_unary(state)
            left = ("bin", "*", left, right)
            continue

        break # break out of the loop if there are no more operators or auto multiplication.

    return left # return the left side of the expression, which is the result of the parsing.


def parse_add_sub(state): 
    left = parse_mul_div_mod(state) 

    while current(state)[0] == "OP" and current(state)[1] in "+-": # while the current token is an operator and the operator is either + or -, continue parsing.
        op = advance_token(state)[1]
        right = parse_mul_div_mod(state)
        left = ("bin", op, left, right)

    return left


def parse_expression(state): # Start with addition and subtraction.
    return parse_add_sub(state)





def format_number(num): # format numbers as they're printed to the parse tree. This removes formatting issues e.g. 1.00000, -0 etc.
    if num == 0:
        return "0"
    
    if float(num).is_integer(): # Changes 1.0 to 1, -0.0 to 0 etc.
        return str(int(num)) # Returns a string of the int.

    return format(num, ".15g") # If the number is a float, returns a string of the number to 15 significant digits.


def tree_text(node): # Converts a parse tree into a string for output.txt.
    tree_kind = node[0]

    if tree_kind == "num": # if the node is a number, then return the formatted number as a string.
        return format_number(node[1])

    if tree_kind == "neg": # if the node is a negation, then return a string representing the negation operation, with the negation operator and the digit.
        return f"(neg {tree_text(node[1])})"

    if tree_kind == "bin": # if the node is a binary operation, then return a string representing the binary operation, with the operator and the left and right digits.
        op = node[1]
        left = tree_text(node[2])
        right = tree_text(node[3])
        return f"({op} {left} {right})"

    raise ValueError("Invalid parse tree") # raise an error if the node is not a number, negation, or binary operation.




def evaluate_tree(node): # Evaluate a parse tree and return the result.
    kind = node[0]

    if kind == "num": # if the node is a number, then return the number value.
        return node[1]

    if kind == "neg": # if the node is a negation, then return the negated value of the digit.
        return -evaluate_tree(node[1])

    if kind == "bin": # if the node is a binary operation, then evaluate the left and right digits and return the result of the operation.
        op = node[1]
        left = evaluate_tree(node[2])
        right = evaluate_tree(node[3])

        if op == "+": 
            value = left + right
        elif op == "-":
            value = left - right
        elif op == "*":
            value = left * right
        elif op == "/":
            value = left / right
        elif op == "%":
            value = left % right
        elif op == "^":
            value = left ** right
        else:
            raise ValueError("Unknown operator") 

        if isinstance(value, complex) or not math.isfinite(value): # if the result is a complex number or not finite (e.g. infinity or NaN), then raise an error because the result is invalid.
            raise ValueError("Invalid numeric result")

        return value # return the result of the binary operation.

    raise ValueError("Invalid parse tree") # raise an error if the node is not a number, negation, or binary operation.




def evaluate_line(expression):

    try: # Stage 1: This will tokenise the input expression and convert it into a list of tokens.
        tokens = token(expression)
        tokens_string = tokens_text(tokens)
    except (ValueError, OverflowError): #  If there is an error in the process, it will return an error message.
        return {
            "input": expression,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR",
        }

    try: # Stage 2: this will parse the list of tokens into a parse tree.
        state = {
            "tokens": tokens,
            "pos": 0,
        }

        tree = parse_expression(state)

        if current(state)[0] != "END": # A valid expression must consume every token.
            raise ValueError("Unexpected token")

        tree_string = tree_text(tree)

    except (ValueError, IndexError):
        return {
            "input": expression,
            "tree": "ERROR",
            "tokens": tokens_string,
            "result": "ERROR",
        }

    try: # Stage 3: this will evaluate the parse tree and return the result. If there is an error in the evaluation process, it will return an error message.
        result = float(evaluate_tree(tree))

        return {
            "input": expression,
            "tree": tree_string,
            "tokens": tokens_string,
            "result": result,
        }

    except (ValueError, ZeroDivisionError, OverflowError):
        return {
            "input": expression,
            "tree": tree_string,
            "tokens": tokens_string,
            "result": "ERROR",
        }


    

def format_result(num): # formats the final result.
    if float(num).is_integer():
        return str(int(num))

    text = f"{num:.4f}".rstrip("0").rstrip(".") # Rounds the number to 4 decimal places, then removes any trailing zeros and the decimal point if there are no decimal digits left.

    if text == "-0":
        return "0" # Returns 0 instead of -0.

    return text




def evaluate_file(input_path: str) -> list[dict]: # Evaluate the .TXT file and return the results as a list of dictionaries.

    results = []

    with open(input_path, "r", encoding="utf-8") as input_file: # Removes line-ending characters only. Keeps other characters as they appeared in the file.
        expressions = input_file.read().splitlines()

    for expression in expressions: # this will append the dictionary returned by evaluate_line to the results list.
        results.append(evaluate_line(expression)) 

    input_path = Path(input_path) # Converts the input path to a Path object.

    output_path = input_path.parent/"output.txt" # Creates output.txt in the same directory as input_path.

    with open(output_path, "w", encoding="utf-8") as output_file: # This will write the results to output.txt. It will overwrite the file if it already exists.
        for index, item in enumerate(results): # 
            output_file.write(f"Input: {item['input']}\n")
            output_file.write(f"Tree: {item['tree']}\n")
            output_file.write(f"Tokens: {item['tokens']}\n") 

            if item["result"] == "ERROR": # if the result is an error, then it will write "ERROR" to the output file. Otherwise, it will format the result and write it to the output file.
                result_text = "ERROR"
            else:
                result_text = format_result(item["result"])

            output_file.write(f"Result: {result_text}\n") 

            if index < len(results) - 1: # inserts a blank line between each output.
                output_file.write("\n")

    return results # return the results list.

results = evaluate_file(input_path)

if all(item["result"] != "ERROR" for item in results):
    print("Evaluation completed successfully.")
else:
    print("Evaluation completed, but one or more expressions returned an ERROR.")