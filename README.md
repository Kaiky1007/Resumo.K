# 📑 Resumo.K - Resumidor de Textos em Português com Machine Learning

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0.1-green.svg)
![NLTK](https://img.shields.io/badge/NLTK-3.6.2-orange.svg)

O Resumo.K é uma aplicação web que utiliza técnicas de Processamento de Linguagem Natural (NLP) para resumir automaticamente textos em português, destacando as informações mais relevantes.

## ✨ Funcionalidades

- 📝 Upload de arquivos (PDF, DOCX, TXT)
- ✍️ Digitação direta de texto
- 🔍 Extração automática de texto de documentos
- ✂️ Resumo por importância de sentenças
- 📊 Comparativo de tamanho original vs. resumo
- 🚀 Processamento rápido e eficiente

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/) - Linguagem principal
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [NLTK](https://www.nltk.org/) - Processamento de linguagem natural
- [PyPDF2](https://pypi.org/project/PyPDF2/) - Leitura de PDFs
- [python-docx](https://python-docx.readthedocs.io/) - Leitura de arquivos Word

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/resumo.k.git
cd resumo.k
```

2. Crie e ative um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executando a Aplicação

```bash
python app.py
```

Acesse a aplicação no navegador: [http://localhost:5000](http://localhost:5000)
