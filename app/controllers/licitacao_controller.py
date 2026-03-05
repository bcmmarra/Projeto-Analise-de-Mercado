import os
import uuid # Para criar nomes únicos
from flask import Blueprint, jsonify, request
from app.models.licitacao_model import LicitacaoModel

licitacao_bp = Blueprint('licitacao', __name__)
UPLOAD_FOLDER = 'uploads'

@licitacao_bp.route('/api/processar', methods=['POST'])
def processar():
    try:
        if 'arquivo' not in request.files:
            return jsonify({"erro": "Nenhum arquivo enviado"}), 400
        
        arquivo = request.files['arquivo']
        
        # Criamos um nome único para o arquivo não ser bloqueado pelo Windows
        nome_unico = f"{uuid.uuid4()}_{arquivo.filename}"
        caminho_salvamento = os.path.join(UPLOAD_FOLDER, nome_unico)
        
        arquivo.save(caminho_salvamento)
        
        # Processa
        dados = LicitacaoModel.processar_arquivo(caminho_salvamento)
        
        return jsonify(dados)

    except Exception as e:
        # Isso vai imprimir o erro real no seu terminal para a gente debugar
        print(f"ERRO NO SERVIDOR: {str(e)}")
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500