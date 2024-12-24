package kuplrg

object Implementation extends Template {

  // ---------------------------------------------------------------------------
  // Basic Data Types
  // ---------------------------------------------------------------------------
  def isEvenPair(x: Int, y: Int): Boolean = {
    if (x < -1000 || x > 1000 || y < -1000 || y > 1000) {
      false  // 범위를 벗어나면 false 반환
    } else {
      (x + y) % 2 == 0  // 짝수이면 true, 홀수이면 false
    }
  }

  def validString(str: String, lower: Int, upper: Int): Boolean = {
    if(str.length >= lower && str.length <= upper) true
    else false
  }
  // ---------------------------------------------------------------------------
  // Functions
  // ---------------------------------------------------------------------------
  def factorial(n: Int): Int = {
    if (n < 0 || n > 10) 0  // 범위 밖이면 0 반환
    else if (n == 0) 1  // 0! = 1
    else (1 to n).product  // 팩토리얼 계산
  }

  def magic(x: Int): Int => Int = {
    if (x < 2 || x > 10) { 
      y => 0  // x가 범위를 벗어나면 기본값 0을 반환
    } else {
      y =>
        if (y % x == 0) y / x  // y가 x로 나누어떨어지면 y / x 반환
        else (x + 1) * y + (x - y % x)  // 그렇지 않으면 지정된 연산 수행
    }
  }

  def applyK(f: Int => Int, k: Int): Int => Int = {
    y =>
      def loop(n: Int, current: Int): Int = {
        if (n == 0) current
        else loop(n - 1, f(current))  // 재귀적으로 f를 k번 적용
      }
      loop(k, y)
  }

  // ---------------------------------------------------------------------------
  // Collections
  // ---------------------------------------------------------------------------
  def productPos(l: List[Int]): Int = {
    val positives = l.filter(_ > 0)
    if (positives.isEmpty) 1
    else positives.product
  }

  def merge(l: List[Int]): List[Int] = l match {
    case Nil => Nil
    case x :: Nil => List(x)
    case x :: y :: tail => (x + y) :: merge(tail)
  }

  def generate(init: Int, f: Int => Int, n: Int): List[Int] = {
    def loop(count: Int, current: Int): List[Int] = {
      if (count == 0) Nil
      else current :: loop(count - 1, f(current))  // 재귀적으로 리스트를 생성
    }
    loop(n, init)
  }

  def incKey(map: Map[String, Int], key: String): Map[String, Int] = {
    map.get(key) match {
      case Some(value) => map + (key -> (value + 1))  // key가 존재하면 값을 1 증가시킴
      case None => map  // key가 없으면 원래 map 반환
    }
  }

  def validSums(
    l: List[Int],
    r: List[Int],
    f: (Int, Int) => Boolean,
  ): Set[Int] = {
    for {
      x <- l
      y <- r
      if f(x, y)  // f(x, y)가 true인 경우
    } yield x + y
  }.toSet

  // ---------------------------------------------------------------------------
  // Trees
  // ---------------------------------------------------------------------------
  import Tree.*

  def count(t: Tree, x: Int): Int = t match {
    case Leaf(value) => if (value == x) 1 else 0
    case Branch(left, value, right) => (if (value == x) 1 else 0) + count(left, x) + count(right, x)
  }

  def heightOf(t: Tree): Int = t match {
    case Leaf(_) => 0
    case Branch(left, _, right) => 1 + math.max(heightOf(left), heightOf(right))
  }

  def min(t: Tree): Int = t match {
    case Leaf(value) => value
    case Branch(left, value, right) => math.min(value, math.min(min(left), min(right)))
  }

  def sumLeaves(t: Tree): Int = t match {
    case Leaf(value) => value
    case Branch(left, _, right) => sumLeaves(left) + sumLeaves(right)
  }

  def inorder(t: Tree): List[Int] = t match {
    case Leaf(value) => List(value)
    case Branch(left, value, right) => inorder(left) ++ List(value) ++ inorder(right)
  }

  // ---------------------------------------------------------------------------
  // Boolean Expressions
  // ---------------------------------------------------------------------------
  import BE.*

  def isLiteral(expr: BE): Boolean = expr match {
    case Literal(_) => true
    case _ => false
  }

  def countImply(expr: BE): Int = expr match {
    case Imply(left, right) => 1 + countImply(left) + countImply(right)
    case And(left, right) => countImply(left) + countImply(right)
    case Or(left, right) => countImply(left) + countImply(right)
    case Not(e) => countImply(e)
    case Literal(_) => 0
  }

  def literals(expr: BE): List[Boolean] = expr match {
    case Literal(value) => List(value)
    case And(left, right) => literals(left) ++ literals(right)
    case Or(left, right) => literals(left) ++ literals(right)
    case Imply(left, right) => literals(left) ++ literals(right)
    case Not(e) => literals(e)
  }

  def getString(expr: BE): String = expr match {
    case Literal(true) => "#t"
    case Literal(false) => "#f"
    case And(left, right) => s"(${getString(left)} & ${getString(right)})"
    case Or(left, right) => s"(${getString(left)} | ${getString(right)})"
    case Imply(left, right) => s"(${getString(left)} => ${getString(right)})"
    case Not(e) => s"!${getString(e)}"
  }

  def eval(expr: BE): Boolean = expr match {
    case Literal(value) => value
    case And(left, right) => eval(left) && eval(right)
    case Or(left, right) => eval(left) || eval(right)
    case Imply(left, right) => !eval(left) || eval(right)  // A => B 는 !A | B와 동일
    case Not(e) => !eval(e)
  }
}
