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

(defn cards-seq->cards-map
  "Convert a list of cards to a map of cards keyed by ID."
  [cards]
  (into {}
        (map (juxt :id identity))
        cards))

(defn process-card-rule
  "Reducer that processes a card rule and returns the updated map of cards"
  [processed-cards card]
  (let [id (:id card)
        common-numbers (set/intersection (:winning-numbers card)
                                         (:my-numbers card))
        ;; set instances of card if not already set
        new-card (assoc card :instances (get-in processed-cards [id :instances] 1))
        new-copies (:instances new-card)
        ;; ids of cards to copy
        cards-to-copy (into []
                            (map inc)
                            (range id (+ id (count common-numbers))))]
    (loop [cards processed-cards
           to-copy cards-to-copy]
      (if (empty? to-copy)
        (assoc cards id new-card)
        (let [copied (first to-copy)
              new-cards (update-in cards [copied :instances] (fnil + 1) new-copies)]
          (recur new-cards (rest to-copy)))))))

(defn process-rules
  "Given a list of parsed cards, process the real rules for each card and
   record any copies of cards"
  [cards]
  (reduce process-card-rule (cards-seq->cards-map cards) cards))

(defn solve-part-2 [input]
  (let [lines (str/split-lines input)
        cards (into []
                    (map parse-card)
                    lines)
        processed-cards (process-rules cards)]
    (reduce + (map :instances (vals processed-cards)))))

;; Tests

(deftest test-parse-card
  (is (= {:id 3
          :winning-numbers #{1 21 53 59 44}
          :my-numbers #{69 82 63 72 16 21 14 1}}
         (parse-card "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1"))))

(deftest test-power-of-two
  (is (= 1 (power-of-two 0)))
  (is (= 2 (power-of-two 1)))
  (is (= 4 (power-of-two 2)))
  (is (= 8 (power-of-two 3)))
  (is (= 16 (power-of-two 4))))

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

(deftest test-process-card-rule
  (let [before
        {2 {:id 2
            :winning-numbers #{13 32 20 16 61}
            :my-numbers #{61 30 68 82 17 32 24 19}}
         3 {:id 3
            :winning-numbers #{1 21 53 59 44}
            :my-numbers #{69 82 63 72 16 21 14 7}}
         4 {:id 4
            :winning-numbers #{41 92 73 84 69}
            :my-numbers #{59 84 76 51 58 5 54 83}}
         5 {:id 5
            :winning-numbers #{87 83 26 28 32}
            :my-numbers #{88 30 70 12 93 22 82 36}}}
        after
        {2 {:id 2
            :winning-numbers #{13 32 20 16 61}
            :my-numbers #{61 30 68 82 17 32 24 19}}
         3 {:id 3
            :winning-numbers #{1 21 53 59 44}
            :my-numbers #{69 82 63 72 16 21 14 1}
            :instances 1}
         4 {:id 4
            :winning-numbers #{41 92 73 84 69}
            :my-numbers #{59 84 76 51 58 5 54 83}
            :instances 2}
         5 {:id 5
            :winning-numbers #{87 83 26 28 32}
            :my-numbers #{88 30 70 12 93 22 82 36}
            :instances 2}}
        card {:id 3
              :winning-numbers #{1 21 53 59 44}
              :my-numbers #{69 82 63 72 16 21 14 1}}]
    (is (= after
           (process-card-rule before card))))
  (let [before
        {2 {:id 2
            :winning-numbers #{13 32 20 16 61}
            :my-numbers #{61 30 68 82 17 32 24 19}}
         3 {:id 3
            :winning-numbers #{1 21 53 59 44}
            :my-numbers #{69 82 63 72 16 21 14 1}
            :instances 2}
         4 {:id 4
            :winning-numbers #{41 92 73 84 69}
            :my-numbers #{59 84 76 51 58 5 54 83}
            :instances 2}
         5 {:id 5
            :winning-numbers #{87 83 26 28 32}
            :my-numbers #{88 30 70 12 93 22 82 36}}}
        after
        {2 {:id 2
            :winning-numbers #{13 32 20 16 61}
            :my-numbers #{61 30 68 82 17 32 24 19}}
         3 {:id 3
            :winning-numbers #{1 21 53 59 44}
            :my-numbers #{69 82 63 72 16 21 14 1}
            :instances 2}
         4 {:id 4
            :winning-numbers #{41 92 73 84 69}
            :my-numbers #{59 84 76 51 58 5 54 83}
            :instances 4}
         5 {:id 5
            :winning-numbers #{87 83 26 28 32}
            :my-numbers #{88 30 70 12 93 22 82 36}
            :instances 3}}
        card {:id 3
              :winning-numbers #{1 21 53 59 44}
              :my-numbers #{69 82 63 72 16 21 14 1}}]
    (is (= after
           (process-card-rule before card)))))

(deftest test-process-rules
  (let [cards [{:id 1
                :winning-numbers #{41 48 83 86 17}
                :my-numbers #{83 86 6 31 17 9 48 53}}
               {:id 2
                :winning-numbers #{13 32 20 16 61}
                :my-numbers #{61 30 68 82 17 32 24 19}}
               {:id 3
                :winning-numbers #{1 21 53 59 44}
                :my-numbers #{69 82 63 72 16 21 14 1}}
               {:id 4
                :winning-numbers #{41 92 73 84 69}
                :my-numbers #{59 84 76 51 58 5 54 83}}
               {:id 5
                :winning-numbers #{87 83 26 28 32}
                :my-numbers #{88 30 70 12 93 22 82 36}}
               {:id 6
                :winning-numbers #{31 18 13 56 72}
                :my-numbers #{74 77 10 23 35 67 36 11}}]
        processed-cards
        {1 {:id 1
            :winning-numbers #{41 48 83 86 17}
            :my-numbers #{83 86 6 31 17 9 48 53}
            :instances 1}
         2 {:id 2
            :winning-numbers #{13 32 20 16 61}
            :my-numbers #{61 30 68 82 17 32 24 19}
            :instances 2}
         3 {:id 3
            :winning-numbers #{1 21 53 59 44}
            :my-numbers #{69 82 63 72 16 21 14 1}
            :instances 4}
         4 {:id 4
            :winning-numbers #{41 92 73 84 69}
            :my-numbers #{59 84 76 51 58 5 54 83}
            :instances 8}
         5 {:id 5
            :winning-numbers #{87 83 26 28 32}
            :my-numbers #{88 30 70 12 93 22 82 36}
            :instances 14}
         6 {:id 6
            :winning-numbers #{31 18 13 56 72}
            :my-numbers #{74 77 10 23 35 67 36 11}
            :instances 1}}]
    (is (= processed-cards (process-rules cards)))))

(deftest test-solve-part-2
  (let [input (slurp "example.txt")]
    (is (= 30 (solve-part-2 input)))))

(when (some->> *command-line-args*
               first
               io/as-file
               (#(.exists %)))
  (let [input-file (first *command-line-args*)
        input (slurp input-file)]
    (println "Input file: " input-file)
    (println "Part 1:" (time (solve-part-1 input)))
    (println "Part 2:" (time (solve-part-2 input)))))
