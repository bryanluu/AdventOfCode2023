#!/usr/bin/env bb

(defn solve-part-1 [input]
  ;; Do stuff
  )

(defn solve-part-2 [input]
  ;; Do stuff
  )

(let [input-file (or (first *command-line-args*) "input.txt")
      input (slurp input-file)]
  (println "Input file: " input-file)
  (println "Part 1:" (time (solve-part-1 input)))
  (println "Part 2:" (time (solve-part-2 input))))
