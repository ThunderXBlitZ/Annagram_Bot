class Config:
    DATA_PATH = r"./data/length_{}.txt"


class State:
    IDLE = 1
    RUNNING = 2
    ROUND_END = 3


class MsgTemplate:
    help_msg = """
❗️*Hi! I'm Anna!* \U0001f481\U0001f3fb Come play *"Annagram!"* with me! .\U0001f64b\U0001f3fb

\U0001f3c1 *"Annagram!" scrambles up English words *\u2049\ufe0f and it is up to you to deduce *what is the correct word!*  \u2714\ufe0f

\U0001f389 \U0001f389 \U0001f389 \U0001f389 \U0001f389 \U0001f389 \U0001f389 \U0001f389 \U0001f389

*Use these commands* to talk to me \U0001f481\U0001f3fb:
    \U0001f481\U0001f3fb */start* - starts the game \U0001f3c1
    \U0001f481\U0001f3fb */stop* - stops the game \u26d4\ufe0f
    \U0001f481\U0001f3fb */next* - start the next round when the round is completed \U0001f3c1
    \U0001f481\U0001f3fb */help* - to display this message \U0001f64b\U0001f3fb
    \U0001f481\U0001f3fb */rules* - view Anna's rules \U0001f481\U0001f3fb"""

    rule_msg = "\U0001f481\U0001f3fb *The rules are simple:* \n\n" \
               "\t _I give you the question, you guess the word!_ \t \n\n" \
               "\U0001f481\U0001f3fb Time limit is *60 seconds* \U0001f551 \n" \
               "\U0001f481\U0001f3fb Each round has *15 questions!* \n" \
               "\U0001f481\U0001f3fb Whoever answers first, *wins* the round! \U0001f60b \n" \
               "\U0001f481\U0001f3fb *No penalties* for giving wrong answers! \U0001f629 \n" \
               "\U0001f481\U0001f3fb *Hints* will be given after 30 seconds \U0001f481\U0001f3fb \n"

    start_msg = "\U0001f481\U0001f3fb \U0001f3c1 OK! *ROUND %s* begin! \U0001f3c1"

    question_msg = "\U0001f481\U0001f3fb \U0001f3c1 *QUESTION %s :* \U0001f3c1 \n" \
                   "\u25b6\ufe0f QUESTION: \t %s \n"

    hint_msg = "\U0001f481\U0001f3fb \U0001f3c1 *HINT:* \n %s"
    answer_msg = "\U0001f481\U0001f3fb \U0001f389 *Correct!* %s got it right! _+ %s points!_ \U0001f389"

    result_msg_1 = "\U0001f481\U0001f3fb \U0001f389 Here are the current results! \U0001f389 \n\n"

    round_completed_msg = "\U0001f481\U0001f3fb \U0001f44f\U0001f3fb *That's it for this round!* " \
                          "\U0001f44f\U0001f3fb \n" \
                          "%s" \
                          "\U0001f64b\U0001f3fb Type in */next* to continue! "

    stop_msg = "\U0001f481\U0001f3fb \u26d4\ufe0f *Game stopped!* \n" \
               "%s" \
               "\U0001f389 I had a great time playing with you! See you next time! "

    timeout_msg_0 = "\U0001f481\U0001f3fb *Strange!* Guess no one got it right!"

    timeout_msg_1 = "\U0001f481\U0001f3fb *Strange!* Guess no one got it right! \n\n % s \n\n" \
                    "\U0001f481\U0001f3fb Type _'/start'_ to start the next game!"

    timeout_msg_2 = "\U0001f481\U0001f3fb *Strange!* Didn't hear anything from you. \n" \
                    "Wake me up when you want to play again..."

    timer_msg_list = ["[   ○   ○       ○        ]", "[••••   ○       ○        ]", "[••••••••       ○        ]",
                      "[••••••••••••••••        ]"]
