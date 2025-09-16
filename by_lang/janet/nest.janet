(defmacro nest
  "Created a nested expression from the sequence of forms in `body`. All arguments, except the last one, must be lists.
  Every element is nested as the last element its predecessor, such that the first element is the outermost list.

  As an example:
  (nest
    (for i 0 3)
    (for j 0 3)
    (pp [i j]))

  Is the same as:
  (for i 0 3
    (for j 0 3)
      (pp [i j]))
  "
  [& body]

  (def [forms end]
    (if (empty? body)
      [[] nil]
      [(array/slice body 0 (dec (length body)))
       (last body)]))

  (var result end)

  (var i (dec (length forms)))
  (while (>= i 0)
    (def form (in forms i))
    (assert (tuple? form) (string/format "form should be a tuple, got %j" form))
    (set result [;form result])
    (-- i))

  result)

(nest
  (for i 0 3)
  (for j 0 3)
  (pp [i j]))
