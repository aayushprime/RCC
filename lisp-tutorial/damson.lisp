;;;; looping
(setq *print-case* :capitalize)

;;; for loop
(loop for x from 1 to 10
    do (print x))

;;; do while loop
(setq x 1)

(loop (format t "~d ~%" x)
    (setq x (+ x 1))
    (when (> x 10) (return x)))

(loop for x in '(Peter Paul Mary)
    do (format t "~a ~%" x))

(loop for y from 100 to 110 do (format t "~d ~%" y))

(dotimes (y 12) (print y))

(cons 'superman 'batman)
(list 'superman 'batman 'flash)
(cons 'aquaman '(superman batman flash))

(car '(superman batman flash)) ; superman
(cdr '(superman batman flash)) ; (batman flash)

;;; we can use cadddr to get the fourth element of the list only 3 deep

(listp '(superman batman flash)) ; t : check if it is a list which it is

(member 3 '(2 4 5)); nil : check if it is a member of the list

(append '(just) '(another) '(list)) ; (just another list)

(nth 2 '(superman batman flash)) ; flash : get the nth element of the list

(push 1 '(2 3 4)) ; (1 2 3 4) : add to the front of the list


;;; :name and :superpower are just symbols like "peter parker" and "spiderman"
;;; so the following list is a list of 4 symbols
(defvar spiderman (list :name "Peter Parker" :superpower "spider-sense"))

;;; (getf spiderman :name) returns "Peter Parker"; can be read as get following element
;;; nil if not found

(defvar heros nil)
(push spiderman heros)


(dolist (hero heros) 
  (format t "~{ ~a : ~a ~} ~%" hero)) ; format magic ~{ and ~} are used to surround the fields ~a to insert key values

