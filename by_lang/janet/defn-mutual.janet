(defmacro defn-mutual
  "Define mutually recursive functions.
  Somewhat based off scheme's `letrec` macro."
  [& decls]

  (def d-types (map 0 decls))
  (def d-names (map 1 decls))
  (def d-rest (map |(array/slice $ 2) decls))

  (def var-defs
    (map
      (fn [[d-type d-name & _]]
        (assert (symbol? d-type))
        (assert (symbol? d-name))

        (case d-type
          'defn ~(var ,d-name nil)
          'defn- ~(var- ,d-name nil)
          (error (string/format "unsupported definition type: %j" d-type))))
      decls))

  (def set-functions
    (map
      (fn [[_ d-name & rest]]
        ~(set ,d-name (fn ,;rest)))
      decls))

  ~(def [,;d-names]
     (do
       ,;var-defs
       ,;set-functions
       [,;d-names])))

(defn-mutual
  # comprehensible? I hardly know her
  (defn foo [x]
    (when (> x 0)
      (pp x)
      (bar (dec x))))
  (defn bar [x]
    (when (> x 0)
      (foo (dec x)))))

(foo 7)
