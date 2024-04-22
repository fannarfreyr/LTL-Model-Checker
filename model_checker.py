from interface import parse, getpath, getpath_from_file
from parsing.parser import Parser
from parsing.lexer import Lexer
from input_paths.path import Path 
from parsing.ast import Ast
from parsing.token import Token, TokenType
from Operators import Operators, Operator_bool_lis

# A model checker for LTL on regular paths

def evaluate(operators: list[Ast], path: Path, loop: int) -> list[bool]:
	dp: list[Operator_bool_lis] = []
	checker: Operators = Operators(path, loop, dp)

	for oper in operators:
		dp.append(solve(checker, oper))
	return dp[-1].bool_lis
	
def modelcheck(m,f):
	if isinstance(m, Path):
		path_obj: Path = m
	else:
		path_obj: Path = getpath(m)
          
	if isinstance(f, Ast):
		formula_parsed: Ast = f
	else:
		formula_parsed: Ast = parse(f)
	operators_inorder: list[Ast] = inorder_operators(formula_parsed)
	return evaluate(operators_inorder, path_obj.path, path_obj.loop)[0]

	
def solve(checker: Operators, operator: Ast) -> Operator_bool_lis:
	match operator.oper():
		case TokenType.ATOM: return checker.ATOM(operator)
		case TokenType.NOT: return checker.NOT(operator)
		case TokenType.AND: return checker.AND(operator)
		case TokenType.OR: return checker.OR(operator)
		case TokenType.IMPL: return checker.IMPL(operator)
		case TokenType.U: return checker.U(operator)
		case TokenType.X: return checker.X(operator)
		case TokenType.F: return checker.F(operator)
		case TokenType.R: return checker.R(operator)
		case TokenType.G: return checker.G(operator)
		case TokenType.W: return checker.W(operator)
		case _: raise Exception("Invalid operator: " + operator)


def _inorder_operators(node:Ast, res):
	for child in node.children(): _inorder_operators(child, res)
	res.append(node)

def inorder_operators(root:Ast) -> list[Ast]:
	res = []
	_inorder_operators(root, res)
	return res


## change the return value to True if you want longer feedback from the autograder
## the feedback can be long for some tests, so the default value is set to False
def longer_feedback():
	return False

## adjust the following return values to select how long and how many random paths
## you will check your solution on for the self-check version of the autograder

def how_many_tests():
	return 1

def how_long_paths():
	return 100


# Testing the desired properties from chapter 6, in the assignment description
def test():
    formulas = {
        1: "G(!(wolf_left && goat_left && !employee_left) && !(wolf_right && goat_right && !employee_right))",
        2: "G(!(popeye_left && spinach_left && !employee_left) && !(popeye_right && spinach_right && !employee_right))",
        3: "G(!(popeye_left && wine_left && computer_left && !employee_left) && !(popeye_right && wine_right && computer_right && !employee_right))",
        4: "G(!(wolf_left && goat_left && !employee_left && X(wolf_left && goat_left && !employee_left && X(wolf_left && goat_left && !employee_left && X(wolf_left && goat_left && !employee_left)))) && !(wolf_right && goat_right && !employee_right && X(wolf_right && goat_right && !employee_right && X(wolf_right && goat_right && !employee_right && X(wolf_right && goat_right && !employee_right)))))",
        5: "!F((employee_left && X(employee_left && X(employee_left && X(employee_left)))) || (employee_right && X(employee_right && X(employee_right && X(employee_right)))))",
        6: "!F((popeye_right && employee_right && !spinach_right) && X((popeye_right && employee_right && !spinach_right) U ((popeye_right && !employee_right) && X((popeye_right && !employee_right) U (popeye_right && employee_right && !spinach_right)))))",
        7: "G(!(goat_trans && X(!sheep_trans U goat_trans)) && !(sheep_trans && X(!goat_trans U sheep_trans)))",
        8: "G((employee_left U (employee_trans && X(employee_right))) || (employee_right U (employee_trans && X(employee_left))))"
    }
    passed = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
    for i in range(8):
        print("----------------New Path-----------------------")
        path:Path = getpath_from_file(f"paths/path{i}.txt")
        for j in range(1,9):
            form = parse(formulas[j])
            res = modelcheck(path, form)
            if res == True:
                passed[j].append(i)
            print(f"path {i} - formula {j}: {res}")
	
    print(passed)
	

if __name__ == "__main__":
     test()