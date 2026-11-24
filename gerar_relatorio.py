"""
Gerador do Relatório Comparativo de Escalas (v5) - EC 141/2026 + Portaria MTE nº 2.041/2026
Base: 70 funcionários por turno (210 funcionários efetivos no total em 3 turnos de 8h).
Cobertura operacional atual: 52,5 postos simultâneos 24x7 (1.260 horas-homem/dia).
"""

from math import ceil
from gerar_docx import md_para_docx

BASE_POR_TURNO = 70
TURNOS_8H = 3
TOTAL_EFETIVO_ATUAL = BASE_POR_TURNO * TURNOS_8H  # 210 funcionários
POSTOS_SIMULTANEOS = 52.5  # 75% de 70 por turno (52,5 trabalhando por hora, 24h/dia)
HORAS_HOMEM_DIA = int(POSTOS_SIMULTANEOS * 24)  # 1.260 horas-homem/dia

FINALISTAS = [
    {
        "perfil": "Referência Atual",
        "nome": "6x2 (Atual)",
        "padrao": "TTTTTTFF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 4,
        "passo": 2,
        "legal": "Ilegal pós-EC 141 (42h/sem, 1,75 folga/sem, falha §1º e §4º)",
    },
    {
        "perfil": "Máx. eficiência (folga isolada, §1º)",
        "nome": "3x1 + 2x1 + 2x1",
        "padrao": "TTTFTTFTTF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 10,
        "passo": 1,
        "legal": "OK pelo §1º (2 folgas/7d); falha em 3/10 fases em fev. 29d pelo §4º",
    },
    {
        "perfil": "Máx. eficiência (folga dupla, §1º)",
        "nome": "5x2 + 5x2 + 4x2",
        "padrao": "TTTTTFFTTTTTFFTTTTFF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 10,
        "passo": 2,
        "legal": "OK pelo §1º (2 folgas/7d); falha em fases de 29/30/31d pelo §4º",
    },
    {
        "perfil": "Ciclo curto (folga dupla, §1º)",
        "nome": "5x2 + 4x2",
        "padrao": "TTTTTFFTTTTFF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 13,
        "passo": 1,
        "legal": "OK pelo §1º (2 folgas/7d); falha em fases de 29/30/31d pelo §4º",
    },
    {
        "perfil": "Maior jornada 100% §4º (folga isolada)",
        "nome": "(4x 2x1) + 3x1",
        "padrao": "TTFTTFTTFTTFTTTF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 16,
        "passo": 1,
        "legal": "OK pelo §1º E 100% no §4º (8–10 folgas/mês em todas as turmas)",
    },
    {
        "perfil": "Simplicidade + Blindagem §4º (folga dupla)",
        "nome": "4x2",
        "padrao": "TTTTFF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 3,
        "passo": 2,
        "legal": "OK pelo §1º E 100% no §4º (sem depender de ACT/CCT)",
    },
    {
        "perfil": "Simplicidade + Melhores domingos (isolada)",
        "nome": "2x1",
        "padrao": "TTF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 3,
        "passo": 1,
        "legal": "OK pelo §1º E 100% no §4º (domingo exato a cada 21 dias)",
    },
    {
        "perfil": "Conforto (3 folgas) + 3 turmas (§1º e §4º)",
        "nome": "5x2 + 5x3",
        "padrao": "TTTTTFFTTTTTFFF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 3,
        "passo": 5,
        "legal": "OK pelo §1º E 100% no §4º (porém máx. 77d sem domingo)",
    },
    {
        "perfil": "Conforto (3 folgas) + Domingos <=28d (§3º/§4º)",
        "nome": "6x3",
        "padrao": "TTTTTTFFF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 3,
        "passo": 3,
        "legal": "OK via ACT/CCT (§3º: máx. 6d seguidos) E 100% no §4º (domingo <=28d)",
    },
    {
        "perfil": "Exceção (ACT/CCT) - Turnos de 12h",
        "nome": "12x36 (1x1)",
        "padrao": "TF",
        "horas_dia": 12,
        "turnos": 2,
        "turmas_por_turno": 2,
        "passo": 1,
        "legal": "Exceção via ACT/CCT (Art. 8º: 42h exige compensação/HE em dez/2027)",
    },
]

