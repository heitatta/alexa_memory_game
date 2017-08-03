#!/usr/bin/env python3
import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session


app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent('AMAZON.YesIntent')
def next_round():
    numbers = [randint(0, 9) for _ in range(3)]
    round_msg = render_template('round', numbers=numbers)
    session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(round_msg)


@ask.intent("AnswerIntent",
            convert={'first': int, 'second': int, 'third': int})
def answer(first, second, third):
    winning_numbers = session.attributes['numbers']
    if [first, second, third] == winning_numbers:
        msg = render_template('win')
    else:
        msg = render_template('lose')
    return statement(msg)


# Built-in intents
#
# These intents are built-in intents. Conveniently, built-in intents
# do not need you to define utterances, so you can use them straight
# out of the box. Depending on whether you wish to implement these in
# your application, you may keep or delete them/comment them out.
#
# More about built-in intents: http://d.pr/KKyx

@ask.intent('AMAZON.StopIntent')
def handle_stop():
    """
    (STATEMENT) Handles the 'stop' built-in intention.
    """
    farewell_text = render_template('stop_bye')
    return statement(farewell_text)


@ask.intent('AMAZON.CancelIntent')
def handle_cancel():
    """
    (STATEMENT) Handles the 'cancel' built-in intention.
    """
    farewell_text = render_template('cancel_bye')
    return statement(farewell_text)


@ask.intent('AMAZON.HelpIntent')
def handle_help():
    """
    (QUESTION) Handles the 'help' built-in intention.

    You can provide context-specific help here by rendering templates
    conditional on the help referrer.
    """

    help_text = render_template('help_text')
    return question(help_text)


@ask.intent('AMAZON.NoIntent')
def handle_no():
    """
    (?) Handles the 'no' built-in intention.
    """
    pass


@ask.intent('AMAZON.PreviousIntent')
def handle_back():
    """
    (?) Handles the 'go back!'  built-in intention.
    """
    pass


@ask.intent('AMAZON.StartOverIntent')
def start_over():
    """
    (QUESTION) Handles the 'start over!'  built-in intention.
    """
    pass


@ask.default_intent
def default_intent():
    if 'numbers' in session.attributes:
        return next_round()
    return question('unknonw')


# Ending session
#
# This intention ends the session.
@ask.session_ended
def session_ended():
    """
    Returns an empty for `session_ended`.

    .. warning::
    The status of this is somewhat controversial. The `official
    documentation`_ states that you cannot return a response
    to ``SessionEndedRequest``. However, if it only returns a
    ``200/OK``, the quit utterance (which is a default test
    utterance!) will return an error and the skill will not validate.

    """
    return statement("")


if __name__ == '__main__':
    app.run(debug=True)
