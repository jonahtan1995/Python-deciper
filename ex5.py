import json
import os


#everyone stuff
def checkIfUper(char):
    if (ord(char) >= ord('A') and ord(char) <= ord('Z')):
        return True
    else:
        return False

def checkIfLower(char):
    if (ord(char) >= ord('a') and ord(char) <= ord('z')):
        return True
    else:
        return False

#ceaser stuff
def applayNewString(string,key):
    new_string=''
    for char in string:
        if (checkIfUper(char)):
            if (ord(char) + key > ord('Z')):  # takes care of siclic pass Z
                charRes1 = ord(char) + key - (ord('Z') - ord('A') + 1)
                new_string = new_string + chr(charRes1)
            elif (ord(char) + key < ord('A')):  # takes care of siclic pass A
                charRes2 = ord(char) + key + (ord('Z') - ord('A') + 1)
                new_string = new_string + chr(charRes2)
            else:
                new_string = new_string + chr(ord(char) + key)

        elif (checkIfLower(char)):
            if (ord(char) + key > ord('z')):  # takes care of siclic pass Z
                charRes1 = ord(char) + key - (ord('z') - ord('a') + 1)
                new_string = new_string + chr(charRes1)
            elif (ord(char) + key < ord('a')):  # takes care of siclic pass A
                charRes2 = ord(char) + key + (ord('z') - ord('a') + 1)
                new_string = new_string + chr(charRes2)
            else:
                new_string = new_string + chr(ord(char) + key)
        else:
            new_string = new_string + char
    return new_string

class CaesarCipher:#
    def __init__(self,key):
        self.key=key%26

    def encrypt(self,string):
        new_string1=applayNewString(string,self.key)
        return new_string1
        #print(new_string1)

    def decrypt(self,string):
        new_string2=applayNewString(string,-self.key)
        return new_string2
        #print(new_string2)


#vigenere stuff
#def vigenereHelper(string,list,flag,index):
 #   new_str1 = ''
  #  sizeOfList = len(list)
   # for char in string:
    #    if (index >= sizeOfList):
      #      index = 0
     #   if(flag):#when we decrypt
       #     new_str1 += applayNewString(char, -list[index])
        #if(not flag):
         #   new_str1 += applayNewString(char, list[index])
        #if (not (checkIfUper(char) or checkIfLower(char))):
         #   continue
        #index+=1
    #return new_str1

def changeCharToInt(char):
    if (checkIfUper(char)):
        return (ord(char)-ord('A'))
    else:
        return (ord(char)-ord('a'))

class VigenereCipher:
    index1=0
    index2=0
    def __init__(self,list):
        self.list=[elem%26 for elem in list]
        #VigenereCipher.index=0

    def encrypt(self,string):
        new_str=''
        sizeOfList=len(self.list)
        for char in string:
            if self.index1>=sizeOfList:
                self.index1=0
            new_str+=applayNewString(char,self.list[self.index1])
            if(not(checkIfUper(char) or checkIfLower(char))):
                continue
            self.index1+=1
        return new_str
        #new_str=vigenereHelper(string,self.list,False,self.index)
        #return new_str
    def decrypt(self, string):
        new_str1=''
        sizeOfList=len(self.list)
        for char in string:
            if self.index2>=sizeOfList:
                self.index2=0
            new_str1+=applayNewString(char,-self.list[self.index2])
            if(not(checkIfUper(char) or checkIfLower(char))):
                continue
            self.index2+=1
        return new_str1


        #new_str1=vigenereHelper(string,self.list,True,self.index)
        #return new_str1

def getVigenereFromStr(string):
    my_list=[]
    for char in string:
        if (not (checkIfUper(char) or checkIfLower(char))):#means char is not a letter
            continue
        my_list.append(changeCharToInt(char))

    vigenere_cipher = VigenereCipher(my_list)
    return vigenere_cipher


def iskeyStringOrList(var):
    if(type(var) is list):
        return True
    else:
        return False


