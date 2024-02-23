from sklearn.tree import DecisionTreeClassifier
import sys

#Load Training Dataset
try:
    a = []
    with open(sys.argv[1], "r") as train_file:
        a = train_file.readlines()
    train = []
    for row in a:
        train.append(row.split())

    #Creating a word-index Dictionary
    unique_words = set()
    index_word_pair = dict()
    for j in train:
        unique_words.add(j[1])
    for index, word in enumerate(unique_words):
        index_word_pair[word] = index
    index_word_pair[""] = len(index_word_pair)
    index_word_pair["[NOTFOUND]"] = len(index_word_pair)

    #Forming the Dataset
    punctuations = [",", ".", "-", "?", "(", ")"]
    train_df = []
    for j in train:
        if not 'TOK' in j:
            word_l = []
            z = train.index(j)
            # word_l.append(b[z][0])
            word_l.append(index_word_pair[train[z][1]]) #Attribute 1, left word
            try :
                word_l.append(index_word_pair[train[z+1][1]]) #Attribute 2, right word
                word_l.append(1 if len(train[z][1][:-1])<3 else 0) #Attribute 3, length check on left word
                word_l.append(1 if (train[z][1]).istitle() else 0) #Attribute 4, left word capital check
                word_l.append(1 if(train[z+1][1]).istitle() else 0) #Attribute 5, right word capital check
                word_l.append(1 if len(train[z+1][1]) < 5 else 0) #Custom Attribute 6
                word_l.append(1 if train[z+1][1][0] == "\"" else 0) #Custom Attribute 7
                context = train[z-3][1] + train[z-2][1] + train[z-1][1] + train[z][1] + train[z+1][1] + train[z+2][1] + train[z+3][1]
                word_l.append(1 if any(x in context for x in punctuations) else 0) #Custom Attribute 8
                word_l.append(train[z][2]) #Decision Attribute
                train_df.append(word_l)
            except(IndexError): 
                word_l.append(index_word_pair[""])
                word_l.append(1 if len(train[z][1][:-1])<3 else 0)
                word_l.append(1 if(train[z][1]).istitle() else 0)
                word_l.append(1 if"".istitle() else 0)
                word_l.append(1 if len("") < 5 else 0)
                word_l.append(1 if "" == "\"" else 0)
                context = train[z-3][1] + train[z-2][1] + train[z-1][1] + train[z][1]
                word_l.append(1 if any(x in context for x in punctuations) else 0)
                word_l.append(train[z][2])
                train_df.append(word_l)
    trainY = []
    trainX = []
    for row in train_df:
        trainX.append(row[:-1]) #Train With All Attributes
        # trainX.append(row[:-4]) #Train With Original 5 Attributes
        # trainX.append(row[5:-1]) #Train with custom 3 attributes
        trainY.append(row[-1])
    print("Length of Train Dataset: ", len(trainX))
    #Decision Tree Fitting
    clf = DecisionTreeClassifier()
    clf = clf.fit(trainX, trainY)

    #Reading Test File
    try:
        a = []
        with open(sys.argv[2], "r") as test_file:
            a = test_file.readlines()
        test = []
        for row in a:
            test.append(row.split())
        test_df = []
        for j in test:
            if not 'TOK' in j:
                word_l = []
                z = test.index(j)
                # word_l.append(b[z][0])
                try:
                    word_l.append(index_word_pair[test[z][1]]) #Attribute 1, left word
                except(KeyError):
                    word_l.append(index_word_pair["[NOTFOUND]"])
                try :
                    try:
                        word_l.append(index_word_pair[test[z+1][1]]) #Attribute 2, right word
                    except(KeyError):
                        word_l.append(index_word_pair["[NOTFOUND]"])
                    word_l.append(1 if len(test[z][1][:-1])<3 else 0) #Attribute 3, length check on left word
                    word_l.append(1 if (test[z][1]).istitle() else 0) #Attribute 4, left word capital check
                    word_l.append(1 if(test[z+1][1]).istitle() else 0) #Attribute 5, right word capital check
                    word_l.append(1 if len(test[z+1][1]) < 5 else 0) #Custom Attribute 6
                    word_l.append(1 if test[z+1][1][0] == "\"" else 0) #Custom Attribute 7
                    context = test[z-3][1] + test[z-2][1] + test[z-1][1] + test[z][1] + test[z+1][1] + test[z+2][1] + test[z+3][1]
                    word_l.append(1 if any(x in context for x in punctuations) else 0) #Custom Attribute 8
                    word_l.append(test[z][2]) #Decision Attribute
                    test_df.append(word_l)
                except(IndexError): 
                    word_l.append(index_word_pair[""])
                    word_l.append(1 if len(test[z][1][:-1])<3 else 0)
                    word_l.append(1 if(test[z][1]).istitle() else 0)
                    word_l.append(1 if"".istitle() else 0)
                    word_l.append(1 if len("") < 5 else 0)
                    word_l.append(1 if "" == "\"" else 0)
                    context = test[z-3][1] + test[z-2][1] + test[z-1][1] + test[z][1]
                    word_l.append(1 if any(x in context for x in punctuations) else 0)
                    word_l.append(test[z][2])
                    test_df.append(word_l)
        
        testY = []
        testX = []
        for row in test_df:
            testX.append(row[:-1]) #Test with all 8 Attributes
            # testX.append(row[:-4]) #Test with original 5 attributes
            # testX.append(row[5:-1]) #Test with custom 3 attributes
            testY.append(row[-1])
        print("Length of Test Dataset: ", len(testX))

        #Classifying Test Dataset
        Y_pred = clf.predict(testX)
        acc = (sum(Y_pred == testY)/len(testY)) * 100
        print("The accuracy on Test Dataset: ", acc)

        #Writing output to File
        output_data = []
        for row in test:
            if "TOK" not in row:
                output_data.append([row[0], row[1]])
        with open("./SBD.test.out", "w") as output_file:
            for index, row in enumerate(output_data):
                output_file.write(row[0]+" "+row[1] + " " +Y_pred[index] +"\n")
        print("Write Complete")

    except(FileNotFoundError):
        print("No such file or directory: ", sys.argv[2])
except(FileNotFoundError):
    print("No such file or directory: ", sys.argv[1])


    