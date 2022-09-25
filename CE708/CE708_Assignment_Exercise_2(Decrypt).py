# This function splits cipher text into groups of 2 letters
def SplitCipherText(CipherText):
    # Split the ciphertext every 2nd index 
    CipherTextFinal = " ".join(CipherText[i:i+2] for i in range(0, len(CipherText), 2))
    SplitCipherText = CipherTextFinal.split()
    return SplitCipherText


# This function creates playfair matrix using the key provided by the user
def CreateMatrix(Key):
    # Initialise lists and dictionaries for making the matrix
    Alphabet = list("abcdefghijklmnopqrstuvwxyz")
    Matrix = []
    count = {}
    Unsplit = []
    N = 1
    # For each character in the key, if its only appeared once, add it to a list
    for i in Key:
        if i not in count:
            Unsplit.append(i)
            count[i] = 1
        else:
            pass
    # When Key is finished, for each letter in alphabet, if it's not already appeared
    # add it to the list
    for i in Alphabet:
        if i not in count:
            Unsplit.append(i)
            count[i] = 1
        else:
            pass
    # Split the list into 5 strings(rows) each containing 5 chronological characters from the list
    Row1 = "".join(Unsplit[0:5])
    Row2 = "".join(Unsplit[5:10]) 
    Row3 = "".join(Unsplit[10:15])
    Row4 = "".join(Unsplit[15:20])
    Row5 = "".join(Unsplit[20:25])
    # Create a list of strings acting as our playfair matrix
    Matrix = [Row1, Row2, Row3, Row4, Row5]
    return Matrix


# This function decrypts the plaintext using the opposite first two rules
# The third rule is interchangeable
def Decrypt(Matrix, SplitCipherText):
    print(Matrix)
    print(SplitCipherText)
    DecryptedMessage = ""
    #for each pair of letters in the SplitCipherText
    for x in SplitCipherText:
        Letters_added = False
        # if they are in the same row, replace each with the letter to its left
        for row in Matrix:
            if x[0] in row and x[1] in row:
                Letters_added = True
                DecryptedLetters = row[(row.find(x[0]) - 1) % 5] + row[(row.find(x[1]) - 1) % 5]
                DecryptedMessage = DecryptedMessage + DecryptedLetters
        if Letters_added == True:
            continue

        # if they are in the same column replace each with the letter above it
        for counter in range(5):
            Column = "".join([Matrix[i][counter] for i in range(5)])
            if x[0] in Column and x[1] in Column:
                Letters_added = True
                DecryptedLetters = Column[(Column.find(x[0]) - 1) % 5] + Column[(Column.find(x[1]) - 1) % 5]
                DecryptedMessage = DecryptedMessage + DecryptedLetters
        if Letters_added == True:
            continue

        # it rule 1 and 2 not applied
        # replace each with letter we'd get if column indices were swapped
        FirstLetterOriginal = 0
        SecondLetterOriginal = 0
        FirstLetterChange = 0
        SecondLetterChange = 0
        for i in range(5):
            row = Matrix[i]
            if x[0] in row:
                FirstLetterOriginal = i
                FirstLetterChange = row.find(x[0])
            if x[1] in row:
                SecondLetterOriginal = i
                SecondLetterChange = row.find(x[1])
        DecryptedLetters = Matrix[FirstLetterOriginal][SecondLetterChange] + Matrix[SecondLetterOriginal][FirstLetterChange]
        DecryptedMessage = DecryptedMessage + DecryptedLetters
    return DecryptedMessage


# This function removes any digram "x"'s from the body of the decrypted message
def RemoveX(DecryptedMessage):
    List = list()
    # for each character in decrypted message, if x between double letters detected
    # then remove the x otherwise, append to List
    for c in DecryptedMessage:
        if c not in List:
            List.append(c)
        else:
            if c == List[-2] and List[-1] == "x":
                List.remove(List[-1])
                List.append(c)
            else:
                List.append(c)
    PlainTextFinal = "".join(List)
    print(PlainTextFinal)    
    

# obtain user input for CipherText and key and then apply the relevant functions
CipherText = input("Please enter the Encrypted Message you wish to decrypt: ")
Key = input("Please enter the key you wish to use: ")
Answer = Decrypt(CreateMatrix(Key), SplitCipherText(CipherText))
RemoveX(Answer)


