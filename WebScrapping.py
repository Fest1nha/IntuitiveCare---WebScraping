import requests
from bs4 import BeautifulSoup  
import os
import zipfile

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
response = requests.get(url)
soup= BeautifulSoup(response.text, "html.parser")

for link in soup.find_all("a", href=True):
    print(link.text, "->", link["href"])

download_folder = "anexos_ans"
zip_anexos = "anexos_ans.zip"

os.makedirs(download_folder, exist_ok=True)

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

pdf_links = []
for link in soup.find_all("a", href=True):
    href = link["href"]
    if href.lower().endswith(".pdf") and "Anexo I" in link.text or "Anexo II" in link.text:
        pdf_links.append(link["href"] if link["href"].startswith("http") else "https://www.gov.br" + link["href"])
print("links econtrados:", pdf_links)

def download_file(url, folder):
    filename = url.split("/")[-1]
    filepath = os.path.join(folder, filename)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filepath, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Baixando {filename}")
    return filepath

arquivos_pdf = [download_file(link, download_folder) for link in pdf_links]

with zipfile.ZipFile(zip_anexos, "w") as zip_f:
    for pdf in os.listdir(download_folder):
        file_path = os.path.join(download_folder, pdf)
        if os.path.isfile(file_path):
            zip_f.write(file_path, arcname=pdf)

print(f"Compactação concluida")