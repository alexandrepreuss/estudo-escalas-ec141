"""
Gerador do Relatório Comparativo de Escalas - EC 141/2026
Base: 100 funcionários por turno (300 funcionários efetivos no total em 3 turnos de 8h).
Cobertura operacional atual: 75 postos simultâneos 24x7 (1.800 horas-homem/dia).
"""

from math import ceil

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
        "legal": "Ilegal pós-EC 141 (42h/sem, 1,75 folga/sem)",
    },
    {
        "perfil": "Perfil 1 - Máx. eficiência (folga isolada)",
        "nome": "3x1 + 2x1 + 2x1",
        "padrao": "TTTFTTFTTF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 10,
        "passo": 1,
        "legal": "OK - Regra Geral (<=40h, >=2 folgas em 7d)",
    },
    {
        "perfil": "Perfil 2A - Máx. eficiência (folga dupla)",
        "nome": "5x2 + 5x2 + 4x2",
        "padrao": "TTTTTFFTTTTTFFTTTTFF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 10,
        "passo": 2,
        "legal": "OK - Regra Geral (<=40h, >=2 folgas em 7d)",
    },
    {
        "perfil": "Perfil 2B - Ciclo curto (folga dupla)",
        "nome": "5x2 + 4x2",
        "padrao": "TTTTTFFTTTTFF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 13,
        "passo": 1,
        "legal": "OK - Regra Geral (<=40h, >=2 folgas em 7d)",
    },
    {
        "perfil": "Perfil 3A - Simplicidade (folga dupla)",
        "nome": "4x2",
        "padrao": "TTTTFF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 3,
        "passo": 2,
        "legal": "OK - Regra Geral (<=40h, >=2 folgas em 7d)",
    },
    {
        "perfil": "Perfil 3B - Simplicidade (folga isolada)",
        "nome": "2x1",
        "padrao": "TTF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 3,
        "passo": 1,
        "legal": "OK - Regra Geral (<=40h, >=2 folgas em 7d)",
    },
    {
        "perfil": "Perfil 4 - Conforto (3 folgas) + 3 turmas",
        "nome": "5x2 + 5x3",
        "padrao": "TTTTTFFTTTTTFFF",
        "horas_dia": 8,
        "turnos": 3,
        "turmas_por_turno": 3,
        "passo": 5,
        "legal": "OK - Regra Geral (<=40h, >=2 folgas em 7d)",
    },
    {
        "perfil": "Exceção (ACT/CCT) - Turnos de 12h",
        "nome": "12x36 (1x1)",
        "padrao": "TF",
        "horas_dia": 12,
        "turnos": 2,
        "turmas_por_turno": 2,
        "passo": 1,
        "legal": "Exceção via ACT/CCT (§2º/§3º) — média 42h/sem",
    },
]


def gerar_matriz_turmas(padrao: str, turmas: int, passo: int) -> list[list[str]]:
    n = len(padrao)
    return [[padrao[(d - t * passo) % n] for d in range(n)] for t in range(turmas)]


def calcular_intervalos_domingo(padrao: str) -> tuple[float, int, list[int]]:
    """
    Calcula os intervalos reais (em dias) entre um domingo de folga e o próximo
    ao longo do superciclo de N semanas (para N não múltiplo de 7).
    Retorna (media_dias, max_dias, lista_intervalos).
    """
    n = len(padrao)
    dom_folga = [w * 7 for w in range(n) if padrao[(w * 7) % n] == "F"]
    intervalos = [
        dom_folga[i + 1] - dom_folga[i] for i in range(len(dom_folga) - 1)
    ] + [n * 7 - dom_folga[-1] + dom_folga[0]]
    media = sum(intervalos) / len(intervalos)
    return media, max(intervalos), intervalos


