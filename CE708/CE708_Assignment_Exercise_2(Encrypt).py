# This function deals with any digrams and splits the result into groups of 2 letters
def SplitPlainText(Plaintext):
    # Remove any spaces from the plaintext 
    Plaintext = Plaintext.replace(" ", "")
    List = list()
    # Add each character of the plaintext to List and pad double letters with "x"
    for c in Plaintext:
        if c not in List:
            List.append(c)
        else:
            if c == List[-1]:
                List.append("x" + c)
            else:
                List.append(c)
    # Join the list, group in twos and then split the list again
    PlainTextFinal = "".join(List)
    PlainTextFinal = " ".join(PlainTextFinal[i:i+2] for i in range(0, len(PlainTextFinal), 2))
    SplitPlainText = PlainTextFinal.split()
    # If the last element in the list is single, pad it with an "x"
    if len(SplitPlainText[-1]) == 1:
        SplitPlainText[-1] = SplitPlainText[-1]+"x"
    # Return the Plain Text in it's new padded and split form 
    return SplitPlainText


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


# This function encrypts the plaintext using the three rules 
def Encrypt(Matrix, SplitPlainText):
    print(Matrix)
    print(SplitPlainText)
    EncryptedMessage = ""
    #for each pair of letters in the SplitPlainText
    for x in SplitPlainText:
        Letters_added = False
        # if they are in the same row, replace each with the letter to its right
        for row in Matrix:
            if x[0] in row and x[1] in row:
                Letters_added = True
                EncryptedLetters = row[(row.find(x[0]) + 1) % 5] + row[(row.find(x[1]) + 1) % 5]
                EncryptedMessage = EncryptedMessage + EncryptedLetters
        if Letters_added == True:
            continue 

        # if they are in the same column replace each with the letter below it
        for counter in range(5):
            Column = "".join([Matrix[i][counter] for i in range(5)])
            if x[0] in Column and x[1] in Column:
                Letters_added = True
                EncryptedLetters = Column[(Column.find(x[0]) + 1) % 5] + Column[(Column.find(x[1]) + 1) % 5]
                EncryptedMessage = EncryptedMessage + EncryptedLetters
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
        EncryptedLetters = Matrix[FirstLetterOriginal][SecondLetterChange] + Matrix[SecondLetterOriginal][FirstLetterChange]
        EncryptedMessage = EncryptedMessage + EncryptedLetters

    # print the fully encrypted message
    print(EncryptedMessage)                    

# obtain user input for plaintext and key and then apply the relevant functions
Plaintext = input("Please enter the plaintext you wish to encrypt: ")
Key = input("Please enter the key you wish to use: ")
Encrypt(CreateMatrix(Key), SplitPlainText(Plaintext))
