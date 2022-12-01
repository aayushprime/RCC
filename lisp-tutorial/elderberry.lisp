;;; 
(setq *print-case* :capitalize)

(defparameter heros '((Superman (Clark kent))
                      (Flash (Barry Allen))
                      (Batman (Bruce Wayne))))

(print heros)
;;; association lists
;;; get superman data from the list heros
(format t "Superman Data ~a ~%" (assoc 'Superman heros)) ; => (SUPERMAN (CLARK KENT))

;;; optional parameters: make c and d optional parameters (like python kwargs)
(defun my-function (a b &optional c d)
  (format t "a: ~a b: ~a c: ~a d:~a ~%" a b c d))

(my-function 1 2 3); => a: 1 b: 2 c: 3 d: NIL

(defparameter total 0)
;;; receive multiple values, &rest is like python *args
(defun sum (&rest nums)
  (dolist (num nums) (set total (+ total num)))
  (format t "SUM: ~a ~%" total))

(sum 1 2 3) ; 6

;;; &key for keyword arguments
(defun print-list (&optional &key x y z)
  (format t "List: ~a ~%" (list x y z)))

(print-list :x 1 :y 2 :z 3)

;;; returning from function
(defun function_name (params)
  (return-from function_name params)) ; identity function return its parameters

;;; format strings/template literals like python and js example
(defparameter heros '((Superman (Clark kent))
                      (Flash (Barry Allen))
                      (Batman (Bruce Wayne))))


;;; backtick (`) means quasiquote comma (,) means unquote
(defun get-hero-data (heros)
  (format t "~a" `(,(caar heros) part of string ,(cdar heros))))

(get-hero-data heros) ; Superman part of string ((Clark Kent))

;;; map function
(print (mapcar #'numberp (list 1 2 3 'f 'g)) ); => (T T T F F)