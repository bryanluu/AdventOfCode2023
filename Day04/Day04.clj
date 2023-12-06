#!/usr/bin/env bb
(ns Day04
  (:require [clojure.string :as str]
            [clojure.set :as set]))

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
        my-numbers (extract-numbers (.group m "myNumbers"))
        matches (set/intersection winning-numbers my-numbers)
        points (case (count matches)
                 0 0
                 1 1
                 (reduce * 1 (repeat (dec (count matches)) 2)))]
    {:id id
     :winning-numbers winning-numbers
     :my-numbers my-numbers
     :points points}))

(defn solve-part-1 [input]
  (let [lines (str/split-lines input)
        cards (map parse-card lines)]
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

(let [input-file (or (first *command-line-args*) "input.txt")
      input (slurp input-file)]
  (println "Input file: " input-file)
  (println "Part 1:" (time (solve-part-1 input)))
  (println "Part 2:" (time (solve-part-2 input))))
