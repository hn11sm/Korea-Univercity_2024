package kuplrg

object Implementation extends Template {

  import Expr.*
  import Value.*
  import Inst.*
  import Control.*

  // ---------------------------------------------------------------------------
  // Problem #1
  // ---------------------------------------------------------------------------
  def reduce(st: State): State =
    val State(k, s, h, mem) = st
    k match
      case Nil => st
      case inst :: rest => 
        inst match
          case IEval(env, expr) =>
            expr match
              case EUndef => State(rest, UndefV :: s, h, mem)
              case ENum(number) => State(rest, NumV(number) :: s, h, mem)
              case EBool(bool) => State(rest, BoolV(bool) :: s, h, mem)

              case EAdd(left, right) => State(IEval(env, left) :: IEval(env, right) :: IAdd :: rest, s, h, mem)
              case EMul(left, right) => State(IEval(env, left) :: IEval(env, right) :: IMul :: rest, s, h, mem)
              case EDiv(left, right) => State(IEval(env, left) :: IEval(env, right) :: IDiv :: rest, s, h, mem)
              case EMod(left, right) => State(IEval(env, left) :: IEval(env, right) :: IMod :: rest, s, h, mem)

              case EEq(left, right) => State(IEval(env, left) :: IEval(env, right) :: IEq :: rest, s, h, mem)
              case ELt(left, right) => State(IEval(env, left) :: IEval(env, right) :: ILt :: rest, s, h, mem)

              case EVar(name, init, body) => State(IEval(env, init) :: IDef(List(name), env, body) :: rest, s, h, mem)

              case EId(name) => 
                val addr = lookup(env, name)
                val value = mem.getOrElse(addr, error(s"Memory access error: Address($addr) was not found"))
                State(rest, value :: s, h, mem)

              case EAssign(name, expr) =>
                val addr = lookup(env, name)
                State(IEval(env, expr) :: IWrite(addr) :: rest, s, h, mem)
              case ESeq(left, right) => State(IEval(env, left) :: IPop :: IEval(env, right) :: rest, s, h, mem)

              case EIf(cond, thenExpr, elseExpr) => State(IEval(env, cond) :: IJmpIf(KValue(IEval(env, thenExpr) :: rest, s, h)) :: IEval(env, elseExpr) :: rest, s, h, mem)
              
              case EWhile(cond, body) =>
                val _break = rest
                val _continue = IPop :: IEval(env, EWhile(cond, body)) :: rest
                val H_body = h + (Control.Continue -> KValue(_continue, s, h)) + (Control.Break -> KValue(_break, s, h))
                val _body = IEval(env, body) :: IJmp(Control.Continue) :: Nil
                State(IEval(env, cond) :: IJmpIf(KValue(_body, s, H_body)) :: rest, UndefV :: s, h, mem)

              case EBreak => State(IJmp(Control.Break) :: Nil, UndefV :: s, h, mem)
              case EContinue => State(IJmp(Control.Continue) :: Nil, UndefV :: s, h, mem)

              case EFun(ps, b) => State(rest, CloV(ps, b, env) :: s, h, mem)
              case EApp(f, es) =>
                val argSize = es.size
                State(IEval(env, f) :: es.map(e => IEval(env, e)) ::: ICall(argSize) :: rest, s, h, mem)
              case EReturn(e) => State(IEval(env, e) :: IReturn :: rest, s, h, mem)

              case ETry(b, x, c) =>
                val _finally = rest
                val _throw = IDef(List(x), env, c) :: rest
                val H_body = h + (Control.Throw -> KValue(_throw, s, h)) + (Control.Finally -> KValue(_finally, s, h))
                State(IEval(env, b) :: IJmp(Control.Finally) :: Nil, s, H_body, mem)

              case EThrow(e) => State(IEval(env, e) :: IJmp(Control.Throw) :: Nil, s, h, mem)

              case EGen(ps, b) => State(rest, GenV(ps, b, env) :: s, h, mem)
              case EIterNext(iter, arg) => arg match
                case None => State(IEval(env, iter) :: IEval(env, EUndef) :: INext :: rest, s, h, mem)
                case Some(arg) => State(IEval(env, iter) :: IEval(env, arg) :: INext :: rest, s, h, mem)
              
              case EYield(e) => 
                val _next = KValue(rest, s, h)
                State(IEval(env, e) :: IYield :: Nil, BoolV(false) :: ContV(_next) :: s, h, mem)

              case EValueField(res) => State(IEval(env, res) :: IValueField :: rest, s, h, mem)
              case EDoneField(res) => State(IEval(env, res) :: IDoneField :: rest, s, h, mem)
              
          case IAdd => s match
            case NumV(b) :: NumV(a) :: tail => State(rest, NumV(a + b) :: tail, h, mem)
            case _ => error("invalid state")
          case IMul => s match
            case NumV(b) :: NumV(a) :: tail => State(rest, NumV(a * b) :: tail, h, mem)
            case _ => error("invalid state")
          case IDiv => s match
            case NumV(b) :: NumV(a) :: tail =>
              if b == 0 then error("invalid state")
              else State(rest, NumV(a / b) :: tail, h, mem)
            case _ => error("invalid state")
          case IMod => s match
            case NumV(b) :: NumV(a) :: tail =>
              if b == 0 then error("invalid state")
              else State(rest, NumV(a % b) :: tail, h, mem)
            case _ => error("invalid state")

          case IEq => s match
            case r :: l :: tail => State(rest, BoolV(eq(l, r)) :: tail, h, mem)
            case _ => error("invalid state")

          case ILt => s match
            case NumV(b) :: NumV(a) :: tail => State(rest, BoolV(a < b) :: tail, h, mem)
            case _ => error("invalid state")
            
