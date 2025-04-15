# Resumo.K
# Resumo Automático de Textos com Flask e Machine Learning

Este projeto cria um aplicativo web para resumir textos automaticamente utilizando o modelo `facebook/bart-large-cnn` da Hugging Face, juntamente com o Flask para criação da interface web. O aplicativo também integra o **LanguageTool** para corrigir o texto gerado e melhorar a qualidade do resumo.

## Funcionalidades

- Geração automática de resumos com o modelo BART.
- Correção gramatical do texto original e do resumo gerado utilizando **LanguageTool**.
- Interface simples com Flask para interação com o usuário.

## Tecnologias Utilizadas

- **Flask**: Framework web em Python para construção da interface.
- **Transformers (Hugging Face)**: Biblioteca para manipulação de modelos de NLP como o BART.
- **LanguageTool**: Ferramenta para correção gramatical de textos.
- **Torch**: Framework utilizado para rodar o modelo de aprendizado de máquina.
- **HTML/CSS**: Para a criação da interface.

## Como Rodar o Projeto

### Requisitos

1. Python 3.6+ instalado.
2. Dependências necessárias:
   - `transformers`
   - `torch`
   - `flask`
   - `language_tool_python`
   
### Passos para rodar o projeto 

### 1. Clone este repositório:

   ```bash
   git clone https://github.com/Kaiky1007/Resumo.K.git
   cd Resumo.K.git
   ```

### 2. Instale as dependências:
    
    pip install -r requirements.txt

### 3. Rodar o servidor Flask:

    python app.py

### 4. Acesse a aplicação em seu navegador em:
    http://127.0.0.1:5000/
    
### Arquivos Principais
- app.py: Código Python principal que roda o servidor Flask, integra o modelo de resumo e o LanguageTool.

- templates/index.html: Interface web onde o usuário pode inserir o texto e visualizar o resumo.

- requirements.txt: Lista de dependências para instalação.