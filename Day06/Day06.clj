#!/usr/bin/env bb
(ns Day06
  (:require [clojure.java.io :as io]
            [clojure.string :as str]
            [clojure.set :as cset]
            [clojure.test :refer [deftest is testing run-tests]]))

(defn parse-line-pt-1 [input]
  (let [[header vals] (str/split input #":\s+")]
    [header (mapv parse-long (str/split vals #"\s+"))]))

(defn collect-races [records]
  (map-indexed (fn [idx _]
                 {:id idx
                  :time (get-in records ["Time" idx])
                  :distance (get-in records ["Distance" idx])})
               (get records "Time")))

(defn process-race
  "Determine number of ways to beat best-time"
  [{:keys [time distance] :as _race}]
  (let [;; the equation based on distance = speed * time
        _charge-time->distance #(* % (- time %))
        ;; using the quadratic eqn, we solve for charge-time that beats distance
        ;; this is the value under the square root
        radical (Math/sqrt (- (* time time) (* 4 distance)))
        t-min (inc (Math/floor (/ (- time radical) 2)))
        t-max (dec (Math/ceil (/ (+ time radical) 2)))
        ways-to-win (count (range t-min (inc t-max)))]
    {:t-min t-min
     :t-max t-max
     :ways-to-win ways-to-win}))
(defn solve-part-1 [input]
  (let [lines (str/split-lines input)

        races (->> lines
                   (into {} (map parse-line-pt-1))
                   (collect-races))
        best-times (mapv process-race races)]
    (->> best-times
         (map :ways-to-win)
         (apply *))))

(comment
  (let [input-file "input.txt"
        input (slurp input-file)]
    (println "Input file: " input-file)
    (println "Part 1:" (time (solve-part-1 input))))
  :rcf)

(defn parse-line-pt-2 [input]
  (let [[header vals] (str/split input #":\s+")]
    [header [(parse-long (str/join (str/split vals #"\s+")))]]))

(defn solve-part-2 [input]
  (let [lines (str/split-lines input)
        race (->> lines
                  (into {} (map parse-line-pt-2))
                  (collect-races)
                  (first))
        best-times (process-race race)]
    (:ways-to-win best-times)))

(comment
  (let [input-file "input.txt"
        input (slurp input-file)]
    (println "Input file: " input-file)
    (println "Part 2:" (time (solve-part-2 input))))
  :rcf)

(when (some->> *command-line-args*
               first
               io/as-file
               (#(.exists %)))
  (let [input-file (first *command-line-args*)
        input (slurp input-file)]
    (println "Input file: " input-file)
    (println "Part 1:" (time (solve-part-1 input)))
    (println "Part 2:" (time (solve-part-2 input)))))
