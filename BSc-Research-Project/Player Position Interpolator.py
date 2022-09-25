# Final function responsible for calculating proportions
# and relocating players onto a virtual court for
# redisplay
def Final(Filename) :
    x = open(Filename, "r")
    j = open("RightCourtPosition.txt", "w")
    # Footage court dimension coordinates
    CourtTopLeftY = 4
    CourtTopLeftX = 138
    CourtTopRightY = 638
    CourtTopRightX = 150
    CourtBotLeftY = -167
    CourtBotLeftX = 26
    CourtBotRightY = 870
    CourtBotRightX = 50
    PlayerID = 1

    for aline in x:
        DocumentValue = aline.split()
        # For every value that isn't a frame marker calculate the proportion
        # along the top, the bottom and across the court
        if DocumentValue[0] != "start-frame" and DocumentValue[0] != "end-frame":
            Playerx = float(DocumentValue[0])
            PlayerY = 360 - float(DocumentValue[1])
            XProportionTop = Playerx / (CourtTopRightY - CourtTopLeftY)
            XProportionBot = Playerx / (CourtBotRightY - CourtBotLeftY)
            AverageXProportion = (XProportionTop + XProportionBot) / 2
            YProportion = PlayerY / (180 - CourtBotLeftX)

            # Interpolate the player position along the court 
            VolleyBallX = (60 * AverageXProportion)
            NFVolleyBallX = -30 + VolleyBallX
            FVolleyBallX = str(NFVolleyBallX)
            
            # Interpolate the player position across the court
            VolleyBallY = (30 * YProportion)
            NFVolleyBallY = 15 - VolleyBallY
            ACROSSCOURT = str(NFVolleyBallY)
            
            # Write the results in a format the is valid in the
            # Visualization program
            j.write("red " + str(PlayerID) + " " + ACROSSCOURT + " " + FVolleyBallX + "\n")
            PlayerID += 1
        else:
            j.write(DocumentValue[0] + "\n")
    x.close()
    j.close()


Final('FINALRESULTS.txt')


