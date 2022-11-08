import pickle


bestDistance = 807137
initialGuesses = [i for i in range(1, 824)][:4]


initialGFile = open("initialGuess.pickle", "wb")
pickle.dump(bestDistance, initialGFile)
pickle.dump(initialGuesses, initialGFile)
initialGFile.close()

print(bestDistance)
print(initialGuesses)
