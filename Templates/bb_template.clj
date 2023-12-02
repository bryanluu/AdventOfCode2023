#!/usr/bin/env bb

(defn solve-part-1 [input-file]
  ;; Do stuff
  ,)

(defn solve-part-2 [input-file]
  ;; Do stuff
  )

(let [input-file (first *command-line-args*)]
  (println "Input file: " input-file)
  (println "Part 1:" (time (solve-part-1 input-file)))
  (println "Part 2:" (time (solve-part-2 input-file))))
