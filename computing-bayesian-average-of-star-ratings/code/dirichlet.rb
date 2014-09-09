DEFAULT_PRIOR = [2, 2, 2, 2, 2]

## input is a five-element array of integers
## output is a score between 1.0 and 5.0
def score votes, prior=DEFAULT_PRIOR
    posterior = votes.zip(prior).map { |a, b| a + b }
    sum = posterior.inject { |a, b| a + b }
    puts sum
    posterior.
        map.with_index { |v, i| (i + 1) * v }.
        inject { |a, b| a + b }.
        to_f / sum
end

votes = [9, 16, 57, 176, 325]

result = score(votes)
puts result
