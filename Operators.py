class Operator_bool_lis:
    def __init__(self, oper, bool_lis) -> None:
        self.operator = oper
        self.bool_lis = bool_lis

class Operators:

    def __init__(self, path, loop, dp):
        self.path = path
        self._loop = loop
        self.dp = dp


    # base 
    def _NOT(self, child) -> list[bool]:
        res = child.copy()
        for i in range(len(res)):
            res[i] = not res[i]
        return res
    
    def _AND(self, left, right) -> list[bool]:
        res = []
        for i in range(len(left)):
            res.append(left[i] and right[i])
        return res
    
    def _OR(self, left, right) -> list[bool]:
        res = []
        for i in range(len(left)):
            res.append(left[i] or right[i])
        return res
    
    def _X(self, child) -> list[bool]:
        res = child.copy()
        loop_start = len(child) - self._loop
        res.append(child[loop_start])
        res.pop(0)
        return res
    
    def _get_first_bool_index(self,lis, start_index, value):
        try:
            return lis.index(value, start_index)
        except:
            return len(lis)
    
    def _U(self, left, right) -> list[bool]:
        #place holder array with some value, extra element for beginning of loop
        res = ["ph" for _ in range(len(left)+1)]

        # replace placeholder value with true if right[i] == true else replace with false
        for i in range(len(left)):
            if right[i]:
                res[i] = True
            elif left[i] == False:
                res[i] = False
        
		# set the extra element as the same as the start of loop
        loop_start = len(left) - self._loop
        res[-1] = res[loop_start]

        # get rid of the rest of the placeholder values
        while(res.count("ph") > 0):
            ph_first:int = res.index("ph") # index offirst placeholder value
            first_true:int = self._get_first_bool_index(res, ph_first, True) # first true value
            first_false:int = self._get_first_bool_index(res, ph_first, False) # first false value

            res[ph_first] = not ((first_true == first_false) or (first_false < first_true))
            if (ph_first == loop_start):
                res[-1] = res[loop_start]
        res.pop(-1)
        return res

    # Atom
    def ATOM(self, operator) -> Operator_bool_lis:
        bools = [] # list of bools
        for state in self.path:
            bools.append(operator in state.labeling)
        return Operator_bool_lis(operator, bools)
    
    # Unary

    def _get_Operator_bool_lis(self, operator, dp) -> Operator_bool_lis:
        return next((filter(lambda Operator_bool_lis: Operator_bool_lis.operator == operator, dp)))

    def _unary_operator_solve(self, operator, type) -> Operator_bool_lis:
        child = self._get_Operator_bool_lis(operator.children()[0],self.dp).bool_lis
        return Operator_bool_lis(operator, type(child))
    
    def NOT(self, operator) -> list[bool]:
        return self._unary_operator_solve(operator, self._NOT)

    def X(self, operator) -> list[bool]:
        return self._unary_operator_solve(operator, self._X)
    
    def F(self, operator) -> list[bool]:
        # F(x) == True U x
        operation_type = lambda x: self._U([True for _ in range(len(x))], x)
        return self._unary_operator_solve(operator, operation_type)
    
    def G(self, operator) -> list[bool]:
        #G(x) == False R x == !F(!x) == !(True U !x)
        operation_type = lambda x: self._NOT(self._U([True for _ in range(len(x))], self._NOT(x)))
        return self._unary_operator_solve(operator, operation_type)
    
    # binary

    def _binary_operator_solve(self, operator, type):
        left:Operator_bool_lis = self._get_Operator_bool_lis(operator.children()[0], self.dp).bool_lis
        right:Operator_bool_lis = self._get_Operator_bool_lis(operator.children()[1], self.dp).bool_lis
        return Operator_bool_lis(operator, type(left, right))
    
    def U(self, operator):
        return self._binary_operator_solve(operator, self._U)
    
    def AND(self, operator):
        return self._binary_operator_solve(operator, self._AND)
    
    def OR(self, operator):
        return self._binary_operator_solve(operator, self._OR)
    
    def IMPL(self, operator):
        # x -> y == !x || y
        operation_type = lambda x, y: self._OR(self._NOT(x), y)
        return self._binary_operator_solve(operator, operation_type)
    
    def R(self, operator):
        # x R y == !(!x U !y)
        operation_type = lambda x, y: self._NOT(self._U(self._NOT(x), self._NOT(y)))
        return self._binary_operator_solve(operator, operation_type)
    
    def W(self, operator):
        # x W y == (x U y) || G(x) == x U (y || G(x)) == y R (y || x) == !(!y U !(y || x))
        operation_type = lambda x, y: self._NOT(self._U(self._NOT(y), self._NOT(self._OR(y, x))))
        return self._binary_operator_solve(operator, operation_type)

