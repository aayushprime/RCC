;;; if, multiline if, switch case, if else ladder

(setq *print-case* :capitalize)



(defvar *age* 18);

;;; < > <= >=
(if (> *age* 18); if condition
    (print "You are an adult")
    (print "You are not an adult"))

(if ( not (> *age* 18)); notice how to use "not" here
    (print "You are an adult")
    (print "You are not an adult"))

;;; or is also similar
(if (and (<= *age* 14) (>= *age* 18)); notice how to use "and" here
    (print "You are an adult")
    (print "You are not an adult"))

(defvar num 2)
(if (= num 2)
    (progn 
        (setf num 3)
        (print num)
        (setf num 4)
        (print num))
    (print "num is not 2"))

(defvar age 5)

(defun get-school (age)
    (case age
        (5 (print "KG"))
        (6 (print "First grade"))
        (otherwise (print "Other grades"))))

(terpri) ; print a new line

(defvar age 5)
;;; multiple statements when condition is true/false
(when (> age 4) ; if true then run
    (print "When")
    (print "You are in school"))

(unless (= age 4) ; if false then run
    (print "unless")
    (print "second"))

;;; if else if else
(cond ((> age 18)  ; if 
            (print "ready") 
            (print "ready again"))
        ((< age 15) ; else if 
            (print "not ready") 
            (print "not ready again"))
        ((< age 18) ; else if
            (print "not ready part 3") 
            (print "not ready part 3"))
        (t (print "default"))) ; else
