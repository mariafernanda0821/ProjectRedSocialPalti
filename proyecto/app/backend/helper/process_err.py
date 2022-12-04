from flask import Flask, render_template, redirect, request, session, url_for, jsonify

def process_error(message, next_page, texto_boton):
    return render_template("error.html", error_message=message, next=next_page, texto_boton=texto_boton)
