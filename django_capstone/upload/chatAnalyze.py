from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re


'''
1. Load chatlog and words for scoring
2. Do preprocessing by reading one line at one time
3. Store the each result of sentences to a dictionary {time - preprocessed words} in a list
4. Review the list that contains a set of dictionary to score them with labeledwords
5. Store the each result of sentences to a dictionary {time - normalized_score} in a list
6. Return the list when it is called to be executed.
'''

# How to Use
'''
    labeldwords = ['a set of lists of words']
    f = open("test.txt", 'rt', encoding='UTF8')
    chatanlyze = ChatAnalyze(f, labeldwords)
    score = chatanlyze.Preprocessing()
    result = chatanlyze.Scoring(score)
    cand = chatanlyze.makeCandidateList(histogram=result,
                                    numOfMaximumHighlight=10,
                                    delay=1000,
                                    videoLen=19000)
'''


class ChatAnalyze:

    # chatlog <== file = open("test.txt", 'rt', encoding='UTF8')
    # labeledwords <== list
    # table_time = list()
    # table_data = list()
    # Final_Result = dict()

    def __init__(self, chatlog, labeledwords):

        # server setting
        import nltk
        nltk.download('stopwords')
        nltk.download('punkt')

        self.chatlog = chatlog
        self.labeledwords = labeledwords
        self.table_time = list()
        self.table_data = list()
        self.Final_Result = dict()


    def Preprocessing(self):
        # Line by Line seperating
        while True:
            line = self.chatlog.readline().lower()

            if not line:
                break

            timeline, data = line.split(" ", maxsplit=1)
            self.table_time.append(timeline)
            self.table_data.append(data)

    # Stemming
        score = [0]*len(self.table_time)

        return score

    def Scoring(self, score):
        ps = PorterStemmer()

        # Stopwords
        stopWords = set(stopwords.words('english'))

        # Append most common top 10 Term freqency to labeled words
        filtered_sentence = []
        for eachData in self.table_data:

            words = word_tokenize(eachData)
            output = []
            for check in words:
                check = check.replace("[", "").replace("]", "").replace("_", "").replace("-", "").replace("@", "").replace("'", "").replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(
                    "<", "").replace(">", "").replace("|", "").replace("-", "").replace("?", "").replace("!", "").replace(":", "").replace("/", "").replace("\"", "").replace(" ", "").lower()
                output.append(check)
                # pattern = re.compile(r'\s+')
                # sentence = re.sub(pattern, '', check)
                # output.append(sentence)
            # print(output)
            for w in output:
                if w not in stopWords and not w.isdigit():
                    filtered_sentence.append(w)

        counts = Counter(filtered_sentence)

        # Apeend
        for i in range(10):
            self.labeledwords.append(list(counts.keys())[i+1])

        print(self.labeledwords)

        # Scoring
        for eachData in self.table_data:
            words = word_tokenize(eachData)
            target_score = 0

            for word in words:
                if(ps.stem(word) in self.labeledwords):
                    target_score += 1

            score[self.table_data.index(eachData)] = target_score

        # Normalization
        # skip

        # Result
        result = sorted(Counter(self.table_time).items())
        index = 0

        for eachResult in result:
            # How many times chats appeared in same time
            iteration = eachResult[1]

            sum = 0
            for i in range(iteration):
                sum += score[i+index]
                self.Final_Result[eachResult[0]] = sum
            index += iteration

        return self.Final_Result



    # string to seconds
    def second(self, str):
        arr = re.split("[:]",str)
        if len(arr) != 3:
            print("check time string :"+str)
        return int(arr[0])*3600 + int(arr[1])*60 + int(arr[2])



    # make candidate list
    def makeCandidateList(self, histogram, numOfMaximumHighlight, delay, videoLen):
        # make raw candidate list
        sorted_list = sorted(histogram.items(), key=lambda t: t[1], reverse=True)[:numOfMaximumHighlight]
        sorted_list = [self.second(i[0]) for i in sorted_list]
        candidates = sorted(sorted_list)

        # if picked points are too close
        deleteList = []
        for i in range(len(candidates) - 1):
            if candidates[i+1] - candidates[i] < delay:
                deleteList.append(i+1)
        for i in deleteList:
            del candidates[i]

        candidates = [[i-delay, i+delay] for i in candidates]

        # post-processing
        for i in range(len(candidates)):
            if candidates[i][0] < 0:
                candidates[i][0]=0
            if candidates[i][1] > videoLen:
                candidates[i][1] = videoLen

        return candidates


# How to use this class
if __name__ == '__main__':
    labeldwords = ['pog', 'poggers', 'pogchamp', 'holy', 'shit', 'wow', 'ez', 'clip', 'nice', 'omg', 'wut', 'gee', 'god', 'dirty', 'way', 'moly', 'wtf', 'fuck', 'crazy', 'omfg']
    f = open("test.txt", 'rt', encoding='UTF8')
    chatanlyze = ChatAnalyze(f, labeldwords)
    score = chatanlyze.Preprocessing()
    result = chatanlyze.Scoring(score)
    cand = chatanlyze.makeCandidateList(histogram=result,
                                        numOfMaximumHighlight=10,
                                        delay=1000,
                                        videoLen=19000)

    print(cand)