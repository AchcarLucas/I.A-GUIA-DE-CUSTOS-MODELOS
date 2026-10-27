"""
Gera o PDF comparativo de modelos e custos do GitHub Copilot.

Requisitos:
    python -m pip install reportlab

Execução:
    python gerar_guia_copilot.py

O PDF será criado na mesma pasta deste script. Os dados dos modelos e preços
estão no bloco `models` abaixo; atualize-os e revise as fontes oficiais antes
de republicar, pois nomes, tarifas e disponibilidade podem mudar.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, HRFlowable
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
import shutil
from pathlib import Path

VERSION = "2.1"
OUTPUT_DIR = Path(__file__).resolve().parent
OUT = str(OUTPUT_DIR / f"guia_copilot_modelos_custos-detalhado-v{VERSION}.pdf")
LATEST_OUT = str(OUTPUT_DIR / "guia_copilot_modelos_custos-detalhado-latest.pdf")

# Typography
regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if os.path.exists(regular):
    pdfmetrics.registerFont(TTFont("DV", regular))
    pdfmetrics.registerFont(TTFont("DV-Bold", bold))
    F, FB = "DV", "DV-Bold"
else:
    F, FB = "Helvetica", "Helvetica-Bold"

# Palette
navy = colors.HexColor("#16324F")
blue = colors.HexColor("#2463A6")
pale_blue = colors.HexColor("#EAF2F8")
pale = colors.HexColor("#F5F7FA")
line = colors.HexColor("#D5DDE6")
ink = colors.HexColor("#17212B")
gray = colors.HexColor("#566273")
white = colors.white
amber = colors.HexColor("#FFF3D6")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitleX", fontName=FB, fontSize=25, leading=30, textColor=white, spaceAfter=7))
styles.add(ParagraphStyle(name="CoverSubX", fontName=F, fontSize=10, leading=15, textColor=colors.HexColor("#E8F0F7")))
styles.add(ParagraphStyle(name="H1X", fontName=FB, fontSize=16, leading=20, textColor=navy, spaceBefore=2, spaceAfter=7))
styles.add(ParagraphStyle(name="H2X", fontName=FB, fontSize=10.5, leading=14, textColor=blue, spaceBefore=7, spaceAfter=4))
styles.add(ParagraphStyle(name="BodyX", fontName=F, fontSize=8.2, leading=11.3, textColor=ink, spaceAfter=4))
styles.add(ParagraphStyle(name="SmallX", fontName=F, fontSize=6.8, leading=8.7, textColor=gray, spaceAfter=3))
styles.add(ParagraphStyle(name="CellX", fontName=F, fontSize=6.25, leading=7.8, textColor=ink))
styles.add(ParagraphStyle(name="CellBoldX", fontName=FB, fontSize=6.35, leading=7.9, textColor=navy))
styles.add(ParagraphStyle(name="CellHeadX", fontName=FB, fontSize=6.3, leading=7.6, textColor=white))
styles.add(ParagraphStyle(name="CalloutX", fontName=F, fontSize=8, leading=11, textColor=ink))
styles.add(ParagraphStyle(name="SourceX", fontName=F, fontSize=7, leading=9.5, textColor=blue))

def P(s, style="BodyX"):
    return Paragraph(s, styles[style])

def page_decor(canvas, doc):
    canvas.saveState()
    w, h = doc.pagesize
    if doc.page > 1:
        canvas.setFillColor(navy)
        canvas.rect(0, h - 9*mm, w, 9*mm, fill=1, stroke=0)
        canvas.setFont(FB, 7)
        canvas.setFillColor(white)
        canvas.drawString(13*mm, h - 6.1*mm, "GUIA COPILOT | MODELOS, EMPRESAS E CUSTOS")
        canvas.setStrokeColor(line)
        canvas.line(13*mm, 12*mm, w - 13*mm, 12*mm)
        canvas.setFont(F, 6.5)
        canvas.setFillColor(gray)
        canvas.drawString(13*mm, 7.5*mm, "USD por 1 milhão de tokens | Consulta: 26/10/2026")
        canvas.drawRightString(w - 13*mm, 7.5*mm, f"Página {doc.page}")
    canvas.restoreState()

# Columns: provider/license; direct API input/output; Copilot input/cached/write/output; context note.
# Prices are USD per 1M tokens. Direct API is only filled where a public exact/model-equivalent tariff could be verified.
models = [
    # OpenAI
    dict(model="GPT-5.3-Codex", comp="OpenAI | Proprietário", direct="$1.75 / $14.00", ci="$1.75", cc="$0.175", cw="—", co="$14.00", note="Categoria Copilot: Powerful. Sem tier longo listado na tabela de preços."),
    dict(model="GPT-5.4 nano", comp="OpenAI | Proprietário", direct="$0.20 / $1.25", ci="$0.20", cc="$0.02", cw="—", co="$1.25", note="Categoria: Lightweight."),
    dict(model="GPT-5.6 Luna", comp="OpenAI | Proprietário", direct="$0.20 / $1.20", ci="$0.20", cc="$0.02", cw="$0.25", co="$1.20", note="Padrão ≤200K: mostrado. Longo >200K: entrada $0.40, cache $0.04, gravação $0.50, saída $1.80."),
    dict(model="GPT-5.6 Sol", comp="OpenAI | Proprietário", direct="$4.00 / $20.00", ci="$4.00", cc="$0.40", cw="$5.00", co="$20.00", note="Padrão ≤272K. Longo >272K: entrada $8, cache $0.80, gravação $10, saída $30. API: tarifa padrão consultada; preço promocional pode variar."),
    dict(model="GPT-5.6 Terra", comp="OpenAI | Proprietário", direct="$2.00 / $12.00", ci="$2.00", cc="$0.20", cw="$2.50", co="$12.00", note="Padrão ≤272K. Longo >272K: entrada $4, cache $0.40, gravação $5, saída $18."),
    dict(model="GPT-6 Astra", comp="OpenAI | Proprietário", direct="$10.00 / $50.00", ci="$10.00", cc="$1.00", cw="$12.50", co="$50.00", note="Padrão ≤272K. Longo >272K: entrada $20, cache $2, gravação $25, saída $75."),
    dict(model="GPT-6 Luna", comp="OpenAI | Proprietário", direct="$0.10 / $0.50", ci="$0.10", cc="$0.01", cw="$0.125", co="$0.50", note="Padrão ≤272K. Longo >272K: entrada $0.20, cache $0.02, gravação $0.25, saída $0.75."),
    dict(model="GPT-6 Sol", comp="OpenAI | Proprietário", direct="$2.00 / $10.00", ci="$2.00", cc="$0.20", cw="$2.50", co="$10.00", note="Padrão ≤272K. Longo >272K: entrada $4, cache $0.40, gravação $5, saída $15."),
    dict(model="GPT-6.1 Sol", comp="OpenAI | Proprietário", direct="$2.00 / $10.00", ci="$2.00", cc="$0.10", cw="$2.50", co="$10.00", note="Padrão ≤272K. Longo >272K: entrada $4, cache $0.20, gravação $5, saída $15."),
    dict(model="GPT-6.1 Terra", comp="OpenAI | Proprietário", direct="$1.00 / $5.00", ci="$1.00", cc="$0.05", cw="$1.25", co="$5.00", note="Padrão ≤272K. Longo >272K: entrada $2, cache $0.10, gravação $2.50, saída $7.50."),
    # Anthropic
    dict(model="Claude Haiku 4.5", comp="Anthropic | Proprietário", direct="$1.00 / $5.00", ci="$1.00", cc="$0.10", cw="$1.25", co="$5.00", note="Categoria Copilot: Versatile."),
    dict(model="Claude Haiku 5.5", comp="Anthropic | Proprietário", direct="$0.10 / $0.50 (≤100K)", ci="$0.10", cc="$0.01", cw="$0.125", co="$0.50", note="Padrão ≤100K. Longo >100K: entrada $0.50, cache $0.05, gravação $0.625, saída $2.50. API direta também tem tarifa longa."),
    dict(model="Claude Sonnet 4.6", comp="Anthropic | Proprietário", direct="$3.00 / $15.00", ci="$3.00", cc="$0.30", cw="$3.75", co="$15.00", note="Categoria Copilot: Versatile."),
    dict(model="Claude Opus 4.8", comp="Anthropic | Proprietário", direct="$5.00 / $25.00", ci="$5.00", cc="$0.50", cw="$6.25", co="$25.00", note="Categoria Copilot: Powerful."),
    dict(model="Claude Opus 4.8 (fast mode)", comp="Anthropic | Proprietário", direct="N/D*; base $5 / $25", ci="$10.00", cc="$1.00", cw="$12.50", co="$50.00", note="Preview no Copilot. *Tarifa direta da variante fast não confirmada com SKU equivalente."),
    dict(model="Claude Opus 5", comp="Anthropic | Proprietário", direct="$5.00 / $25.00", ci="$5.00", cc="$0.50", cw="$6.25", co="$25.00", note="Categoria Copilot: Powerful."),
    dict(model="Claude Opus 5.5", comp="Anthropic | Proprietário", direct="$4.00 / $20.00", ci="$4.00", cc="$0.20", cw="$5.00", co="$20.00", note="Categoria Copilot: Powerful. Cache de leitura: $0.20/M."),
    dict(model="Claude Sonnet 5", comp="Anthropic | Proprietário", direct="$2.00 / $10.00", ci="$2.00", cc="$0.20", cw="$2.50", co="$10.00", note="Categoria Copilot: Versatile."),
    dict(model="Claude Sonnet 5.5", comp="Anthropic | Proprietário", direct="$2.00 / $10.00", ci="$2.00", cc="$0.10", cw="$2.50", co="$10.00", note="Categoria Copilot: Versatile. Preço de cache de leitura foi reduzido para $0.10/M."),
    dict(model="Claude Fable 5", comp="Anthropic | Proprietário", direct="N/D*", ci="$10.00", cc="$1.00", cw="$12.50", co="$50.00", note="*Não localizei tarifa pública de API para o nome exato; preço Copilot oficial informado."),
    dict(model="Claude Fable 5.1", comp="Anthropic | Proprietário", direct="N/D*", ci="$10.00", cc="$0.25", cw="$12.50", co="$50.00", note="*Não localizei tarifa pública de API para o nome exato; preço Copilot oficial informado."),
    # Google
    dict(model="Gemini 3.8 Flash", comp="Google | Proprietário", direct="$0.75 / $3.75**", ci="$0.75", cc="$0.075", cw="—", co="$3.75", note="**API: preço promocional até 31/12/2026; passa a $1.50/$7.50 em 01/01/2027."),
    dict(model="Gemini 4 Argon", comp="Google | Proprietário", direct="$2.00 / $10.00**", ci="$2.00", cc="$0.10", cw="—", co="$10.00", note="**API: preço promocional até 30/11/2026; passa a $4.00/$20.00 em 01/12/2026."),
    # Microsoft
    dict(model="MAI-Code-1.1-Flash", comp="Microsoft | Proprietário", direct="N/D*", ci="$0.20", cc="$0.02", cw="—", co="$1.20", note="*Modelo hospedado no Azure; catálogo Foundry oferece cotação/seleção de preço por implantação."),
    # Moonshot
    dict(model="Kimi K3", comp="Moonshot AI | Proprietário", direct="$3.00 / $15.00", ci="$3.00", cc="$0.30", cw="—", co="$15.00", note="Categoria Copilot: Powerful. API direta informa $0.30/M para entrada em cache."),
    # xAI
    dict(model="Grok 4.5", comp="xAI | Proprietário", direct="$2.00 / $6.00", ci="$2.00", cc="$0.50", cw="—", co="$6.00", note="Padrão ≤200K. Copilot longo >200K: entrada $4, cache $1, saída $12. API direta tem entrada em cache de $0.30/M."),
    dict(model="Grok 4.6", comp="xAI | Proprietário", direct="$2.00 / $6.00", ci="$2.00", cc="$0.50", cw="—", co="$6.00", note="Padrão ≤200K. Longo >200K: entrada $4, cache $1, saída $12."),
    dict(model="Grok 4.7", comp="xAI | Proprietário", direct="$2.00 / $6.00", ci="$2.00", cc="$0.50", cw="—", co="$6.00", note="Padrão ≤200K. Longo >200K: entrada $4, cache $1, saída $12."),
]
assert len(models) == 28, len(models)

doc = SimpleDocTemplate(
    OUT, pagesize=landscape(A4),
    rightMargin=13*mm, leftMargin=13*mm,
    topMargin=14*mm, bottomMargin=15*mm,
    title=f"Guia de modelos do GitHub Copilot e custos por token v{VERSION}",
    author="OpenAI"
)
story=[]

# Cover
banner = Table([
    [P("GUIA DE MODELOS E CUSTOS", "CoverTitleX")],
    [P("GitHub Copilot vs. APIs oficiais • Revisão manual de código", "CoverSubX")],
    [P(f"Versão {VERSION} | Lista de modelos consultada em 26 de outubro de 2026", "CoverSubX")]
], colWidths=[landscape(A4)[0]-26*mm])
banner.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),navy),
    ("LEFTPADDING",(0,0),(-1,-1),12*mm),("RIGHTPADDING",(0,0),(-1,-1),12*mm),
    ("TOPPADDING",(0,0),(-1,0),12*mm),("BOTTOMPADDING",(0,0),(-1,0),2*mm),
    ("TOPPADDING",(0,1),(-1,1),1*mm),("BOTTOMPADDING",(0,1),(-1,1),2*mm),
    ("TOPPADDING",(0,2),(-1,2),0),("BOTTOMPADDING",(0,2),(-1,2),10*mm)
]))
story += [Spacer(1,7*mm), banner, Spacer(1,8*mm)]
story.append(P("Objetivo desta revisão", "H1X"))
story.append(P("Esta versão inclui os 28 modelos listados na documentação oficial de modelos com suporte no GitHub Copilot, identifica o fornecedor e se o modelo é proprietário, compara preços de referência por milhão de tokens no Copilot e na API direta quando há uma tarifa pública verificável e corrige os exemplos matemáticos de custo por token.", "BodyX"))
story.append(P("Leitura rápida", "H2X"))
quick = [
    [P("<b>API direta</b>", "CellX"), P("Você paga ao fornecedor por tokens processados segundo a tarifa do endpoint, com possíveis diferenças de cache, contexto longo, processamento prioritário e região.", "CellX")],
    [P("<b>GitHub Copilot</b>", "CellX"), P("O consumo de modelos é convertido em GitHub AI Credits. 1 crédito equivale a US$ 0,01; a assinatura pode incluir uma franquia de créditos. A tabela representa tarifas de referência para uso adicional, não necessariamente uma cobrança extra em toda interação.", "CellX")],
    [P("<b>Open source</b>", "CellX"), P("Nenhum dos 28 modelos desta lista está identificado aqui como modelo de pesos abertos. Todos são tratados como modelos proprietários/serviços hospedados. A licença exata deve ser verificada na fonte do fornecedor.", "CellX")],
    [P("<b>Preços indisponíveis</b>", "CellX"), P("Quando a API pública não mostra uma tarifa para o nome exato do modelo, o documento marca N/D. Não foi usada uma estimativa inventada para preencher a lacuna.", "CellX")],
]
qt=Table(quick,colWidths=[38*mm,landscape(A4)[0]-26*mm-38*mm])
qt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(0,-1),pale_blue),("BACKGROUND",(1,0),(1,-1),pale),
    ("GRID",(0,0),(-1,-1),0.4,line),("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)
]))
story.append(qt)
story.append(Spacer(1,4*mm))
story.append(P("<b>Como ler a tabela:</b> todos os preços são USD por 1 milhão de tokens. “Entrada” é o texto/contexto enviado ao modelo; “entrada em cache” é conteúdo reutilizado quando elegível; “gravação em cache” é o custo de criar o cache em modelos que cobram por isso; “saída” são os tokens gerados. Os custos de cache não devem ser somados à entrada normal para os mesmos tokens: são categorias alternativas conforme o tipo de token faturado.", "CalloutX"))
story.append(PageBreak())

story.append(P("1. Todos os modelos suportados e seus custos", "H1X"))
story.append(P("A coluna API direta mostra entrada/saída padrão do fornecedor para o modelo correspondente quando foi possível verificar uma tarifa pública. A tabela Copilot é a fonte autoritativa para valores usados no Copilot. Tarifas especiais, cache e contexto longo podem mudar o custo final.", "SmallX"))

table_data = [[
    P("Modelo", "CellHeadX"),
    P("Empresa | tipo", "CellHeadX"),
    P("API direta<br/>Entrada / saída", "CellHeadX"),
    P("Copilot<br/>Entrada", "CellHeadX"),
    P("Entrada<br/>em cache", "CellHeadX"),
    P("Gravação<br/>em cache", "CellHeadX"),
    P("Copilot<br/>Saída", "CellHeadX"),
    P("Contexto, categoria e observações", "CellHeadX"),
]]
for m in models:
    table_data.append([
        P(m["model"], "CellBoldX"),
        P(m["comp"], "CellX"),
        P(m["direct"], "CellX"),
        P(m["ci"], "CellX"),
        P(m["cc"], "CellX"),
        P(m["cw"], "CellX"),
        P(m["co"], "CellX"),
        P(m["note"], "CellX")
    ])
widths=[32*mm,27*mm,31*mm,22*mm,22*mm,23*mm,22*mm,72*mm]
model_table=Table(table_data,colWidths=widths,repeatRows=1,splitByRow=1)
model_table.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),blue),
    ("GRID",(0,0),(-1,-1),0.35,line),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[white,pale]),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",(0,0),(-1,-1),4),
    ("RIGHTPADDING",(0,0),(-1,-1),4),
    ("TOPPADDING",(0,0),(-1,-1),4),
    ("BOTTOMPADDING",(0,0),(-1,-1),4),
]))
story.append(model_table)
story.append(Spacer(1,3*mm))
story.append(P("Legenda: “—” significa que a tabela oficial do Copilot não informa uma tarifa separada de gravação em cache para aquele modelo. “N/D” indica que não foi possível confirmar uma tarifa pública para a API direta com o nome exato; não significa que nunca possa haver acesso por outro provedor ou contrato.", "SmallX"))
story.append(PageBreak())

story.append(P("2. Como entender o custo por token", "H1X"))
story.append(P("O preço por milhão é o formato usado pelas tabelas oficiais. Para obter o custo unitário por token, divida o valor por 1.000.000. O exemplo abaixo considera entrada não armazenada em cache, saída normal, contexto padrão e nenhuma chamada de ferramenta adicional.", "BodyX"))

# Correct per-token math based on official Copilot standard rates.
calc = [
    [P("Modelo (tarifa Copilot padrão)", "CellHeadX"),
     P("Entrada por 1M", "CellHeadX"),
     P("Saída por 1M", "CellHeadX"),
     P("Entrada por token", "CellHeadX"),
     P("Saída por token", "CellHeadX"),
     P("100 mil entrada + 10 mil saída", "CellHeadX")],
    [P("GPT-6 Luna", "CellBoldX"), P("$0.10", "CellX"), P("$0.50", "CellX"),
     P("$0.00000010", "CellX"), P("$0.00000050", "CellX"), P("$0.015 = $0.010 + $0.005", "CellX")],
    [P("Claude Haiku 5.5 (prompt ≤100K)", "CellBoldX"), P("$0.10", "CellX"), P("$0.50", "CellX"),
     P("$0.00000010", "CellX"), P("$0.00000050", "CellX"), P("$0.015 = $0.010 + $0.005", "CellX")],
    [P("Claude Sonnet 5.5", "CellBoldX"), P("$2.00", "CellX"), P("$10.00", "CellX"),
     P("$0.00000200", "CellX"), P("$0.00001000", "CellX"), P("$0.30 = $0.200 + $0.100", "CellX")],
    [P("GPT-6 Sol", "CellBoldX"), P("$2.00", "CellX"), P("$10.00", "CellX"),
     P("$0.00000200", "CellX"), P("$0.00001000", "CellX"), P("$0.30 = $0.200 + $0.100", "CellX")],
    [P("GPT-6 Astra", "CellBoldX"), P("$10.00", "CellX"), P("$50.00", "CellX"),
     P("$0.00001000", "CellX"), P("$0.00005000", "CellX"), P("$1.50 = $1.000 + $0.500", "CellX")],
]
calc_table=Table(calc,colWidths=[47*mm,23*mm,23*mm,31*mm,31*mm,74*mm],repeatRows=1)
calc_table.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),navy),
    ("GRID",(0,0),(-1,-1),0.4,line),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[white,pale]),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)
]))
story.append(calc_table)
story.append(Spacer(1,4*mm))
story.append(P("Fórmula correta", "H2X"))
story.append(P("Custo = (tokens de entrada ÷ 1.000.000 × tarifa de entrada) + (tokens de saída ÷ 1.000.000 × tarifa de saída).", "BodyX"))
story.append(P("Exemplo — GPT-6 Luna", "H2X"))
story.append(P("Entrada: 100.000 ÷ 1.000.000 × US$ 0,10 = US$ 0,010. Saída: 10.000 ÷ 1.000.000 × US$ 0,50 = US$ 0,005. Total: US$ 0,015. O total é 1,5 centavo de dólar, não US$ 0,15 nem US$ 1,50.", "BodyX"))
story.append(P("Atenção ao contexto longo", "H2X"))
story.append(P("O preço pode aumentar quando o prompt ultrapassa o limite específico do modelo. Exemplo: Claude Haiku 5.5 muda de US$ 0,10/US$ 0,50 para US$ 0,50/US$ 2,50 por milhão de tokens acima de 100K tokens de entrada. Para GPT-6 Luna, a tabela Copilot dobra as tarifas de entrada/saída no tier longo acima de 272K tokens. Use a linha do tier correto para estimar.", "BodyX"))
story.append(P("Entrada em cache", "H2X"))
story.append(P("Quando a plataforma informa tokens faturados como entrada em cache, aplique a tarifa de cache àquela parcela. Não calcule o mesmo token simultaneamente pela tarifa normal e pela tarifa cache. Modelos com gravação de cache podem ainda cobrar um valor separado ao criar o cache.", "BodyX"))
story.append(PageBreak())

story.append(P("3. API direta vs. GitHub Copilot", "H1X"))
comparison = [
    [P("Contratação direta por API", "CellHeadX"), P("Uso no GitHub Copilot", "CellHeadX")],
    [P("O fornecedor cobra pelo consumo de tokens, usando as regras do endpoint. Pode haver descontos ou sobretaxas para cache, processamento em lote, contexto longo, prioridade e região.", "CellX"),
     P("O GitHub converte o uso em AI Credits. A tarifa por milhão de tokens é expressa em créditos equivalentes a dólares: 1 AI Credit = US$ 0,01. Os planos incluem franquias de créditos conforme as condições do plano.", "CellX")],
    [P("As tarifas na tabela são do serviço de API correspondente quando publicadas. Um nome de modelo disponível no Copilot pode não estar disponível com o mesmo SKU em uma API pública direta.", "CellX"),
     P("Quando os créditos incluídos cobrem o uso, o custo marginal pago pode ser zero até o limite da franquia. Ao exceder a franquia, aplicam-se as regras de cobrança adicional vigentes.", "CellX")],
]
cmp=Table(comparison,colWidths=[(landscape(A4)[0]-26*mm)/2]*2)
cmp.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),blue),("GRID",(0,0),(-1,-1),0.4,line),
    ("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),8),
    ("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),7),
    ("BOTTOMPADDING",(0,0),(-1,-1),7),("ROWBACKGROUNDS",(0,1),(-1,-1),[white,pale])
]))
story.append(cmp)
story.append(Spacer(1,4*mm))
story.append(P("<b>Nota para revisão de código:</b> a função “Copilot code review” pode selecionar automaticamente o modelo, e a cobrança também pode incluir minutos de GitHub Actions. Portanto, esta comparação de tokens é uma estimativa para entender as tarifas de modelos, não uma previsão garantida do custo de uma revisão automatizada.", "CalloutX"))

story.append(P("4. Recomendações para code review", "H1X"))
workflow=[
    [P("1. Triagem econômica", "CellBoldX"), P("Use um modelo leve para enumerar riscos, funções suspeitas, casos extremos e testes ausentes. Limite o contexto aos arquivos relevantes. <b>Modelos sugeridos:</b> GPT-6 Luna ou Claude Haiku 5.5, opções de menor custo na tabela.", "CellX")],
    [P("2. Investigação complexa", "CellBoldX"), P("Use um modelo versátil ou potente para revisar fluxos entre arquivos, concorrência, autenticação, estado compartilhado e regressões. Forneça o diff e o comportamento esperado. <b>Modelos sugeridos:</b> Claude Opus 5.5 ou GPT-6 Astra para análise profunda; GPT-6 Sol como alternativa de menor custo.", "CellX")],
    [P("3. Verificação", "CellBoldX"), P("Solicite referências a arquivo/linha, hipótese reproduzível e teste que falharia antes da correção. Valide as recomendações executando testes e conferindo o código. <b>Modelos sugeridos:</b> Claude Sonnet 5.5 ou GPT-6 Sol para uma segunda análise equilibrada; execute os testes independentemente do modelo.", "CellX")],
    [P("4. Controle de contexto e custo", "CellBoldX"), P("Evite enviar o repositório inteiro se apenas alguns arquivos forem relevantes. Ao mudar de modelo, não presuma que todo cache sempre será invalidado: isso depende do produto e da implementação. <b>Modelos sugeridos:</b> GPT-6 Luna para contextos menores e GPT-6.1 Terra quando uma análise realmente exigir mais contexto; confira os tiers e custos de cache na tabela.", "CellX")],
]
wt=Table(workflow,colWidths=[42*mm,landscape(A4)[0]-26*mm-42*mm])
wt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(0,-1),pale_blue),("BACKGROUND",(1,0),(1,-1),pale),
    ("GRID",(0,0),(-1,-1),0.4,line),("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)
]))
story.append(wt)
story.append(PageBreak())

story.append(P("5. Fontes oficiais e metodologia", "H1X"))
story.append(P("Lista de modelos e tarifas consultadas em 26/10/2026. Os fornecedores podem alterar nomes, disponibilidade, limites de contexto, descontos e preços. A coluna de API direta reflete tarifas públicas que puderam ser verificadas para o nome exato ou correspondente do modelo; “N/D” foi usado quando isso não foi confirmado.", "BodyX"))

sources=[
    ("GitHub Docs — Modelos e preços para GitHub Copilot",
     "https://docs.github.com/pt/copilot/reference/copilot-billing/models-and-pricing",
     "Fonte das tarifas por 1 milhão de tokens no Copilot, incluindo entrada, cache, gravação de cache, saída e tiers de contexto."),
    ("GitHub Docs — Modelos de IA com suporte no Copilot",
     "https://docs.github.com/en/copilot/reference/ai-models/supported-models",
     "Fonte da lista de modelos com suporte e seus provedores. A disponibilidade pode depender do plano, cliente e políticas da organização."),
    ("OpenAI API — Pricing",
     "https://developers.openai.com/api/docs/pricing",
     "Fonte de referência para os modelos GPT e suas tarifas de API."),
    ("Anthropic — Claude Haiku 5.5",
     "https://www.anthropic.com/claude-haiku-5-5",
     "Fonte para tarifas de Haiku 5.5 e comparação de tarifas atuais de Haiku/Sonnet."),
    ("Anthropic — Claude Sonnet 5.5",
     "https://www.anthropic.com/claude-sonnet-5-5",
     "Fonte para tarifas de Sonnet 5.5 e preços de cache."),
    ("Anthropic — Claude Opus 5.5",
     "https://www.anthropic.com/claude-opus-5-5",
     "Fonte para tarifas de Opus 5.5 e comparação com Opus 5."),
    ("Google — Gemini API Pricing",
     "https://ai.google.dev/gemini-api/docs/pricing",
     "Fonte para preço da API Gemini, incluindo promoções e datas de mudança de tarifa."),
    ("Microsoft Foundry — MAI-Code-1.1-Flash",
     "https://ai.azure.com/catalog/models/mai-code-1.1-flash",
     "Catálogo do modelo; o preço de implantação deve ser confirmado no portal Azure."),
    ("xAI — Pricing",
     "https://docs.x.ai/developers/pricing",
     "Fonte de preços de Grok 4.5, 4.6 e 4.7, incluindo entrada em cache e contexto longo."),
    ("Moonshot AI — anúncio do Kimi K3",
     "https://forum.moonshot.ai/t/kimi-k3-is-here-our-most-capable-model/480",
     "Fonte da tarifa de API publicada para Kimi K3.")
]
for title,url,desc in sources:
    story.append(KeepTogether([
        P(f"<b>{title}</b>", "BodyX"),
        P(f'<link href="{url}" color="#2463A6">{url}</link>', "SourceX"),
        P(desc,"SmallX"),
        Spacer(1,1.4*mm)
    ]))
story.append(Spacer(1,2*mm))
story.append(P("Limitações importantes", "H2X"))
story.append(P("• Preços em USD por 1 milhão de tokens; custos locais dependem de câmbio, impostos, cache efetivamente utilizado, contexto, volume e modalidade de API.<br/>• “Proprietário” identifica o modelo como serviço/modelo fechado na comparação; não é uma avaliação jurídica completa de termos e licenças.<br/>• O total estimado por interação não inclui ferramentas, pesquisa web, chamadas de função, minutos de GitHub Actions, execução agentic ou outros custos fora dos tokens listados.<br/>• Para orçamento real, registre consumo por modelo e calcule o custo de várias revisões típicas.", "SmallX"))
story.append(Spacer(1,3*mm))
story.append(HRFlowable(width="100%", thickness=1, color=line))
story.append(Spacer(1,2*mm))
story.append(P("Conclusão: escolha o modelo pelo tipo de revisão e não só pelo preço por token. Uma análise curta com modelo potente pode sair mais barata que uma sequência longa de tentativas com um modelo inadequado; compare o custo por tarefa com evidências e resultados reais.", "CalloutX"))

doc.build(story,onFirstPage=page_decor,onLaterPages=page_decor)
shutil.copyfile(OUT, LATEST_OUT)

print(f"PDF atualizado: {OUT}")
print(f"Alias da última versão: {LATEST_OUT}")
print(f"Tamanho: {os.path.getsize(OUT):,} bytes")
print(f"Modelos incluídos: {len(models)}")