          case IDef(xs, env, body) =>         
            val addr = malloc(mem, xs.length)
            val values = s.take(xs.length).reverse
            val newEnv = env ++ xs.zip(addr)
            val newMem = mem ++ addr.zip(values)
            State(IEval(newEnv, body) :: rest, s.drop(xs.length), h, newMem)

          case IWrite(addr) => s match
            case value :: tail => State(rest, value :: tail, h, mem + (addr -> value))
            case _ => error("invalid state")

          case IPop => s match
            case value :: tail => State(rest, tail, h, mem)
            case _ => error("invalid state")

          case IJmpIf(kv) => s match
              case BoolV(true) :: _ => State(kv.cont, kv.stack, kv.handler, mem)
              case BoolV(false) :: tail => State(rest, tail, h, mem)
              case _ => error("invalid state")

          case IJmp(c) => s match
            case value :: _ => 
              val kvalue = lookup(h, c)
              val _H = 
                if (h.contains(Control.Yield)) 
                  kvalue.handler + (Control.Yield -> lookup(h, Control.Yield))
                else 
                  kvalue.handler
              State(kvalue.cont, value :: kvalue.stack, _H, mem)
            case _ => error("invalid state")

          case ICall(argSize) => s.drop(argSize) match
            case CloV(ps, body, fenv) :: tail => 
              val _return = KValue(rest, tail, h)
              val H_body = h + (Control.Return -> _return) - Control.Break - Control.Continue - Control.Yield
              val argCount = Math.min(ps.length, argSize) 
              val args_temp = s.take(argSize).reverse
              val args = args_temp.take(argCount).reverse
              val s_body = List.fill(ps.length - argSize)(UndefV) ++ args ++ Nil
              State(IDef(ps, fenv, EReturn(body)) :: Nil, s_body, H_body, mem)
            case GenV(ps, body, fenv) :: tail =>
              val addr = malloc(mem)
              val argCount = Math.min(ps.length, argSize) 
              val args_temp = s.take(argSize).reverse
              val args = args_temp.take(argCount).reverse
              val s_body = List.fill(ps.length - argSize)(UndefV) ++ args ++ Nil
              lazy val freshIdList: LazyList[String] = LazyList.from(1).map(i => s"anyIdentifier_x$i")
              val xId = freshIdList.head
              val x = EId(xId)
              val k_body = IPop :: IDef(ps, fenv, EReturn(ETry(body, xId, x))) :: Nil
              val emptyH: Handler = Map.empty[Control, KValue]
              val _body = KValue(k_body, s_body, emptyH)
              State(rest, IterV(addr) :: tail, h, mem + (addr -> ContV(_body)))
            case _ => error("invalid state")

          case IReturn => s match
            case value :: tail => 
              val emptyH: Handler = Map.empty[Control, KValue]
              val _done = KValue(IReturn :: Nil, Nil, emptyH)
              if (h.contains(Control.Yield))
                State(IYield :: Nil, value :: BoolV(true) :: ContV(_done) :: tail, h, mem)
              else 
                State(IJmp(Control.Return) :: Nil, value :: Nil, h, mem)
            case _ => error("invalid state")
            
          case INext => s match
            case value :: IterV(addr) :: tail => 
              mem.get(addr) match
                case Some(ContV(KValue(_k, _s, _h))) =>
                  val kvalue = KValue(rest, IterV(addr) :: tail, h)
                  val H_body = _h + (Control.Yield -> kvalue) + (Control.Return -> kvalue)
                  State(_k, value :: _s, H_body, mem)
                case _ => error("invalid state")
            case _ => error("invalid state")

          case IYield => s match
            case value1 :: BoolV(b) :: value2 :: _ => 
              val kvalue = lookup(h, Control.Yield)
              val _k = kvalue.cont
              val _s = kvalue.stack
              val _h = kvalue.handler
              _s match
                case IterV(addr) :: tail =>
                  State(_k, ResultV(value1, b) :: tail, _h, mem + (addr -> value2))
                case _ => error("invalid state")
            case _ => error("invalid state")

          case IValueField => s match
            case ResultV(v, _) :: tail => State(rest, v :: tail, h, mem)
            case _ => error("invalid state")

          case IDoneField => s match
            case ResultV(_, bool) :: tail => State(rest, BoolV(bool) :: tail, h, mem)
            case _ => error("invalid state")

  // ---------------------------------------------------------------------------
  // Problem #2
  // ---------------------------------------------------------------------------
  def bodyOfSquares: String = """
    while (from <= to) {
      yield from * from;
      from += 1;
    }
  """

  // ---------------------------------------------------------------------------
  // Helper functions
  // ---------------------------------------------------------------------------
  def malloc(mem: Mem, n: Int): List[Addr] =
    val a = malloc(mem)
    (0 until n).toList.map(a + _)

  def malloc(mem: Mem): Addr = mem.keySet.maxOption.fold(0)(_ + 1)

  def lookup(env: Env, x: String): Addr =
    env.getOrElse(x, error(s"free identifier: $x"))

  def lookup(handler: Handler, x: Control): KValue =
    handler.getOrElse(x, error(s"invalid control operation: $x"))

  def eq(l: Value, r: Value): Boolean = (l, r) match
    case (UndefV, UndefV)                   => true
    case (NumV(l), NumV(r))                 => l == r
    case (BoolV(l), BoolV(r))               => l == r
    case (IterV(l), IterV(r))               => l == r
    case (ResultV(lv, ld), ResultV(rv, rd)) => eq(lv, rv) && ld == rd
    case _                                  => false
}
