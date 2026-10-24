#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Title: bpe.py
Version: 1.0.0
Description:


Author: Shane Hussey
Create Date: 2026-10-22
Licence: MIT
Usage:
	python bpe.py --corpus "input.txt" --k 1000 --verbose

"""

def fs_train_bpe(
        trn_corpus: list,
        num_merges: int,
        min_frequency: int,
        end_of_word: str):
    """

    :param trn_corpus: Input training corpus
    :param num_merges: Maximum number of merges
    :param min_frequency: Minimum frequency of a symbol-pair that would qualify for merging.
    :param end_of_word: End of word symbol

    :return tokens: list[list]
    :return vocab: set
    :return merges: list[tuple]
    """
    from re import escape, split, sub
    from collections import Counter

    # initialize vocabulary with end of word token
    V = {char for word in trn_corpus for char in word} | {end_of_word}

    # add spaces between each token in the corpus for handling merges
    #  and add the end of word token at the end
    trn_corpus = list(map(
        lambda w: sub(r'(.)', r'\1 ', w) + end_of_word, trn_corpus))


    merges = []
    for loop in range(num_merges):

        # generate list of all character pairs in corpus
        pairs = []
        for word in trn_corpus:
            word = word.split()
            for character in range(len(word) - 1):
                pairs.append((word[character], word[character + 1]))

        # count the most frequent pairs
        pair_counts = Counter(pairs)
        if not pair_counts:
            break
        # check that the "most frequent pair"/ first pair is not less
        #  the min frequency
        most_frequent_pair = pair_counts.most_common(1)[0][0]
        if pair_counts[most_frequent_pair] < min_frequency:
            break

        # add the fused most frequent pairs to the vocab
        V.add(f'{most_frequent_pair[0]}{most_frequent_pair[1]}')

        # update the corpus to replace the most frequent pair with a
        # the new pair token
        re_sub_from = r'(?<!\S)' + escape(f'{most_frequent_pair[0]} {most_frequent_pair[1]}') + r'(?!\S)'
        re_sub_to = f'{most_frequent_pair[0]}{most_frequent_pair[1]}'
        new_corpus = []
        for word in trn_corpus:
            new_corpus.append(sub(re_sub_from, lambda _: re_sub_to, word))
        trn_corpus = new_corpus

        # add the pair for merging / encoding
        merges.append(most_frequent_pair)

    # clean corpus output tokens
    # ['new ew</w>', ... ] -> [['new', 'ew</w>'], ...]
    trn_corpus = list(map(lambda x: x.split(), trn_corpus))

    return trn_corpus, V, merges




class FSTokenizer:
    def __init__(self, merges, end_of_word):
        self.merges = merges
        self.eow = end_of_word

    def pretokenize(self, text):
        tokens = []
        for line in text.split("\n"):
            for token in line.split(" "):
                if token:
                    tokens.append(token)
        return tokens

    def encode_utterance(self, word):
        """encodes individual words using BPE trained merges"""
        # add eow to word
        utterance = list(word) + [self.eow]
        #print(utterance)

        # replace learned merges in order
        for pair_0, pair_1 in self.merges:
            merged, i = [], 0
            while i < len(utterance):
                #print(i)
                #print(pair_0, pair_1)
                if i < len(utterance) - 1 and \
                        utterance[i] == pair_0 and \
                        utterance[i + 1] == pair_1:
                    merged.append(pair_0 + pair_1)
                    # makes sure we dont l l l -> lll by accidnet
                    i += 2
                else:
                    merged.append(utterance[i])
                    i += 1
            utterance = merged

        return utterance

    def encode(self, text):
        """Loops through text, splits to words, and encodes them."""
        encoded = []
        for token in self.pretokenize(text):
            encoded.extend(self.encode_utterance(token))
        return encoded




def main():
	parser = ArgumentParser(
		prog="",
		description="")
	parser.add_argument('--corpus', type=str, help="path to text corpus file")
	parser.add_argument('-k')
	args = parser.parse_args()





if __name__ == '__main__':
	main()