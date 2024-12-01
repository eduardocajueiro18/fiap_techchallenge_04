# fiap_techchallenge_04

# **Análise de Vídeo com MediaPipe e DeepFace**

Este projeto utiliza as bibliotecas MediaPipe, DeepFace e OpenCV para analisar vídeos, detectando emoções, atividades corporais e movimentos anômalos. Ao final do processamento, um relatório JSON é gerado com o resumo das análises.

---

## **Pré-requisitos**

Certifique-se de ter os seguintes itens instalados no seu ambiente:

1. **Python**: versão 3.8 ou superior.
2. **Bibliotecas Python**:  
   Instale as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Arquivos de vídeo**:  
   Certifique-se de ter o vídeo a ser analisado no diretório `videos/` (ou modifique o caminho no código).

---

## **Instalação**

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Como Executar**

1. **Verifique o caminho do vídeo**:  
   Altere a variável `caminho_video` no arquivo `main.py` para o caminho do seu vídeo:
   ```python
   caminho_video = "videos/seu_video.mp4"
   ```

2. **Execute o script principal**:
   ```bash
   python main.py
   ```

3. **Acompanhe o processamento**:  
   O terminal exibirá mensagens de progresso, como:
   ```
   Processando frame 1/1000...
   Processando frame 2/1000...
   ```

4. **Resultado**:  
   Após o processamento, um arquivo `relatorio.json` será gerado no diretório do projeto. Ele contém:
   - Total de rostos detectados.
   - Resumo das emoções.
   - Resumo das atividades corporais.
   - Total de anomalias detectadas.

---

## **Estrutura do Projeto**

```plaintext
├── main.py                  # Arquivo principal para execução
├── requirements.txt         # Dependências do projeto
├── videos/                  # Diretório de vídeos de entrada
├── relatorio.json           # Relatório gerado após processamento
└── README.md                # Documentação do projeto
```

---

## **Exemplo de Saída do Relatório**

```json
{
    "Total de Frames": 1000,
    "Total de Rostos Detectados": 150,
    "Total de Anomalias Detectadas": 10,
    "Resumo de Emoções": {
        "happy": 50,
        "neutral": 90,
        "sad": 10
    },
    "Resumo de Atividades": {
        "Sentado": 300,
        "Em pé": 600,
        "Pulando": 100
    }
}
```

---

## **Problemas Comuns**

1. **Erro de dependências não instaladas**:
   - Verifique se o `pip` está atualizado:
     ```bash
     pip install --upgrade pip
     ```
   - Certifique-se de instalar todas as dependências:
     ```bash
     pip install -r requirements.txt
     ```

2. **Vídeo não encontrado**:
   - Verifique se o caminho do vídeo está correto.
   - Certifique-se de que o arquivo de vídeo está no formato suportado (ex.: `.mp4`).

3. **Problemas de performance**:
   - Use vídeos menores ou otimize os parâmetros no processamento.

---

## **Licença**

Este projeto está licenciado sob a [MIT License](LICENSE).
