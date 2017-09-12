
'''

    generator:
        pairs of (word_index, other_word_index) + label: 1 if other_word is from context window, 0 if random

    training:
        -> embeddings: W(word_index), W2(other_word_index) -> they have to be different embeddings because p(a|b) != p(b|a)
        -> p(other_word|word) = activation(dot(embeddings))

        training: MSE I guess??

    usage:
        -> new model (simple embedding reusing W)


'''