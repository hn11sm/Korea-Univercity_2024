package kuplrg

object Implementation extends Template {

  import Expr.*
  import RecDef.*
  import Value.*
  import Type.*
  import TypeInfo.*

  //typechecker
  def typeCheck(expr: Expr, tenv: TypeEnv): Type = expr match
    case EUnit => UnitT
    case ENum(number) => NumT
    case EBool(bool) => BoolT
    case EStr(string) => StrT
    case EId(name) => tenv.vars.getOrElse(name, error(s"$name is not found"))
    case EAdd(left, right) => 
      val lty = typeCheck(left, tenv)
      val rty = typeCheck(right, tenv)
      (lty, rty) match
        case (NumT, NumT) => NumT
        case _ => error(s"$lty, $rty")
    case EMul(left, right) =>
      val lty = typeCheck(left, tenv)
      val rty = typeCheck(right, tenv)
      (lty, rty) match
        case (NumT, NumT) => NumT
        case _ => error(s"$lty, $rty")
    case EDiv(left, right) =>
      val lty = typeCheck(left, tenv)
      val rty = typeCheck(right, tenv)
      (lty, rty) match
        case (NumT, NumT) => NumT
        case _ => error(s"$lty, $rty")
    case EMod(left, right) =>
      val lty = typeCheck(left, tenv)
      val rty = typeCheck(right, tenv)
      (lty, rty) match
        case (NumT, NumT) => NumT
        case _ => error(s"$lty, $rty")
    case EConcat(left, right) => 
      val lty = typeCheck(left, tenv)
      val rty = typeCheck(right, tenv)
      (lty, rty) match
        case (StrT, StrT) => StrT
        case _ => error(s"$lty, $rty")
    case EEq(left, right) => 
      val lty = typeCheck(left, tenv)
      val rty = typeCheck(right, tenv)
      mustSame(lty, rty)
      BoolT
    case ELt(left, right) => 
      val lty = typeCheck(left, tenv)
      val rty = typeCheck(right, tenv)
      (lty, rty) match
        case (NumT, NumT) => BoolT
        case _ => error(s"$lty, $rty")
    case ESeq(left, right) => 
      val _ = typeCheck(left, tenv)
      val rty = typeCheck(right, tenv)
      rty
    case EIf(cond, thenExpr, elseExpr) =>
      val cty = typeCheck(cond, tenv)
      val tty = typeCheck(thenExpr, tenv)
      val ety = typeCheck(elseExpr, tenv)
      cty match
        case BoolT =>
          mustSame(tty, ety)
          tty
        case _ => error("")
    case EVal(x, tyOpt, expr, body) => tyOpt match
      case Some(ty) =>
        val exty = typeCheck(expr, tenv)
        mustSame(ty, exty)
        typeCheck(body, tenv.addVar(x -> ty))
      case None => 
        val exty = typeCheck(expr, tenv)
        typeCheck(body, tenv.addVar(x -> exty))
    case EFun(params, body) =>
      val ptys = params.map(_.ty)
      for (pty <- ptys) mustValid(pty, tenv)
      val rty = typeCheck(body, tenv.addVars(params.map(p => p.name -> p.ty)))
      ArrowT(Nil, ptys, rty)
    case EApp(fun, tys, args) =>
      for (ty <- tys) {
        mustValid(ty, tenv)
      }
      typeCheck(fun, tenv) match
        case ArrowT(tvars, paramTys, retTy) =>
          if (paramTys.length != args.length) error("arity mismatch")
          (paramTys zip args).map((paramTy, arg) => mustSame(typeCheck(arg, tenv), subst(paramTy, tvars, tys)))
          subst(retTy, tvars, tys)
        case _ =>
          error(s"not a function type: $fun")
    case ERecDefs(defs, body) =>
      val finalEnv = defs.foldLeft(tenv) { (currentEnv, defItem) =>
        updateTypeEnv(defItem, currentEnv) 
      }
      RDefTypeCheck(defs, finalEnv)
      val bty = typeCheck(body, finalEnv)
      mustValid(bty, tenv)
      bty
    case EMatch(expr, cases) => typeCheck(expr, tenv) match
      case IdT(t, types) =>
        tenv.tys.getOrElse(t, error(s"unknown type: $t")) match {
          case TIAdt(tvars, variants) =>
            if (types.length != tvars.length) error("arity mismatch")
            mustValidMatch(t, cases, variants)
            val tys = for (MatchCase(x, ps, b) <- cases)
              yield 
                val tmaps = variants(x).map(ps => ps.ty)
                val substys = tmaps.map(ty => subst(ty, tvars, types))
                typeCheck(b, tenv.addVars((ps zip substys)))
            tys.reduce((lty, rty) => { mustSame(lty, rty); lty })
          case _ => error(s"not a variant")
        }
      case _ => error(s"not a variant")
    case EExit(ty, e) =>
      mustValid(ty, tenv)
      val eTy = typeCheck(e, tenv)
      if (eTy == StrT) ty
      else error(s"$ty")
      
