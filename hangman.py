"""Evil Hangman"""
import random

# Name: Swati Misra
# EID: SM83264

# Name: Sanjitha Venkata
# EID: sv28325

# Name of the dictionary file.
# Change to dictionary.txt for full version of the game.

#DICTIONARY_FILE = "smallDictionary.txt"
DICTIONARY_FILE = "dictionary.txt"
class Hangman:
    """
    Manages the details of Evil Hangman. This class keeps
    tracks of the possible words from a dictionary during
    rounds of hangman, based on guesses so far.
    """

    def __init__(self, words, debug=True):
        """
        Create a new Hangman from the provided set of words and phrases.
        :param words: A set with the words for this instance of Hangman.
        :param debug: True if we should print out debugging to terminal.
        """
        if words is not None and len(words) > 0:
            self.__words = words

        # print(words)
        self.__word_list = list(self.__words)
        self.__difficulty = None
        self.__player_guesses = []
        self.__debug = debug
        self.__num_guesses = 0
        self.__word_len = 0
        self.__current_pattern = ""
        self.__word_dict = {}
        self.__num_word_dict = {}
        # self.__running_word_list= []

    def num_words(self, length):
        """
        Get the number of words in this Hangman of the given length.
        :param length: The given length to check.
        :return: the number of words in the original Dictionary
        with the given length
        """
        word_count = 0
        self.__word_len = length
        self.__word_list=self.__words
        for word in self.__word_list:
            if len(word) == length:
                word_count += 1
        return word_count

    def prep_for_round(self, word_len, num_guesses, diff):
        """
        Get for a new round of Hangman.
        :param word_len: the length of the word to pick this time.
        :param num_guesses: the number of wrong guesses before the
        player loses the round.
        :param diff: The difficulty for this round.
        """
        self.__num_guesses = num_guesses
        self.__word_len = word_len
        self.__difficulty = diff.lower()
        self.__player_guesses=[]
        self.__current_pattern = self.__word_len*"-"
        #("prep for game- current pattern", self.__current_pattern)

        # for word in self.__words:
        #     if len(word) != self.__word_len:
        #         self.__words.remove(word)

        # file_path = DICTIONARY_FILE
        # file = open(file_path, 'r', encoding='utf-8')
        # self.__words = {line.strip() for line in file}
        # file.close()
        # print("length of self words",len(self.__words))
        # print("WORDS", self.__words)
        # print("WORDLIST", self.__word_list)

        self.__word_list = self.__words
        self.__word_list = [word for word in self.__word_list if len(word) == self.__word_len]
        # print("WORDS AFTER", self.__words)
        # print("WORDLIST AFTER", self.__word_list)

    def num_words_current(self):
        """
        The number of words still possible (active) based on the guesses so far.
        :return: the number of words that are still possibilities based on the
        original dictionary and the guesses so far.
        """
        # word_count = 0
        # for word in self.__words:
        #     if len(word) == self.__word_len:
        #         word_count += 1

        # add word_count being decremented after each guess
        return self.num_words(self.__word_len)

    def get_guesses_left(self):
        """
        Get the number of wrong guesses the user has left in
        this round (game) of Hangman.
        :return: the number of wrong guesses the user has left
        in this round (game) of Hangman.
        """
        return self.__num_guesses

    def get_guesses_made(self):
        """
        Return a string that contains the letters the user has guessed so far during this round.
        The characters in the string are in alphabetical order.
        The string is in the form [let1, let2, let3, ... letN].
        For example, if the user has guessed 'a', 'c', 'e', 's', 't',
        and 'z', the string would be '[a, c, e, s, t, z]'.

        :return: A string that contains the letters the user has guessed so far during this round.
        """
        guesses=self.__player_guesses[:]
        len_guesses=len(guesses)
        for i in range(len_guesses-1):
            for j in range(0, len_guesses - i - 1):
                if guesses[j] > guesses[j+1]:
                    guesses[j], guesses[j+1] = guesses[j +1], guesses[j]
        return guesses

    def already_guessed(self, guess):
        """
        Check the status of a character.
        :param guess: The character to check.
        :return: true if guess has been used or guessed this round of Hangman,
                false otherwise.
        """
        return guess in self.__player_guesses

    def get_pattern(self):
        """
        Get the current pattern. The pattern contains '-''s for
        unrevealed (or guessed) characters and the actual character
        for "correctly guessed" characters.
        :return: the current pattern.
        """
        #print("get pattern- current pattern", self.__current_pattern)
        return self.__current_pattern

    def make_guess(self, guess):
        """
        Update the game status (pattern, wrong guesses, word list),
        based on the given guess.
        :param guess: the current guessed character
        :return: a dict with the resulting patterns and the number of
        words in each of the new patterns.
        The return value is for testing and debugging purposes.
        """
        if self.__debug:
            self.debugging(guess)

        #UPDATED PATTERN
        #loop through dictionary, find key with longest list of words
        #current pattern = the key (The dashed pattern)
        #word list = the value

        # max_length = 0
        # counter = 0
            #MAKING WORD DICT
        self.get_map_pattern(guess) #creates self.__word_dict
        #print("word dict", self.__word_dict)

        #NEW DICTIONARY WITH Pattern : # of words
        #MAKING NUM WORD DICT
        self.__num_word_dict = {}
        #print("word dict in make guess:", self.__word_dict)
        for key, value in self.__word_dict.items():
            self.__num_word_dict[key]=len(value)
        #print("num word dict",self.__num_word_dict)
        #CREATING ENTRY_LIST for difficulty picking (call get_difficulty())
        entry_list=[]
        #fill with (word list length, pattern, word list)
        #then choose hardest or second hardest based on index
        #sort tuples after adding them all so its sorted by length then pattern

        #UPDATING PLAYER GUESSES LIST
        if guess not in self.__player_guesses:
            self.__player_guesses.append(guess)
            self.__num_guesses -= 1

        flipped_dict = {}
        dashed_dict = {}
        biggest_key=0
        biggest_dash_key = 0

        for key, value in self.__num_word_dict.items():
        #makes flipped dict: number of words of  pattern: the patterns
            if value not in flipped_dict:
                flipped_dict[value] = [key]
            else:
                flipped_dict[value].append(key)
        # print("flipped dict:", flipped_dict)
        # print("num word dict", self.__num_word_dict)
        #     #find biggest key in flipped dict, which is the biggest word list's length

        #new code
        entry_list = list(self.__word_dict.items())
        if self.get_difficulty(entry_list)==0:
            biggest_key = max(flipped_dict.keys()) # biggest_key = max(biggest_key, value)
        else:
            #if len(self.__player_guesses)>1:
            secondbiggest=self.sort(list(flipped_dict.keys()))
            if len(secondbiggest)>1:
                biggest_key = secondbiggest[-2]
            else:
                biggest_key=secondbiggest[0]
            # else:
            #     biggest_key = max(flipped_dict.keys()) # biggest_key = max(biggest_key, value)
        #end of new code

        # biggest_key = max(flipped_dict.keys()) # biggest_key = max(biggest_key, value)

        # if only one value, assign to current pattern and word list
        if len(flipped_dict[biggest_key])==1:
            self.__current_pattern=flipped_dict[biggest_key][0]
            # ADDED
            self.__word_list=self.__word_dict[flipped_dict[biggest_key][0]]
            #print("make guess biggest key after flipped dict:", biggest_key)
        # if multiple values, check which pattern (value) has most dashes, and
        # assign that to current pattern and assign word list to word_dict[currentpattern]=value
        else:
            for i in range(len(flipped_dict[biggest_key])):
                dash_count=0
                temp = flipped_dict[biggest_key][i] #pattern with biggest num
                #print("flipped dict at biggest key",flipped_dict[biggest_key] )
                # of words attached to it from flipped dict (basically biggest
                len_temp = len(temp)

                for j in range(len_temp): #iterates through every letter of each pattern
                    # key (length of word list):pattern)
                    if temp[j] == "-":
                        dash_count += 1
                # temp_count = dash_count
                #print("tempcount",temp_count)
                #make dashed_dict
                if dash_count not in dashed_dict:
                    dashed_dict[dash_count]=[temp]
                    #print("dashed dict not in:", dashed_dict)
                else:
                    dashed_dict[dash_count].append(temp)
                #print("dashed dict in:", dashed_dict)
            biggest_dash_key = max(dashed_dict.keys())
                #find biggest key (biggest amount of dashes in a pattern)
            #if only one pattern mapped to biggest dash key, set current pattern
            if len(dashed_dict[biggest_dash_key])==1:
                self.__current_pattern=dashed_dict[biggest_dash_key][0]
                #ADDED
                self.__word_list=self.__word_dict[dashed_dict[biggest_dash_key][0]]
                #print("make guess current pattern after flipped dict 2:", self.__current_pattern)
            else:
                    #if more than one pattern mapped to biggest dash key, set
                    # current pattern after sorting
                tempsort=self.sort(dashed_dict[biggest_dash_key])
                # print("after sorting", dashed_dict[biggest_dash_key])
                self.__current_pattern=tempsort[0]
                #ADDED, updates word list
                self.__word_list=self.__word_dict[tempsort[0]]
        #         #print("make guess current pattern after flipped dict 3:", self.__current_pattern)
        # print("flipped dict",flipped_dict)
        # print("dashed dict",dashed_dict)



        #UPDATED GUESSES
        # wrong_guesses = 0
        # if guess not in self.__player_guesses:
        #     self.__player_guesses.append(guess)
        #     self.__num_guesses -= 1
        if guess in self.__current_pattern:
            self.__num_guesses += 1

        #UPDATED WORD LIST
        # self.__running_word_list= self.__word_list[:]

        # for word in self.__word_list:
        #     if self.make_dash_pattern(word, guess) == self.__current_pattern\
        #           and word not in self.__running_word_list:
        #         self.__running_word_list.append(word)
        #         wrong_guesses+=1
        #     len_pattern = len(self.__current_pattern)
        #     for i in range(len_pattern):
        #         if word in self.__running_word_list and \
        #             self.__current_pattern[i]!=word[i] and self.__current_pattern[i]!="-":
        #             self.__running_word_list.remove(word)

        #     print("making dash pattern",self.make_dash_pattern(word,guess))
        # print("current pattern in make guess", self.__current_pattern)
        # print("RUNNING word list in make guess",self.__running_word_list)
        # print("WORD list in make guess", self.__word_list)


        # print("make guess after monster- current pattern", self.__current_pattern)


        return self.__num_word_dict




    def get_map_pattern(self, guess):
        """
        Precondition: guess has not been guessed before in this round.
        Postcondition: Returns a dictionary that maps patterns to a list of words that
        follow said pattern.
        :param guess: The current guessed character.
        :return: A dictionary that maps patterns to a list of words that follow said pattern.
        """
        self.__word_dict = {}
        # if guess not in self.__player_guesses:
        for word in self.__word_list:
            temp_key = self.make_dash_pattern(word, guess)
            # print("tempkey",temp_key)
            if temp_key in self.__word_dict:
                self.__word_dict[temp_key].append(word)
            else:
                self.__word_dict[temp_key] = [word]


        return self.__word_dict




    def make_dash_pattern(self, word, guess):
        """
        Precondition: guess has not been guessed before in this round, word is not None.
        Postcondition: Builds possible word patterns for each word based on the user's guess and
        the previous pattern.
       
        :param word: The word to build the pattern for.
        :param guess: The current guessed character.
        :return: The dash pattern for the given word based on the user's guess and the previous
        dash pattern.
        """


        dashed_word= "-"*self.__word_len
        dashed_word=list(dashed_word)
        #print("make dash pattern- current pattern", self.__current_pattern)
        if word is not None and guess not in self.__player_guesses:
            len_current_pattern = len(self.__current_pattern)
            for i in range(len_current_pattern):
                if guess == word[i] and dashed_word[i]=="-":
                    dashed_word[i]=guess
                for letter in self.__player_guesses:
                    if word[i] == letter:
                        dashed_word[i]=letter
            #print(word,"dashedword",dashed_word)
        return ''.join(dashed_word)




    def sort(self, entries):
        '''
        Return sorted data. When called by order_entries, entries will be tuples sorted
        by the number of words in the word list, then the number of dashes in the pattern,
        then the pattern, and finally the word list itself.
        Otherwise, entries will be any sortable list.
        You must make sure that your merge_sort method is generalized with the ability
        to also sort lists. You must implement merge sort.


        Precondition: entries must be a list of tuples
        (-size word list, -dash count, pattern, word list) OR any sortable list
        Postcondition: return sorted list of entries. If tuple, first sort by
        number of words in word list,
        then the dash amount in the pattern, next the lexicographic ordering for the pattern,
        and finally the word list itself
        :param entries: The Family tuples to sort or any sortable list.
        :returns: a new sorted list.
        '''
        if len(entries)<=1:
            return entries


        mid=len(entries)//2
        left=entries[:mid]
        right=entries[mid:]
        sort_left=self.sort(left)
        sort_right=self.sort(right)
        return self.merge(sort_left,sort_right)


    def merge(self, left, right):
        """merges"""
        sorted_list = []
        while(len(left) != 0 and len(right) != 0):
            if left[0] < right[0]:
                sorted_list.append(left[0])
                left.pop(0)
            else:
                sorted_list.append(right[0])
                right.pop(0)
        if len(left) != 0:
            sorted_list += left
        if len(right) != 0:
            sorted_list += right
        return sorted_list


    def order_entries(self, word_family):
        """
        Precondition: word_family is not None.
        Postcondition: For each key-value pair of (pattern, word list) in word_family, a Family
        tuple (-size word list, -dash count, pattern, word list) is created and added to a list.
        The entry list is then sorted based on the size of each word list, the number
        of characters revealed in the pattern, and the lexicographical ordering of the patterns.
       
        :param word_family: A dictionary containing patterns as keys and lists of words as values.
        :return: A sorted list of Entry tuples (-size word list, -dash count, pattern, word list).
        """
        family_tuple_list=[]
        dash_count = 0
        for key, value in word_family:
            len_key = len(key)
            for i in range(len_key):
                if key[i]=="-":
                    dash_count+=1

            family_tuple_list.append((len(value),dash_count,key,value))
        return family_tuple_list


    def get_diff(self, entries):
        """
        Precondition: entries is not None.
        Postcondition: Returns an integer that describes the state of the selection process
        of word list based on a player's turn and game difficulty.
        Returns a 2 if the AI CAN pick the 2nd hardest word list. For easy mode, it's
        every other valid guess. For medium, it's every 4th valid guess.
        Returns 1 if the AI SHOULD pick the 2nd hardest word list on easy/medium mode,
        but entries.size() <= 1, so it picks the hardest.
        Returns 0 if the AI is picking the hardest list.
       
        :param entries: A list of tuples () representing patterns and associated word lists.
        :return: An integer representing the state of the selection process.
        """
        if not entries:
            raise ValueError("Entries can't be None")
        medium_guess = 4
        easy_mode = "easy"
        medium_mode = "medium"
        # if len(self.__player_guesses)>1:
        if ((self.__difficulty == medium_mode and len(self.__player_guesses) % medium_guess == 0)
            or(self.__difficulty == easy_mode and len(self.__player_guesses) % 2 == 0)):
            if len(entries) > 1:
                return 2
            return 1
        return 0


    def get_difficulty(self, entries):
        """
        Precondition: entries is not None.
        Postcondition: Returns the index of the Entry tuple from the list that the AI
        will choose for its word list/family depending on the state of the selection process.
        :param entries: A list of Entry tuples representing patterns and associated word lists.
        #word dict
        :return: The index of the Entry tuple that the AI will choose.
        """
        if not entries:
            raise ValueError("Entries can't be None")
        diff = self.get_diff(entries)
        if diff == 2:
            return 1 #medium or easy
        return 0 #hard


    def get_secret_word(self):
        """
        Return the secret word this Hangman finally ended up picking
        for this round. You must sort your word list before picking a
        secret word. If there are multiple possible words left, one is
        selected at random. The seed should be initialized to 0 before picking.
        :return: return the secret word the manager picked.
        """
        secret_word = ""
        # print("running word list",self.__running_word_list)
        # print("current pattern",self.__current_pattern)

        self.__word_list=self.sort(self.__word_list)
        if len(self.__word_list)>1:
            random.seed(0)
            secret_word=random.choice(self.__word_list)
        else:
            secret_word=random.choice(self.__word_list)
            # print("secret word", secret_word)
            # len_secret_word=len(secret_word)
            # for i in range(len_secret_word):
            #     if self.__current_pattern[i]==secret_word[i] and self.__current_pattern[i]!="-":
            #         continue
            #     else:
            #         secret_word=random.choice(self.__running_word_list)

        return secret_word


    def debugging(self, entries):
        """
        Precondition: entries is not None.
        Postcondition: Prints out custom debugging messages about which word family
        and pattern is chosen depending on difficulty and player's turn.
        """
        sb = []
        diff = self.get_diff(entries)
        sb.append("DEBUGGING: ")
        if diff == 2:
            sb.append("Difficulty second hardest pattern and list.\n\n")
        elif diff == 1:
            sb.append("Should pick second hardest pattern this turn, "
                    + "but only one pattern available.\n")
            sb.append("\nDEBUGGING: Picking hardest list.\n")
        else:
            sb.append("Picking hardest list.\n")

        sb.append("DEBUGGING: New pattern is: ")
        sb.append(self.get_pattern())
        sb.append(". New family has ")
        sb.append(str(self.num_words_current()))
        sb.append(" words.")
        print(''.join(sb))
