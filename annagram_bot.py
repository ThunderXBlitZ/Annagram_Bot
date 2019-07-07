import random
import math
from threading import Timer

import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space

from src import anagram_engine, utils


class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)

        self._chat_id = ""
        self.state = utils.State.IDLE
        self.round = 0
        self.user_name_id = {}
        self.user_id_score = {}

        # round vars
        self.counter = 0
        self.question_list = []
        self.answer_list = []

        self.hint_given = False

        self.timer = Timer(1, print)  # empty Timer
        self.timer2 = Timer(1, print)

    def reset_round_vars(self):
        self.counter = 0
        self.question_list = []
        self.answer_list = []

        self.hint_given = False

    def init(self, initial_length=5, round=0):
        """
        Start a new round of questions
        """
        self.reset_round_vars()
        self.state = utils.State.RUNNING
        self.round = round

        inc = 0 if self.round < 3 else 1  # grow in difficulty after 3 rounds
        self.question_list, self.answer_list = self.create_words(initial_length+inc)
        bot.sendMessage(self._chat_id, utils.MsgTemplate.start_msg % str(self.round + 1), parse_mode="Markdown")
        self.display_question()

    def display_question(self):
        # words > 8 length are too tough to guess
        if len(self.question_list[self.counter]) < 8:
            question_msg = utils.MsgTemplate.question_msg % \
                           (str(self.counter + 1), " , ".join(list(self.question_list[self.counter])).upper())
        else:
            question_msg = utils.MsgTemplate.question_msg % \
                           (str(self.counter + 1), self.create_hint(self.answer_list[self.counter], num_hint=1))

        bot.sendMessage(self._chat_id, question_msg, parse_mode="Markdown")
        self.timer = Timer(25, self.display_hint, [self.answer_list[self.counter]], {})
        self.timer.start()
        self.timer2 = Timer(60, self.time_up)
        self.timer2.start()

    def check_answer(self, player_answer, player_id, player_username):
        """
        Check's players' answers. If correct, awards points to player and starts next question.
        If all questions ar answered, start the next round
        """

        answer = self.answer_list[self.counter]  # string

        # Optimization: don't check every msg received
        if len(player_answer) != len(answer):
            return

        elif player_answer.lower().strip() == answer:  # correct!
            if self.timer.isAlive(): self.timer.cancel()
            if self.timer2.isAlive(): self.timer2.cancel()

            '''
            # old scoring system
            if time.time() < self.time + 30:
                score = math.floor(len(answer) / 2)
            else:
                score = math.floor(len(answer) / 4)
            '''

            # new scoring system
            num_rounds = len(self.answer_list)
            if self.counter+1 == num_rounds:
                score = 3
            elif self.counter > math.floor(num_rounds*2/3):
                score = 2
            else:
                score = 1

            # register/update user
            if player_id not in self.user_name_id.keys():
                self.user_name_id[player_id] = player_username

            if player_id in self.user_id_score.keys():
                self.user_id_score[player_id] += score
            else:
                self.user_id_score[player_id] = score

            response = utils.MsgTemplate.answer_msg % (self.user_name_id[player_id], score)
            bot.sendMessage(self._chat_id, response, parse_mode="Markdown")

            self.counter += 1
            if self.counter < len(self.answer_list):
                self.display_question()
            else:
                self.round_completed()

    def round_completed(self):
        """
        After a round is completed ,reset variables and prompt user to continue/stop
        """
        self.reset_round_vars()
        self.state = utils.State.ROUND_END
        msg = utils.MsgTemplate.round_completed_msg % str(self.gen_results_str())
        bot.sendMessage(self._chat_id, msg, parse_mode="Markdown")

    def stop(self):
        """
        Stops the bot and display scores to players. Player data is not saved
        """
        if self.timer.isAlive(): self.timer.cancel()
        if self.timer2.isAlive(): self.timer2.cancel()
        self.reset_round_vars()
        self.state = utils.State.IDLE
        msg = utils.MsgTemplate.stop_msg % str(self.gen_results_str())
        bot.sendMessage(self._chat_id, msg, parse_mode="Markdown")

    # Superclass function, invoked by Telepot framework upon receiving a new message
    def on_chat_message(self, msg):
        """
        Main function for handling player input. Makes decision on what to do
        :param msg: player's Telegram msg
        """
        # get user details
        user_id = msg["from"]["id"]
        sender_username = "Unknown username"

        if "first_name" in msg["from"]:
            sender_username = msg["from"]["first_name"]

        content_type, _chat_type, chat_id = telepot.glance(msg)
        if self._chat_id == '':  # record chat_id to make responses
            self._chat_id = chat_id

        # make response
        if content_type == 'text':
            if msg['text'] == "/help":
                self.display_help()

            elif msg['text'] == "/rules":
                self.display_rules()

            elif self.state == utils.State.IDLE:
                if msg['text'] == "/start":
                    self.init()

            elif self.state == utils.State.RUNNING:
                if msg['text'] == "/stop":
                    self.stop()
                else:
                    self.check_answer(msg['text'], user_id, sender_username)

            elif self.state == utils.State.ROUND_END:
                if msg['text'] == "/next":
                    self.init(round=self.round+1)
                if msg['text'] == "/stop":
                    self.stop()

    # Overwrite parent class (ChatHandler)'s on_close function to create timeout message
    def on_close(self, ex):
        if self.timer.isAlive(): self.timer.cancel()
        if self.timer2.isAlive(): self.timer2.cancel()

        if self.state == utils.State.RUNNING:
            msg = utils.MsgTemplate.timeout_msg_1 % "The answer is '*{}*'".format(self.answer_list[self.counter]) + "!"
            bot.sendMessage(self._chat_id, msg, parse_mode="Markdown")
        elif self.state == utils.State.IDLE:
            pass
        else:
            bot.sendMessage(self._chat_id, utils.MsgTemplate.timeout_msg_2, parse_mode="Markdown")
        super(MessageCounter, self).on_close(ex)

    # Timer functions
    def display_hint(self, answer):
        msg = utils.MsgTemplate.hint_msg % self.create_hint(answer)
        bot.sendMessage(self._chat_id, msg, parse_mode="Markdown")

    def time_up(self):
        bot.sendMessage(self._chat_id, utils.MsgTemplate.timeout_msg_0, parse_mode="Markdown")
        self.counter += 1
        if self.counter < len(self.answer_list):
            self.display_question()
        else:
            self.round_completed()

    # Helper functions
    def create_words(self, initial_length):
        """
        Creates list of words and scrambles them for player to answer
        Currently using 5 words of length 5, 4 words of length 6, 3 of length 7, 2 of length 8, 1 of length 9.
        Total 15 words per round.
        :return: list of scrambled words, list of answers
        """

        answer_list = anagram_engine.get_set_of_words(utils.Config.DATA_PATH, initial_length)
        question_list = []
        for word in answer_list:
            word_chars = list(word)
            while word_chars == list(word):  # Ensure scrambled word will never be the same as answer
                random.shuffle(word_chars)

            question_list.append(word_chars)

        print(answer_list)
        print(question_list)
        return question_list, answer_list

    def create_hint(self, word, num_hint=0):
        """
        Creates a hint message to display after some time has passed.
        First 1/4 characters are displayed in order, rest are still scrambled e.g.
        💁🏻 🏁 HINT:
        * P , L  * , E , C, A
        :param word: answer word
        :param num_hint: if specified, show first X letters instead of using first 1/4 of the letters by default
        :return: display string for word list with hints in place and bolded
        """

        word_list = list(word)
        separator = math.floor(len(word_list) / 6) + 1
        if num_hint != 0:
            separator = num_hint
        display_list = list(word[0:separator])
        shuffled_list = word_list[separator:len(word_list)]

        while display_list + shuffled_list == word_list:
            random.shuffle(shuffled_list)

        return "*" + ' , '.join(display_list).upper() + "*" + " , " + ' , '.join(shuffled_list).upper()

    # deprecated, too difficult to guess even with this hint
    def create_hint_new(self, word):
        """
        New feature: use any chars in the word to be used as hint, instead of first X chars.
        Makes it tougher.
        :param word: answer word
        :return: display string for word list with hints in place and bolded
        """

        word_list = list(word)
        num_hint = math.floor(len(word_list) / 4) + 1
        hints = list(random.sample(set([i for i in range(len(word_list))]), num_hint))  # index of hint chars to display

        display_list = word_list.copy()
        for i in sorted(hints, reverse=True):
            del display_list[i]
        random.shuffle(display_list)

        for i in sorted(hints, reverse=False):
            display_list.insert(i, "*"+word_list[i]+"*")

        return " , ".join(display_list).upper()

    def display_help(self):
        bot.sendMessage(self._chat_id, utils.MsgTemplate.help_msg, parse_mode="Markdown")

    def display_rules(self):
        bot.sendMessage(self._chat_id, utils.MsgTemplate.rule_msg, parse_mode="Markdown")

    def gen_results_str(self):
        """
        :return: Header + formatted string of "username: score"
        e.g. "Results: Tom: 5 points \n Sally: 4 points \n"
        """
        sorted_user_id_by_score = sorted(self.user_id_score, key=self.user_id_score.get, reverse=True)
        message = utils.MsgTemplate.result_msg_1
        for k in sorted_user_id_by_score:
            message += "_" + str(self.user_name_id[k]) + ": " + str(self.user_id_score[k]) + " points\n" + "_"
        message += "\n"
        return message


# Start bot service
# A bot instance is created per chat (group)
if __name__ == "__main__":
    TOKEN = '<BOT KEY HERE>'  # sys.argv[1]

    bot = telepot.DelegatorBot(TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open, MessageCounter, timeout=120),
    ])
    bot.message_loop(run_forever='Listening ...')


# if we set privacy to disabled, receives all msgs
# enabled only receives msgs with '/' or @bot (in other chats)
