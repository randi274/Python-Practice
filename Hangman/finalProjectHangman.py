__author__ = 'Randi'

from tkinter import *
from tkinter import ttk
import random, json
#import sqlite3, time

class makeHangman:
    def __init__(self, master):

        self.canvas = Canvas(master, width = 250, height = 300, background='yellow')
        self.canvas.grid(rowspan=5, column=2, columnspan = 2, padx = 10, pady = 10)

        self.initHangman()

        ttk.Label(master, text = "Choose a category and click 'Start' to begin!").grid(
            row = 0, columnspan = 2, padx = 10, pady = 5, sticky=(S))

        with open('hangmandict.json') as data_file:
            self.wordDict = json.load(data_file)

        optionList = ["Animals","Food","Games","Cities"]

        self.varOption = StringVar(master)
        self.varOption.set(optionList[0])

        w = OptionMenu(master, self.varOption, *optionList)
        w.grid(row=1, column = 0, padx=5, pady=5)

        ttk.Button(master, text = "Start", command=self.startGame).grid(
            row = 1, column = 1, padx = 10, pady = 5)

        guessedLetterLabel = ttk.Label(master, text="Input letter: ").grid(row=3,column=0, padx=10, pady=10, sticky=(S))
        self.guessLetterVar = StringVar(master)
        self.guessedLetterEntry = ttk.Entry(master, textvariable = self.guessLetterVar)
        self.guessedLetterEntry.grid(row=3, column=1, padx = 10, pady = 10, sticky=(S))

        self.guessButton = Button(master, text="Guess", state=DISABLED, command=self.guess)
        self.guessButton.grid(row=4, columnspan=2, padx = 10, pady=10, sticky=(W, E, N))

        self.guessMessage = StringVar()
        ttk.Label(master, textvariable=self.guessMessage, justify=CENTER).grid(row=5, columnspan=2, padx=5, pady =5)

        self.displayWord = StringVar()
        ttk.Label(master, textvariable = self.displayWord,
                  font=(14)).grid(row=5, column = 2, columnspan =2,padx = 10, pady = 10)

        self.incorrectLabel = StringVar()
        ttk.Label(master, textvariable = self.incorrectLabel).grid(row=6, column=2, padx=5, pady=5)
        self.displayIncorrect = StringVar()
        ttk.Label(master, textvariable=self.displayIncorrect).grid(row=7, column=2, padx=5, pady =5)

        self.remainingLabel = StringVar()
        ttk.Label(master, textvariable = self.remainingLabel).grid(row=6, column=3, padx=5, pady=5)
        self.guessesRemaining = StringVar()
        ttk.Label(master, textvariable=self.guessesRemaining).grid(row=7, column=3, padx=5, pady =5)

    def initHangman(self):
        self.canvas.create_line(30, 50, 200, 50, width=3) #top
        self.canvas.create_line(30, 50, 30, 250, width=3) #post
        self.canvas.create_line(5, 250, 130, 250, width=4) #floor
        self.canvas.create_line(30, 90, 70, 50, width=2) #triangle
        self.canvas.create_line(200, 50, 200, 70) #noose


    def updateHangman(self):

        if self.guesses == 5:
            self.canvas.create_oval(180, 70, 220, 110, width=2)
        elif self.guesses == 4:
            self.canvas.create_line(200, 110, 200, 200, width=2)
        elif self.guesses == 3:
            self.canvas.create_line(200, 130, 170, 170, width=2)
        elif self.guesses == 2:
            self.canvas.create_line(200, 130, 230, 170, width=2)
        elif self.guesses == 1:
            self.canvas.create_line(200, 200, 230, 250, width=2)
        elif self.guesses == 0:
            self.canvas.create_line(200, 200, 170, 250, width=2)
            self.canvas.create_line(0, 0, 250, 300, width=5, fill="red")
            self.canvas.create_line(250, 0, 0, 300, width=5, fill="red")

    def startGame(self):

        #get the game word and mask it for display
        category = self.varOption.get()
        categoryList = self.wordDict[category]
        self.gameWord = random.choice(categoryList)

        self.hiddenWord = '_'*len(self.gameWord)
        self.displayHiddenWord = '_ '*len(self.gameWord)
        self.listHiddenWord = list(self.hiddenWord)
        self.displayWord.set(self.displayHiddenWord)
        #used for testing: print(self.gameWord, self.hiddenWord)

        #reset canvas
        self.canvas.delete(ALL)
        self.canvas.config(background="yellow")
        self.initHangman()

        #reset states/variables of the app
        self.guessButton['state'] = 'active'
        self.guessMessage.set('')

        self.incorrectLetters = []
        self.displayIncorrect.set('')
        self.incorrectLabel.set("Incorrect Letters: ")

        self.guesses = 6 #head, body, arms + legs
        self.guessesRemaining.set(self.guesses)
        self.remainingLabel.set("Remaining Guesses: ")

    def guess(self):

        guessedLetter = self.guessLetterVar.get().lower()
        self.guessedLetterEntry.delete(0, 'end')

        if guessedLetter in self.gameWord:

            for i, j in enumerate(self.gameWord):
                if j==guessedLetter:
                    self.listHiddenWord[i] = guessedLetter

            newDisplay = ''.join(self.listHiddenWord)
            showDisplay = ' '.join(self.listHiddenWord)
            self.displayWord.set(showDisplay)

            ##check if user has won##
            if newDisplay == self.gameWord:
                self.guessMessage.set("You win!\n\nClick 'Start Game' to play again.")
                self.guessButton['state'] = 'disabled'
                self.canvas.config(background="green")
            else:
                self.guessMessage.set("You guessed correctly!")


        else:
            self.guesses -= 1
            self.guessesRemaining.set(self.guesses)
            self.incorrectLetters.append(guessedLetter)
            displayIncorrectStr = ', '.join(self.incorrectLetters)
            self.displayIncorrect.set(displayIncorrectStr)

            self.updateHangman()

            ##check if user has lost##
            if self.guesses == 0:
                self.guessMessage.set("You lose. Better luck next time!")
                self.guessButton['state'] = 'disabled'
                self.displayWord.set(self.gameWord)

            else:
                self.guessMessage.set("You guessed poorly!")


def main():
    root = Tk()
    root.title("Hangman")
    app = makeHangman(root)
    root.mainloop()

if __name__ == "__main__": main()

##nice to haves
# make pretty/fancy letters to select instead of input
# better designs?
#store a temp list of words that have been chosen