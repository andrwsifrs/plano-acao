import pandas as pd
from playwright.sync_api import sync_playwright

# 1. Carrega os dados da planilha anexada
ARQUIVO_EXCEL = "planilha.xlsx"
df = pd.read_excel(ARQUIVO_EXCEL, sheet_name="Planilha1")

print(f"Planilha carregada com sucesso! Total de ações para cadastrar: {len(df)}")

with sync_playwright() as p:
    # Abre o navegador visível
    navegador = p.chromium.launch(headless=False, slow_mo=150)
    contexto = navegador.new_context(viewport={"width": 1280, "height": 900})
    pagina = contexto.new_page()

    # Abre direto na tela de login do SIGPP
    pagina.goto("https://sig.ifrs.edu.br/sigpp/login.jsf")

    print("\n" + "=" * 60)
    print("PASSO MANUAL:")
    print("1. Faça o login no SIGPP na janela que abriu.")
    print("2. Navegue até à página 'Dados da Ação' (onde fica 'Ações Internas').")
    print("=" * 60)
    input("\n>>> Quando estiver na tela de cadastro das AÇÕES INTERNAS, aperte ENTER aqui no terminal do PyCharm para começar...")

    # Localiza a aba correta onde está o bloco "cadastroPlanoMetas:linhaAcoesInternas"
    alvo = pagina
    for p_aba in contexto.pages:
        try:
            if p_aba.locator("[id='cadastroPlanoMetas:linhaAcoesInternas']").count() > 0:
                alvo = p_aba
                pagina = p_aba
                break
        except:
            continue

    # Isola APENAS o bloco de Ações Internas
    bloco = alvo.locator("[id='cadastroPlanoMetas:linhaAcoesInternas']")

    campo_acao = bloco.locator(
        "xpath=.//span[@id='cadastroPlanoMetas:nome_acao_interna_label']/ancestor::tr[1]//td//*[self::textarea or self::input]").first
    select_motivacao = bloco.locator("xpath=.//th[contains(., 'Motivação:')]/following-sibling::td[1]//select").first
    campo_rubrica = bloco.locator(
        "xpath=.//th[contains(., 'brica:')]/following-sibling::td[1]//input[@type='text']").first
    campo_valor = bloco.locator(
        "xpath=.//th[contains(., 'Valor Planejado:')]/following-sibling::td[1]//input[@type='text']").first
    campo_responsavel = bloco.locator(
        "xpath=.//th[contains(., 'Responsável pela Ação Interna:')]/following-sibling::td[1]//input[@type='text']").first

    # Botão Adicionar restrito estritamente ao bloco de Ações Internas
    botao_adicionar = bloco.locator("xpath=.//input[@value='Adicionar']").first

    print("🔍 Verificando campos dentro de 'cadastroPlanoMetas:linhaAcoesInternas' (1 = OK):")
    print(f"   - Ação Interna (textarea): {campo_acao.count()}")
    print(f"   - Motivação (select):      {select_motivacao.count()}")
    print(f"   - Rúbrica (input):         {campo_rubrica.count()}")
    print(f"   - Valor Planejado (input): {campo_valor.count()}")
    print(f"   - Responsável (input):     {campo_responsavel.count()}")
    print(f"   - Botão Adicionar Exato:   {botao_adicionar.count()}")

    # Loop pelas linhas da planilha
    for indice, linha in df.iterrows():
        acao = str(linha["Ação Interna"]).strip()
        motivacao = str(linha["Motivação"]).strip().replace("ORCAMENTÁRIO", "ORÇAMENTÁRIO")
        rubrica = str(linha["Rúbrica"]).strip()

        # Formata o valor monetário padrão
        valor_formatado = f"R$ {int(linha['Valor Planejado']):,}".replace(",", ".") + ",00"

        responsavel = str(linha["Responsável"]).strip()

        print(f"\n[{indice + 1}/{len(df)}] Cadastrando: {acao} | Rubrica: {rubrica} | Valor: {valor_formatado}")

        try:
            # 1. Preenche Ação Interna (textarea)
            campo_acao.wait_for(state="visible", timeout=10000)
            campo_acao.click()
            campo_acao.fill(acao)
            pagina.wait_for_timeout(300)

            # 2. Seleciona a Motivação (ORÇAMENTÁRIO - CAMPUS)
            select_motivacao.select_option(label=motivacao)
            pagina.wait_for_timeout(800)

            # 3. Preenche Rúbrica e confirma com Enter (seleciona a opção destacada em azul)
            campo_rubrica.click()
            campo_rubrica.fill("")
            campo_rubrica.press_sequentially(rubrica, delay=120)

            pagina.wait_for_timeout(1500)  # Aguarda o autocomplete carregar
            campo_rubrica.press("Enter")  # Confirma a seleção em azul
            pagina.wait_for_timeout(800)

            # 4. Preenche Valor Planejado
            campo_valor.click()
            campo_valor.press("Control+A")
            campo_valor.press("Backspace")
            campo_valor.fill(valor_formatado)
            pagina.wait_for_timeout(400)

            # 5. Preenche Responsável pela Ação Interna e confirma com Enter
            campo_responsavel.click()
            campo_responsavel.fill("")
            campo_responsavel.press_sequentially(responsavel, delay=100)

            pagina.wait_for_timeout(1800)  # Aguarda o autocomplete carregar
            campo_responsavel.press("Enter")  # Confirma a seleção em azul
            pagina.wait_for_timeout(1000)

            # 6. Clica estritamente no botão Adicionar da tabela de Ações Internas
            botao_adicionar.click()

            # 7. Aguarda o SIGPP processar o AJAX e limpar o campo 'Ação Interna'
            for _ in range(15):
                pagina.wait_for_timeout(500)
                try:
                    if campo_acao.input_value().strip() == "":
                        break
                except:
                    pass

            pagina.wait_for_timeout(1000)

            print(f"✅ Linha {indice + 1} adicionada com sucesso!")

        except Exception as erro:
            print(f"❌ Erro na linha {indice + 1} ({acao}): {erro}")
            resposta = input("Deseja tentar continuar para a próxima linha? (s/n): ")
            if resposta.lower() != 's':
                break

    print("\n🎉 Processo finalizado! Verifique a lista na tela do SIGPP antes de gravar/avançar.")
    print("\n ATENÇÃO! Não feche o terminal ou página antes de clicar no botão: 'Atualizar Ação'")
    input("Aperte ENTER no terminal para fechar o navegador...")
    navegador.close()