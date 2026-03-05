import sys
import os

# 1. Forçamos o Python a enxergar a raiz do projeto
# Isso resolve o erro 'No module named app'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from flask_cors import CORS

# 2. Agora sim importamos suas Blueprints e Controllers
try:
    from app.controllers.licitacao_controller import licitacao_bp
    print("Módulos carregados com sucesso!")
except ImportError as e:
    print(f"Erro ao carregar módulos: {e}")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

app.register_blueprint(licitacao_bp)

if __name__ == "__main__":
    # O debug=True é ótimo para você ver os erros direto no navegador
    app.run(debug=True, port=5000)