from flask import Flask

app = Flask(__name__)

import codeitsuisse.routes.square
import codeitsuisse.routes.secret_message
import codeitsuisse.routes.parasite
import codeitsuisse.routes.asteroid
import codeitsuisse.routes.stonks
import codeitsuisse.routes.fixedrace
import codeitsuisse.routes.stocker_hunter
