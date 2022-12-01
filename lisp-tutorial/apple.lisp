;;;; Main file comment

;;; comment block: Notes from lisp tutorial video : https://www.youtube.com/watch?v=ymSq4wHrqyU

(+ 
2 ; comment after code (inline)
;; full line comment in between code
3)

#|| 
multiline comment
||#


(format t "Hello World ~% On a new line") ; print to console ~% is newline
(print "What's your name?") ; print to console

(defvar *testvar* "aayush") ; define a global variable, * is optional
(defvar *name* (read)) ; read from console: (read)

(print *name*)

(defun hello-you (*name*) ; create function
    (format t "Hello ~a ~%" *name*) ; format string ~% is new line
 ) 

;;; ~a: show value as is
;;; ~s: show value as string (in quotes)
;;; ~10a: 10 spaces, extra right padded with spaces
;;; ~10@a: 10 spaces, extra left padded with spaces


(hello-you "aayush") ; call function

;;; set variable to :capitalize (prints in caps by default, dont do that)
(setq *print-case* :capitalize) ; :upcase :downcase :capitalize :preserve (alternatives)

(hello-you *name*) ; call function