def loadEncryptionSystem(dir_path):
    #with open('config.json','r')as f:
    config_path = os.path.join(dir_path, 'config.json')
    with open(config_path, 'r') as f:
        loaded_dict = json.load(f)
        if(loaded_dict["type"]=="Caesar"):
            CaesarFlag=True
        else:
            CaesarFlag = False
        if(loaded_dict["encrypt"]=='True'):#encrypte
            for filename in os.listdir(dir_path):
                if filename.endswith(".txt"):
                    #with open(filename,'r')as g:
                    file_path=os.path.join(dir_path, filename)
                    with open(file_path) as g:
                        if (CaesarFlag):
                            new_fileName = filename[:-4] + ".enc"
                            #with open(new_fileName, 'w') as h:
                            file_path1 = os.path.join(dir_path, new_fileName)
                            with open(file_path1, 'w') as h:
                                ceasar_cipher = CaesarCipher(loaded_dict["key"])
                                for line in g:
                                    h.write(ceasar_cipher.encrypt(line))
                                    #modifedLine = line + "\n"  # did this so it will go down a line not 100% sure
                                    #h.write(ceasar_cipher.encrypt(modifedLine))
                        else:
                            new_fileName = filename[:-4] + ".enc"
                            #with open(new_fileName, 'w') as h:
                            file_path1 = os.path.join(dir_path, new_fileName)
                            with open(file_path1, 'w') as h:
                                flagOfVigenere = iskeyStringOrList(loaded_dict["key"])
                                if (flagOfVigenere):
                                    vigenere_cipher = VigenereCipher(loaded_dict["key"])
                                else:
                                    vigenere_cipher = getVigenereFromStr(loaded_dict["key"])
                                for line in g:
                                    h.write((vigenere_cipher.encrypt(line)))
                                vigenere_cipher.index1=0
                                    #modifedLine = line + "\n"   did this so it will go down a line not 100% sure
                                    #h.write(vigenere_cipher.encrypt(modifedLine))

                else:
                    continue

        else:#this is for dycper
            for filename in os.listdir(dir_path):
                if filename.endswith(".enc"):
                    #with open(filename, 'r') as g:
                    file_path2 = os.path.join(dir_path, filename)
                    with open(file_path2,'r') as g:
                        if (CaesarFlag):
                            new_fileName = filename[:-4] + ".txt"
                            #with open(new_fileName, 'w') as h:
                            file_path3 = os.path.join(dir_path, new_fileName)
                            with open(file_path3, 'w') as h:
                                ceasar_cipher = CaesarCipher(loaded_dict["key"])
                                for line in g:
                                    h.write(ceasar_cipher.decrypt(line))
                        else:
                            new_fileName = filename[:-4] + ".txt"
                            #with open(new_fileName, 'w') as h:
                            file_path3 = os.path.join(dir_path, new_fileName)
                            with open(file_path3, 'w') as h:
                                flagOfVigenere = iskeyStringOrList(loaded_dict["key"])
                                if (flagOfVigenere):
                                    vigenere_cipher = VigenereCipher(loaded_dict["key"])
                                else:
                                    vigenere_cipher = getVigenereFromStr(loaded_dict["key"])
                                for line in g:
                                    h.write(vigenere_cipher.decrypt(line))
                                vigenere_cipher.index2 = 0

                else:
                     continue


# CaesarCipher TEST
#c=CaesarCipher(3)
#print(c.encrypt('Mtm is the BEST!'))
#print(c.decrypt('Pwp lv wkh EHVW!'))

#Vigenere TESTS
#V=VigenereCipher([3])
#print((V.encrypt('l')))
#print(V.decrypt('o'))

#v=VigenereCipher([2,-4,-14,-16,-17,-17])
#print(v.encrypt('we wish you best of luck in all of your exams'))
#print(v.decrypt('ya isbq akg lnbv kr vdlm ez kuu qb kyda gtmwb'))

#v=VigenereCipher([1,2,3,4,-5])
#print(v.encrypt('Hello World!'))
#print(v.decrypt('Igopj Xqupy!'))


#TODO this test was problematic when i had only one index
#v=getVigenereFromStr('python rules, C drools')
#print(v.encrypt('JK, C is awesome'))
#print(v.decrypt('YI, V pg nnydseg'))

#TODO we need to figure index behavior
#dir_path=r'C:\mtm2023\ex5\tests\output\797'
#loadEncryptionSystem(dir_path)
