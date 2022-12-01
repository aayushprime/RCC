; (operator operand1 operand2)
(+ 2 4)

; define a variable
(define foo 3)

; use variable
(+ foo 4)

; define a function; notice the brackets in the first argument of define
(define (square x) (* x x))

; use function
(square 3)

; if statement: if (condition) (then) (else)
(define (abs x) (if (< x 0) (-x) x))

abs(3) ; 3

; list 
(list 1 2 3)

(sort (list 1 2 3) <)

(length (list 1 2 3))

; Scheme is weird.
; = Building lists from pairs
; = Recursion for everything
; = Passing functions into functions
; = Data/code duality

(define x (list 1 2 4))
(car x) ; 1
(cdr x) ; (2 4) : list of remaining elements
(cons "a" "b"); ("a"."b") : make a pair of "a" and "b"
(define p (cons "a" "b"))
(cdr p) ; "b" : note not a list of remaining things but just 2nd element

null; () : empty list
(cons 2 null); (2) : list with one element

; list are chain of pairs with last element being null
; (1 2 3) = (1 . (2 . (3 . null)))
