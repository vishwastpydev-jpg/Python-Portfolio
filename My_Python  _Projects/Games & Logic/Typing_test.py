import english_words 
from tkinter import *
import tkinter.font as font
import random
# from os import startfile # Not needed, as we are using a function for transition

# --- Global Variables ---
# These will be initialized properly in the startGame function.
score = 0
missed = 0
time = 0
count = 0
words = []

# Placeholders for the main game window (wn2) and its key widgets.
wn2 = None
timer = None
nextWord = None
userInput = None
scoreboard = None
scorelabel = None
timerlabel = None

# --- Main Game Functions ---

def timeFunc():
    """
    Updates the timer every second and handles the game-over state.
    It uses timer.after() for recursive scheduling.
    """
    global time, score, count, wn2, timer, nextWord, userInput, scorelabel, scoreboard, timerlabel
    
    # Check if the main game window still exists before proceeding.
    if wn2 is None or not wn2.winfo_exists():
        return

    if(count <= 20):
        # Continue timing
        time += 1
        timer.configure(text=time)
        timer.after(1000, timeFunc)
    else:
        # Game over condition (after 10 words have been processed/attempted)
        
        # Calculate missed words: total attempts (count - 1, since count starts at 0) minus correct score.
        missed_calculated = (count - 1) - score
        
        # Display Results
        result = Label(wn2, text='', font=('arial', 25, 'italic bold'), fg='grey', bg='honeydew2', justify=LEFT)
        result.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        result.configure(text=
            f'Time taken = {time}s\n'
            f'Score (Correct) = {score}\n'
            f'Missed (Incorrect/Skipped) = {missed_calculated}'
        )
        
        # Destroy all game control widgets
        nextWord.destroy()
        userInput.destroy()
        scorelabel.destroy()
        scoreboard.destroy()
        timerlabel.destroy()
        timer.destroy()


def mainGame(event):
    """
    Handles the game flow upon pressing the Enter key:
    1. Starts the timer on the first press.
    2. Checks the typed word against the target word.
    3. Moves to the next word.
    """
    global score, count, words, nextWord, userInput, scoreboard, time
    
    # 1. Start Condition (time == 0)
    if time == 0:
        # Show the first word (words[0])
        nextWord.configure(text=words[0])
        userInput.delete(0, END)
        timeFunc() # Start the timer
        return

    # 2. Process Input (After the game has started)
    # Check if the user's input matches the currently displayed word
    if userInput.get().strip() == nextWord['text'].strip():
        score += 1 
        scoreboard.configure(text=score)
        
    # 3. Move to the next word
    count += 1
    
    if(count <= 10):
        # Display the next word (words[1] through words[10])
        nextWord.configure(text=words[count])
        userInput.delete(0, END) # Clear the input box for the new word
    else:
        # Game over: timeFunc will handle final cleanup
        userInput.delete(0, END)
        userInput.configure(state='disabled') # Disable input


def startGame():
    """
    Fixes the application flow: Destroys the welcome window and initializes the main game window.
    """
    global score, missed, time, count, words, wn2, timer, nextWord, userInput, scoreboard, scorelabel, timerlabel
    
    # Destroy the welcome window (wn) to transition to the game
    wn.destroy() 
    
    # --- Initialize Global Variables ---
    score = 0
    missed = 0
    time = 0
    count = 0
    
    # *** CORRECTED FIX FOR THE TYPEERROR ***
    # We must provide the 'sources' argument. 'web2' is a good general dictionary.
    try:
        words = list(english_words.get_english_words_set(sources=['web2']))
    except Exception as e:
        print(f"Error loading words: {e}. Ensure the 'english-words' package is installed.")
        # Fallback to a small list if the package fails
        words = ['python', 'geeks', 'typing', 'test', 'error', 'word', 'list', 'failure', 'start', 'again', 'check']
        
    random.shuffle(words) # Initial shuffle of all words

    # --- Create Main Game Window (wn2) ---
    wn2 = Tk()
    wn2.geometry('700x600')
    wn2.title('Typing Test By Vishwas')
    wn2.config(bg='honeydew2')

    # Project Title
    Label(wn2, text='Typing Test By Vishwas', font=('arial', 25, 'italic bold'), fg='gray', width=40, bg='honeydew2').place(x=10, y=10)

    # Score Labels
    scorelabel = Label(wn2, text='Your Score:', font=('arial', 25, 'italic bold'), fg='red', bg='honeydew2')
    scorelabel.place(x=10, y=100)
    scoreboard = Label(wn2, text=score, font=('arial', 25, 'italic bold'), fg='blue', bg='honeydew2')
    scoreboard.place(x=100, y=180)
    
    # Timer Labels
    timerlabel = Label(wn2, text='Time Elapsed:', font=('arial', 25, 'italic bold'), fg='red', bg='honeydew2')
    timerlabel.place(x=500, y=100)
    timer = Label(wn2, text=time, font=('arial', 25, 'italic bold'), fg='blue', bg='honeydew2')
    timer.place(x=560, y=180)

    # Word/Instruction Label
    nextWord = Label(wn2, text='Hit ENTER to start and after typing the word', font=('arial', 20, 'italic bold'), fg='black', bg='honeydew2')
    nextWord.place(relx=0.5, rely=0.4, anchor=CENTER)

    # User Input Entry Box
    userInput = Entry(wn2, font=('arial', 25, 'italic bold'), bd=10, justify='center')
    userInput.place(relx=0.5, rely=0.6, anchor=CENTER, width=350)
    userInput.focus_set()

    # Bind the Enter key
    wn2.bind('<Return>', mainGame)
    
    # Start the main loop for the game window
    wn2.mainloop()

# ----------------------------------------
## 🏠 Welcome Window Initialization
# ----------------------------------------

# Creating the main window (wn) for the welcome screen
wn = Tk()
wn.geometry('600x600')
wn.title("Vishwas Typing Test")
wn.config(bg='LightBlue1')

# Title Frame
headingFrame1 = Frame(wn, bg="snow3", bd=5)
headingFrame1.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.16)

headingLabel = Label(headingFrame1, text="Welcome to \n Vishwas's Typing Test", bg='azure2', fg='black', font=('Courier', 15, 'bold'))
headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

# Start Button - calls startGame()
btn = Button(wn, text="Start", bg='old lace', fg='black', width=20, height=2, command=startGame)
btn['font'] = font.Font(size=12)
btn.place(x=200, y=300)

# Runs the Welcome screen loop until the user clicks 'Start' or closes the window
wn.mainloop()