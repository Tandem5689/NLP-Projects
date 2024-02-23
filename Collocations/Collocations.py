import sys
import math

list_of_punctuations = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "+", "{", "}", "[", "]", ":", ";", "\"", ",", ".", "/", "?", ">", "<", "~", "`"]

def tokenize_corpus(text):
    sentence = text.split()
    words = []
    for index, ele in enumerate(sentence):
        if ele not in list_of_punctuations:
            if "'" not in ele:
                if index < len(sentence)-1 and "'" in sentence[index+1]:
                    words.append(ele + " " +sentence[index+1])
                else:
                    words.append(ele)
    return words

def calculate_chi_score(bigrams_freq):
    chi_square_values = {}
    #Form Expected Frequency Dictionary
    bigram_poistion_freq = {}

    for bigram in bigrams_freq:
        unigram_list = tokenize_corpus(bigram)
        unigram_0, unigram_1 = unigram_list[0], unigram_list[1]
        if unigram_0 not in bigram_poistion_freq:
            bigram_poistion_freq[unigram_0] = {0:0}
            for bg in bigrams_freq:
                u_list = tokenize_corpus(bg)
                if unigram_0 == u_list[0]:
                    bigram_poistion_freq[unigram_0][0] += bigrams_freq[bg]
        elif 0 not in bigram_poistion_freq[unigram_0]:
            bigram_poistion_freq[unigram_0][0] = 0
            for bg in bigrams_freq:
                u_list = tokenize_corpus(bg)
                if unigram_0 == u_list[0]:
                    bigram_poistion_freq[unigram_0][0] += bigrams_freq[bg]
        if unigram_1 not in bigram_poistion_freq:
            bigram_poistion_freq[unigram_1] = {1:0}
            for bg in bigrams_freq:
                u_list = tokenize_corpus(bg)
                if unigram_1 == u_list[1]:
                    bigram_poistion_freq[unigram_1][1] += bigrams_freq[bg]
        elif 1 not in bigram_poistion_freq[unigram_1]:
            bigram_poistion_freq[unigram_1][1] = 0
            for bg in bigrams_freq:
                u_list = tokenize_corpus(bg)
                if unigram_1 == u_list[1]:
                    bigram_poistion_freq[unigram_1][1] += bigrams_freq[bg]

    length = sum(bigrams_freq.values())

    for bigram in bigrams_freq:
        bi_gram_to_unigram = tokenize_corpus(bigram)
        word1, word2 = bi_gram_to_unigram[0], bi_gram_to_unigram[1]
        expected = (bigram_poistion_freq[word1][0] * bigram_poistion_freq[word2][1]) / length
        observed = bigrams_freq[bigram]
        chi_square = ((observed - expected) ** 2) / expected
        chi_square_values[bigram] = chi_square
    
    sorted_chi = {k:v for k,v in (sorted(chi_square_values.items(), key= lambda x: x[1], reverse=True))}
    first_n_chi_Scores = list(sorted_chi.items())[:20]
    for key, value in first_n_chi_Scores:
        print("Bi-Gram:", key, "||| CHI Score-",value)

def calculate_pmi_score(bigrams_freq, unigrams_freq):
    pmi_score_values = {}
    length = sum(unigrams_freq.values())
    for bigram in bigrams_freq:
        bi_gram_to_unigram = tokenize_corpus(bigram)
        word1, word2 = bi_gram_to_unigram[0], bi_gram_to_unigram[1]
        p_word1 = unigrams_freq[word1] / length
        p_word2 = unigrams_freq[word2] / length
        p_bigram = bigrams_freq[bigram] / length
        pmi = math.log2(p_bigram / (p_word1 * p_word2))
        pmi_score_values[bigram] = pmi
    sorted_pmi = {k:v for k,v in (sorted(pmi_score_values.items(), key= lambda x: x[1], reverse=True))}
    first_n_pmi_Scores = list(sorted_pmi.items())[:20]
    for key, value in first_n_pmi_Scores:
        print("Bi-Gram:", key, "||| PMI Score-",value)

try:
    corpus = []
    with open(sys.argv[1], "r") as input_file:
        corpus = input_file.readlines()

    #Get Unigrams from all sentences and calculate their frequency    
    unigrams = []
    for sent in corpus:
        unigrams += tokenize_corpus(sent.lower())

    unigrams_freq = {}
    for word in unigrams:
        if word in unigrams_freq:
            unigrams_freq[word] += 1
        else:
            unigrams_freq[word] = 1
        
    #Form Bi-Grams and get their frequency
    bigrams_freq = {}
    for sentence in corpus:
        sentence_unigrams = tokenize_corpus(sentence.lower())
        for index, unigram in enumerate(sentence_unigrams[:-1]):
            bi_gram = unigram + " " + sentence_unigrams[index+1]
            if bi_gram in bigrams_freq:
                bigrams_freq[bi_gram] += 1
            else:
                bigrams_freq[bi_gram] = 1

    #Calculate Chi-Square Score or PMI Score based on the given Argument
    try:
        if sys.argv[2] == "chi-square": 
            calculate_chi_score(bigrams_freq)
        elif sys.argv[2] == "PMI":
            calculate_pmi_score(bigrams_freq, unigrams_freq)
        else:
            print("Incorrect argument")
    except(IndexError):
        print("Measure Argument not specified")


except(FileNotFoundError):
    print("No such file or directory:", sys.argv[1])