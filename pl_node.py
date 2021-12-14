#!/usr/bin/env python
""" generated source for module Node """

#  (C) 2013 Jim Buffenbarger
#  All rights reserved.

from pl_function import Function
from pl_evalexception import EvalException
import math
class Node(object):
    """ generated source for class Node """
    pos = 0
    
    def eval(self, env):
        """ generated source for method eval """
        raise EvalException(self.pos, "cannot eval() node!")

    def __str__(self):
        """ generated source for method toString """
        result = ""
        result += str(self.__class__.__name__)
        result += " ( "
        fields = self.__dict__
        for field in fields:
            result += "  "
            result += str(field)
            result += str(": ")
            result += str(fields[field])
        result += str(" ) ")
        return result


class NodeAddop(Node):
    """ generated source for class NodeAddop """

    def __init__(self, pos, addop):
        """ generated source for method __init__ """
        super(NodeAddop, self).__init__()
        self.pos = pos
        self.addop = addop

    def op(self, o1, o2):
        """ generated source for method op """
        if self.addop == "+":
            return o1 + o2
        if self.addop == "-":
            return o1 - o2
        raise EvalException(self.pos, "bogus addop: " + self.addop)
        
        
class NodeAddop(Node):
    """ generated source for class NodeAddop """

    def __init__(self, pos, addop):
        """ generated source for method __init__ """
        super(NodeAddop, self).__init__()
        self.pos = pos
        self.addop = addop

    def op(self, o1, o2):
        """ generated source for method op """
        if self.addop == "+":
            return o1 + o2
        if self.addop == "-":
            return o1 - o2
        raise EvalException(self.pos, "bogus addop: " + self.addop)


class NodeAssn(Node):
    """ generated source for class NodeAssn """

    def __init__(self, id, expr):
        """ generated source for method __init__ """
        super(NodeAssn, self).__init__()
        self.id = id
        self.expr = expr

    def eval(self, env):
        """ generated source for method eval """
        return env.put(self.id, self.expr.eval(env))

        
class NodeBegin(Node):
    """ generated source for class NodeBegin """

    def __init__(self, block):
        """ generated source for method __init__ """
        super(NodeBegin, self).__init__()
        self.block = block

    def eval(self, env):
        """ generated source for method eval """
        return self.block.eval(env)

class NodeBlock(Node):
    """ generated source for class NodeBlock """

    def __init__(self, stmt, block):
        """ generated source for method __init__ """
        super(NodeBlock, self).__init__()
        self.stmt = stmt
        self.block = block

    def eval(self, env):
        """ generated source for method eval """
        r = self.stmt.eval(env)
        return r if self.block == None else self.block.eval(env)

class NodeBoolExpr(Node):
    """ generated source for class NodeBoolExpr """

    def __init__(self, exprl, relop, exprr):
        """ generated source for method __init__ """
        super(NodeBoolExpr, self).__init__()
        self.exprl = exprl
        self.relop = relop
        self.exprr = exprr

    def eval(self, env):
        """ generated source for method eval """
        return self.relop.op(self.exprl.eval(env), self.exprr.eval(env))
        
        
class NodeIf(Node):
    def __init__(self, bool_expr, stmt, sub_stmt):
        super(NodeIf, self).__init__()
        self.bool_expr = bool_expr
        self.stmt = stmt
        self.sub_stmt = sub_stmt
        
    def eval(self, env):
        if self.bool_expr.eval(env):
            return self.stmt.eval(env)
        elif self.sub_stmt is not None:
            return self.sub_stmt.eval(env)
        return None


class NodeWhile(Node):
    def __init__(self, bool_expr, stmt):
        super(NodeWhile, self).__init__()
        self.bool_expr = bool_expr
        self.stmt = stmt
        
    def eval(self, env):
        r = None
        while self.bool_expr.eval(env):
            r = self.stmt.eval(env)
        return r


class NodeExpr(Node):
    """ generated source for class NodeExpr """

    def __init__(self, term, addop, expr):
        """ generated source for method __init__ """
        super(NodeExpr, self).__init__()
        self.term = term
        self.addop = addop
        self.expr = expr

    def append(self, expr):
        if self.expr is None:
            self.addop = expr.addop
            self.expr = expr
            expr.addop = None
        else:
            self.expr.append(expr)

    def eval(self, env):
        """ generated source for method eval """
        return self.term.eval(env) if self.expr is None else self.addop.op(self.expr.eval(env), self.term.eval(env))


class NodeFact(Node):
    """ generated source for class NodeFact """
    pass


class NodeFactFact(NodeFact):
    """ generated source for class NodeFactFact """

    def __init__(self, fact):
        """ generated source for method __init__ """
        super(NodeFactFact, self).__init__()
        self.fact = fact

    def eval(self, env):
        """ generated source for method eval """
        return -self.fact.eval(env)

class NodeRelop(Node):
    """ generated source for class NodeRelop """

    def __init__(self, pos, relop):
        """ generated source for method __init__ """
        super(NodeRelop, self).__init__()
        self.pos = pos
        self.relop = relop

    def op(self, o1, o2):
        """ generated source for method op """
        if self.relop == "<":
            return 1 if o1 < o2 else 0
        if self.relop == "<=":
            return 1 if o1 <= o2 else 0
        if self.relop == ">":
            return 1 if o1 > o2 else 0
        if self.relop == ">=":
            return 1 if o1 >= o2 else 0
        if self.relop == "<>":
            return 1 if o1 != o2 else 0
        if self.relop == "==":
            return 1 if o1 == o2 else 0
        raise EvalException(pos, "bogus relop: " + self.relop)

