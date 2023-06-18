# import os
# import googlemaps
# from flask import Flask, redirect, render_template, request, url_for, jsonify, requests


# gmaps = googlemaps.Client('AIzaSyAUu5mSd5dc5VdMJ3lrcvCDXY-SzaGZMas')

# app = Flask(__name__)

# @app.route('/', methods=('GET', 'POST')) 
# def addLocation():
#     temp = requests.form['location']
#     geocoder = gmaps.geocode(temp)
#     print(geocoder)