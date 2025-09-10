# A Janet equivalent to Scheme's named lets.

(defmacro named-let
  [name bindings & body]

  (if (not (symbol? name))
    (error "expected symbol for loop name in named-let"))

  (if (odd? (length bindings))
    (error "expected even number of bindings to named-let"))

  (def b-pairs (partition 2 bindings))
  (def b-names (map 0 b-pairs))
  (def b-values (map 1 b-pairs))

  ~((fn ,name [,;b-names]
      ,;body)
    ,;b-values))

(named-let
  rec [x 10]

  (if (> x 0)
    (do
      (pp x)
      (rec (dec x)))
    (pp 'end)))
