from Models import START_TOKEN, END_TOKEN
# from Models import  torch, nn
import pandas as pd

import nltk
nltk.download('punkt')

File = pd.read_csv("Data/eng_-french.csv",nrows=25000)
File.dropna(subset=["English words/sentences", "French words/sentences"])

EnglishFile = File["English words/sentences"]
FrenchFile = File["French words/sentences"]

print(File.head(5))
print(File.tail(5))

print(File.info())

# Index the data
# Store each unique word
EnglishVocab = []
FrenchVocab = []

# Store the Max Len of a specific word
MaxEnglishLen = 0
MaxFrenchLen = 0

# Now store the Text Data in Indexes from Vocabs and VocabMap
EnglishIndicecs = []
FrenchIndices = []

# Set each unique word and thing to a index
for x in EnglishFile:
    Words = nltk.word_tokenize(x)
    for word in Words:
        if not(word in EnglishVocab):
            EnglishVocab.append(word)
EnglishVocab.append(START_TOKEN)
EnglishVocab.append(END_TOKEN)
print(EnglishVocab[:10])

# Set each unique word and thing to a index
for x in FrenchFile:
    Words = nltk.word_tokenize(x)
    for word in Words:
        if not(word in FrenchVocab):
            FrenchVocab.append(word)
FrenchVocab.append(START_TOKEN)
FrenchVocab.append(END_TOKEN)
print(FrenchVocab[:10])

# Now use the Index to get the index by using a word
EnglishVocabMap = {word : x for x, word in enumerate(EnglishVocab)}
FrenchVocabMap = {word : x for x, word in enumerate(FrenchVocab)}

print("len(EnglishVocabMap): ", len(EnglishVocabMap))
print("len(FrenchVocabMap): ", len(FrenchVocabMap))

# Get the Max Length of a sentence in the File 
for x in EnglishFile:
    if len(x) > MaxEnglishLen:
        MaxEnglishLen = len(x)

# Get the Max Length of a sentence in the File 
for x in FrenchFile:
    if len(x) > MaxFrenchLen:
        MaxFrenchLen = len(x)

print("MaxEnglishLen: ", MaxEnglishLen)
print("MaxFrenchLen: ",MaxFrenchLen)

# To convert the data into numerical form required by Torch
def convert_to_indices(String, vocab_mapping):
    Indices = []
    Token = nltk.word_tokenize(String)
    
    for Seq in Token:
        Indices.append(vocab_mapping[Seq])
    
    return Indices

for x in EnglishFile:
    EnglishIndicecs.append(convert_to_indices(x, EnglishVocabMap))

for x in FrenchFile:
    FrenchIndices.append(convert_to_indices(x, FrenchVocabMap))

# To make the Sequences be a specific len for now respective MaxLength
def pad_sequences(sequences, max_length, padding_value=0):
    padded_sequences = []
    for sequence in sequences:
        if len(sequence) >= max_length:
            padded_sequence = sequence[:max_length]
        else:
            padded_sequence = sequence + [padding_value] * (max_length - len(sequence))
        padded_sequences.append(padded_sequence)

    return padded_sequences

EnglishPadSeq = pad_sequences(EnglishIndicecs, MaxEnglishLen)
FrenchPadSeq = pad_sequences(FrenchIndices, MaxEnglishLen)
print((EnglishPadSeq[101]))
print(EnglishIndicecs[101])
