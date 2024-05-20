from Models import START_TOKEN, END_TOKEN, SPACE_TOKEN
# from Models import  torch, nn

def ReadFile(NLines) -> [str]:
    try:
        f = open("Data/eng-fra.txt", encoding="utf-8")
        FileText = []
    
        for i in range(NLines):
            FileText.append(f.readline())
        
        f.close()
        return FileText
    
    except IOError:
        raise IOError("File not Found!!")

N_LINES = 5000

FileText : list[str] = ReadFile(N_LINES)
EngText : list[str] = []
FchText : list[str] = []

LangNames = ["Eng", "Fch"]
Lang2Idx = {"Eng" : 0, "Fch" : 1}

for x in FileText:
    Line = x.split(sep="\t")
    Line[Lang2Idx["Fch"]] = Line[-1][:len(Line[-1])-1] + " \n"
    EngText.append(Line[Lang2Idx["Eng"]])
    FchText.append(Line[Lang2Idx["Fch"]])

# Create a Tokenizing Class
SepWords = ['.', ',','!']

class Lang:
    def __init__(self, Name) -> None:
        self.Name = Name
        self.N_Words = 3
        self.Word2Idx = {START_TOKEN : 0, END_TOKEN : 1, SPACE_TOKEN : 2}
        self.Words = [START_TOKEN, END_TOKEN, SPACE_TOKEN]

        for x in SepWords:
            self.AddWord(x)

    def AddSentence(self, Sentence : str):
        L = Sentence.split(' ')

        for x in L:
            # Flag specifing if the x has been updated by the presence of SepWords
            Updated = False

            # Loop through each of the sep words
            for SepWord in SepWords:
                idx = x.find(SepWord)
                # if idx == -1 then no SepWord found
                if idx != -1:
                    # split into multiple strs seperated by SepWord
                    NL = x.split(SepWord)
                    for nx in NL:
                        # Only on normal words add " "
                        if nx != SepWord:
                            nx = nx + " "
                            self.AddWord(nx)

                    # SepWord flag Updated True
                    Updated = True
            
            if Updated == False:
                x = x + " "
                self.AddWord(x)

    def AddWord(self, Word : str):
        if not(Word in self.Words):
            self.Words.append(Word)
            self.Word2Idx[Word] = self.N_Words
            self.N_Words += 1

EngLang = Lang("Eng")
FchLang = Lang("Fch")

for x in EngText:
    EngLang.AddSentence(x)

for x in FchText:
    FchLang.AddSentence(x)
