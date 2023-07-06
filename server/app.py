#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, jsonify, session, abort, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource
from functools import wraps
import ipdb

# Local imports
from config import *

# Views go here!

if __name__ == '__main__':
    app.run(port=5555, debug=True)
