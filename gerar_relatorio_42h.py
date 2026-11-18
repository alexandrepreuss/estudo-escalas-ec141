"""
Gerador do Relatório da Etapa Intermediária (Transição 42h/semana)
Vigência: 16/12/2026 a 15/12/2027 (EC 141/2026 + Liminar STF ADIs 8.041 e 8.042)
Jornada diária: 8h24min (8,4 horas/dia).
Base atual: 100 funcionários por turno (300 efetivos), 75 postos simultâneos (1.800 h-h/dia).
"""

from math import ceil
from gerar_docx import md_para_docx
from gerar_relatorio import (
    BASE_POR_TURNO,
    FINALISTAS,
    HORAS_HOMEM_DIA,
    POSTOS_SIMULTANEOS,
    TOTAL_EFETIVO_ATUAL,
    calcular_intervalos_domingo,
)

HORAS_DIA_TRANSICAO = 8.4  # 8h24min


def gerar_markdown_42h(caminho_saida: str) -> None:
    linhas: list[str] = []
    linhas.append("# Estudo de Escalas — Etapa Intermediária (Teto de 42h/semana | 8h24min/dia)\n")
    linhas.append(
        "**Vigência:** 16 de dezembro de 2026 a 15 de dezembro de 2027 (1º ano de transição da EC 141/2026, "
        "conforme decisão cautelar do STF nas ADIs 8.041 e 8.042).\n"
    )
    linhas.append(
        f"**Premissas da Empresa:** Operação 24x7 | Base atual: **{BASE_POR_TURNO} funcionários/turno** "
        f"(**{TOTAL_EFETIVO_ATUAL} efetivos**) | Meta operacional atual: **{POSTOS_SIMULTANEOS:.1f} postos simultâneos/hora** "
        f"(**{HORAS_HOMEM_DIA} horas-homem/dia**).\n"
    )
    linhas.append(
        "**Impacto da jornada de 8h24min (8,4h/dia) nos 3 turnos:** "
        "Com 3 turnos de 8h24min, a soma diária é de **25h12min**, gerando **24 minutos de sobreposição** em cada troca de turno "
        "(1h12min/dia de passagem de turno). O colaborador entrega **+5% de horas** por dia em relação à jornada de 8h.\n"
    )

    linhas.append("---\n")
    linhas.append("## 1. Quadro Resumo Comparativo — Transição 42h/sem (Jornada de 8h24min/dia)\n")
    linhas.append(
        f"| Perfil | Escala | Ciclo | Horas/Sem (8h24/d) | Efetivo Diário (%) | "
        f"Quadro p/ {POSTOS_SIMULTANEOS:.1f}/turno | Extras ({POSTOS_SIMULTANEOS:.1f}/turno) | Quadro p/ {HORAS_HOMEM_DIA} h-h/dia | Extras (h-h) | Domingos (Méd / Máx) |"
    )
    linhas.append(
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    )

    # Inclui 5x2 apenas para referência na transição de 42h, além das finalistas de 8h
    opcoes_transicao = [
        {
            "perfil": "Referência 5x2 (Folga fixa)",
            "nome": "5x2",
            "padrao": "TTTTTFF",
            "horas_dia": 8.4,
            "turnos": 3,
        }
    ] + [
        {
            "perfil": item["perfil"],
            "nome": item["nome"],
            "padrao": item["padrao"],
            "horas_dia": 12.0 if item["horas_dia"] == 12 else 8.4,
            "turnos": item["turnos"],
        }
        for item in FINALISTAS[1:]
    ]

    for item in opcoes_transicao:
        padrao = item["padrao"]
        n = len(padrao)
        dias_t = padrao.count("T")
        horas_dia = item["horas_dia"]
        turnos = item["turnos"]

        horas_sem = dias_t * horas_dia * (7.0 / n)
        efetivo_frac = dias_t / n

        # Cenário A: manter 75 pessoas escaladas em cada turno (com 24min de sobreposição nas trocas)
        quadro_turno_total = ceil((POSTOS_SIMULTANEOS / efetivo_frac) * turnos)
        extras_turno = quadro_turno_total - TOTAL_EFETIVO_ATUAL

        # Cenário B: manter exatamente 1.800 horas-homem/dia (aproveitando os +5% de horas da jornada 8h24)
        trab_dia_hh = HORAS_HOMEM_DIA / horas_dia
        quadro_hh_total = ceil(trab_dia_hh / efetivo_frac)
        extras_hh = quadro_hh_total - TOTAL_EFETIVO_ATUAL

        if n % 7 == 0:
            dom_str = "Fixo (0d ou 7d)"
        else:
            dom_med, dom_max, _ = calcular_intervalos_domingo(padrao)
            dom_str = f"{dom_med:.1f}d / {dom_max}d"

        h_str = f"{horas_sem:.2f}h" + (" (12h)" if horas_dia == 12 else "")

        linhas.append(
            f"| {item['perfil']} | **{item['nome']}** | {n}d | {h_str} | "
            f"**{efetivo_frac*100:.2f}%** | "
            f"{quadro_turno_total} | **+{extras_turno}** | "
            f"{quadro_hh_total} | **+{extras_hh}** | {dom_str} |"
        )

    linhas.append(
        "\n> **Leitura das duas colunas de dimensionamento:**\n"
        f"> - **Quadro p/ {POSTOS_SIMULTANEOS:.1f}/turno:** Mantém exatamente {POSTOS_SIMULTANEOS:.1f} pessoas em média presentes em cada turno de 8h24min (os 24min extras ficam como passagem de turno/sobreposição). Exige as mesmas contratações da etapa definitiva.\n"
        f"> - **Quadro p/ {HORAS_HOMEM_DIA} h-h/dia:** Se a operação puder aproveitar os 24min extras diários para reduzir ligeiramente o efetivo por turno (~50,0 pessoas/turno × 8,4h × 3 turnos = {HORAS_HOMEM_DIA} h-h/dia), a necessidade imediata de contratação cai durante 2027.\n"
    )

    linhas.append("---\n")
    linhas.append("## 2. Recomendações Práticas para a Transição (Dez/2026 a Dez/2027)\n")
    linhas.append(
        "1. **Não há ganho de teto em novas escalas com 8h24min:** Como 5 dias × 8h24min já atingem exatamente **42,00h/semana** (71,43% de efetivo), continua impossível ultrapassar 71,43% de efetivo diário respeitando as 2 folgas a cada 7 dias.\n"
        "2. **Atenção ao degrau de dezembro/2027:** Se a empresa dimensionar o quadro por horas-homem (+5 pessoas usando 8h24min/dia na escala de 70%) em dezembro/2026, precisará contratar o restante (+10 pessoas, fechando +15) até dezembro/2027, quando a jornada cai definitivamente para **40h/semana (8h/dia)**.\n"
        f"3. **Escala `12x36` na transição:** Durante o período de 42h/semana (até dez/2027), a `12x36` (média de 42,00h/sem) fica **100% aderente ao teto semanal** sem necessidade de folgas compensatórias adicionais, mantendo os **{TOTAL_EFETIVO_ATUAL} funcionários (+0 extras)** — ainda dependendo de previsão em ACT/CCT.\n"
    )

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print(f"Relatório 42h gerado com sucesso em: {caminho_saida}")


if __name__ == "__main__":
    md_path = "/mnt/a/SANDBOX/ESCALAS/relatorio_escalas_42h_v2.md"
    docx_path = "/mnt/a/SANDBOX/ESCALAS/relatorio_escalas_42h_v2.docx"
    gerar_markdown_42h(md_path)
    md_para_docx(md_path, docx_path)
