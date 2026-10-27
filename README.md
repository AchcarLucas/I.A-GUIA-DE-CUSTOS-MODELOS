# Guia de Modelos de IA e Custos — GitHub Copilot

Guia comparativo de modelos de inteligência artificial voltados para **revisão manual de código (Code Review)**, com foco em custo-benefício, qualidade de análise e eficiência no desenvolvimento de software.

O objetivo é ajudar desenvolvedores a escolher o modelo mais adequado para cada tarefa, comparando os custos de contratação direta por API com os valores de referência do GitHub Copilot.

## 🛠️ Gerando o guia

É necessário ter o Python instalado. No terminal, na pasta do projeto, crie e ative um ambiente virtual:

**Linux ou macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Com o ambiente virtual ativado, instale as dependências e execute o script:

```bash
python -m pip install -r requirements.txt
python gerar_guia.py
```

O PDF gerado, `guia_copilot_modelos_custos_revisado_v2.pdf`, será salvo na pasta do projeto. Para sair do ambiente virtual, execute `deactivate`.


## 📄 Documento

[**Baixar ou visualizar o guia em PDF**](guia_copilot_modelos_custos-detalhado-v2.pdf)

## 📊 O que você encontrará

- **Comparativo de modelos:** modelos da OpenAI, Anthropic e Google.
- **Empresa e licença:** identificação dos fornecedores e distinção entre modelos proprietários e modelos de pesos abertos.
- **Custos por token:** estimativas dos preços de entrada e saída por milhão de tokens.
- **API direta vs. GitHub Copilot:** comparação dos custos de referência e explicação do sistema de créditos do Copilot.
- **Recomendações de uso:** escolha de modelos para revisões simples, investigação de bugs complexos e análise de grandes volumes de código.
- **Estratégias de economia:** boas práticas para reduzir o consumo de tokens sem comprometer a qualidade das revisões.

## 🎯 Objetivo

O foco é otimizar o processo de revisão de código, ajudando a identificar problemas lógicos, possíveis vulnerabilidades, erros de concorrência e oportunidades de refatoração sem gerar despesas desnecessárias.

A proposta é utilizar modelos mais econômicos para tarefas simples e reservar modelos mais capazes para análises que realmente exigem raciocínio aprofundado.

## 💰 Como os custos são comparados?

Os preços são apresentados em dólares americanos (USD), considerando:

- Tokens de entrada (*input tokens*).
- Tokens de saída (*output tokens*).
- Tarifas de referência por milhão de tokens.
- Diferenças entre o uso direto das APIs e o sistema de créditos do GitHub Copilot.

**Importante:** os preços são estimativas de referência e podem mudar. O custo efetivo do Copilot depende do plano contratado, dos créditos incluídos, do modelo utilizado e das regras de cobrança vigentes. Assinaturas de produtos de IA não devem ser confundidas com créditos de API.

## ⚠️ Observações

- A disponibilidade dos modelos pode variar conforme o plano, a região e a integração utilizada.
- Modelos proprietários não são considerados open source apenas por estarem disponíveis no Copilot.
- Modelos de pesos abertos também podem gerar custos de infraestrutura, hardware, energia e hospedagem.
- Os valores não representam uma cotação contratual. Consulte as fontes oficiais antes de tomar decisões financeiras.

## 🔗 Fontes oficiais

- [GitHub Copilot — Modelos e preços](https://docs.github.com/pt/copilot/reference/copilot-billing/models-and-pricing)
- [GitHub Copilot — Cobrança e utilização](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing)
- [OpenAI API — Preços](https://developers.openai.com/api/docs/pricing)
- [Anthropic — Preços da API Claude](https://docs.anthropic.com/en/docs/about-claude/pricing)
- [Google Gemini API — Preços](https://ai.google.dev/gemini-api/docs/pricing)

## 📅 Atualização

Versão do guia: **26 de outubro de 2026**.

Como os fornecedores atualizam modelos, tarifas e condições de acesso, recomenda-se verificar as fontes oficiais antes de utilizar os valores em estimativas de orçamento.

## 📜 Licença

Este repositório reúne material informativo e comparativo. Caso deseje permitir reutilização, modificação e redistribuição do conteúdo, adicione um arquivo `LICENSE` com a licença escolhida.

---

Desenvolvido para auxiliar desenvolvedores na escolha de modelos de IA para revisão de código com melhor custo-benefício.
