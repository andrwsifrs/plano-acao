# 🤖 Robô de Automação de Plano de Ação (SIGPP / IFRS)

Script de automação em **Python** utilizando **Playwright** e **Pandas** para preenchimento automatizado de ações internas no sistema **SIGPP** a partir de uma planilha Excel (`planilha.xlsx`).

---

## 🚀 Tecnologias Utilizadas
* **Python 3.x**
* **Playwright** (Automação web moderna e estável)
* **Pandas & OpenPyXL** (Leitura e manipulação de dados do Excel)

---

## ⚙️ Como Configurar e Executar

1. **Clone o repositório:**
   No terminal, execute: `git clone https://github.com/SEU-USUARIO/PlanoAcao.git` e depois entre na pasta com `cd PlanoAcao`

2. **Crie e ative o ambiente virtual (venv):**
   - Crie o ambiente: `python -m venv .venv`
   - Ative no Windows (CMD): `.venv\Scripts\activate.bat`
   - Ative no Windows (PowerShell): `.venv\Scripts\Activate.ps1`

3. **Instale as dependências:**
   Execute no terminal: `pip install -r requirements.txt` e depois `playwright install chromium`

4. **Adicione a planilha:**
   * Certifique-se de que o arquivo `planilha.xlsx` está na raiz do projeto com as colunas corretas (`Ação Interna`, `Motivação`, `Rúbrica`, `Valor Planejado`, `Responsável`).

5. **Execute o robô:**
   Execute no terminal: `python main.py`
   * *O navegador abrirá na tela de login do SIGPP. Faça o login manualmente, navegue até a tela de **"Dados da Ação"**, volte ao terminal do PyCharm e aperte **ENTER** para o robô assumir o cadastro linha por linha.*