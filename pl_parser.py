from pl_syntaxexception import SyntaxException
from pl_node import *
from pl_scanner import Scanner
from pl_token import Token


class Parser(object):
    built_ins = {'square', 'sqrt', 'ceil', 'floor', 'factorial', 'length'}
    
    """ generated source for class Parser """    
    def __init__(self):
        self.scanner = None

    def match(self, s):
        """ generated source for method match """
        self.scanner.match(Token(s))

    def curr(self):
        """ generated source for method curr """
        return self.scanner.curr()

    def pos(self):
        """ generated source for method pos """
        return self.scanner.position()

    def parseMulop(self):
        """ generated source for method parseMulop """
        if self.curr() == Token("*"):
            self.match("*")
            return NodeMulop(self.pos(), "*")
        if self.curr() == Token("/"):
            self.match("/")
            return NodeMulop(self.pos(), "/")
        return None

    def parseAddop(self):
        """ generated source for method parseAddop """
        if self.curr() == Token("+"):
            self.match("+")
            return NodeAddop(self.pos(), "+")
        if self.curr() == Token("-"):
            self.match("-")
            return NodeAddop(self.pos(), "-")
        return None
    
    def parseRelop(self):
        """ generated source for method parseRelop """
        if self.curr() == Token("<"):
            self.match("<")
            return NodeRelop(self.pos(), "<")
        if self.curr() == Token("<="):
            self.match("<=")
            return NodeRelop(self.pos(), "<=")
        if self.curr() == Token(">"):
            self.match(">")
            return NodeRelop(self.pos(), ">")
        if self.curr() == Token(">="):
            self.match(">=")
            return NodeRelop(self.pos(), ">=")
        if self.curr() == Token("<>"):
            self.match("<>")
            return NodeRelop(self.pos(), "<>")
        if self.curr() == Token("=="):
            self.match("==")
            return NodeRelop(self.pos(), "==")
        return None
    
    def parseBoolExpr(self):
        """ generated source for method parseBoolExpr """
        exprl = self.parseExpr()
        relop = self.parseRelop()
        exprr = self.parseExpr()
        boolexpr = NodeBoolExpr(exprl, relop, exprr)
        return boolexpr

    def parseFact(self):
        """ generated source for method parseFact """
        if self.curr() == Token("("):
            self.match("(")
            expr = self.parseExpr()
            self.match(")")
            return NodeFactExpr(expr)
        if self.curr() == Token("-"):
            self.match("-")
            fact = self.parseFact()
            return NodeFactFact(fact)
        if self.curr() == Token("id"):
            nid = self.curr()
            if nid.lex() in self.built_ins:
                built_in = self.parseBuiltIn()
                return built_in
            self.match("id")
            if self.curr() == Token("["):
                self.match("[")
                expr = self.parseExpr()
                if self.curr() == Token(":"):
                    self.match(":")
                    expr2 = self.parseExpr()
                    self.match("]")
                    return NodeSubString(nid.lex(), expr, expr2)
                self.match("]")
                return NodeCharAt(nid.lex(), expr)
            if self.curr() == Token("("):
                self.match("(")
                expr = self.parseExpr()
                self.match(")") 
                return NodeFuncCall(nid.lex(), expr)
            return NodeFactId(self.pos(), nid.lex())
        if self.curr() == Token("string"):
            string = self.curr()
            self.match("string")
            return NodeFactString(string.lex())
        num = self.curr()
        self.match("num")
        return NodeFactNum(num.lex())

    def parseTerm(self):
        """ generated source for method parseTerm """
        fact = self.parseFact()
        mulop = self.parseMulop()
        if mulop is None:
            return NodeTerm(fact, None, None)
        term = self.parseTerm()
        term.append(NodeTerm(fact, mulop, None))
        return term

    def parseExpr(self):
        """ generated source for method parseExpr """
        term = self.parseTerm()
        addop = self.parseAddop()
        if addop is None:
            return NodeExpr(term, None, None)
        expr = self.parseExpr()
        expr.append(NodeExpr(term, addop, None))
        return expr

    def parseAssn(self):
        """ generated source for method parseAssn """
        nid = self.curr()
        self.match("id")
        self.match("=")
        expr = self.parseExpr()
        assn = NodeAssn(nid.lex(), expr)
        return assn

    def parseWr(self):
        """ generated source for method parseWr """
        self.match("wr")
        expr = self.parseExpr()
        wr = NodeWr(expr)
        return wr
        
    def parseRd(self):
        """ generated source for method parseRd """
        self.match("rd")
        nid = self.curr()
        self.match("id")
        rd = NodeRd(nid.lex())
        return rd
    
    def parseAssert(self):
        self.match("assert")
        self.match("(")
        bool_expr = self.parseBoolExpr()
        self.match(",")
        message = self.parseExpr()
        self.match(")")
        return NodeAssert(bool_expr, message)
        
    def parseBuiltIn(self):
        nid = self.curr()
        self.match("id")
        self.match("(")
        expr = self.parseExpr()
        if nid.lex() == "sqrt":
            self.match(")")
            return NodeSqrt(expr)
        if nid.lex() == "square":
            self.match(")")
            return NodeSqr(expr)
        if nid.lex() == "factorial":
            self.match(")")
            return NodeFactorial(expr)
        if nid.lex() == "length":
            self.match(")")
            return NodeLength(expr)

    def parseIf(self):
        self.match("if")
        bool_expr = self.parseBoolExpr()
        self.match("then")
        stmt = self.parseStmt()
        sub_stmt = None
        if self.curr() == Token("else"):
            self.match("else")
            sub_stmt = self.parseStmt()
        if_stmt = NodeIf(bool_expr, stmt, sub_stmt)
        return if_stmt
        
    def parseWhile(self):
        self.match("while")
        bool_expr = self.parseBoolExpr()
        self.match("do")
        stmt = self.parseStmt()
        while_stmt = NodeWhile(bool_expr, stmt)
        return while_stmt
        
    def parseBegin(self):
        """ generated source for method parseBegin """
        self.match("begin")
        block = self.parseBlock()
        self.match("end")
        begin = NodeBegin(block)
        return begin

    def parseStmt(self):
        """ generated source for method parseStmt """
        if self.curr() == Token("rd"):
            rd = self.parseRd()
            return NodeStmt(rd)
        if self.curr() == Token("wr"):
            wr = self.parseWr()
            return NodeStmt(wr)
        if self.curr() == Token("if"):
            if_stmt = self.parseIf()
            return NodeStmt(if_stmt)
        if self.curr() == Token("while"):
            while_stmt = self.parseWhile()
            return NodeStmt(while_stmt)
        if self.curr() == Token("begin"):
            begin = self.parseBegin()
            return NodeStmt(begin)
        if self.curr() == Token("def"):
            func_decl = self.parseFuncDecl()
            return NodeStmt(func_decl)
        if self.curr() == Token("id"):
            assn = self.parseAssn()
            return NodeStmt(assn)
        if self.curr() == Token("assert"):
            assert_func = self.parseAssert()
            return NodeStmt(assert_func)
        return None

    def parseBlock(self):
        """ generated source for method parseBlock """
        stmt = self.parseStmt()
        rest = None
        if self.curr() == Token(";"):
            self.match(";")
            rest = self.parseBlock()
        block = NodeBlock(stmt, rest)
        return block
        
    def parseProg(self):
        """ generated source for method parseProg """
        block = self.parseBlock()
        if not self.scanner.done():
            raise SyntaxException(self.pos(), Token("EOF"), self.curr())
        prog = NodeProg(block)
        return prog

    def parse(self, program):
        """ generated source for method parse """
        self.scanner = Scanner(program)
        self.scanner.next()
        return self.parseProg()
    
    def parseFuncDecl(self):
        self.match("def")
        id = self.curr()
        if id.lex() in self.built_ins:
            raise SyntaxException(self.pos(), "is built in func", self.curr())
        self.match("id")
        self.match("(")
        param = self.curr()
        self.match("id")
        self.match(")")
        self.match("=")
        expr = self.parseExpr()
        func_decl = NodeFuncDecl(id.lex(), param.lex(), expr)
        return func_decl