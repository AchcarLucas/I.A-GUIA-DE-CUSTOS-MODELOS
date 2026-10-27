# Guia de custos de modelos de IA — GitHub Copilot e das APIs oficiais

Guia comparativo de modelos de inteligência artificial voltados para **revisão manual de código (Code Review)**, com foco em custo-benefício, qualidade de análise e eficiência no desenvolvimento de software.

O objetivo é ajudar desenvolvedores a escolher o modelo mais adequado para cada tarefa, comparando os custos de contratação direta por API com os valores de referência do GitHub Copilot.

<p align="center">
	<img src="assets/og-guia.png" alt="Capa do guia de custos de modelos de IA">
</p>

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
python gerar_guia_copilot.py
python gerar_og_guia.py
```

`gerar_og_guia.py` recria a imagem de compartilhamento em `assets/og-guia.svg` e `assets/og-guia.png`. Além do pacote Python, ele precisa da biblioteca de sistema libcairo (no Ubuntu/Debian: `libcairo2`).

## 📄 Documento

- [**Acessar o guia online**](https://ia.guia.lcadev.com.br)
- [**Baixar ou visualizar a última versão em PDF**](guia_copilot_modelos_custos-detalhado-latest.pdf)

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

- [GitHub Copilot — preços por modelo](https://docs.github.com/pt/copilot/reference/copilot-billing/models-and-pricing): tarifas por tokens e multiplicadores de uso.
- [GitHub Copilot — modelos compatíveis](https://docs.github.com/en/copilot/reference/ai-models/supported-models): disponibilidade e provedores dos modelos.
- [GitHub Copilot — cobrança e utilização](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing): regras de cobrança e créditos do plano.
- [OpenAI API — preços](https://developers.openai.com/api/docs/pricing): tarifas de entrada, saída e cache.
- [Anthropic — Claude Haiku 5.5](https://www.anthropic.com/claude-haiku-5-5), [Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5) e [Opus 5.5](https://www.anthropic.com/claude-opus-5-5): preços dos modelos Claude e cache.
- [Google — preços da Gemini API](https://ai.google.dev/gemini-api/docs/pricing): tarifas dos modelos Gemini.
- [Microsoft Foundry — catálogo MAI-Code-1.1-Flash](https://ai.azure.com/catalog/models/mai-code-1.1-flash): detalhes do modelo; o custo de implantação deve ser conferido no Azure.
- [xAI — preços da API](https://docs.x.ai/developers/pricing): tarifas de modelos Grok.
- [Moonshot AI — anúncio do Kimi K3](https://forum.moonshot.ai/t/kimi-k3-is-here-our-most-capable-model/480): referência publicada para o modelo Kimi.

## 📅 Atualização

Versão do guia: **26 de outubro de 2026**.

Modelos, tarifas e condições de acesso podem mudar. Consulte as fontes oficiais antes de estimar custos; a inclusão de um modelo em um catálogo não significa que exista uma tarifa pública direta para ele.

## 📜 Licença

Este repositório reúne material informativo e comparativo. Caso deseje permitir reutilização, modificação e redistribuição do conteúdo, adicione um arquivo `LICENSE` com a licença escolhida.

---

Desenvolvido para auxiliar desenvolvedores na escolha de modelos de IA para revisão de código com melhor custo-benefício.