class NodeFactExpr(NodeFact):
    """ generated source for class NodeFactExpr """

    def __init__(self, expr):
        """ generated source for method __init__ """
        super(NodeFactExpr, self).__init__()
        self.expr = expr

    def eval(self, env):
        """ generated source for method eval """
        return self.expr.eval(env)

class NodeFactString(NodeFact):
    def __init__(self, string):
        super(NodeFactString, self).__init__()
        self.string = string

    def eval(self, env):
        return self.string 
    
class NodeFactId(NodeFact):
    """ generated source for class NodeFactId """

    def __init__(self, pos, id):
        """ generated source for method __init__ """
        super(NodeFactId, self).__init__()
        self.pos = pos
        self.id = id

    def eval(self, env):
        """ generated source for method eval """
        return env.get(self.pos, self.id)

class NodeFactNum(NodeFact):
    """ generated source for class NodeFactNum """

    def __init__(self, num):
        """ generated source for method __init__ """
        super(NodeFactNum, self).__init__()
        self.num = num

    def eval(self, env):
        """ generated source for method eval """
        return float(self.num)


class NodeMulop(Node):
    """ generated source for class NodeMulop """

    def __init__(self, pos, mulop):
        """ generated source for method __init__ """
        super(NodeMulop, self).__init__()
        self.pos = pos
        self.mulop = mulop

    def op(self, o1, o2):
        """ generated source for method op """
        if self.mulop == "*":
            return o1 * o2
        if self.mulop == "/":
            return o1 / o2
        raise EvalException(self.pos, "bogus mulop: " + self.mulop)


class NodeStmt(Node):
    """ generated source for class NodeStmt """

    def __init__(self, node):
        """ generated source for method __init__ """
        super(NodeStmt, self).__init__()
        self.node = node

    def eval(self, env):
        """ generated source for method eval """
        return self.node.eval(env)


class NodeTerm(Node):
    """ generated source for class NodeTerm """

    def __init__(self, fact, mulop, term):
        """ generated source for method __init__ """
        super(NodeTerm, self).__init__()
        self.fact = fact
        self.mulop = mulop
        self.term = term

    def append(self, term):
        if self.term is None:
            self.mulop = term.mulop
            self.term = term
            term.mulop = None
        else:
            self.term.append(term)

    def eval(self, env):
        """ generated source for method eval """
        return self.fact.eval(env) if self.term is None else self.mulop.op(self.term.eval(env), self.fact.eval(env))

class NodeProg(Node):
    """ generated source for class NodeProg """

    def __init__(self, block):
        """ generated source for method __init__ """
        super(NodeProg, self).__init__()
        self.block = block

    def eval(self, env):
        """ generated source for method eval """
        return self.block.eval(env)

class NodeRd(Node):
    """ generated source for class NodeRd """

    def __init__(self, id):
        """ generated source for method __init__ """
        super(NodeRd, self).__init__()
        self.id = id

    def eval(self, env):
        """ generated source for method eval """
        scanner = input();
        if "'" not in scanner:
            scanner = float(scanner)
        else:
            scanner = scanner[1: len(scanner) - 1]
        return env.put(self.id, scanner)   
    
class NodeWr(Node):
    """ generated source for class NodeWr """

    def __init__(self, expr):
        """ generated source for method __init__ """
        super(NodeWr, self).__init__()
        self.expr = expr

    def eval(self, env):
        """ generated source for method eval """
        val = self.expr.eval(env)
        print(val)
        return val
          

class NodeFuncDecl(Node):
    def __init__(self, id, param, expr):
        super(NodeFuncDecl, self).__init__()
        self.id = id
        self.param = param
        self.expr = expr

    def eval(self, env):
        func = Function(self.param, self.expr)
        return env.putFunc(self.id, func)


class NodeFuncCall(Node):
    def __init__(self, id, expr):
        super(NodeFuncCall, self).__init__()
        self.id = id
        self.expr = expr

    def eval(self, env):
        func = env.getFunc(self.pos, self.id)
        param = self.expr.eval(env)
        return func.call(param)
    

class NodeSqrt(Node):
    def __init__(self, expr):
        super(NodeSqrt, self).__init__()
        self.expr = expr

    def eval(self, env):
        val = self.expr.eval(env)
        return math.sqrt(val)

class NodeSqr(Node):
    def __init__(self, expr):
        super(NodeSqr, self).__init__()
        self.expr = expr

    def eval(self, env):
        val = self.expr.eval(env)
        return val * val

class NodeLength(Node):
    def __init__(self, expr):
        super(NodeLength, self).__init__()
        self.expr = expr

    def eval(self, env):
        val = self.expr.eval(env)
        return len(val)
    
class NodeAssert(Node):
    def __init__(self, bool_expr, expr):
        super(NodeAssert, self).__init__()
        self.bool_expr = bool_expr
        self.expr = expr
        
    def eval(self, env):
        if self.bool_expr.eval(env):
            return None
        raise Exception(self.expr.eval(env))
    
class NodeCharAt(Node):
    def __init__(self, id, expr):
        super(NodeCharAt, self).__init__()
        self.id = id
        self.expr = expr

    def eval(self, env):
        string = env.get(self.pos, self.id)
        i = self.expr.eval(env)
        return string[int(i)]
    
class NodeSubString(Node):
    def __init__(self, id, expr, expr2):
        super(NodeSubString, self).__init__()
        self.id = id
        self.expr = expr
        self.expr2 = expr2

    def eval(self, env):
        string = env.get(self.pos, self.id)
        i = self.expr.eval(env)
        i2 = self.expr2.eval(env)
        return string[int(i):int(i2)]