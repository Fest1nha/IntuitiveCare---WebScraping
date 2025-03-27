import pandas as pd
import zipfile
import pdfplumber
import re

# Definir o nome do arquivo de entrada e saída
pdf_file = "anexos_ans/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
csv_file = "Rol_de_Procedimentos.csv"
zip_file = "Teste_OcthorFesta.zip"

# Dicionário para substituir as abreviações OD e AMB
substituicoes = {
    "OD": "Odontológico",
    "AMB": "Ambulatorial"
}

def extrair_tabela_do_pdf(pdf_path):
    dados = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    dados.append(row)
    return dados

# Extrair os dados do PDF
dados_extraidos = extrair_tabela_do_pdf(pdf_file)

# Criar um DataFrame
df = pd.DataFrame(dados_extraidos)

# Substituir as abreviações OD e AMB
df = df.applymap(lambda x: substituicoes.get(x, x) if isinstance(x, str) else x)

# Salvar em CSV
df.to_csv(csv_file, index=False, encoding='utf-8')

# Compactar o CSV em um arquivo ZIP
with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_file)

print(f"Arquivo {zip_file} criado com sucesso!")