HISTORICO_COMPLETO = [
    ("6x2 (Atual)", "TTTTTTFF", 8.0, 3, "Ilegal pós-EC 141 (42h/sem, <2 folgas/sem)"),
    ("5x2 (Fixa)", "TTTTTFF", 8.0, 3, "OK §1º; rejeitada por folgas fixas (sem rotação)"),
    ("4x2 + 6x2", "TTTTFFTTTTTTFF", 8.0, 3, "Reprovada: exige §3º, mas falha no §4º (8 folgas em 30/31d)"),
    ("3x1 + 2x1 + 2x1", "TTTFTTFTTF", 8.0, 3, "OK §1º; falha em 3/10 fases apenas em fev. 29d no §4º"),
    ("5x2 + 5x2 + 4x2", "TTTTTFFTTTTTFFTTTTFF", 8.0, 3, "OK §1º; falha §4º em 29–31d; máx. 105d sem domingo"),
    ("5x2 + 4x2", "TTTTTFFTTTTFF", 8.0, 3, "OK §1º; falha §4º em 29–31d; máx. 70d sem domingo"),
    ("(4x 2x1) + 3x1", "TTFTTFTTFTTFTTTF", 8.0, 3, "OK §1º e 100% §4º; folgas isoladas, 16 turmas"),
    ("4x2", "TTTTFF", 8.0, 3, "OK §1º e 100% §4º; 3 turmas, folgas duplas, dom. <=35d"),
    ("2x1", "TTF", 8.0, 3, "OK §1º e 100% §4º; 3 turmas, folgas isoladas, dom. = 21d"),
    ("5x2 + 5x3", "TTTTTFFTTTTTFFF", 8.0, 3, "OK §1º e 100% §4º; 3 turmas, 3 folgas/15d, dom. <=77d"),
    ("6x3", "TTTTTTFFF", 8.0, 3, "OK §3º (exige ACT/CCT) e 100% §4º; 3 turmas, dom. <=28d"),
    ("3x3 (8h)", "TTTFFF", 8.0, 3, "Proposta sindical inviável em 8h (+105 pessoas / +50%)"),
    ("4x4 (8h)", "TTTTFFFF", 8.0, 3, "Proposta sindical inviável em 8h (+105 pessoas / +50%)"),
    ("3x3 (12h)", "TTTFFF", 12.0, 2, "Risco fadiga/jurídico (3x 12h seguidas) + regra 42h dez/2027"),
    ("4x4 (12h)", "TTTTFFFF", 12.0, 2, "Risco fadiga/jurídico (4x 12h seguidas) + regra 42h dez/2027"),
    ("12x36 (1x1 - 12h)", "TF", 12.0, 2, "ACT/CCT; Art. 8º exige compensação/HE em dez/2027; dom. = 14d"),
]


def gerar_matriz_turmas(padrao: str, turmas: int, passo: int) -> list[list[str]]:
    n = len(padrao)
    return [[padrao[(d - t * passo) % n] for d in range(n)] for t in range(turmas)]


def calcular_intervalos_domingo(padrao: str) -> tuple[float, int, list[int]]:
    n = len(padrao)
    if n % 7 == 0:
        return 0.0, 0, []
    dom_folga = [w * 7 for w in range(n) if padrao[(w * 7) % n] == "F"]
    intervalos = [
        dom_folga[i + 1] - dom_folga[i] for i in range(len(dom_folga) - 1)
    ] + [n * 7 - dom_folga[-1] + dom_folga[0]]
    media = sum(intervalos) / len(intervalos)
    return media, max(intervalos), intervalos


def folgas_por_mes(padrao: str, dias_mes: int) -> tuple[int, int, int]:
    n = len(padrao)
    meta = ceil((2 * dias_mes) / 7)
    contagens = [
        sum(1 for d in range(dias_mes) if padrao[(inicio + d) % n] == "F")
        for inicio in range(n)
    ]
    abaixo = sum(1 for c in contagens if c < meta)
    return min(contagens), max(contagens), abaixo


def atende_par4_100(padrao: str) -> bool:
    return all(folgas_por_mes(padrao, d)[2] == 0 for d in (28, 29, 30, 31))


