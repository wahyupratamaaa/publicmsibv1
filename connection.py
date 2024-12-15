from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

app = Flask(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

cred = credentials.Certificate('yourcredential')
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_collection(collection_name):
    return db.collection(collection_name)