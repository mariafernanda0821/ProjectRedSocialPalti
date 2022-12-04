"""
login

registro

logout

"""
from flask import Flask, render_template, redirect, request, session, url_for, jsonify

 def aut_login():
     """
     when user acess into webpage domain,
     server shows them login or home if user is in session
     :return: content of register.html or login.html
     """
     if 'useremail' in session:
         return redirect( url_for('home') )
     return render_template('login.html', title="Palti - Login", form_title="Iniciar Sesion", login_or_register_href="register", login_or_register_text="Registrar")
