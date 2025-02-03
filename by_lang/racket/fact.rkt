#lang racket

;; A generic factorial implementation. Not sure if it is even worth it
;; placing something like this here.

(define (fact n)
  (if (> n 1)
    (* n (fact (- n 1))) 1))