  //interpreter
  def interp(expr: Expr, env: Env): Value = expr match
    case EUnit => UnitV
    case ENum(number) => NumV(number)
    case EBool(bool) => BoolV(bool)
    case EId(name) => 
      val Idv = env.getOrElse(name, error(s"$env, $name"))
      Idv match
        case ExprV(e, lenv) => interp(e,lenv())
        case v => Idv
    case EStr(string) => StrV(string)
    case EAdd(left, right) =>
      val lval = interp(left, env)
      val rval = interp(right, env)
      (lval, rval) match {
        case (NumV(l), NumV(r)) => NumV(l + r)
        case _ => error(s"Type mismatch in addition")
      }
    case EMul(left, right) =>
      val lval = interp(left, env)
      val rval = interp(right, env)
      (lval, rval) match {
        case (NumV(l), NumV(r)) => NumV(l * r)
        case _ => error("Type mismatch in multiplication")
      }
    case EDiv(left, right) =>
      val lval = interp(left, env)
      val rval = interp(right, env)
      (lval, rval) match {
        case (NumV(l), NumV(r)) if r != 0 => NumV(l / r)
        case (NumV(_), NumV(0)) => error("Division by zero")
        case _ => error("Type mismatch in division")
      }
    case EMod(left, right) =>
      val lval = interp(left, env)
      val rval = interp(right, env)
      (lval, rval) match {
        case (NumV(l), NumV(r)) if r != 0 => NumV(l % r)
        case (NumV(_), NumV(0)) => error("Modulo by zero")
        case _ => error("Type mismatch in modulo")
      }
    case EEq(left, right) =>
      val lval = interp(left, env)
      val rval = interp(right, env)
      BoolV(eq(lval, rval))
    case ELt(left, right) =>
      val lval = interp(left, env)
      val rval = interp(right, env)
      (lval, rval) match {
        case (NumV(l), NumV(r)) => BoolV(l < r)
        case _ => error("Type mismatch in less-than comparison")
      }
    case EConcat(left, right) =>
      val lval = interp(left, env)
      val rval = interp(right, env)
      (lval, rval) match {
        case (StrV(l), StrV(r)) => StrV(l + r)
        case _ => error("Type mismatch in string concatenation")
      }
    case ESeq(left, right) =>
      interp(left, env)
      interp(right, env)
    case EIf(cond, thenExpr, elseExpr) =>
      val cval = interp(cond, env)
      cval match {
        case BoolV(true)  => interp(thenExpr, env)
        case BoolV(false) => interp(elseExpr, env)
        case _ => error("Condition must be boolean")
      }
    case EVal(x, tyOpt, expr, body) =>
      val value = interp(expr, env)
      interp(body, env + (x -> value))
    case EFun(params, body) =>
      CloV(params.map(_.name), body, () => env)
    case EApp(fun, tys, args) =>
      interp(fun, env) match 
        case CloV(params, body, closureEnv) =>
          if (params.length != args.length) error("arity mismatch")
          val argVals = args.map(interp(_, env))
          val newEnv = closureEnv() ++ params.zip(argVals).toMap
          interp(body, newEnv)
        case ConstrV(constructorName) =>
          val argVals = args.map(interp(_, env))
          VariantV(constructorName, argVals)
        case _ =>
          error("not a function")
    case ERecDefs(defs, body) =>
      lazy val finalEnv: Env = defs.foldLeft(env) { (currentEnv, defItem) =>
        updateEnv(defItem, currentEnv, () => finalEnv)
      }
      interp(body, finalEnv)
    case EMatch(expr, cases) =>
      val value = interp(expr, env)
      value match 
        case VariantV(variantName, variantArgs) =>
          val matchingCase = cases.find(_.name == variantName).getOrElse {
            error(s"no matching case for variant")
          }
          val caseEnv = env ++ matchingCase.params.zip(variantArgs).toMap
          interp(matchingCase.body, caseEnv)
        case _ =>
          error("match expression must be a variant value")
    case _ => error(s"")

