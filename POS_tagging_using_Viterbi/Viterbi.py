from collections import defaultdict
import sys

try:
    file1 = open(sys.argv[1], "r")
    a = file1.readlines()

    tags_count = defaultdict(lambda : 0)
    count = 0
    for sample in a:
        sample = sample.split()
        for i in range(len(sample)):
            index = 0
            for j in range(len(sample[i])-1, -1, -1):
                if sample[i][j] == '/':
                    word = sample[i][:j]
                    tag = sample[i][j+1:]
                    tags_count[tag] += 1
                    break

    tag_mapper = {}
    count = 1
    for key in tags_count.keys():
        tag_mapper[count] = key
        count += 1

    word_tag_count = defaultdict(dict)

    for sample in a:
        sample = sample.split()
        for i in range(len(sample)):
            for j in range(len(sample[i])-1, -1, -1):
                if sample[i][j] == '/':
                    word = sample[i][:j]
                    tag = sample[i][j+1:]
                    if word not in word_tag_count:
                        for key in tags_count.keys():
                            word_tag_count[word][key] = 0
                    word_tag_count[word][tag] += 1
                    break

    tag_first_count = defaultdict(lambda : 0)
    for sent in a:
        word = sent.split()
        for j in range(len(word[0])-1, -1, -1):
            if word[0][j] == '/':
                tag = word[0][j+1:]
                tag_first_count[tag] += 1
                break

    tag_pair_count = defaultdict(dict)
    for sample in a:
        sample = sample.split()
        prev_tag = ''
        for i in range(len(sample)):
            for j in range(len(sample[i])-1, -1, -1):
                if sample[i][j] == '/':
                    word = sample[i][:j]
                    tag = sample[i][j+1:]
                    if i == 0:
                        prev_tag = tag
                    else:
                        if prev_tag not in tag_pair_count:
                            for key in tags_count.keys():
                                tag_pair_count[prev_tag][key] = 0
                        tag_pair_count[prev_tag][tag] += 1
                        prev_tag = tag
                    break
        
    def cleanSentence(sent):
        clean_sentence = []
        tags = []
        sent = sent.split()
        for i in range(len(sent)):
            for j in range(len(sent[i])-1, -1, -1):
                if sent[i][j] == '/':
                    clean_sentence.append(sent[i][:j])
                    tags.append(sent[i][j+1:])
                    break
        return(clean_sentence, tags)
    try:
        file1 = open(sys.argv[2], "r")
        b = file1.readlines()

        count = 0
        correct_predictions = 0
        total_predictions = 0
        for test_sent in b:
            count += 1
            cleaned_sentence, tags = cleanSentence(test_sent)
            scores = defaultdict(lambda : defaultdict(int))
            backptr = defaultdict(lambda : defaultdict(int))
            for tag in tag_mapper.values():
                scores[tag][0] = (word_tag_count[cleaned_sentence[0]].get(tag,0)/tags_count[tag]) * (tag_first_count[tag]/len(a))
                backptr[tag][0] = 0
            for w in range(1, len(cleaned_sentence)):
                for tag in tag_mapper.values():
                    max_score, max_tag = 0, 0
                    for tag_key, sub_tag in tag_mapper.items():
                        score = scores[sub_tag][w-1] * (tag_pair_count[sub_tag][tag]/tags_count[sub_tag])
                        if score >= max_score:
                            max_score = score
                            max_tag = tag_key
                    scores[tag][w] = (word_tag_count[cleaned_sentence[w]].get(tag,0)/tags_count[tag]) * max_score
                    backptr[tag][w] = sub_tag
            predictions = {}
            for w in range(len(cleaned_sentence)-1, -1, -1):
                max_score, max_tag = 0, ''
                for tag, score_list in scores.items():
                    if score_list[w] >= max_score:
                        max_score = score_list[w]
                        max_tag = tag
                predictions[w] = max_tag
            
            predictions = list(predictions.values())[::-1]
            correct_predictions += len([1 for x, y in zip(predictions, tags) if x == y])
            total_predictions += len(tags)

        print("Accuracy:", (correct_predictions/total_predictions)*100)
    except(FileNotFoundError):
        print("No such file or directory: ", sys.argv[2])
except(FileNotFoundError):
        print("No such file or directory: ", sys.argv[1])