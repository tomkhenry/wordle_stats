# Author: Tom Henry
# A wordle support program to help beat your friends!

# class taken from https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def gen_word_list():
    import nltk
    nltk.download('words')
    fd = open("wordle_words.txt", "a")
    word_list = [word for word in  nltk.corpus.words.words() if len(word) == 5]
    for valid_word in word_list:
        fd.write(f'{valid_word}\n')

def update_word_list(inword, notin, current, words):
    #update the words list with the letters that work
    for index, green in enumerate(current):
        if green != '':
            words = set(filter(lambda x: x[index]==green, words))
    
    for letter in inword:
        words = set(filter(lambda y: letter in y, words))

    for bad in notin:
        words = set(filter(lambda z: bad not in z, words))

    return words


def wordle_helper(guess_list, winning_word):
    import pathlib
    #read in the possible five letter words
    word_file = open(str(pathlib.Path(__file__).parent.absolute()) + "/wordle_words.txt", "r")
    word_raw_txt = word_file.read()
    words = set((word_raw_txt.split("\n"))[:-1])
     
    #save used letters
    used_letters = set()
    current = ['','','','','']
    inword = set()
    notin = set()

    total_score = 0
    
    for turn in range(1,7,1):
        guess = guess_list[turn-1]
        for index, letter in enumerate(guess):
            if letter == winning_word[index]:
                current[index] = letter
                inword.add(letter)
            elif letter in winning_word:
                inword.add(letter)
            else:
                if letter not in inword:
                    notin.add(letter)

        #check if they won
        prev_len = len(words)
        words = update_word_list(inword, notin, current, words)
        new_len = len(words)
        score = (1 - (new_len/prev_len)) * 100
        total_score += score

        print(f"Your guess score for word {bcolors.BOLD}{guess}{bcolors.ENDC} is rated: {bcolors.OKCYAN}{score:.2f}{bcolors.ENDC}")

        if '' not in current:
            print(f"\n{bcolors.HEADER}Congratulations! You solved this in {turn} rounds!{bcolors.ENDC}\n")
            total_score += 200 * (6-turn)
            print(f'Your Wordle performance score is: {bcolors.OKGREEN}{bcolors.BOLD}{total_score:.2f}{bcolors.ENDC}')
            break


def main():
    while(1):
        winning_word = input("Enter the winning word of the day: ")
        if len(winning_word) != 5:
            print(f"{bcolors.WARNING}Word must be 5 characters long!{bcolors.ENDC}")
            continue
        else:
            break

    guesses = list()
    while(1):
        guess = input("Enter guessed word: ")
        if len(guess) != 5:
            print(f"{bcolors.WARNING}Word must be 5 characters long!{bcolors.ENDC}")
            continue
        guesses.append(guess)
        if guess == winning_word:
            break
    wordle_helper(guesses, winning_word)

main()
