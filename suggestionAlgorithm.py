from webcolors import hex_to_rgb
from webcolors import CSS3_HEX_TO_NAMES

class suggestionAlgorithm:

    def __init__(self, AnalysisResult, image_folder):
        self.like = AnalysisResult.like
        self.dislike = AnalysisResult.dislike
        self.image_folder = image_folder
        self.aDict = AnalysisResult.aDict
        self.likeProfile = {}
        self.probaDict = {}
        self.calculateSizeLike()
        self.calculateOrientationLike()
        self.calculateColorLike()

    def calculateSizeLike(self):
        likeBig = 0
        likeSmall = 0
        likeMedium = 0

        for i in self.like:
            
            if i["Taille"] == "Big":
                likeBig += 1
            elif i["Taille"] == "Medium":
                likeMedium += 1
            elif i["Taille"] == "Small":
                likeSmall +=1

        for j in self.dislike:
            
            if j["Taille"] == "Big":
                likeBig -= 1
            elif j["Taille"] == "Medium":
                likeMedium -= 1
            elif j["Taille"] == "Small":
                likeSmall -=1
                
        self.likeProfile["Big"]= (likeBig/(1+len(self.like)+len(self.dislike)))
        self.likeProfile["Medium"]=(likeMedium/(1+len(self.like)+len(self.dislike)))
        self.likeProfile["Small"]=(likeSmall/(1+len(self.like)+len(self.dislike)))
    
    def calculateOrientationLike(self):
        likePortrait = 0
        likeLandscape = 0
        likeCarre = 0

        for i in self.like:
            if i['Orientation'] == "Portrait":
                likePortrait +=1
            elif i['Orientation'] == "Paysage":
                likeLandscape += 1
            elif i["Orientation"] == "Carre":
                likeCarre +=1
        for j in self.dislike:
            if j['Orientation'] == "Portrait":
                likePortrait -=1
            elif j['Orientation'] == "Paysage":
                likeLandscape -= 1
            elif j["Orientation"] == "Carre":
                likeCarre -=1

        self.likeProfile["Portrait"] = (likePortrait/(1+len(self.like)+len(self.dislike)))
        self.likeProfile["Paysage"] = (likeLandscape/(1+len(self.like)+len(self.dislike)))
        self.likeProfile["Carre"] = (likeCarre/(1+len(self.like)+len(self.dislike)))

    def calculateColorLike(self):
        colorLikeDict = {}
        for key in CSS3_HEX_TO_NAMES.items():
            colorLikeDict[key[1]] = 0
        for i in self.like:
            colorLikeDict[i["Couleur dominante 1"][0]] += 3/(len(self.like)+len(self.dislike))
            colorLikeDict[i["Couleur dominante 2"][0]] += 2/(len(self.like)+len(self.dislike))
            colorLikeDict[i["Couleur dominante 3"][0]] += 1/(len(self.like)+len(self.dislike))
            colorLikeDict[i["Couleur dominante 4"][0]] += 0.5/(len(self.like)+len(self.dislike))
            colorLikeDict[i["Couleur dominante 5"][0]] += 0.25/(len(self.like)+len(self.dislike))
        for j in self.dislike:
            colorLikeDict[i["Couleur dominante 1"][0]] -= 3/(len(self.like)+len(self.dislike))
            colorLikeDict[i["Couleur dominante 2"][0]] -= 2/(len(self.like)+len(self.dislike))
            colorLikeDict[i["Couleur dominante 3"][0]] -= 1/(len(self.like)+len(self.dislike))
            colorLikeDict[i["Couleur dominante 4"][0]] -= 0.5/(len(self.like)+len(self.dislike))
            colorLikeDict[i["Couleur dominante 5"][0]] -= 0.25/(len(self.like)+len(self.dislike))
        self.likeProfile["Colors"] = colorLikeDict
        
    def calculateLikeProbability(self):
        for item in self.aDict.items():
            
            probaScore = self.likeProfile[item[1]["Taille"]]+self.likeProfile[item[1]["Orientation"]]+self.likeProfile['Colors'][item[1]["Couleur dominante 1"][0]]
            self.probaDict[item[0]] = probaScore
        

    def suggestImage(self, image_name):
        if self.probaDict[image_name] > 1.5:
            return True
        else:
            return False