file://<HOME>/Work/Major/Programing%20Language/Assignments/assignment1/src/main/scala/kuplrg/Implementation.scala
### java.lang.AssertionError: NoDenotation.owner

occurred in the presentation compiler.

presentation compiler configuration:
Scala version: 3.3.3
Classpath:
<HOME>/Library/Caches/Coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala3-library_3/3.3.3/scala3-library_3-3.3.3.jar [exists ], <HOME>/Library/Caches/Coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.13.12/scala-library-2.13.12.jar [exists ]
Options:



action parameters:
offset: 1399
uri: file://<HOME>/Work/Major/Programing%20Language/Assignments/assignment1/src/main/scala/kuplrg/Implementation.scala
text:
```scala
package kuplrg

object Implementation extends Template {

  // ---------------------------------------------------------------------------
  // Basic Data Types
  // ---------------------------------------------------------------------------
  def isEvenPair(x: Int, y: Int): Boolean = {
    if ((x + y) % 2 == 0) true 
    else false
  }

  def validString(str: String, lower: Int, upper: Int): Boolean = {
    if(str.length >= lower && str.length <= upper) true
    else false
  }
  // ---------------------------------------------------------------------------
  // Functions
  // ---------------------------------------------------------------------------
  def factorial(n: Int): Int = {
    if(n == 0) 1 
    else n * factorial(n - 1)
  }

  def magic(x: Int): Int => Int = {
    y =>
      if(y % x == 0) y / x
      else (x + 1) * y + (x - y % x)
  }

  def applyK(f: Int => Int, k: Int): Int => Int = {
    y =>
      var result = y
      for (i <- 1 to k) {
        result = f(result)
      }
      result
  }

  // ---------------------------------------------------------------------------
  // Collections
  // ---------------------------------------------------------------------------
  def productPos(l: List[Int]): Int = {
    val positives = l.filter(_ > 0)
    if (positives.isEmpty) 1
    else positives.product
  }

  def merge(l: List[Int]): List[Int] = {
    val result: list[@@]
    if (l.isEmpty) 
  }

  def generate(init: Int, f: Int => Int, n: Int): List[Int] = ???

  def incKey(map: Map[String, Int], key: String): Map[String, Int] = ???

  def validSums(
    l: List[Int],
    r: List[Int],
    f: (Int, Int) => Boolean,
  ): Set[Int] = ???

  // ---------------------------------------------------------------------------
  // Trees
  // ---------------------------------------------------------------------------
  import Tree.*

  def count(t: Tree, x: Int): Int = ???

  def heightOf(t: Tree): Int = ???

  def min(t: Tree): Int = ???

  def sumLeaves(t: Tree): Int = ???

  def inorder(t: Tree): List[Int] = ???

  // ---------------------------------------------------------------------------
  // Boolean Expressions
  // ---------------------------------------------------------------------------
  import BE.*

  def isLiteral(expr: BE): Boolean = ???

  def countImply(expr: BE): Int = ???

  def literals(expr: BE): List[Boolean] = ???

  def getString(expr: BE): String = ???

  def eval(expr: BE): Boolean = ???
}

```



#### Error stacktrace:

```
dotty.tools.dotc.core.SymDenotations$NoDenotation$.owner(SymDenotations.scala:2607)
	scala.meta.internal.pc.SignatureHelpProvider$.isValid(SignatureHelpProvider.scala:83)
	scala.meta.internal.pc.SignatureHelpProvider$.notCurrentApply(SignatureHelpProvider.scala:94)
	scala.meta.internal.pc.SignatureHelpProvider$.$anonfun$1(SignatureHelpProvider.scala:48)
	scala.collection.StrictOptimizedLinearSeqOps.dropWhile(LinearSeq.scala:280)
	scala.collection.StrictOptimizedLinearSeqOps.dropWhile$(LinearSeq.scala:278)
	scala.collection.immutable.List.dropWhile(List.scala:79)
	scala.meta.internal.pc.SignatureHelpProvider$.signatureHelp(SignatureHelpProvider.scala:48)
	scala.meta.internal.pc.ScalaPresentationCompiler.signatureHelp$$anonfun$1(ScalaPresentationCompiler.scala:435)
```
#### Short summary: 

java.lang.AssertionError: NoDenotation.owner