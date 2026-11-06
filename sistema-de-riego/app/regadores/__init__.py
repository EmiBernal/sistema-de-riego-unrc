from flask import Blueprint

regadores_bp = Blueprint("regadores", __name__, url_prefix="/regadores")

from . import routes