  //helper functions
  def mustSame(l: Type, r: Type): Unit =
    if (!isSame(l, r)) error(s"type $l != $r")

  def isSame(lty: Type, rty: Type): Boolean = (lty, rty) match {
    case (UnitT, UnitT) => true 
    case (NumT, NumT) => true  
    case (BoolT, BoolT) => true 
    case (StrT, StrT) => true  
    case (IdT(tnl, Nil), IdT(tnr, Nil)) => tnl == tnr
    case (IdT(tnl, ltys), IdT(tnr, rtys)) =>
      tnl == tnr && ltys.length == rtys.length && ltys.zip(rtys).forall { case (tyl, tyr) => isSame(tyl, tyr) }
    case (ArrowT(ltns, lpsTy, lretTy), ArrowT(rtns, rpsTy, rretTy)) =>
      if (ltns.length != rtns.length || lpsTy.length != rpsTy.length) false
      else {
        lpsTy.zip(rpsTy).forall {
          case (tyl, tyr) =>
            isSame(tyl, subst(tyr, rtns, ltns.map(rtn => IdT(rtn, Nil))))
        }
        isSame(lretTy, subst(rretTy, rtns, ltns.map(rtn => IdT(rtn, Nil))))
      }

    case _ => false 
  }

  def subst(bodyTy: Type, names: List[String], tys: List[Type]): Type = bodyTy match {
    
    case UnitT => UnitT
    case NumT => NumT
    case BoolT => BoolT
    case StrT => StrT
    case IdT(x, Nil) =>
      names.zip(tys).find(_._1 == x).map(_._2).getOrElse(IdT(x, Nil))
    case IdT(x, typeArgs) =>
      val substitutedArgs = typeArgs.map(arg => subst(arg, names, tys))
      IdT(x, substitutedArgs)
    case ArrowT(tvars, paramTys, retTy) =>
      val (filteredNames, filteredTys) = names.zip(tys).filterNot { case (name, _) => tvars.contains(name) }.unzip
      val substitutedParams = paramTys.map(param => subst(param, filteredNames, filteredTys))
      val substitutedRet = subst(retTy, filteredNames, filteredTys)
      ArrowT(tvars, substitutedParams, substitutedRet)
  }
      
  def mustValid(ty: Type, tenv: TypeEnv): Type = ty match {
    case UnitT => UnitT
    case NumT => NumT
    case BoolT => BoolT
    case StrT => StrT
    case IdT(name, tys) =>
      val typeInfo = tenv.tys.getOrElse(name, error(s"unknown type: $name"))
      typeInfo match {
        case TIAdt(tvars, _) =>
          for (ty <- tys) mustValid(ty, tenv)
          IdT(name, tys)
        case TIVar => IdT(name, tys)
      }
    case ArrowT(tvars, paramTys, retTy) =>
      val extendedTenv = tenv.addTypeVars(tvars)
      paramTys.foreach(mustValid(_, extendedTenv))
      mustValid(retTy, extendedTenv)
      ArrowT(tvars, paramTys, retTy)
  }

