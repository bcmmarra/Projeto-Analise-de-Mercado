import pandas as pd

class LicitacaoModel:
    @staticmethod
    def processar_arquivo(caminho_arquivo):
        # Lemos o Excel
        df = pd.read_excel(caminho_arquivo, engine='openpyxl')
        
        relatorio_final = []
        item_atual = None
        vencedor_valor = 0
        
        # Itera pelas linhas do DataFrame
        for _, linha in df.iterrows():
            # Limpa os dados das colunas principais
            posicao = str(linha['Posição']).strip() if pd.notna(linha['Posição']) else ""
            item_num = str(linha['Item']).strip() if pd.notna(linha['Item']) else ""
            descricao = str(linha['Descrição']).strip() if pd.notna(linha['Descrição']) else ""
            empresa = str(linha['Nome Empresa']).strip().upper() if pd.notna(linha['Nome Empresa']) else ""
            marca = str(linha['Marca']).strip() if pd.notna(linha['Marca']) else "-"
            
            # Tratamento do Valor Unitário
            valor_bruto = linha['Valor Unitário']
            try:
                valor_unitario = float(valor_bruto) if pd.notna(valor_bruto) else 0.0
            except:
                valor_unitario = 0.0

            # 1. IDENTIFICA INÍCIO DE NOVO ITEM
            if item_num != "" and posicao == "":
                item_atual = {
                    "item": item_num,
                    "descricao": descricao,
                    "concorrentes": []
                }
                relatorio_final.append(item_atual)
                vencedor_valor = 0
                continue

            # 2. PROCESSA CONCORRENTES
            if item_atual and posicao != "" and empresa != "":
                if "1" in posicao:
                    vencedor_valor = valor_unitario
                
                dados_concorrente = {
                    "posicao": posicao,
                    "empresa": empresa,
                    "marca": marca,
                    "valor": valor_unitario,
                    "diferenca": valor_unitario - vencedor_valor
                }
                
                item_atual["concorrentes"].append(dados_concorrente)
                
                # REGRA: Para após encontrar a DENTAL MARIA
                if "DENTAL MARIA" in empresa:
                    item_atual = None 

        # No MVC, o Model retorna os dados brutos (lista), não o JSON final
        return relatorio_final

# Para testes rápidos fora do Flask
if __name__ == "__main__":
    arquivo = 'Resultados_CN_93020_2026_PREFEITURA MUNICIPAL DE BEZERROS - PE.xlsx'
    resultado = LicitacaoModel.processar_arquivo(arquivo)
    print(resultado)