"""
Lista histórica consolidada de escalas estudadas (EC 141/2026 + Portaria MTE nº 2.041/2026).
Calcula:
- Efetivo diário (%) e Quadro Total (base 210 = 70/turno, meta 52,5 postos simultâneos)
- Jornada Média Semanal para 8h00/dia e para 8h24min/dia (8,40h)
- Quantidade de folgas no mês-calendário (28, 29, 30 e 31 dias) e conformidade com Art. 4º, § 4º
- Intervalo entre domingos (Média / Máximo)
"""

from math import ceil

TOTAL_EFETIVO_ATUAL = 210
POSTOS_SIMULTANEOS = 52.5

# (Nome, Padrão, Horas/dia base, Turnos/dia)
ESCALAS = [
    ("6x2 (Atual)", "TTTTTTFF", 8.0, 3),
    ("5x2 (Fixa)", "TTTTTFF", 8.0, 3),
    ("4x2 + 6x2 (14d)", "TTTTFFTTTTTTFF", 8.0, 3),
    ("3x1 + 2x1 + 2x1 (10d)", "TTTFTTFTTF", 8.0, 3),
    ("5x2 + 5x2 + 4x2 (20d)", "TTTTTFFTTTTTFFTTTTFF", 8.0, 3),
    ("5x2 + 4x2 (13d)", "TTTTTFFTTTTFF", 8.0, 3),
    ("(4x 2x1) + 3x1 (16d)", "TTFTTFTTFTTFTTTF", 8.0, 3),
    ("4x2 (6d)", "TTTTFF", 8.0, 3),
    ("2x1 (3d)", "TTF", 8.0, 3),
    ("5x2 + 5x3 (15d)", "TTTTTFFTTTTTFFF", 8.0, 3),
    ("6x3 (9d)", "TTTTTTFFF", 8.0, 3),
    ("3x3 (6d - 8h)", "TTTFFF", 8.0, 3),
    ("4x4 (8d - 8h)", "TTTTFFFF", 8.0, 3),
    ("3x3 (6d - 12h)", "TTTFFF", 12.0, 2),
    ("4x4 (8d - 12h)", "TTTTFFFF", 12.0, 2),
    ("12x36 (1x1 - 12h)", "TF", 12.0, 2),
]

MESES = [28, 29, 30, 31]


def folgas_por_mes(padrao: str, dias_mes: int) -> tuple[int, int, int]:
    """Retorna (min_folgas, max_folgas, qtd_fases_abaixo_meta) considerando todas as fases 0..n-1."""
    n = len(padrao)
    meta = ceil((2 * dias_mes) / 7)
    contagens = [
        sum(1 for d in range(dias_mes) if padrao[(inicio + d) % n] == "F")
        for inicio in range(n)
    ]
    abaixo = sum(1 for c in contagens if c < meta)
    return min(contagens), max(contagens), abaixo


def intervalos_domingo(padrao: str) -> str:
    n = len(padrao)
    if n % 7 == 0:
        return "Fixo"
    dom_folga = [w * 7 for w in range(n) if padrao[(w * 7) % n] == "F"]
    gaps = [
        dom_folga[i + 1] - dom_folga[i] for i in range(len(dom_folga) - 1)
    ] + [n * 7 - dom_folga[-1] + dom_folga[0]]
    return f"{sum(gaps) / len(gaps):.1f}d / {max(gaps)}d"


def main() -> None:
    print("Meta Art. 4º, § 4º (Portaria MTE 2.041/2026): 28d=8 | 29d=9 | 30d=9 | 31d=9 folgas\n")
    cab = (
        f"{'Escala':<23} | {'Ciclo':>5} | {'Efetivo':>7} | {'Quadro(210)':>12} | "
        f"{'J.8h':>6} | {'J.8h24':>6} | {'28d':>5} | {'29d':>5} | {'30d':>5} | {'31d':>5} | {'§4º 100%?':<9} | {'Dom(Méd/Máx)'}"
    )
    print("=" * len(cab))
    print(cab)
    print("-" * len(cab))

    for nome, padrao, hd, turnos in ESCALAS:
        n = len(padrao)
        dt = padrao.count("T")
        ef = dt / n
        q_total = ceil((POSTOS_SIMULTANEOS / ef) * turnos)
        extras = q_total - TOTAL_EFETIVO_ATUAL
        q_str = f"{q_total:3d} ({extras:+4d})"

        j_8 = dt * hd * 7.0 / n
        j_84 = j_8 if hd == 12.0 else dt * 8.4 * 7.0 / n
        j_8_str = f"{j_8:5.2f}h"
        j_84_str = "  —   " if hd == 12.0 else f"{j_84:5.2f}h"

        f_cols = []
        ok_total = True
        for dm in MESES:
            fmin, fmax, abaixo = folgas_por_mes(padrao, dm)
            if abaixo > 0:
                ok_total = False
            f_cols.append(f"{fmin}" if fmin == fmax else f"{fmin}-{fmax}")

        ok_str = "SIM" if ok_total else "NÃO"
        dom_str = intervalos_domingo(padrao)

        print(
            f"{nome:<23} | {n:4d}d | {ef*100:6.2f}% | {q_str:>12} | "
            f"{j_8_str} | {j_84_str} | "
            f"{f_cols[0]:>5} | {f_cols[1]:>5} | {f_cols[2]:>5} | {f_cols[3]:>5} | "
            f"{ok_str:<9} | {dom_str}"
        )


if __name__ == "__main__":
    main()
