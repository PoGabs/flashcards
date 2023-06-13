import numpy as np
import random
import os
import sys
import argparse

class LoggerOut:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.filename = filename

    def write(self, message):
        self.terminal.write(message)
        with open(self.filename, "a") as file:
            print(message, file=file, flush=True, end='')

    def flush(self):
        pass


class LoggerIn:
    def __init__(self, filename):
        self.terminal = sys.stdin
        self.filename = filename

    def readline(self):
        entry = self.terminal.readline()
        with open(self.filename, "a") as file:
            print(entry.rstrip(), file=file, flush=True)
        return entry


default_log = "default.txt"
sys.stdout = LoggerOut(default_log)
sys.stdin = LoggerIn(default_log)

list_of_flashcards = []
flashcard_dictionary = {}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="", description="")
    parser.add_argument("--import_from", type=str,
                        help="")
    parser.add_argument("--export_to", type=str,
                        help="")
    args = parser.parse_args()
if args.import_from:
    import_file_name = args.import_from
    npy_file_name = import_file_name + ".npy"
    try:
        os.rename(import_file_name, npy_file_name)
    except FileNotFoundError:
        print("File not found.")
    else:
        try:
            imported = np.load(npy_file_name, allow_pickle="TRUE").item()
        except FileNotFoundError:
            print("File not found.")
        else:
            for i in imported:
                flashcard_dictionary[i] = imported.get(i)
            os.rename(npy_file_name, import_file_name)
            print(str(len(imported)) + " cards have been loaded.")


class flashcard(object):
    def __int__(self, term, definition):
        self.term = term
        self.definition = definition

menu_options = ("add", "remove", "import", "export", "ask", "exit", "log", "hardest card", "reset stats")
while True:
    print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
    user_input = input()
    if user_input == menu_options[0]:
        while True:
            term = input()
            if term in flashcard_dictionary.keys():
                print(f"The term \"{term}\" already exists. Try again:")
                continue
            else:
                break
        while True:
            definition = input()
            list_of_values_and_error_rates = list(flashcard_dictionary.values())
            list_of_only_values = []
            for i in list_of_values_and_error_rates:
                list_of_only_values.append(i[0])
            if definition in list_of_only_values:
                print(f"The definition \"{definition}\" already exists. Try again:")
                continue
            else:
                break
        flashcard_dictionary[term] = [definition, 0]
        print(f"The pair(\"{term}\":\"{definition}\") has been added.")
    elif user_input == menu_options[1]:
        print("Which card?")
        user_input = input()
        if user_input in flashcard_dictionary.keys():
            flashcard_dictionary.pop(user_input)
            print("The card has been removed.")
        else:
            print(f"Can't remove \"{user_input}\": there is no such card.")
    elif user_input == menu_options[2]:
        print("File name:")
        user_input = input()
        npy_file_name = user_input + ".npy"
        try:
            os.rename(user_input, npy_file_name)
        except FileNotFoundError:
            print("File not found.")
        else:
            try:
                imported = np.load(npy_file_name, allow_pickle="TRUE").item()
            except FileNotFoundError:
                print("File not found.")
            else:
                for i in imported:
                    flashcard_dictionary[i] = imported.get(i)
                os.rename(npy_file_name, user_input)
                print(str(len(imported)) + " cards have been loaded.")
    elif user_input == menu_options[3]:
        print("File name:")
        user_input = input()
        np.save(user_input, flashcard_dictionary)
        npy_file_name = user_input + ".npy"
        os.rename(npy_file_name, npy_file_name[0:len(npy_file_name) - 4])
        print(str(len(flashcard_dictionary)) + " cards have been saved.")
    elif user_input == menu_options[4]:
        number_of_cards = int(input("How many times to ask?\n"))
        pairs = []
        counter = 0
        while counter < number_of_cards:
            a, b = random.choice(list(flashcard_dictionary.items()))
            pairs.append((a, b[0]))
            counter += 1
        for pair in pairs:
            print("Print the definition of " + "\"" + pair[0] + "\"")
            user_input = input()
            if user_input == pair[1]:
                print("Correct!")
            else:
                flashcard_dictionary[pair[0]][1] += 1
                list_of_values_and_error_rates = flashcard_dictionary.values()
                list_of_only_values = []
                for i in list_of_values_and_error_rates:
                    list_of_only_values.append(i[0])
                if user_input in list_of_only_values:
                    equivalent_key = list(flashcard_dictionary.keys())[
                        list_of_only_values.index(user_input)]
                    print(
                        f"Wrong. The right answer is \"{pair[1]}\", but your definition is correct for \"{equivalent_key}\"")
                else:
                    print("Wrong. The right answer is " + "\"" + pair[1] + "\"")
    elif user_input == menu_options[5]:
        print("Bye bye!")
        if __name__ == '__main__' and args.export_to:
            export_file_name = args.export_to
            np.save(export_file_name, flashcard_dictionary)
            npy_file_name = export_file_name + ".npy"
            try:
                os.rename(npy_file_name, npy_file_name[0:len(npy_file_name) - 4])
            except FileExistsError:
                os.remove(npy_file_name[0:len(npy_file_name) - 4])
                os.rename(npy_file_name, npy_file_name[0:len(npy_file_name) - 4])
            print(str(len(flashcard_dictionary)) + " cards have been saved.")
        exit()
    elif user_input == menu_options[6]:
        print("File name:")
        log_file_name = input()
        try:
            os.rename("default.txt", log_file_name)
        except FileExistsError:
            os.remove(log_file_name)
            os.rename("default.txt", log_file_name)
        print("The log has been saved.")
    elif user_input == menu_options[7]:
        list_of_card_names_and_mistake_scores = []
        for i in flashcard_dictionary:
            list_of_card_names_and_mistake_scores.append((flashcard_dictionary[i][1], flashcard_dictionary[i][0]))
        if len(list_of_card_names_and_mistake_scores) == 0:
            print("There are no cards with errors.")
            continue
        list_of_card_names_and_mistake_scores.sort()
        if list_of_card_names_and_mistake_scores[-1][0] == 0:
            print("There are no cards with errors.")
        else:
            list_of_error_numbers = []
            for i in list_of_card_names_and_mistake_scores:
                list_of_error_numbers.append(i[0])
            how_many_times_the_biggest_integer_appears = list_of_error_numbers.count(list_of_error_numbers[-1])
            if how_many_times_the_biggest_integer_appears > 1:
                list_of_cards_with_highest_error_rate = []
                counter = -1
                while counter >= how_many_times_the_biggest_integer_appears * -1:
                    list_of_cards_with_highest_error_rate.append(list_of_card_names_and_mistake_scores[counter][1])
                    counter = counter - 1
                print("The hardest cards are ", end="")
                print(*('"{}"'.format(item) for item in list_of_cards_with_highest_error_rate), sep=', ', end=".")
                print(" You have ", list_of_error_numbers[-1], " errors answering them.", sep="")
            elif how_many_times_the_biggest_integer_appears == 1:
                hardest_card_term = list(flashcard_dictionary.keys())[
                        list(flashcard_dictionary.values()).index([list_of_card_names_and_mistake_scores[-1][1], list_of_card_names_and_mistake_scores[-1][0]])]
                print(f"The hardest card is \"{hardest_card_term}\". You have {str(list_of_card_names_and_mistake_scores[-1][0])} errors answering it.")

    elif user_input == menu_options[8]:
        for i in flashcard_dictionary:
            reset_item = [flashcard_dictionary.get(i), 0]
            flashcard_dictionary[i] = reset_item
        print("Card statistics have been reset.")
