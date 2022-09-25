# This function brute forces encrypted message with all possible keys
def Assignment_Exercise_1(message):
    # initialise an alphabet and keep a counter of which key is being used
    message = message.upper()
    Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    attempt = 0
    
    for x in range (26):
        # for each letter in the message apply caesar cipher using the attempt
        # number as the key, increment after every full iteration 
        for letter in message:
            if letter in Alphabet:
                letter_index = (Alphabet.find(letter) - attempt) % len(Alphabet)
                result = result + Alphabet[letter_index]
            else:
                result = result + letter
        #return the decrypted message on seperate lines for readability 
        result = result + " Key: " + str(x) + "\n" + "\n"
        attempt += 1
    return(result + "\n")

# Execute the above function using the encrypted message as the parameter
print(Assignment_Exercise_1("""vjg ugetgvu hqt dgkpi iqqf cv etarvqitcrja ku vq
rtcvkeg cp kpetgfkdng coqwpv qh jqwtu vtblqj
ghfubswlqj brxu rzq fbskhuwhaw zlwk udqgrp
qxpehuv dv nhbv. brx frxog xvh udqgrp nhb
bzizmvodji vgbjmdochn. oj wz xjindyzmzy vn v
hvnozm, v ojovg ja 10000 cjpmn dn mzlpdmzy"""))
