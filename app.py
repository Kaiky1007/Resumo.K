from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
from heapq import nlargest
import PyPDF2
import docx
import tempfile
import re
import gunicorn

# def check_nltk_resources():
#     """Verifica e baixa os recursos necessários do NLTK com tratamento de erros"""
#     resources = {
#         'punkt': 'tokenizers/punkt',
#         'stopwords': 'corpora/stopwords'
#     }
    
#     for resource_name, resource_path in resources.items():
#         try:
#             nltk.data.find(resource_path)
#             print(f"Recurso do NLTK '{resource_name}' já instalado.")
#         except LookupError:
#             try:
#                 print(f"Baixando recurso do NLTK '{resource_name}'...")
#                 nltk.download(resource_name)
#                 print(f"Recurso '{resource_name}' baixado com sucesso.")
#             except Exception as e:
#                 raise Exception(f"Falha ao baixar recurso '{resource_name}': {str(e)}")

# try:
#     check_nltk_resources()
# except Exception as e:
#     print(f"Erro ao configurar recursos do NLTK: {str(e)}")
#     exit(1)
nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
MAX_FILE_SIZE_MB = 16

app = Flask(__name__)
app.secret_key = 'chavefoda123'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_MB * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['TEMPLATES_AUTO_RELOAD'] = True

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_text(texto):
    """Realiza limpeza básica do texto"""
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r'[^\w\sáéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ.,;:!?()-]', '', texto)
    return texto.strip()

def extract_text_from_file(filepath, extension):
    """Extrai texto de diferentes formatos de arquivo"""
    text = ""
    try:
        if extension == 'pdf':
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if not text.strip():
                raise Exception("Não foi possível extrair texto do PDF (pode ser um PDF de imagem)")
                
        elif extension in ['docx', 'doc']:
            doc = docx.Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"
                
        elif extension == 'txt':
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()
                
    except Exception as e:
        raise Exception(f"Erro ao extrair texto do arquivo: {str(e)}")
    
    return clean_text(text)

def resumir_texto(texto, num_sentencas=3):
    """Gera resumo do texto com base na frequência de palavras"""
    if not texto.strip():
        return ""
    
    texto = clean_text(texto)
    
    stop_words = set(stopwords.words('portuguese') + list(punctuation))
    palavras = word_tokenize(texto.lower())
    
    freq_palavras = {}
    for palavra in palavras:
        if palavra not in stop_words and palavra.isalnum():
            freq_palavras[palavra] = freq_palavras.get(palavra, 0) + 1
    
    if not freq_palavras:
        return "Texto muito curto ou sem palavras significativas para resumir."
    
    max_freq = max(freq_palavras.values())
    for palavra in freq_palavras:
        freq_palavras[palavra] /= max_freq
    
    sentencas = sent_tokenize(texto)
    if len(sentencas) <= num_sentencas:
        return texto
    
    sentenca_pontuacao = {}
    for sentenca in sentencas:
        for palavra in word_tokenize(sentenca.lower()):
            if palavra in freq_palavras:
                sentenca_pontuacao[sentenca] = sentenca_pontuacao.get(sentenca, 0) + freq_palavras[palavra]
    
    num_sentencas = min(num_sentencas, len(sentencas))
    sentencas_resumo = nlargest(num_sentencas, sentenca_pontuacao, key=sentenca_pontuacao.get)
    
    resumo = [sentenca for sentenca in sentencas if sentenca in sentencas_resumo]
    return ' '.join(resumo)

@app.route('/', methods=['GET', 'POST'])
def index():
    texto = ""
    resumo = ""
    filename = None
    char_count = 0
    char_count_resumo = 0
    
    if request.method == 'POST':
        if 'arquivo' in request.files:
            file = request.files['arquivo']
            if file.filename != '':
                if file.filename == '':
                    flash('Nenhum arquivo selecionado', 'warning')
                elif not allowed_file(file.filename):
                    flash('Tipo de arquivo não permitido. Use PDF, DOC, DOCX ou TXT.', 'warning')
                else:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    try:
                        file.save(filepath)
                        extension = filename.rsplit('.', 1)[1].lower()
                        texto = extract_text_from_file(filepath, extension)
                        os.remove(filepath)
                        flash(f'Arquivo "{filename}" processado com sucesso!', 'success')
                        flash('Agora você pode gerar o resumo do texto extraído.', 'info')
                    except Exception as e:
                        flash(f'Erro ao processar arquivo: {str(e)}', 'error')
        
        if not texto and 'texto' in request.form:
            texto = request.form.get('texto', '')
            if texto.strip():
                flash('Texto recebido para processamento.', 'info')
        
        if not texto.strip():
            flash('Por favor, insira um texto ou faça upload de um arquivo.', 'warning')
        else:
            try:
                char_count = len(texto)
                if char_count < 50:
                    flash('Texto muito curto. Para melhores resultados, insira um texto com pelo menos 50 caracteres.', 'warning')
                
                resumo = resumir_texto(texto, num_sentencas=3)
                char_count_resumo = len(resumo)
                
                if resumo:
                    reducao = int((1 - char_count_resumo/char_count) * 100)
                    flash(f'Resumo gerado com sucesso! Redução de {reducao}%.', 'success')
                    flash('Você pode copiar o resumo abaixo ou fazer um novo.', 'info')
                else:
                    flash('Não foi possível gerar o resumo. O texto pode estar muito curto ou sem conteúdo significativo.', 'warning')
                    
            except Exception as e:
                flash(f'Erro ao gerar resumo: {str(e)}', 'error')
                flash('Por favor, tente novamente com um texto diferente.', 'info')
    
    return render_template(
        'index.html',
        texto=texto,
        resumo=resumo,
        filename=filename,
        char_count=char_count,
        char_count_resumo=char_count_resumo
    )

# if __name__ == '__main__':
#     app.run(debug=True)