package kuplrg

object Implementation extends Template {

  import Expr.*
  import Value.*

  // ---------------------------------------------------------------------------
  // Problem #1
  // ---------------------------------------------------------------------------
  def interp(expr: Expr, env: Env): Value = expr match
    case ENum(number) => NumV(number)
    case EBool(bool) => BoolV(bool)
    case EId(name) => env.getOrElse(name, error("free identifier"))
    case EAdd(left, right) =>
      (interp(left, env), interp(right, env)) match
        case (NumV(l), NumV(r)) => NumV(l + r)
        case v => error("invalid operation")
    case EMul(left, right) =>
      (interp(left, env), interp(right, env)) match
        case (NumV(l), NumV(r)) => NumV(l * r)
        case v => error("invalid operation")
    case EDiv(left, right) =>
      (interp(left, env), interp(right, env)) match
        case (NumV(l), NumV(r)) => 
          (NumV(l), NumV(r)) match
          case (NumV(l), NumV(0)) => error("invalid operation")
          case v => NumV(l / r)
        case v => error("invalid operation")
    case EMod(left, right) =>
      (interp(left, env), interp(right, env)) match
        case (NumV(l), NumV(r)) => 
          (NumV(l), NumV(r)) match
          case (NumV(l), NumV(0)) => error("invalid operation")
          case v => NumV(l % r)
        case v => error("invalid operation")
    case EEq(left, right) => 
      val leftValue = interp(left, env)
      val rightValue = interp(right, env)
      BoolV(eq(leftValue, rightValue))
    case ELt(left, right) => 
      (interp(left, env), interp(right, env)) match
        case (NumV(l), NumV(r)) => BoolV(l < r)
        case v => error("invalid operation")
    case EIf(cond, thenExpr, elseExpr) =>
      interp(cond, env) match 
        case BoolV(true) => interp(thenExpr, env)
        case BoolV(false) => interp(elseExpr, env)
        case v => error("not a boolean")
    case ENil => NilV
    case ECons(head, tail) => 
      val tail_list = interp(tail, env)
      tail_list match
        case NilV => ConsV(interp(head, env), tail_list)
        case ConsV(_, _) => ConsV(interp(head, env), tail_list)
        case _ => error("not a list")
    case EHead(list) => 
      interp(list, env) match
        case ConsV(head, _) => head
        case NilV => error("empty list")
        case _ => error("not a list")
    case ETail(list) => 
      interp(list, env) match
        case ConsV(_, tail) => tail
        case NilV => error("empty list")
        case _ => error("not a list")
    case EMap(list, fun) =>                            
      interp(list, env) match
        case NilV => NilV                                 
        case ConsV(_, _) => map(interp(list, env), interp(fun, env))
        case _ => error("not a list")            
    case EFlatMap(list, fun) =>
      interp(list, env) match
        case NilV => NilV                    
        case ConsV(_, _) => join(map(interp(list, env), interp(fun, env))) 
        case _ => error("not a list")
    case EFilter(list, fun) =>
      interp(list, env) match
        case NilV => NilV                                  
        case ConsV(_, _) => filter(interp(list, env), interp(fun, env))
        case _ => error("not a list")          
    case EFoldLeft(list, init, fun) =>                   
      interp(list, env) match
        case NilV => interp(init, env)                          
        case ConsV(_, _) => foldLeft(interp(list, env), interp(init, env), interp(fun, env)) 
        case _ => error("not a list")         
    case ETuple(exprs) => TupleV(exprs.map(interp(_, env)))
    case EProj(tuple, index) =>
      interp(tuple, env) match
        case TupleV(values) =>
          if (index <= values.length) values(index-1) 
          else error("out of bounds")
        case _ => error("not a tuple")
    case EVal(name, value, scope) =>
      val newEnv = env + (name -> interp(value, env))
      interp(scope, newEnv)
    case EFun(params, body) => CloV(params, body, () => env)
    case ERec(defs, scope) =>
      lazy val newEnv: Env = env ++ defs.map((defn => defn.name -> CloV(defn.params, defn.body, () => newEnv)))
      interp(scope, newEnv)
    case EApp(fun, args) =>
      val funcV = interp(fun, env)
      val argV = args.map(interp(_, env))
      app(funcV, argV)

  def eq(left: Value, right: Value): Boolean = (left, right) match
    case (NumV(l), NumV(r)) => l == r
    case (BoolV(l), BoolV(r)) => l == r
    case (NilV, NilV) => true
    case (ConsV(lHead, lTail), ConsV(rHead, rTail)) => eq(lHead, rHead) && eq(lTail, rTail)
    case _ => false

  def map(list: Value, func: Value): Value = (list, func) match
    case (NilV, _) => NilV
    case (ConsV(head, tail), CloV(params, body, fenv)) =>
      val newHead = app(func, List(head))
      ConsV(newHead, map(tail, func))
    case _ => error("not a function")

  def join(list: Value): Value = list match
    case NilV => NilV
    case ConsV(ConsV(head, tail), rest) => ConsV(head, join(ConsV(tail, rest)))
    case ConsV(NilV, rest) => join(rest)
    case _ => error("not a list")

  def filter(list: Value, func: Value): Value = (list, func) match
    case (NilV, _) => NilV
    case (ConsV(head, tail), CloV(params, body, fenv)) =>
      app(func, List(head)) match
        case BoolV(true) => ConsV(head, filter(tail, func))
        case BoolV(false) => filter(tail, func)
        case _ => error("not a boolean")
    case _ => error("not a function")

  def foldLeft(list: Value, init: Value, func: Value): Value = (list, func) match 
    case (NilV, _) => init
    case (ConsV(head, tail), CloV(params, body, fenv)) =>
      val newInit = app(func, List(init, head))
      foldLeft(tail, newInit, func)
    case _ => error("not a function")

  def app(func: Value, args: List[Value]): Value = func match
    case CloV(params, body, fenv) =>
      if (params.length != args.length) error("arity mismatch")
      else
        val newEnv = fenv() ++ params.zip(args)
        interp(body, newEnv)
    case _ => error("not a function")

  // ---------------------------------------------------------------------------
  // Problem #2
  // ---------------------------------------------------------------------------
  def subExpr1: String = "x <- lists.flatMap(y => y.filter(pred));"

  def subExpr2: String = "x * x"
}
