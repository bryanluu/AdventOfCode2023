#!/usr/bin/env bb
(ns Day04
  (:require [clojure.string :as str]
            [clojure.set :as set]
            [clojure.java.io :as io])
  (:require [clojure.test :refer [deftest is testing run-tests]]))

(def CARD_REGEX #"^Card\s+(?<id>\d+):(?<winningNumbers>(?:\s*\d+\s*)+)\|(?<myNumbers>(?:\s*\d+\s*)+)$")

(defn extract-numbers
  "Extract numbers from a space-separated list of numbers."
  [s]
  (into #{}
        (comp
         (filter #(not (str/blank? %)))
         (map #(Integer/parseInt %)))
        (str/split s #"\s+")))

(defn parse-card
  "Parse card's ID, winning numbers, and your numbers from a line of input."
  [line]
  (let [m (re-matcher CARD_REGEX line)
        _ (re-find m)
        id (Integer/parseInt (.group m "id"))
        winning-numbers (extract-numbers (.group m "winningNumbers"))
        my-numbers (extract-numbers (.group m "myNumbers"))]
    {:id id
     :winning-numbers winning-numbers
     :my-numbers my-numbers}))

(defn power-of-two [n]
  (reduce * 1 (repeat n 2)))

(defn compute-points
  "Compute the points for a card."
  [card]
  (let [winning-numbers (:winning-numbers card)
        my-numbers (:my-numbers card)
        common-numbers (set/intersection winning-numbers my-numbers)
        points (case (count common-numbers)
                 0 0
                 (power-of-two (dec (count common-numbers))))]
    (assoc card :common common-numbers :points points)))

(defn solve-part-1 [input]
  (let [lines (str/split-lines input)
        cards (into []
                    (comp
                     (map parse-card)
                     (map compute-points))
                    lines)]
    (reduce + (map :points cards))))

(comment
  (def line "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
  (parse-card line)
  (def m (re-matcher CARD_REGEX line))
  (re-find m)
  (.group m "id")
  (.group m "winningNumbers")
  (.group m "myNumbers")
  :rcf)

(defn solve-part-2 [input]
  ;; Do stuff
  )

;; Tests

(deftest test-parse-card
  (is (= {:id 3
          :winning-numbers #{1 21 53 59 44}
          :my-numbers #{69 82 63 72 16 21 14 1}}
         (parse-card "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1"))))

(deftest test-compute-points
  (is (= {:id 3
          :winning-numbers #{1 21 53 59 44}
          :my-numbers #{69 82 63 72 16 21 14 1}
          :common #{1 21}
          :points 2}
         (compute-points {:id 3
                          :winning-numbers #{1 21 53 59 44}
                          :my-numbers #{69 82 63 72 16 21 14 1}}))))

(deftest test-solve-part-1
  (let [input (slurp "example.txt")]
    (is (= 13 (solve-part-1 input)))))

(when (some->> *command-line-args*
               first
               io/as-file
               #(.exists %))
  (let [input-file (first *command-line-args*)
        input (slurp input-file)]
    (println "Input file: " input-file)
    (println "Part 1:" (time (solve-part-1 input)))
    (println "Part 2:" (time (solve-part-2 input)))))
