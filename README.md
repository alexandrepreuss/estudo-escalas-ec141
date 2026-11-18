# O fim da escala 6x1 (e 6x2) nas empresas 24/7: o que a matemática diz sobre a nova lei?

Com a aprovação da **EC 141/2026**, o Brasil entrou oficialmente na transição para o fim da escala 6x1, reduzindo o teto constitucional de 44h para **40h semanais** e garantindo **2 dias de folga** a cada período de 7 dias.

Para quem trabalha em horário comercial (segunda a sexta), a conta é simples: é a velha e boa **5x2**. Mas e para quem opera **24 horas por dia, 7 dias por semana** — indústrias, logística, saúde, TI, segurança, call centers — e simplesmente **não pode parar**?

Aqui na empresa, operamos 24/7 com 3 turnos de 8 horas e usávamos 4 turmas por turno na escala **6x2** (trabalha 6 dias, folga 2). Na base de **100 funcionários por turno** (**300 funcionários efetivos no total**), isso garantia sempre **75 pessoas trabalhando por hora** (75% de efetivo, totalizando 225 trabalhadores/dia e 1.800 horas-homem/dia). Com a nova regra, essa conta quebrou.

Resolvi colocar a mão na massa com a ajuda do Gemini e rodar simulações em Python para testar todas as combinações possíveis de escalas (`t x f`) dentro da nova lei. O que descobrimos é um choque de realidade — mas também traz saídas muito interessantes.

---

## Para quem tem pressa

* **O problema:** A EC 141/2026 reduz a jornada para 40h/semana e exige 2 folgas a cada 7 dias. A `5x2` padrão resolve a lei, mas trava as folgas nos mesmos dias da semana, gerando conflito em operações 24/7.
* **O limite matemático:** Com 8h/dia e 40h/semana, o teto teórico é de **71,43%** de efetivo diário; garantindo rotação semanal, o máximo prático cai para **70,00% a 70,59%** (contra 75% da antiga `6x2`), exigindo **+7,14% a +12,50%** de contratações.
* **O fator domingo (Art. 386 da CLT):** Ciclos longos (como 20 dias) agrupam folgas e deixam o colaborador até **105 dias sem um domingo livre**, o que pesa muito em equipes com maioria feminina. Nesse quesito, **`2x1`** (21d), **`4x2`** (máx. 35d) e **`12x36`** (14d) levam vantagem.
* **A saída `12x36`:** Mantém **0 contratações extras**, mas depende de acordo/convenção coletiva, tem média de 42h/semana (risco em dez/2027) e aumenta o risco de fadiga (NR-1).

