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

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
app.secret_key = 'chavefoda123'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

def resumir_texto(texto, num_sentencas=3):
    if not texto.strip():
        return ""
    
    stop_words = set(stopwords.words('portuguese') + list(punctuation))
    palavras = word_tokenize(texto.lower())
    
    freq_palavras = {}
    for palavra in palavras:
        if palavra not in stop_words:
            freq_palavras[palavra] = freq_palavras.get(palavra, 0) + 1
    
    max_freq = max(freq_palavras.values()) if freq_palavras else 1
    for palavra in freq_palavras.keys():
        freq_palavras[palavra] = freq_palavras[palavra] / max_freq
    
    sentencas = sent_tokenize(texto)
    
    sentenca_pontuacao = {}
    for sentenca in sentencas:
        for palavra in word_tokenize(sentenca.lower()):
            if palavra in freq_palavras:
                if sentenca not in sentenca_pontuacao:
                    sentenca_pontuacao[sentenca] = freq_palavras[palavra]
                else:
                    sentenca_pontuacao[sentenca] += freq_palavras[palavra]
    
    num_sentencas = min(num_sentencas, len(sentencas))
    sentencas_resumo = nlargest(num_sentencas, sentenca_pontuacao, key=sentenca_pontuacao.get)
    
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
                resumo = resumir_texto(texto, num_sentencas=3)
            except Exception as e:
                flash(f'Ocorreu um erro ao gerar o resumo: {str(e)}', 'error')
    
    return render_template('index.html', texto=texto, resumo=resumo)

if __name__ == '__main__':
    app.run(debug=True)