def gerar_markdown(caminho_saida: str) -> None:
    linhas: list[str] = []
    linhas.append("# Estudo Comparativo de Escalas de Trabalho — EC 141/2026\n")
    linhas.append(
        f"**Premissas da Empresa:** Operação contínua 24x7 | Base atual: **{BASE_POR_TURNO} funcionários por turno** "
        f"(**{TOTAL_EFETIVO_ATUAL} funcionários efetivos** nos 3 turnos de 8h) | "
        f"Cobertura atual: **{POSTOS_SIMULTANEOS:.1f} postos simultâneos/hora** "
        f"(**157,5 trabalhando/dia** em 3 turnos de 8h = **{HORAS_HOMEM_DIA} horas-homem/dia**).\n"
    )
    linhas.append(
        "**Critérios Legais e de Gestão Aplicados:** Regra Geral estrita da EC 141/2026 "
        "($\\le 40\\text{h/sem}$ e $\\ge 2$ folgas em qualquer janela móvel de 7 dias) + "
        "rotação semanal (ciclo não múltiplo de 7 para alternar dias de folga e domingos), "
        "além da análise da exceção **12x36** (2 turnos de 12h).\n"
    )

    linhas.append("---\n")
    linhas.append(f"## 1. Quadro Resumo Comparativo (Base {TOTAL_EFETIVO_ATUAL} Efetivos / {POSTOS_SIMULTANEOS:.1f} Postos Simultâneos)\n")
    linhas.append(
        "| Perfil | Escala | Ciclo | Horas/Sem | Turnos x Turmas | Efetivo Diário (%) | "
        f"Quadro Total p/ {POSTOS_SIMULTANEOS:.1f} postos | Extras (Total) | Dom/mês (méd) | Dias entre domingos (Méd / Máx) |"
    )
    linhas.append(
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    )

    for item in FINALISTAS:
        padrao = item["padrao"]
        n = len(padrao)
        dias_t = padrao.count("T")
        dias_f = padrao.count("F")
        horas_dia = item["horas_dia"]
        turnos = item["turnos"]
        turmas = item["turmas_por_turno"]

        horas_sem = dias_t * horas_dia * (7.0 / n)
        efetivo_frac = dias_t / n

        quadro_por_turno_exato = POSTOS_SIMULTANEOS / efetivo_frac
        quadro_total_exato = quadro_por_turno_exato * turnos
        quadro_total_int = ceil(quadro_total_exato)
        extras_total = quadro_total_int - TOTAL_EFETIVO_ATUAL
        extras_pct = ((quadro_total_exato - TOTAL_EFETIVO_ATUAL) / TOTAL_EFETIVO_ATUAL) * 100.0

        dom_mes = (dias_f / n) * (30.4 / 7.0)
        dom_med, dom_max, dom_lista = calcular_intervalos_domingo(padrao)
        print(f"{item['nome']:<18} | intervalos={dom_lista} | med={dom_med:.1f}d | max={dom_max}d")

        linhas.append(
            f"| {item['perfil']} | **{item['nome']}** | {n}d | {horas_sem:.2f}h | "
            f"{turnos}x {turmas}t (p.{item['passo']}d) | "
            f"**{efetivo_frac*100:.2f}%** | "
            f"{quadro_total_int} ({quadro_total_exato:.1f}) | "
            f"**+{extras_total}** (+{extras_pct:.2f}%) | "
            f"{dom_mes:.2f} | **{dom_med:.1f}d / {dom_max}d** |"
        )

    linhas.append(
        "\n> **Nota sobre 'Dias entre domingos (Méd / Máx)':** Quando há folgas seguidas (como `6x2` ou `5x2`), o colaborador pode folgar **2 domingos seguidos** (intervalo de 7 dias) e depois ficar um período maior trabalhando aos domingos até o próximo bloco de folga. "
        "Na `6x2`, por exemplo, os intervalos reais são `[7d, 49d]`: média de **28,0 dias**, mas espera máxima de **49 dias** (7 semanas) sem folgar no domingo.\n"
    )
    linhas.append("---\n")
    linhas.append(f"## 2. Estudo da Escala 12x36 (1x1) com {TOTAL_EFETIVO_ATUAL} Funcionários Efetivos\n")
    linhas.append(
        "Na escala **12x36** (`1x1` em dias), a operação deixa de ter 3 turnos de 8h e passa a operar com **2 turnos de 12h** "
        f"(ex.: 06h–18h e 18h–06h). Mantendo os **{TOTAL_EFETIVO_ATUAL} funcionários atuais**, a distribuição fica assim:\n"
    )
    linhas.append(
        "- **Efetivo por turno de 12h:** **105 funcionários** no turno diurno e **105 funcionários** no turno noturno (total = **210 ativos**).\n"
        "- **Divisão em turmas (4 turmas no total):**\n"
        "  - **Turno Diurno:** Turma A (**52 a 53**) nos dias ímpares e Turma B (**52 a 53**) nos dias pares.\n"
        "  - **Turno Noturno:** Turma C (**52 a 53**) nos dias ímpares e Turma D (**52 a 53**) nos dias pares.\n"
        "- **Ativos trabalhando por dia (24h):** **105 funcionários/dia** (**50,00%** dos 210) trabalhando e **105 funcionários/dia** folgando.\n"
        "- **Cobertura simultânea:** Em qualquer hora do dia ou da noite, há **52,5 funcionários em média (52 a 53) trabalhando ao mesmo tempo**, entregando $105 \\times 12\\text{h} = \\mathbf{1.260\\text{ horas-homem/dia}}$ (exatamente igual aos 157,5 funcionários × 8h da `6x2`).\n"
        "- **Contratações extras:** **0 (zero)** na `12x36` pura. *(Atenção: como a média é de 42h/sem, se a convenção coletiva exigir ajuste para 40h/sem em dez/2027, serão necessários ~11 funcionários extras no total — quadro de ~221 — para cobrir as folgas compensatórias).* \n"
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
        horas_sem = dias_t * horas_dia * (7.0 / n)
        efetivo_frac = dias_t / n
        quadro_por_turno_exato = POSTOS_SIMULTANEOS / efetivo_frac
        quadro_total_exato = quadro_por_turno_exato * turnos
        quadro_total_int = ceil(quadro_total_exato)
        extras_total = quadro_total_int - TOTAL_EFETIVO_ATUAL
        dom_med, dom_max, _ = calcular_intervalos_domingo(padrao)

        linhas.append(f"### {item['perfil']}: `{item['nome']}` (Ciclo de {n} dias)\n")
        linhas.append(
            f"- **Padrão:** `{padrao}` ({dias_t}T / {dias_f}F de {horas_dia}h) | "
            f"**Jornada média:** {horas_sem:.2f}h/sem | **Dias entre domingos:** {dom_med:.1f}d méd / {dom_max}d máx\n"
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
        "- A manutenção da `6x2` (42h/sem e apenas 1,75 folga/sem na média) após o início da transição da EC 141/2026 "
        "expõe a empresa a passivo trabalhista direto (pagamento de horas extras excedentes, nulidade da escala e reflexos em DSR/férias/13º), "
        "além de risco de autuação em fiscalizações e desgaste sindical.\n"
    )
    linhas.append(
        "### 4.2. Impacto Orçamentário na Folha e Ponte de Transição (2026–2027)\n"
        "- **Teto físico da lei:** Com jornadas de 8h/dia e limite de 40h/semana, o teto absoluto de efetivo diário é `40 / 56 = 71,43%` "
        "(e no máximo `70,00%` com rotação semanal). Portanto, qualquer escala de 8h exige aumento de quadro.\n"
        "- **Faixa de impacto direto na folha:** Sobre os **210 efetivos atuais**, manter os 52,5 postos simultâneos exige entre "
        "**+15 pessoas (+7,14%)** nas opções de maior aproveitamento (`3x1 + 2x1 + 2x1` e `5x2 + 5x2 + 4x2`) e **+27 pessoas (+12,50%)** "
        "nas opções mais simples (`4x2`, `2x1` e `5x2 + 5x3`), além de encargos trabalhistas, benefícios e custo de recrutamento/integração.\n"
        "- **Alívio de fluxo de caixa na transição (dez/2026 a dez/2027):** Conforme detalhado no estudo de 42h/semana, "
        "durante o primeiro ano (jornada de 8h24min/dia), se os 24 minutos extras puderem ser aproveitados em horas-homem (1.260 h-h/dia), "
        "a contratação imediata cai para **+5 pessoas** em dez/2026 na escala de 70%, permitindo escalonar os **+10 restantes** ao longo de 2027 até a entrada do teto definitivo de 40h.\n"
    )
    linhas.append(
        "### 4.3. Riscos Financeiros e Operacionais da Exceção `12x36`\n"
        "- **Dependência sindical integral:** A `12x36` só é juridicamente válida mediante **Acordo ou Convenção Coletiva de Trabalho (ACT/CCT)**.\n"
        "- **Risco de degrau em dezembro/2027 (42h → 40h):** Como a `12x36` gera média de 42h/semana, a aplicação do teto de 40h/semana em dez/2027 "
        "pode exigir folgas compensatórias adicionais via CCT, elevando o quadro de 210 para **~221 pessoas (+11 / +5,0%)**.\n"
        "- **Custos indiretos ocultos:** A migração de 3 turnos de 8h para 2 turnos de 12h altera a incidência de **adicional noturno**, "
        "exige revisão de **rotas e horários de transporte fretado**, impacta o **pagamento/compensação de feriados** e encarece a cobertura de faltas/atestados "
        "(pois cobrir um turno de 12h com hora extra custa mais caro e aumenta o risco de fadiga e passivos na **NR-1**).\n"
    )
    linhas.append(
        "### 4.4. Risco Trabalhista (Art. 386 da CLT) e Turnover no Efetivo Feminino (70%+)\n"
        "- O **Art. 386 da CLT** prevê escala de revezamento quinzenal aos domingos para mulheres quando há trabalho dominical (e convenções coletivas frequentemente exigem ao menos 1 domingo/mês).\n"
        "- Escalas com ciclos longos (`5x2 + 5x2 + 4x2` com máx. **105 dias**, `5x2 + 5x3` com **77 dias**, `5x2 + 4x2` com **70 dias** e `3x1 + 2x1 + 2x1` com **56 dias**) "
        "geram longos períodos sem domingo livre, elevando o risco de **passivo trabalhista** e **rotatividade (turnover)** — cujo custo de reposição e perda de produtividade pode anular a economia inicial de folha frente à `4x2` (máx. 35 dias) ou `2x1` (21 dias fixos).\n"
        "- **Recomendação pré-decisão:** Submeter as opções finalistas à validação do Jurídico Trabalhista e do Sindicato antes da aprovação orçamentária.\n"
    )
    linhas.append(
        "### 4.5. Arredondamento de Turmas, Férias e Reserva Técnica\n"
        "- Nas escalas de **10 ou 13 turmas por turno** (ex.: 225 pessoas ÷ 3 turnos = 75 pessoas/turno ÷ 10 turmas), as turmas ficam com **7 a 8 pessoas cada** (heterogêneas). "
        "É necessário prever cobertura de férias e absenteísmo (reserva técnica), pois uma única ausência em uma microturma de 7 pessoas representa ~14% de perda pontual naquela equipe.\n"
        "- A troca de escala exige ainda **plano de gestão da mudança** (comunicação, adequação de transporte e período de adaptação de 60 a 90 dias) para evitar picos de desligamento voluntário.\n"
    )

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"Relatório gerado com sucesso em: {caminho_saida}")


if __name__ == "__main__":
    from gerar_docx import md_para_docx
    md_v4 = "/mnt/a/SANDBOX/ESCALAS/relatorio_escalas_v4.md"
    docx_v4 = "/mnt/a/SANDBOX/ESCALAS/relatorio_escalas_v4.docx"
    gerar_markdown(md_v4)
    md_para_docx(md_v4, docx_v4)
