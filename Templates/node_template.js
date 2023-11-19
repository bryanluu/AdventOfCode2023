#!/usr/bin/node
var filename = process.argv.length > 2 ? process.argv[2] : 'input.txt' // Input file

// Solves the challenge with input filename
function solve (filename) {
  // solution here
}

// run if script is run
console.log('Input file: ', filename)
var start = process.hrtime() // Time the solve attempt
solve(filename)
var end = process.hrtime(start)
console.log('solve(%s) took: %ds %dms', filename, end[0], end[1] / 1000000)
