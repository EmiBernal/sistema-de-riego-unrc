from . import regadores_bp

@regadores_bp.route("/")
def index():
    return 'Lista de '