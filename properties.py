from os.path import exists

class Properties(object):
    def __init__(self):
        self.fileName = "properties.txt"
        self.mainScreen = [ 0, 0, 1920, 1080 ]
        self.mainScreenScale = 1.0
        self.subScreen = [ 0, 0, 1920, 1080 ]
        self.subScreenScale = 1.0
    def loadFile(self):
        # Creates a properties file if one is not found. 
        if not exists(self.fileName):
            self.saveFile() 
            return 

        properties = open(self.fileName, 'r')

        for line in properties.readlines():
            wordPair = Properties.seperate(line)

            if "Scale" in line:
                if "mainScreen" in line:
                    self.mainScreenScale = float(wordPair[1])
                else:
                    self.subScreenScale = float(wordPair[1])
            elif "mainScreen" in line:
                for i in range(len(self.mainScreen)):
                    variableName = Properties.generateScreenVariable(
                        "mainScreen", i)

                    # Checks if variable matches.
                    if wordPair[0] == variableName[:-1]:
                        # If so, copy the value to the array. 
                        self.mainScreen[i] = int(wordPair[1])
            elif "subScreen" in line:
                for i in range(len(self.subScreen)):
                    variableName = Properties.generateScreenVariable(
                        "subScreen", i)
                    
                    if wordPair[0] == variableName[:-1]:
                        self.subScreen[i] = int(wordPair[1])
            
        properties.close()
    def saveFile(self):
        properties = open(self.fileName, 'w')

        # Writes the top screen variables
        properties.write("# Refers to the top screen of the DS\n")
        properties.write(f"mainScreenScale={self.mainScreenScale}\n") 
        for i, element in enumerate(self.mainScreen):
            properties.write(Properties.generateScreenVariable("mainScreen", i)
                + str(element) + '\n')
        # Writes the bottom screen variables
        properties.write("\n# Refers to the bottom screen of the DS\n")
        properties.write(f"subScreenScale={self.subScreenScale}\n")
        for i, element in enumerate(self.subScreen):
            properties.write(Properties.generateScreenVariable("subScreen", i)
                + str(element) + '\n')

        properties.close() 
    @staticmethod
    def generateScreenVariable(name, index) -> str:
        # Generates the names of the variables in the properties file. 
        if index < 2:
            return f"{name}{'X' if index % 2 == 0 else 'Y'}="
        return name + ("Width=" if index == 2 else "Height=")
    @staticmethod 
    def seperate(string, symbol = '=') -> list:
        # Splits a string into 2 parts based on a seperator symbol. 
        symbolIndex = string.find(symbol)
        return [ 
            string[:symbolIndex if symbolIndex != -1 else len(string)],
            string[symbolIndex+1:] if symbolIndex != -1 else ""
        ]

properties = Properties() 