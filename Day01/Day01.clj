#!/usr/bin/env bb

(require '[clojure.string :as str])


(def cv-pattern-part-1 #"\d")

(defn extract-calibration-value-part-1
  "Extracts the calibration value from a line of input."
  [line]
  (some-> (re-seq cv-pattern-part-1 line)
          vec
          (#(list (first %) (last %)))
          (str/join)
          (parse-long)))

(defn solve-part-1 [input-file]
  (let [input (slurp input-file)
        lines (str/split-lines input)
        calibration-values
        (some->> lines
                 (map str/trim)
                 (map extract-calibration-value-part-1))]
    (when (not-any? nil? calibration-values)
     (reduce + calibration-values))))

(def numbers
  "Defines the map of number words to numbers."
  {"one" 1
   "two" 2
   "three" 3
   "four" 4
   "five" 5
   "six" 6
   "seven" 7
   "eight" 8
   "nine" 9})

(def cv-pattern-part-2
  (re-pattern (re-pattern (str "\\d|" (str/join "|" (keys numbers))))))

(defn extract-calibration-value-part-2
  "Extracts the calibration value from a line of input."
  [line]
  (let [->number #(get numbers % %)]
    (some->> (re-seq cv-pattern-part-2 line)
             (map ->number)
             vec
             (#(list (first %) (last %)))
             (str/join)
             (parse-long))))

(defn solve-part-2 [input-file]
  (let [input (slurp input-file)
        lines (str/split-lines input)
        calibration-values
        (some->> lines
                 (map str/trim)
                 (map extract-calibration-value-part-2))]
    (when (not-any? nil? calibration-values)
      (reduce + calibration-values))))

(let [input-file (first *command-line-args*)]
  (println "Input file: " input-file)
  (println "Part 1" (time (solve-part-1 input-file)))
  (println "Part 2" (time (solve-part-2 input-file))))
