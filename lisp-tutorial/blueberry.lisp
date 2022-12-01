;;;; formatting and function calls

(setq *print-case* :capitalize)

(+ 5 4); how to call a function
;;; this is equal to [+] [5] [4] [nil]
;;; list is a chain of atoms with nil at end

(defvar *number* 0) ; define a variable
(setf *number* 5) ; change a variable

(format t "Number with commas ~:d" 1000000) ; puts commas around numbers
;;; t means go to console, nil means go to string

(format t "~5f" 3.141593); show only 5 characters
(format t "~,4f" 3.141593); No of decimals (4 chars after comma)
(format t "~,,2f" 10); percent
(format t "~$" 10); dollar format

;;; + - / * are functions
(rem 5 4) ; remainder
(mod 5 4) ; mod

;;; ' means quote take the literal value (not as code)
(eq 'dog 'dog) ; true
(eq 'dog 'cat) ; false

;;; sqrt log exp (e to the power) expt (exponentiation 2^3=8)
;;; ceiling max min oddp (check if it is odd) evenp (check if it is even)
;;; numberp (check value is a number?)
;;; (null value) check if value is null/nil
;;; sin cos tan asin acos atan are available

(defparameter *name* 'Aayush)

(format t "(eq *name 'Aayush) = ~a" (eq *name* 'Aayush)) ; true

;;; equal  check for symbols ('aayush), numbers, floats, strings, 
;;; equality checks for case (lower or upper)
;;; (equalp 1.0 1) ; true equalp ignores case also in case of strings
