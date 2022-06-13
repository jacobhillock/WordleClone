from colors import colors
from words import Words

def correct(letter):
    return f"{colors.fg.lightgrey}{colors.bg.green} {letter} {colors.reset}"
def not_present(letter):
    return f"{colors.fg.lightgrey}{colors.bg.black} {letter} {colors.reset}"
def wrong_spot(letter):
    return f"{colors.fg.darkgrey}{colors.bg.yellow} {letter} {colors.reset}"

def replace_next_empty(result_list, to_place):
    for j in range(len(result_list)):
        if result_list[j] == '':
            result_list[j] = to_place
            break
    return result_list

def checker(answer, guess):
    result = []
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            result += [correct(guess[i])]
        else:
            result += ['']
    
    rem_guess = ''.join([guess[i] for i in range(len(guess)) if result[i]==''])
    rem_answer = ''.join([answer[i] for i in range(len(answer)) if result[i]==''])

    for i in range(len(rem_guess)):
        if rem_guess[i] in rem_answer:
            rem_answer = rem_answer.replace(rem_guess[i], '', 1)
            result = replace_next_empty(result, wrong_spot(rem_guess[i]))
        else:
            result = replace_next_empty(result, not_present(rem_guess[i]))


    return ''.join(result)

def get_guess(word_bank):
    guess = ''
    while not word_bank.check_word(guess):
        guess = input('Five letter word guess: ')

    return guess

def main():
    word_bank = Words()
    word = word_bank.get_word()
    guess = ''
    count = 0
    while (count < 6):
        guess = get_guess(word_bank)
        print(">>>" + checker(word, guess) + "<<<")
        if word == guess:
            print('Yay')
            break
        count += 1
    if count == 6:
        print(f"saad, word is: {word}")

if __name__ == '__main__':
    main()