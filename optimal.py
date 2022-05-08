# generates the mask of a word for a certain letter, which is a list containing
# the indexes where a letter is contained in a word and the indexes where it is not contained
#Example: mask("a","abacate") = [0,2,4]
def genmask(letter,word):
    indexes = [[],[]]
    for i,a in enumerate(word):
        if a == letter:
            indexes[0].append(i)
        else:
            indexes[1].append(i)
    return(indexes)

#generates a list containing all masks for a dictionary and specified letter
def allmask(letter,dictionary):
    allmasks = [[[],[]]] #Should it contain the empty mask?
    for word in dictionary:
        allmasks.append(genmask(letter,word))
    #Remove duplicates
    noduplicates = []
    for elem in allmasks:
        if elem not in noduplicates:
            noduplicates.append(elem)

    return(noduplicates)

#checks whether a mask fits a word for a specified letter
def checkmask(letter,word,mask):
    for position in mask[0]:
        if word[position] != letter:
            return(False)
    for position in mask[1]:
        if word[position] == letter:
            return(False)
    return(True)

#filters a dictionary by removing words that don't fit a mask for a specified letter
def filterdict(dictionary,mask,letter):
    newdict = [x for x in dictionary if checkmask(letter,x,mask)]
    return(newdict)

#helper function
def cc(m):
    if m[0] == []:
        return(1)
    else:
        return(0)

#returns a list with the most frequent letters in a dictionary for a given alphabet in descending order. The frequency is in %
#maxfreq(["abacate"], ["a","b","c"]) = [['a', 100.0], ['b', 100.0], ['c', 100.0]]
#can be used for a simple heuristic strategy
def maxfreq(dictionary,alphabet):
    frequency = []
    for letter in alphabet:
        frequency.append(0)
    for i,letter in enumerate(alphabet):
        filtered_dict = [word for word in dictionary if letter in word]
        frequency[i] += len(filtered_dict)/len(dictionary)*100
    frequency = [list(x) for x in zip(alphabet, frequency)]
    frequency.sort(key=lambda x: x[1],reverse=True)
    return(frequency)

#optimal solution function for some remaining lives, dictionary, and letters not yet guessed
#it returns a list [p,a] where 'p' is the probability of winning from here and 'a' the optimal guess
def optimal(remlives,dictionary,remletters):
    if remletters == []:
        return([1,""]) #there are no letters left to return
    elif remletters != [] and remlives == 0:
        return([0,remletters[0]]) #it is already lost, so let's just return some letter from the remaining ones
    elif remletters != [] and remlives > 0 and len(dictionary) == 1:
        return([1,maxfreq(dictionary,remletters)[0][0]]) #since there is only one word left, maxfreq() will return a winning letter
    else:
        optprobability = 0
        optletter = ""
        for letter in remletters:
            letterprob = 0
            for m in allmask(letter,dictionary):
                letterprob += len(filterdict(dictionary,m,letter))/len(dictionary)*optimal(remlives-cc(m),filterdict(dictionary,m,letter),[x for x in remletters if x != letter])[0]
            if letterprob > optprobability:
                optprobability = letterprob
                optletter = letter
        return([optprobability,optletter])

# at https://stackoverflow.com/a/9950711/15613034 it is shown an example where maxfreq() is not optimal as an algorithm.
# Let's test the optimal then!
dictionary = ["abc","abd","aef","egh"]
alphabet = ["a","b","c","d","e","f","g","h"]
lives = 1

print(maxfreq(dictionary,alphabet))
print(optimal(lives,dictionary,alphabet))

# maxfreq() returns 'a' because it is present in 75% of the words, but it has a lower overall winning probability
# optimal() return [0.5, 'e'] which is exactly what is said in the URL above!