def gerar_markdown(caminho_saida: str) -> None:
    linhas: list[str] = []
    linhas.append("# Estudo Comparativo de Escalas de Trabalho (v5) — EC 141/2026 e Portaria MTE nº 2.041/2026\n")
    linhas.append(
        f"**Premissas da Empresa:** Operação contínua 24x7 | Base atual: **{BASE_POR_TURNO} funcionários por turno** "
        f"(**{TOTAL_EFETIVO_ATUAL} funcionários efetivos** nos 3 turnos de 8h) | "
        f"Cobertura atual: **{POSTOS_SIMULTANEOS:.1f} postos simultâneos/hora** "
        f"(**157,5 trabalhando/dia** em 3 turnos de 8h = **{HORAS_HOMEM_DIA} horas-homem/dia**).\n"
    )
    linhas.append(
        "**Marco Regulatório Atualizado (Portaria MTE nº 2.041, de 19/11/2026 — DOU 23/11/2026 e Decreto nº 13.173/2026):**\n"
        "- **Regra Geral Semanal (Art. 4º, § 1º):** 2 repousos de 24h por semana (consecutivos ou alternados), preservado o intervalo interjornada de 11h.\n"
        "- **Regime Compensatório via ACT/CCT (Art. 4º, §§ 3º e 4º):** Máximo de **6 dias seguidos** de trabalho e mínimo de folgas no mês-calendário igual a $\\lceil 2 \\times \\text{dias}/7 \\rceil$ (**8 folgas** em 28d; **9 folgas** em 29, 30 e 31d).\n"
        "- **Domingos (Art. 5º, §§ 3º e 5º):** Reafirmada a escala quinzenal para mulheres (**Art. 386 da CLT**) e a preferência de ao menos 1 domingo em **no máximo 4 semanas (28 dias)** para todos.\n"
        "- **Divisores Salário-Hora (Art. 10):** Passa de **220** para **210** (fase 42h, dez/2026) e **200** (fase 40h, dez/2027), elevando o valor da hora base em **+10,0%** no definitivo.\n"
    )

    linhas.append("---\n")
    linhas.append(f"## 1. Quadro Resumo das Opções Finalistas (Base {TOTAL_EFETIVO_ATUAL} Efetivos / {POSTOS_SIMULTANEOS:.1f} Postos Simultâneos)\n")
    linhas.append(
        "| Perfil | Escala | Ciclo | J. 8h / 8h24 | Turnos x Turmas | Efetivo (%) | "
        f"Quadro p/ {POSTOS_SIMULTANEOS:.1f} | Extras | §4º 100%? | Domingos (Méd / Máx) |"
    )
    linhas.append(
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    )

    for item in FINALISTAS:
        padrao = item["padrao"]
        n = len(padrao)
        dias_t = padrao.count("T")
        horas_dia = item["horas_dia"]
        turnos = item["turnos"]
        turmas = item["turmas_por_turno"]

        j_8 = dias_t * horas_dia * (7.0 / n)
        j_84 = j_8 if horas_dia == 12 else dias_t * 8.4 * (7.0 / n)
        j_str = f"{j_8:.2f}h / —" if horas_dia == 12 else f"{j_8:.2f}h / {j_84:.2f}h"
        efetivo_frac = dias_t / n

        quadro_por_turno_exato = POSTOS_SIMULTANEOS / efetivo_frac
        quadro_total_exato = quadro_por_turno_exato * turnos
        quadro_total_int = ceil(quadro_total_exato)
        extras_total = quadro_total_int - TOTAL_EFETIVO_ATUAL
        extras_pct = ((quadro_total_exato - TOTAL_EFETIVO_ATUAL) / TOTAL_EFETIVO_ATUAL) * 100.0

        dom_med, dom_max, _ = calcular_intervalos_domingo(padrao)
        dom_str = "Fixo" if n % 7 == 0 else f"**{dom_med:.1f}d / {dom_max}d**"
        ok_p4 = "SIM" if atende_par4_100(padrao) else "Não"

        linhas.append(
            f"| {item['perfil']} | **{item['nome']}** | {n}d | {j_str} | "
            f"{turnos}x {turmas}t (p.{item['passo']}d) | "
            f"**{efetivo_frac*100:.2f}%** | "
            f"{quadro_total_int} ({quadro_total_exato:.1f}) | "
            f"**+{extras_total}** (+{extras_pct:.2f}%) | "
            f"{ok_p4} | {dom_str} |"
        )

    linhas.append(
        "\n> **Nota sobre o § 4º:** Escalas que já concedem 2 folgas em toda janela de 7 dias cumprem a regra semanal (§ 1º) diretamente. "
        "Já a **`6x3`** (que trabalha 6 dias seguidos e depende de ACT/CCT pelo § 3º) atende **100% da conta mensal do § 4º** e limita a espera máxima de domingo a **28 dias** (Art. 5º, § 5º).\n"
    )

    linhas.append("---\n")
    linhas.append(f"## 2. Estudo da Escala 12x36 (1x1) com {TOTAL_EFETIVO_ATUAL} Funcionários Efetivos\n")
    linhas.append(
        "Na escala **12x36** (`1x1` em dias), a operação passa de 3 turnos de 8h para **2 turnos de 12h** "
        f"(ex.: 06h–18h e 18h–06h). Mantendo os **{TOTAL_EFETIVO_ATUAL} funcionários atuais**, a distribuição fica assim:\n"
    )
    linhas.append(
        "- **Efetivo por turno de 12h:** **105 funcionários** no turno diurno e **105 funcionários** no turno noturno (total = **210 ativos**).\n"
        "- **Divisão em turmas (4 turmas no total):**\n"
        "  - **Turno Diurno:** Turma A (**52 a 53**) nos dias ímpares e Turma B (**52 a 53**) nos dias pares.\n"
        "  - **Turno Noturno:** Turma C (**52 a 53**) nos dias ímpares e Turma D (**52 a 53**) nos dias pares.\n"
        "- **Ativos trabalhando por dia (24h):** **105 funcionários/dia** (**50,00%** dos 210) trabalhando e **105 funcionários/dia** folgando.\n"
        "- **Cobertura simultânea:** Em qualquer hora do dia ou da noite, há **52,5 funcionários em média (52 a 53) trabalhando ao mesmo tempo**, entregando $105 \\times 12\\text{h} = \\mathbf{1.260\\text{ horas-homem/dia}}$ (igual aos 157,5 × 8h da `6x2`).\n"
        "- **Regra expressa do Art. 8º da Portaria 2.041/2026:** Enquanto o teto for de 42h/sem (dez/2026–dez/2027), a `12x36` fecha em 42h sem horas extras. A partir de **dez/2027 (teto de 40h/sem)**, o Art. 8º obriga expressamente a **compensação das horas ou o pagamento de horas extras** no mês-calendário via ACT/CCT — o que exigirá **~11 funcionários extras (quadro de ~221 / +5,0%)** caso se opte por folgas compensatórias.\n"
    )

    linhas.append("---\n")
    linhas.append(f"## 3. Detalhamento e Quadro Dia a Dia por Turno (Base {BASE_POR_TURNO}/turno)\n")

    for item in FINALISTAS[1:]:
        padrao = item["padrao"]
        n = len(padrao)
        turmas = item["turmas_por_turno"]
        passo = item["passo"]
        turnos = item["turnos"]
        horas_dia = item["horas_dia"]
        dias_t = padrao.count("T")
        dias_f = padrao.count("F")
        j_8 = dias_t * horas_dia * (7.0 / n)
        j_84 = j_8 if horas_dia == 12 else dias_t * 8.4 * (7.0 / n)
        efetivo_frac = dias_t / n
        quadro_por_turno_exato = POSTOS_SIMULTANEOS / efetivo_frac
        quadro_total_exato = quadro_por_turno_exato * turnos
        quadro_total_int = ceil(quadro_total_exato)
        extras_total = quadro_total_int - TOTAL_EFETIVO_ATUAL
        dom_med, dom_max, _ = calcular_intervalos_domingo(padrao)

        j_txt = f"{j_8:.2f}h/sem" if horas_dia == 12 else f"{j_8:.2f}h/sem (8h/d) | {j_84:.2f}h/sem (8h24/d)"

        linhas.append(f"### {item['perfil']}: `{item['nome']}` (Ciclo de {n} dias)\n")
        linhas.append(
            f"- **Padrão:** `{padrao}` ({dias_t}T / {dias_f}F de {horas_dia}h) | "
            f"**Jornada média:** {j_txt} | **Domingos:** {dom_med:.1f}d méd / {dom_max}d máx\n"
            f"- **Enquadramento:** {item['legal']}\n"
            f"- **Efetivo por turno (para {POSTOS_SIMULTANEOS:.1f} simultâneos):** {quadro_por_turno_exato:.1f} pessoas/turno "
            f"({turnos} turnos = **{quadro_total_int} no total**, **+{extras_total} extras** frente aos {TOTAL_EFETIVO_ATUAL} atuais)\n"
            f"- **Organização por turno:** **{turmas} turmas** defasadas em **{passo} dia(s)**\n"
        )

        matriz = gerar_matriz_turmas(padrao, turmas, passo)
        cabecalho_dias = " | ".join(f"D{d+1:02d}" for d in range(n))
        sep_dias = " | ".join(":---:" for _ in range(n))
        linhas.append(f"| Turma | {cabecalho_dias} |")
        linhas.append(f"| :--- | {sep_dias} |")

        for idx, linha in enumerate(matriz, start=1):
            celulas = " | ".join("T" if c == "T" else "**F**" for c in linha)
            linhas.append(f"| T{idx:02d} | {celulas} |")

        trab_dia = [sum(1 for t in range(turmas) if matriz[t][d] == "T") for d in range(n)]
        folga_dia = [turmas - x for x in trab_dia]
        linhas.append("| **Trab** | " + " | ".join(str(x) for x in trab_dia) + " |")
        linhas.append("| **Folga** | " + " | ".join(str(x) for x in folga_dia) + " |")
        linhas.append("")

    linhas.append("---\n")
    linhas.append("## 4. Considerações Financeiras, Operacionais e Riscos para Tomada de Decisão\n")
    linhas.append(
        "### 4.1. Custo da Inércia (Manter a escala 6x2 após 16/12/2026)\n"
        "- A manutenção da `6x2` (42h/sem e 1,75 folga/sem na média) após o início da vigência da EC 141/2026 e da Portaria 2.041/2026 "
        "expõe a empresa a passivo trabalhista direto (horas extras excedentes, pagamento em dobro do repouso não compensado pelo Art. 5º § 6º, nulidade de cláusula coletiva pelo Art. 13 e autuação).\n"
    )
    linhas.append(
        "### 4.2. Impacto Orçamentário na Folha, Novos Divisores e Ponte de Transição (2026–2027)\n"
        "- **Teto físico da lei:** Com jornadas de 8h/dia e limite de 40h/semana, o teto absoluto é `40 / 56 = 71,43%` (`70,00%` com rotação). Qualquer escala de 8h exige ampliação de quadro.\n"
        "- **Aumento do salário-hora pelos novos divisores (Art. 10 da Portaria 2.041/2026):** O divisor cai de **220** para **210** na fase de 42h (**+4,76%** no valor-hora) e para **200** na fase de 40h (**+10,00%** no valor-hora). "
        "Mesmo mantendo o salário nominal, todas as verbas calculadas por hora (**adicional noturno dos turnos da noite, horas extras e reflexos**) sobem automaticamente **+10%** no patamar definitivo.\n"
        "- **Impacto direto em contratações (base 210):** Entre **+15 pessoas (+7,14%)** nas escalas de 70% (`3x1+2x1+2x1`, `5x2+5x2+4x2`), **+20 (+9,09%)** na `(4x 2x1)+3x1` (68,75%), até **+27 pessoas (+12,50%)** nas escalas de 3 turmas (`4x2`, `2x1`, `5x2+5x3`, `6x3`).\n"
        "- **Alívio de fluxo de caixa no 1º ano (8h24min/dia):** Durante a vigência das 42h/sem (até 15/12/2027), se a operação aproveitar os 24 min extras diários em horas-homem (1.260 h-h/dia), "
        "as escalas de 3 turmas (`4x2`, `6x3`, `5x2+5x3`) atingem **39,20h/sem** e demandam inicialmente **+15 pessoas (quadro 225)** em 2027, escalonando os **+12 restantes** para dezembro/2027.\n"
    )
    linhas.append(
        "### 4.3. Riscos Financeiros e Operacionais da Exceção `12x36` (e das propostas sindicais `3x3` / `4x4`)\n"
        "- **Dependência sindical integral:** A `12x36` exige **ACT/CCT**. Pelo **Art. 8º da Portaria 2.041/2026**, ao cair o teto para 40h em dez/2027, torna-se obrigatória a **compensação de horas ou hora extra**, elevando o quadro de 210 para **~221 (+11 / +5,0%)**.\n"
        "- **Custos indiretos ocultos da `12x36`:** Alteração na incidência de **adicional noturno** (com divisor 200), revisão de **transporte fretado**, pagamento/compensação de **feriados**, cobertura cara de faltas de 12h e riscos de fadiga/SST (**NR-1**).\n"
        "- **Propostas sindicais `3x3` e `4x4`:** Em turnos de 8h são inviáveis (`28,00h/sem`, exigiriam **+105 pessoas / +50%**). Em turnos de 12h, impõem 3 ou 4 plantões seguidos de 12h (apenas 12h de intervalo entre eles), com risco ergonômico e jurídico muito superior à `12x36`.\n"
    )
    linhas.append(
        "### 4.4. Risco Trabalhista (Art. 386 da CLT), Regra dos Domingos (Art. 5º) e Turnover Feminino (70%+)\n"
        "- A Portaria 2.041/2026 reafirmou no **Art. 5º, § 3º** a obrigatoriedade da **escala quinzenal aos domingos para empregadas (Art. 386 da CLT)** e no **§ 5º** a preferência de ao menos **1 domingo a cada 4 semanas (28 dias)** para todos.\n"
        "- Escalas com apagões de **56 a 105 dias** sem domingo (`5x2+5x2+4x2`, `5x2+5x3`, `5x2+4x2`, `3x1+2x1+2x1`) geram risco elevado de passivo trabalhista e *turnover*.\n"
        "- Entre as de 3 turmas com folgas consecutivas, a **`4x2`** (máx. **35d**, sem depender de ACT/CCT) e a **`6x3`** (máx. **28d**, via ACT/CCT pelo § 3º e 100% aderente ao § 4º) oferecem o melhor equilíbrio operacional — devendo ser submetidas ao Jurídico Trabalhista quanto à aplicação do Art. 386 da CLT.\n"
    )
    linhas.append(
        "### 4.5. Arredondamento de Turmas, Férias e Reserva Técnica\n"
        "- Em escalas de **10, 13 ou 16 turmas por turno** (75 ÷ 10 = 7 a 8 pessoas/turma), uma ausência pontual impacta mais fortemente a microturma. Já nas escalas de **3 turmas por turno** (`4x2`, `6x3`, `5x2+5x3`, `2x1`), com ~26 pessoas por turma, a gestão de férias, folgas e cobertura de absenteísmo é muito mais estável.\n"
    )

    linhas.append("---\n")
    linhas.append("## 5. Tabela Histórica Completa de Todas as Escalas Estudadas\n")
    linhas.append(
        "| Escala | Ciclo | Efetivo | Quadro (Base 210) | J. Média (8h) | J. Média (8h24) | "
        "Folgas 28d / 29d / 30d / 31d | §4º 100%? | Dom (Méd / Máx) | Status / Enquadramento |"
    )
    linhas.append(
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |"
    )

    for nome, pat, hd, turnos, obs in HISTORICO_COMPLETO:
        n = len(pat)
        dt = pat.count("T")
        ef = dt / n
        q_tot = ceil((POSTOS_SIMULTANEOS / ef) * turnos)
        ext = q_tot - TOTAL_EFETIVO_ATUAL
        j8 = dt * hd * 7.0 / n
        j84 = "—" if hd == 12.0 else f"{dt * 8.4 * 7.0 / n:.2f}h"
        f_cols = []
        for dm in (28, 29, 30, 31):
            fmin, fmax, _ = folgas_por_mes(pat, dm)
            f_cols.append(f"{fmin}" if fmin == fmax else f"{fmin}–{fmax}")
        ok_p4 = "**Sim**" if atende_par4_100(pat) else "Não"
        dmed, dmax, _ = calcular_intervalos_domingo(pat)
        dom_s = "Fixo" if n % 7 == 0 else f"{dmed:.1f}d / {dmax}d"
        linhas.append(
            f"| **{nome}** | {n}d | {ef*100:.2f}% | {q_tot} ({ext:+d}) | {j8:.2f}h | {j84} | "
            f"{' / '.join(f_cols)} | {ok_p4} | {dom_s} | {obs} |"
        )

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"Relatório v5 gerado com sucesso em: {caminho_saida}")


if __name__ == "__main__":
    md_v5 = "/mnt/a/SANDBOX/ESCALAS/relatorio_escalas_v5.md"
    docx_v5 = "/mnt/a/SANDBOX/ESCALAS/relatorio_escalas_v5.docx"
    gerar_markdown(md_v5)
    md_para_docx(md_v5, docx_v5)
