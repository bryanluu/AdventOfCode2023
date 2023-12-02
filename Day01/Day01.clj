#!/usr/bin/env bb

(require '[clojure.string :as str])

(defn extract-calibration-value [line]
  (-> (re-seq #"\d+" line)
      vec
      (#(list (first %) (last %)))
      (str/join)
      (parse-long)))

(defn solve [input-file]
  (let [input (slurp input-file)
        lines (str/split-lines input)]
    (->> lines
         (map str/trim)
         (map extract-calibration-value)
         (reduce +)
         prn)))

(let [input-file (first *command-line-args*)]
  (println "Input file: " input-file)
  (time (solve input-file)))
