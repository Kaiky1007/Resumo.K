from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
from heapq import nlargest
import heapq
import bs4 as bs
import urllib.request
import re

# Baixar recursos do NLTK (apenas na primeira execução)
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
app.secret_key = 'chavefoda123'  # Necessário para mensagens flash

# Configurações
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para upload

# Função para resumir texto
def resumir_texto(texto, num_sentencas=3):
    # Verifica se o texto está vazio
    if not texto.strip():
        return ""
    
    # Tokenização e limpeza
    stop_words = set(stopwords.words('portuguese') + list(punctuation))
    palavras = word_tokenize(texto.lower())
    
    # Frequência das palavras
    freq_palavras = {}
    for palavra in palavras:
        if palavra not in stop_words:
            freq_palavras[palavra] = freq_palavras.get(palavra, 0) + 1
    
    # Normalização
    max_freq = max(freq_palavras.values()) if freq_palavras else 1
    for palavra in freq_palavras.keys():
        freq_palavras[palavra] = freq_palavras[palavra] / max_freq
    
    # Tokenização de sentenças
    sentencas = sent_tokenize(texto)
    
    # Pontuação das sentenças
    sentenca_pontuacao = {}
    for sentenca in sentencas:
        for palavra in word_tokenize(sentenca.lower()):
            if palavra in freq_palavras:
                if sentenca not in sentenca_pontuacao:
                    sentenca_pontuacao[sentenca] = freq_palavras[palavra]
                else:
                    sentenca_pontuacao[sentenca] += freq_palavras[palavra]
    
    # Seleciona as sentenças mais importantes
    num_sentencas = min(num_sentencas, len(sentencas))
    sentencas_resumo = nlargest(num_sentencas, sentenca_pontuacao, key=sentenca_pontuacao.get)
    
    # Reordena as sentenças para manter a coesão do texto
    resumo = []
    for sentenca in sentencas:
        if sentenca in sentencas_resumo:
            resumo.append(sentenca)
    
    return ' '.join(resumo)

@app.route('/', methods=['GET', 'POST'])
def index():
    texto = ""
    resumo = ""
    
    if request.method == 'POST':
        texto = request.form.get('texto', '')
        
        if not texto.strip():
            flash('Por favor, insira um texto para resumir.', 'error')
        else:
            try:
                # Gera o resumo (ajuste o número de sentenças conforme necessário)
                resumo = resumir_texto(texto, num_sentencas=3)
            except Exception as e:
                flash(f'Ocorreu um erro ao gerar o resumo: {str(e)}', 'error')
    
    return render_template('index.html', texto=texto, resumo=resumo)

if __name__ == '__main__':
    app.run(debug=True)