  def RDefTypeCheck(defs: List[RecDef], tenv: TypeEnv): Unit = 
    for(df <- defs) yield
      df match {
        case LazyVal(name, ty, init) =>
          mustValid(ty, tenv)
          val ity = typeCheck(init, tenv)
          mustSame(ty, ity)
        case RecFun(name, tvars, params, rty, body) => 
          for(tvar <- tvars) if (tenv.tys.contains(tvar)) error("already contain variant")
          val ptys = params.map(_.ty)
          val newTypeEnv = tenv.addTypeVars(tvars)
          for(pty <- ptys) mustValid(pty, newTypeEnv)
          mustValid(rty, newTypeEnv)
          val bty = typeCheck(body, newTypeEnv.addVars(params.map(p => p.name -> p.ty)))
          mustSame(rty, bty)
        case TypeDef(name, tvars, varts) => 
          for(tvar <- tvars) yield if (tenv.tys.contains(tvar)) error("")
          val newTypeEnv = tenv.addTypeVars(tvars)
          for (vart <- varts; pty <- vart.params.map(ps => ps.ty)) mustValid(pty, newTypeEnv)
        }
  
  def updateTypeEnv(defs: RecDef, tenv: TypeEnv): TypeEnv = {
    defs match {
      case LazyVal(name, ty, init) =>
        tenv.addVar(name -> ty)
      case RecFun(name, tvars, params, rty, body) =>
        tenv.addVar(name -> ArrowT(tvars, params.map(_.ty), rty))
      case TypeDef(name, tvars, varts) =>
        if (tenv.tys.contains(name)) error(s"already defined type")
        val newTypeEnv = tenv.addTypeName(name, tvars, varts)
        newTypeEnv.addVars(varts.map(vart => vart.name -> ArrowT(tvars, vart.params.map(ps => ps.ty), IdT(name, tvars.map(tvar => IdT(tvar, Nil))))))
    }
  }

  def updateEnv(defs: RecDef, currentEnv: Env, finalEnv: () => Env): Env = defs match
      case LazyVal(name, ty, init) =>
        currentEnv + (name -> ExprV(init, () => finalEnv()))
      case RecFun(name, tvars, params, rty, body) =>
        currentEnv + (name -> CloV(params.map(_.name), body, () => finalEnv()))
      case TypeDef(name, tvars, varts) =>
        varts.foldLeft(currentEnv) { (updatedEnv, vart) =>
          updatedEnv + (vart.name -> ConstrV(vart.name))
        }

  def mustValidMatch(t:String, cs: List[MatchCase], tmap: Map[String, List[Param]]): Unit =
    val xs = cs.map(_.name)
    val ys = tmap.keySet
    for (x <- xs if xs.count(_ == x)>1) error(s"duplicate case $x for $t")
    for (x <- xs if !ys.contains(x)) error(s"unknown case $x for $t")
    for (y <- ys if !xs.contains(y)) error(s"missing case $y for $t")
    for {
      MatchCase(x, ps, _) <- cs
      n = tmap(x).size
      m = ps.size
      if n != m
    } error(s"arity mismatch ($n != $m) in case $x for $t")
  
  def eq(value1: Value, value2: Value): Boolean = (value1, value2) match {
    case (UnitV, UnitV) => true
    case (NumV(n1), NumV(n2)) => n1 == n2
    case (BoolV(b1), BoolV(b2)) => b1 == b2
    case (StrV(s1), StrV(s2)) => s1 == s2
    case (VariantV(name1, values1), VariantV(name2, values2)) =>
      name1 == name2 && values1.zip(values2).forall { case (v1, v2) => eq(v1, v2) }
    case _ => false
  }
}


        


    
