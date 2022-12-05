"""
chat_messenger

"""
from flask import Flask, render_template, redirect, request, session, url_for, jsonify

def chat_chat_messenger():
    return render_template("chat_messenger.html", title="Palti - Chat Messenger", user_firstname = session["user-firstname"], user_lastname=session["user-lastname"])
