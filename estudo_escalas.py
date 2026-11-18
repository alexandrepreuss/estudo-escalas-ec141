"""
Estudo Combinatório de Escalas de Trabalho (t x f) - EC 141/2026 (Regra Estrita)
Avalia ciclos de 6 a 21 dias buscando:
1. Conformidade estrita com a Regra Geral: <= 40h/semana E >= 2 folgas em TODA janela de 7 dias.
2. Rotatividade real nos dias da semana (ciclo mínimo NÃO múltiplo de 7, evitando folgas fixas).
3. Menor perda de efetivo possível e análise de turmas para cobertura 100% constante.
"""

from math import gcd

BASE_FUNCIONARIOS = 100
HORAS_POR_DIA = 8
LIMITE_HORAS_SEMANAIS = 40.0


def gerar_combinacoes_ciclo(
    tamanho_ciclo: int,
    min_folga: int = 2,
    max_folga: int = 2,
) -> list[tuple[tuple[int, int], ...]]:
    """Gera sequências únicas (descontando rotações) de blocos (t, f) somando `tamanho_ciclo`."""
    resultados_unicos: set[tuple[tuple[int, int], ...]] = set()

    def canonicalizar(seq: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
        rotacoes = [seq[i:] + seq[:i] for i in range(len(seq))]
        return min(rotacoes)

    def backtrack(dias_restantes: int, atual: list[tuple[int, int]]) -> None:
        if dias_restantes == 0:
            resultados_unicos.add(canonicalizar(tuple(atual)))
            return
        for f in range(min_folga, min(max_folga, dias_restantes) + 1):
            for t in range(1, dias_restantes - f + 1):
                atual.append((t, f))
                backtrack(dias_restantes - (t + f), atual)
                atual.pop()

    backtrack(tamanho_ciclo, [])
    return sorted(resultados_unicos)


def expandir_padrao(blocos: tuple[tuple[int, int], ...]) -> str:
    return "".join("T" * t + "F" * f for t, f in blocos)


def periodo_minimo(padrao: str) -> int:
    """Encontra o menor período de repetição da string (ex: TTTTTFFTTTTTFF tem período 7)."""
    n = len(padrao)
    for p in range(1, n + 1):
        if n % p == 0 and padrao[:p] * (n // p) == padrao:
            return p
    return n


def min_folgas_janela_7_dias(padrao: str) -> int:
    n = len(padrao)
    dobrado = padrao * ((7 // n) + 2)
    return min(dobrado[i : i + 7].count("F") for i in range(n))


def analisar_turmas_uniformes(padrao: str) -> list[dict]:
    n = len(padrao)
    divisores = [k for k in range(2, n + 1) if n % k == 0]
    analises = []
    for k in divisores:
        passo = n // k
        contagem = [
            sum(1 for turma in range(k) if padrao[(dia - turma * passo) % n] == "T")
            for dia in range(n)
        ]
        analises.append(
            {
                "turmas": k,
                "passo": passo,
                "uniforme": min(contagem) == max(contagem),
                "min_pct": (min(contagem) / k) * 100.0,
                "max_pct": (max(contagem) / k) * 100.0,
            }
        )
    return analises


def formatar_blocos(blocos: tuple[tuple[int, int], ...]) -> str:
    return " + ".join(f"{t}x{f}" for t, f in blocos)


def buscar_melhores_escalas(
    ciclo_min: int,
    ciclo_max: int,
    min_folga: int,
    max_folga: int,
    min_efetivo_pct: float = 60.0,
) -> list[dict]:
    candidatas = []
    vistos_padrao_minimo = set()

    for n in range(ciclo_min, ciclo_max + 1):
        for blocos in gerar_combinacoes_ciclo(n, min_folga, max_folga):
            padrao = expandir_padrao(blocos)
            p_min = periodo_minimo(padrao)
            if p_min < n:
                continue  # Já foi analisada no seu ciclo mínimo (ex: 5x2+5x2 já aparece em n=7)

            # Evita rotações do padrão mínimo
            rotacoes = [padrao[i:] + padrao[:i] for i in range(n)]
            canon = min(rotacoes)
            if canon in vistos_padrao_minimo:
                continue
            vistos_padrao_minimo.add(canon)

            dias_t = padrao.count("T")
            dias_f = padrao.count("F")
            horas_sem = dias_t * HORAS_POR_DIA * (7.0 / n)
            efetivo_pct = (dias_t / n) * 100.0
            min_f_7d = min_folgas_janela_7_dias(padrao)

            # Restrições estritas solicitadas:
            # 1) Regra geral: <= 40h/sem e >= 2 folgas em TODA janela de 7 dias
            if horas_sem > LIMITE_HORAS_SEMANAIS + 1e-9 or min_f_7d < 2:
                continue
            # 2) Rotatividade na semana: período mínimo NÃO pode ser múltiplo de 7
            if n % 7 == 0:
                continue
            # 3) Filtro de viabilidade operacional (efetivo mínimo)
            if efetivo_pct < min_efetivo_pct:
                continue

            turmas_info = analisar_turmas_uniformes(padrao)
            uniformes = [a for a in turmas_info if a["uniforme"]]
            melhor_turma = uniformes[0] if uniformes else min(
                turmas_info, key=lambda a: (a["max_pct"] - a["min_pct"], a["turmas"])
            )

            candidatas.append(
                {
                    "ciclo": n,
                    "escala": formatar_blocos(blocos),
                    "padrao": padrao,
                    "dias_t": dias_t,
                    "dias_f": dias_f,
                    "horas_sem": horas_sem,
                    "efetivo_pct": efetivo_pct,
                    "turmas": melhor_turma["turmas"],
                    "passo": melhor_turma["passo"],
                    "uniforme": melhor_turma["uniforme"],
                    "domingos_mes": (dias_f / n) * (30.4 / 7.0),
                }
            )

    # Ordena por maior aproveitamento de efetivo (menor necessidade de contratação), depois menor ciclo
    candidatas.sort(key=lambda x: (-x["efetivo_pct"], x["ciclo"], x["turmas"]))
    return candidatas


def imprimir_tabela(titulo: str, lista: list[dict]) -> None:
    print("=" * 105)
    print(titulo)
    print("=" * 105)
    if not lista:
        print("Nenhuma escala encontrada com esses critérios.\n")
        return

    print(
        f"{'Ciclo':>5} | {'Escala':<20} | {'Trab/Folga':<10} | {'Horas/Sem':>9} | "
        f"{'Efetivo':>8} | {'Turmas p/ 100% fixo':<24} | {'Dom/mês (méd)':>13}"
    )
    print("-" * 105)
    for c in lista:
        turma_txt = (
            f"{c['turmas']:2d} turmas (passo {c['passo']}d)"
            if c["uniforme"]
            else f"Não uniforme ({c['turmas']}t)"
        )
        print(
            f"{c['ciclo']:4d}d | {c['escala']:<20} | {c['dias_t']:2d}T / {c['dias_f']:2d}F  | "
            f"{c['horas_sem']:7.2f} h | {c['efetivo_pct']:6.2f}%  | "
            f"{turma_txt:<24} | {c['domingos_mes']:10.2f}"
        )
    print()


if __name__ == "__main__":
    # 1) Apenas blocos de 2 folgas consecutivas (ciclos de 6 a 21 dias, efetivo >= 60%)
    res_f2 = buscar_melhores_escalas(
        ciclo_min=6, ciclo_max=21, min_folga=2, max_folga=2, min_efetivo_pct=60.0
    )
    imprimir_tabela(
        "CENÁRIO A: Folgas de 2 dias consecutivos | Ciclos de 6 a 21 dias | Regra estrita (>=2 folgas em 7d) + Rotativa",
        res_f2,
    )

    # 2) Liberando blocos de 2 ou 3 folgas consecutivas (ciclos de 6 a 21 dias, efetivo >= 60%)
    res_f2_3 = buscar_melhores_escalas(
        ciclo_min=6, ciclo_max=21, min_folga=2, max_folga=3, min_efetivo_pct=60.0
    )
    imprimir_tabela(
        "CENÁRIO B: Folgas de 2 ou 3 dias consecutivos | Ciclos de 6 a 21 dias | Regra estrita (>=2 folgas em 7d) + Rotativa",
        res_f2_3,
    )

    # 3) Sem folgas consecutivas (f = 1) - ciclos de 3 a 21 dias, efetivo >= 60%
    res_f1 = buscar_melhores_escalas(
        ciclo_min=3, ciclo_max=21, min_folga=1, max_folga=1, min_efetivo_pct=60.0
    )
    imprimir_tabela(
        "CENÁRIO C: Sem folgas consecutivas (f = 1) | Ciclos de 3 a 21 dias | Regra estrita (>=2 folgas em 7d) + Rotativa",
        res_f1,
    )

    # 4) Misto: folgas de 1 ou 2 dias (f = 1 ou 2) - ciclos de 3 a 15 dias, efetivo >= 66%
    res_f1_2 = buscar_melhores_escalas(
        ciclo_min=3, ciclo_max=15, min_folga=1, max_folga=2, min_efetivo_pct=66.0
    )
    imprimir_tabela(
        "CENÁRIO D: Misto (f = 1 ou 2) | Ciclos de 3 a 15 dias | Regra estrita (>=2 folgas em 7d) + Rotativa (Efetivo >= 66%)",
        res_f1_2,
    )