**Navegue pelos capítulos:**
* [1. O problema da escala 5x2 em empresas que trabalham 24/7](#1-o-problema-da-escala-5x2-em-empresas-que-trabalham-247)
* [2. As restrições e o argumento matemático que limita a eficiência](#2-as-restrições-e-o-argumento-matemático-que-limita-a-eficiência)
* [3. Quadro resumo comparativo e as vantagens de cada perfil estudado](#3-quadro-resumo-comparativo-e-as-vantagens-de-cada-perfil-estudado)
* [4. O estudo da escala 12x36 e os riscos da adoção](#4-o-estudo-da-escala-12x36-e-os-riscos-da-adoção)
* [Scripts do repositório](#scripts-do-repositório)
* [Fontes](#fontes)

---

## 1. O problema da escala 5x2 em empresas que trabalham 24/7

À primeira vista, a solução óbvia seria pegar a **5x2** e dividir a equipe em 7 turmas (uma começando em cada dia da semana). Matematicamente, funciona: dá 40h/semana e garante cobertura constante todos os dias.

**O problema? Gestão de pessoas.**

Como a escala `5x2` tem ciclo exato de **7 dias**, quem cai na turma que folga terça e quarta vai folgar **terça e quarta para o resto da vida**. Enquanto isso, outra turma vai folgar **sábado e domingo todos os meses**.

Em uma operação 24/7, isso gera:
* Sensação de injustiça e conflitos internos entre turmas;
* Desmotivação de quem nunca pega um fim de semana livre;
* Dificuldade de retenção (turnover justamente nas turmas com "piores" folgas).

A mesma armadilha acontece em escalas mistas que fecham 7 dias, como `3x1 + 2x1`. Por isso, colocamos uma regra de ouro no nosso estudo: **o ciclo da escala não pode ser múltiplo de 7**, para que as folgas girem por todos os dias da semana (e todos tenham domingos livres de forma justa).

---

## 2. As restrições e o argumento matemático que limita a eficiência

Para não depender de interpretações frágeis ou brechas temporárias, aplicamos a regra estrita da EC 141/2026:
1. **Máximo de 40 horas semanais** (5 dias de 8h em média por semana);
2. **Pelo menos 2 folgas em qualquer janela móvel de 7 dias** (sem "empurrar" folgas para a semana seguinte);
3. **Ciclo não múltiplo de 7** (para garantir rotação semanal e distribuição justa de domingos).

Aqui entra a matemática dura — e é o argumento definitivo para refutar qualquer fórmula mágica que apareça em reunião:

> **Teto absoluto:** Com jornadas de 8 horas/dia e limite de 40 horas/semana, o máximo teórico que qualquer escala legal consegue entregar é `40 / 56 = 71,43%` (5 dias de trabalho a cada 7).

E quando exigimos **rotação semanal** (ciclo não múltiplo de 7), o efetivo cai obrigatoriamente um pouco abaixo desse teto, ficando no máximo entre **70,00% e 70,59%**.

Ou seja: sair dos **75%** da antiga `6x2` para **~70%** não é falta de criatividade do RH — é um **limite físico da matemática**.

---

## 3. Quadro resumo comparativo e as vantagens de cada perfil estudado

Usando nossa base de **100 funcionários por turno (300 efetivos no total)** para manter **75 postos simultâneos 24h/dia**, simulamos dezenas de combinações e chegamos aos perfis vencedores — incluindo a exceção `12x36`:

| Escala | Ciclo | Turnos x Turmas | Efetivo Diário (%) | Quadro Total p/ 75 postos | Dias entre domingos (Méd / Máx) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| *6x2 (atual, ilegal pós-EC 141)* | *8d* | *3x 4t* | *75,00%* | *300 (+0 / +0,0%)* | *28,0d / 49d* |
| **3x1 + 2x1 + 2x1** | 10d | 3x 10t | **70,00%** | **322 (+22 / +7,1%)** | 23,3d / 56d |
| **5x2 + 5x2 + 4x2** | 20d | 3x 10t | **70,00%** | **322 (+22 / +7,1%)** | 23,3d / 105d |
| **5x2 + 4x2** | 13d | 3x 13t | **69,23%** | **325 (+25 / +8,3%)** | 22,8d / 70d |
| **4x2** | 6d | 3x 3t | **66,67%** | **338 (+38 / +12,5%)** | 21,0d / 35d |
| **2x1** | 3d | 3x 3t | **66,67%** | **338 (+38 / +12,5%)** | 21,0d / 21d |
| **5x2 + 5x3** | 15d | 3x 3t | **66,67%** | **338 (+38 / +12,5%)** | 21,0d / 77d |
| **12x36 (1x1)** — exceção via acordo/convenção | 2d | 2x 2t | **50,00%** | **300 (+0 / +0,0%)** | 14,0d / 14d |

> *Turma* é o grupo de pessoas que trabalha e folga junto. *"3x 10t"* significa 3 turnos, cada um dividido em 10 turmas.

### Exemplo na prática: a escala 4x2

Na `4x2`, cada pessoa trabalha 4 dias e folga 2. Em cada turno, a equipe é dividida em **3 turmas**, e cada turma começa o ciclo 2 dias depois da anterior. O resultado é que **sempre 2 turmas trabalham e 1 folga**, todos os dias:

| Turma | Dia 1 | Dia 2 | Dia 3 | Dia 4 | Dia 5 | Dia 6 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Turma A | T | T | T | T | **F** | **F** |
| Turma B | **F** | **F** | T | T | T | T |
| Turma C | T | T | **F** | **F** | T | T |
| **Trabalhando** | 2 | 2 | 2 | 2 | 2 | 2 |

Como o ciclo tem 6 dias e a semana tem 7, a folga "anda" pelos dias da semana: ninguém fica preso à mesma terça e quarta. Em média, cada pessoa folga em um domingo a cada 21 dias, e no pior caso espera 35 dias.

Na base de 300 funcionários, são 2 em cada 3 turmas trabalhando, o que dá 66,67% de efetivo por dia. Para manter os 75 postos, o quadro vai a **338 pessoas (+38 / +12,50%)**, ou seja, cerca de 113 por turno em 3 turmas de 37 a 38.

> **Nota importante sobre os domingos (Méd / Máx):** Na `6x2`, você folga 2 domingos seguidos (7 dias de intervalo) e depois fica **49 dias** (7 semanas) sem folgar no domingo — média de 28 dias. O mesmo efeito de "agrupamento" acontece em ciclos longos: na `5x2 + 5x2 + 4x2` (20d), o funcionário chega a ficar **105 dias** sem domingo de folga (e depois pega vários seguidos). Já na **`2x1`** (21 dias fixos) e na **`4x2`** (máx 35 dias), os domingos são muito mais bem distribuídos ao longo do ano.

### O fator humano: o domingo e o efetivo feminino

Esse detalhe dos intervalos de domingo muda completamente o jogo em operações onde **mais de 70% do efetivo é composto por mulheres**. E não se trata apenas de boa prática de gestão, porque há também o lado jurídico:

* **Art. 386 da CLT:** prevê uma escala de revezamento quinzenal que favoreça o repouso dominical da mulher quando há trabalho aos domingos. Vale confirmar a aplicação ao seu caso com o jurídico.
* **Convenções coletivas:** muitas categorias negociam regras próprias, como pelo menos 1 domingo de folga por mês.

Quando olhamos apenas a *média* (cerca de 23 dias entre um domingo de folga e outro), escalas como `5x2 + 5x2 + 4x2` ou `5x2 + 4x2` parecem atender tranquilamente. Mas, no calendário real, ficar **56, 70 ou até 105 dias seguidos sem folgar em um domingo** rompe a regra mensal das convenções e fica longe da lógica quinzenal do Art. 386.

Sob essa ótica:
* A única escala do estudo com domingo de folga a cada **14 dias** é a **`12x36`**.
* Entre as escalas rotativas de 8 horas, as que mais preservam a regularidade mensal sem "apagões" longos são a **`2x1`** (folga garantida a cada **21 dias exatos**) e a **`4x2`** (máximo de **35 dias**).

### O que ganha e o que perde em cada perfil?

* **`3x1 + 2x1 + 2x1` — Ciclo de 10 dias:** Empata no **menor custo de reposição (+22 pessoas no total / +7,14%)**. Tem um ciclo curto e fácil de acompanhar, mas exige 10 turmas por turno e **não oferece folgas duplas** (as folgas são sempre de 1 dia).
* **`5x2 + 5x2 + 4x2` — Ciclo de 20 dias:** Também exige apenas **+22 contratações no total (+7,14%)** e entrega **folgas duplas consecutivas** em todo o ciclo. A troca é gerenciar 10 turmas por turno em um ciclo um pouco mais longo (20 dias).
* **`5x2 + 4x2` — Ciclo de 13 dias:** Custa **+25 contratações no total (+8,33%)**, mantém folgas duplas e tem um ciclo bem curto (13 dias, com média de 22,8 dias entre domingos). Exige 13 turmas por turno.
* **`4x2` ou `2x1` — Ciclos de 6 ou 3 dias:** Aqui o foco é **simplicidade máxima de gestão**. Você reduz de 4 para **apenas 3 turmas por turno** e melhora o descanso aos fins de semana (1 domingo a cada **21 dias** exatos na `2x1`, ou média de 21 dias e máximo de 35 na `4x2`). O preço é o aumento maior de quadro (**+38 pessoas no total / +12,50% na folha**).
* **`5x2 + 5x3` — Ciclo de 15 dias:** Tem o mesmo custo da `4x2` (**+38 pessoas / +12,50%** e **apenas 3 turmas por turno**), mas entrega um benefício enorme de qualidade de vida: a cada 15 dias, o colaborador ganha um **"feriadão" de 3 folgas seguidas**. Excelente para retenção de talentos.

---

## 4. O estudo da escala 12x36 e os riscos da adoção

Sempre que o assunto aperta no 24/7, alguém levanta a mão na sala e pergunta: *"E a escala 12x36 (que na prática é 1x1)?"*

Fizemos a conta considerando nossos **300 funcionários efetivos**. Na `12x36`, o dia deixa de ter 3 turnos de 8h e passa a ter **2 turnos de 12h** (150 pessoas no turno diurno e 150 no noturno). Você divide a equipe em **4 turmas de 75 pessoas** (2 turmas no turno do dia, 2 no da noite):
* Por dia (24h), trabalham **150 pessoas (50%)** e folgam **150 pessoas**.
* Mas como cada uma trabalha 12 horas, você entrega os mesmos **75 postos simultâneos 24h por dia** (`150 x 12h = 1.800 horas-homem/dia`).
* **Custo de reposição:** **Zero contratações extras (+0%)** (mantém os mesmos 300 funcionários) e ainda entrega um domingo de folga a cada **14 dias**!

Parece o mundo perfeito, certo? **Cuidado com os riscos:**

1. **Dependência sindical:** A `12x36` é regime de exceção e exige respaldo expresso em **Acordo ou Convenção Coletiva de Trabalho** (§ 2º e § 3º do Art. 7º). Sem o sindicato, ela é inválida.
2. **A armadilha das 42 horas:** A `12x36` pura gera uma média de **42 horas semanais** (alternando semanas de 36h e 48h). Quando o teto definitivo de **40h semanais** entrar em vigor (dez/2027), convenções coletivas podem exigir folgas extras compensatórias (cerca de 1 folga a mais a cada 3 semanas), o que faria o quadro subir de 300 para **~315 pessoas (+5,0%)**.
3. **Fadiga, acidentes e NR-1:** Turnos de 12 horas em atividades operacionais exigentes aumentam o risco de fadiga, erros e acidentes — algo que agora entra diretamente na fiscalização de **riscos psicossociais da NR-1**. Além disso, qualquer falta ou atestado de última hora em turno de 12h é muito mais difícil e caro de cobrir com hora extra.

---

## Conclusão

Não existe bala de prata para a transição da EC 141/2026 no modelo 24/7. A escolha passa por equilibrar **três pratos**: custo de contratação (+7% a +12,5% no quadro), simplicidade de gestão (3 a 13 turmas) e qualidade de vida (folgas simples, duplas ou triplas).

Na sua empresa, qual desses perfis faz mais sentido para a realidade da operação?

---

## Scripts do Repositório

* `estudo_escalas.py`: busca exaustiva combinatória de escalas `t x f` em ciclos variados, validando a conformidade com a EC 141/2026 e a rotação semanal.
* `gerar_relatorio.py`: gera o relatório comparativo da etapa definitiva (40h/semana), com quadros dia a dia por turma, em `.md` e `.docx`.
* `gerar_relatorio_42h.py`: gera o relatório da etapa intermediária de transição (42h/semana, jornada de 8h24min/dia).
* `gerar_docx.py`: utilitário que converte Markdown em Word (`.docx`) em paisagem, usando `python-docx`.

```bash
python3 estudo_escalas.py
python3 gerar_relatorio.py
python3 gerar_relatorio_42h.py
```

---

## Fontes

* **Emenda Constitucional nº 141/2026** (alteração do Art. 7º da Constituição Federal): https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc141.htm
* **Art. 386 da CLT** (Decreto-Lei nº 5.452/1943): https://www.jusbrasil.com.br/topicos/10722650/artigo-386-do-decreto-lei-n-5452-de-01-de-maio-de-1943
* **Decisão cautelar do STF nas ADIs 8.041 e 8.042** (regra transitória das 42h e da jornada de 8h24min): https://pauseperin.adv.br/noticia/stf-esclarece-regras-de-implementacao-da-jornada-prevista-na-ec-n-141-
* **Nova NR-1 e riscos psicossociais** (notícia do TST): https://www.tst.jus.br/-/nova-nr-1-amplia-prevencao-de-riscos-para-a-saude-mental-nos-ambientes-de-trabalho
