#!/usr/bin/env bb
(ns DayNN
  (:require [clojure.java.io :as io]
            [clojure.test :refer [deftest is testing run-tests]]))

(defn solve-part-1 [input]
  ;; Do stuff
  )

(defn solve-part-2 [input]
  ;; Do stuff
  )

(when (some->> *command-line-args*
               first
               io/as-file
               (#(.exists %)))
  (let [input-file (first *command-line-args*)
        input (slurp input-file)]
    (println "Input file: " input-file)
    (println "Part 1:" (time (solve-part-1 input)))
    (println "Part 2:" (time (solve-part-2 input)))))
