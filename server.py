from flask import Flask, request, render_template, redirect
from collections import defaultdict

import json

app = Flask(__name__)
app.data = defaultdict(int)


chatLog = {"user1": {"user2": ["me: hi", "user2: hi"]},
           "user2": {"user1": ["user1: hi", "me: hi"], "user3": ["me: hi user3!", "me: hello user3!"]},
           "user3": {"user2": ["user2: hi user3!", "user2: hello user3!"]}}


@app.route('/')
def home():
    return render_template("login.html")


@app.route('/chatLog', methods=['GET'])
def chat_log():
    return chatLog


@app.route('/signUp', methods=['POST'])
def sign_up():
    number = json.loads(request.data)['user']
    if number in chatLog:
        return "<p>Already have an account. Please sign in.</p>"
    else:
        chatLog[number] = {}
        return "<p>Successfully Signed Up!</p>"


@app.route('/home', methods=['Post'])
def sign_in():
    if 'user' in request.form:
        user = request.form['user']
    else:
        user = request.form['sender']

    if user in chatLog:
        return print_chat_log(chatLog[user], user)
    else:
        return "<p>Account doesn't exist. Please sign up</p>"


def print_chat_log(log, user):
    s = "<div style='margin:auto; width: 50%; padding: 50px; border: 1px solid;background-color: #f1f1f1'>"
    s = s + "<h2 style='text-align: center;color: #2b708e;font-family: cursive'> Welcome {user}!</h2>".format(user=user)

    for i in log:
        s = s + "<h3 style='text-align: left;color: #2b708e;'> TO: " + i + "</h3>"
        s = s + "<div style='margin:auto; width: 50%; padding: 2%'>"
        for j in log[i]:
            sender = j.split(":")[0]
            if sender == "me":
                s = s + "<span style='padding: 2%; padding-left: 30%'>" + j + "</span><br>"
            else:
                s = s + "<span style='padding: 2%;padding-right: 30%'>" + j + "</span><br>"
    s = s + "<form action='/sendMessage' method='post'> To: <input name='receiver'/> <br> Message: <input name='message'/> <br> <input name='sender' type='hidden' value='{sender}'/> <button type='submit'>Send</button></form>".format(
        sender=user)
    s = s + "</div>"
    s = s + "</div>"
    print(s)
    return s


@app.route("/sendMessage", methods=['POST'])
def send_message():
    info = request.form
    sender = info['sender']
    receiver = info['receiver']
    message = info['message']
    if sender not in chatLog:
        return print_chat_log(chatLog[sender], sender) + "<br> <p>Account= " + sender + " doesn't exist. Please sign up</p>"
    if receiver not in chatLog:
        return print_chat_log(chatLog[sender], sender) + "<br> Account= " + receiver + " doesn't exist. Send Invite</p>"
    if sender not in chatLog[receiver]:
        chatLog[receiver][sender] = [sender + ": " + message]
    else:
        chatLog[receiver][sender].append(sender + ": " + message)
    if receiver not in chatLog[sender]:
        chatLog[sender][receiver] = ["me: " + message]
    else:
        chatLog[sender][receiver].append("me: " + message)

    return redirect('home', 307)


# todo get list of users


app.run(host='0.0.0.0', port=8080)
