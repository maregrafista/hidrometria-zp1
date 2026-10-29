# TideConversor v2.2

Conversão entre a régua de Fazendinha e a tábua de Porto de Santana, horários, **previsão harmônica com componentes anuais** e **comparação previsto × observado**. Setor de Hidrografia da UNIPILOT. Aplicativo estático (HTML, CSS e JS), funciona offline após a primeira visita.

## Versão 3.6 (28/10/2026): tábua da DHN × observado no Curuá

- A aba Previsto × observado do Curuá compara a tábua da DHN 2026 (Igarapé Grande do Curuá, 123 componentes, Carta 222) com o observado e com esta previsão. O cartão "Tábua da DHN × observado" mostra erro típico, tendência, erro sem a tendência, erro em 90 % das marés e erro de horário, para o período escolhido e para todo o registro de 2026. Os losangos rosa no gráfico são as marés da tábua. O CSV ganha as colunas da tábua.
- Referência: as alturas da tábua estão acima do NR da DHN (16,0 cm). O app leva todas ao zero da régua e supõe que o zero do sensor RLS é o zero da régua da DHN.
- Resultado (01/01 a 28/03/2026, 335 marés): erro típico de 17,3 cm na tábua (tendência −12,3 cm) e de 14,3 cm nesta previsão (tendência −7,0 cm). Na baixamar, a tábua fica 18,6 cm abaixo do observado (erro típico 20,2 cm). Na preamar, 5,9 cm abaixo (13,8 cm). O erro de horário da tábua é de −4,5 ± 10,5 min.

## Versão 3.5 (28/10/2026): NR do Curuá por nivelamento

- O NR do Curuá (21,8 cm acima do zero da régua) vem de nivelamento da UNIPILOT. O Quadro de maré passa a dizer isso.
- Comparação com a ficha F-41 da DHN (estação 10656, atualizada em 05/08/2019): NR de 16,0 cm, S0 = 267,4 cm e Z0 = 251,4 cm, com 365 dias de 2018. O NR da UNIPILOT é 5,8 cm maior que o da DHN. Os dois ficam no Quadro de maré.
- O app não guarda os dados do nivelamento (RN usadas, data, fechamento). A ficha da UNIPILOT segue pendente.

## Versão 3.4 (28/10/2026): novo ajuste do Curuá

- O ajuste do Curuá passa a usar 365 dias de 2025 (01/01/2025 a 31/12/2025), com Sa e Ssa. O ajuste anterior incluía a seca de 2024 (jun/2024 a mai/2025).
- Teste independente (01/01 a 28/03/2026): erro típico de 14,3 cm nas preamares e baixamares (antes: 16,7 cm), viés de −7,0 cm e erro de horário de −1,5 ± 12 min. No período do ajuste: 11,9 cm.
- Nível médio S0 = 280,9 cm acima do zero da régua (antes: 274,5 cm). Com o NR informado de 21,8 cm, o nível médio fica 2,59 m acima do NR. A DHN publica 2,52 m. A fórmula do NR dá 39,8 cm.
- Blocos de 32 dias (a partir de 01/01/2025) erram de 18 a 28 cm. Um ano de dados erra menos, porque separa Sa e Ssa e fixa o nível médio.
- Resumo "Teste independente" do Curuá: só jan a mar/2026.

## Versão 3.2 (28/10/2026): estação Curuá

- Nova página `tideconversor/curua/` com as abas Previsão, Previsto × observado e Quadro de maré. O seletor de estação fica no cabeçalho das duas páginas.
- Estação Curuá (Ponta do Céu I): leituras RLS de 01/06/2024 a 28/03/2026, a cada 10 min, sem lacunas. NR = 21,8 cm (informado pelo usuário). Com esse NR, o nível médio fica 2,53 m acima do NR. A DHN publica 2,52 m (Carta 222).
- Análise harmônica da UNIPILOT (método ANHAMA) com 364 dias (02/06/2024 a 31/05/2025). Sa e Ssa ajustados no mesmo bloco. Teste independente: 01/06/2025 a 28/03/2026.
- Resultado no teste independente: erro típico de 17,7 cm nas preamares e baixamares, com tendência de −11,6 cm (o nível observado foi mais alto que o previsto). No período do ajuste: 13,9 cm.
- Comparação com a Tábua de Marés 2026 da DHN (Igarapé Grande do Curuá, 123 componentes): a DHN tem erro de 13,8 cm contra o observado de janeiro a março. A previsão do app tem 16,7 cm no mesmo período e amplitude cerca de 4 % menor.
- NR: a fórmula NR = S0 − (M2 + S2 + N2 + K2) dá 39,3 cm. O NR informado (21,8 cm) vale. A diferença é de 17,5 cm.
- O mesmo tratamento de dados da Fazendinha: filtro de picos (nenhum achado), série horária com interpolação limitada a 30 min e controle de qualidade das marés (nenhuma reprovada, a série é contínua).
- Fazendinha: dados até 28/10/2026 22:05.

## Versão 3.1 (28/10/2026): botão de referência e leitura sem sobreposição

- Previsto × observado: botão "Acima do NR" / "Acima do zero da régua" visível no topo (antes ficava em "Mais opções"). A escolha vale para todas as telas.
- Previsão e Previsto × observado: a leitura do ponto tocado fica em uma faixa fixa acima do gráfico. Ela não cobre mais a curva e não desloca o gráfico.

## Versão 3.0 (27/10/2026): filtro de qualidade dos dados

Motivo: de 11/08 a 27/10/2026 o registrador falhou com frequência. A cobertura caiu para 22–27 % por mês (antes: 95–100 %). A maior lacuna foi de 9,2 dias. Os erros de horário subiram de ~10 min para 25–30 min, sem causa na previsão.

Regras do filtro (arquivo `data/harm.js`, campos `qc`, `qc_regras`, `lagq`):
1. Picos espúrios: mediana móvel de 3 h do resíduo; desvio > 30 cm sai (2 passagens).
2. Série horária: só interpola entre leituras com até 30 min de intervalo (antes: 60 min). Removeu 504 horas, todas depois de 01/08/2026.
3. Preamar e baixamar: só entra nas estatísticas se não houver lacuna maior que 15 min em 90 min antes e depois do extremo. Reprovadas: 159 de 2.615 marés (símbolo ○).
4. Aba Horários: mesmo critério (109 de 943 pares reprovados). Média só com 5 pares ou mais; * de 5 a 9 pares. O filtro pode ser desligado para comparar.

Resultado (marés válidas): erro de horário volta ao normal (desvio ~11 min). O desvio de nível continua: tendência de −11 a −17 cm em ago–out/2026, contra −1 a −5 cm de jan a jul. Esse desvio aparece também nas marés válidas. Não vem de falha de comunicação. Causas possíveis: vazão baixa do rio, efeitos meteorológicos ou deslocamento do sensor. Confira com leitura de régua.

Aba Previsto × observado: quadro "Qualidade dos dados" (leituras, maior lacuna, marés válidas, tendência, erro típico), CSV com coluna de qualidade.

## Versão 2.9 (27/10/2026): símbolos de fase lunar

- Horários: sizígia usa ● (lua nova) e ○ (lua cheia); quadratura usa ◐ (quarto crescente) e ◑ (quarto minguante). Convenção de tábuas náuticas; glifos exatos da DHN não verificados na fonte oficial.

## Versão 2.8 (27/10/2026): menos rolagem
- **Cabeçalho do celular:** de 148 para 93 px. Os 5 botões das telas ficam em uma só linha (12 px, até 2 linhas de texto).
- **Espaços:** margens, preenchimentos e intervalos menores em todas as telas, sem sobrepor nem comprimir os textos (alvos de toque de 38 a 46 px).
- **Leitura do gráfico:** a faixa de leitura virou uma janela sobre o gráfico, que só aparece ao tocar. Ela não ocupa mais espaço fixo.
- **Resultado no celular (375 × 812):** o painel visível passou de 601 para 663 px. A Previsão cabe em uma tela (1, 2 ou 3 dias). A rolagem de Previsto × observado caiu de 1.882 para 1.701 px e a de Horários de 1.525 para 1.381 px; o Quadro de maré, de 3.949 para 3.754 px.

## Versão 2.7 (27/10/2026): escala tipográfica
Revisão só do tamanho das fontes (o conteúdo não mudou). A escala segue a hierarquia de consulta e três referências: o [Material Design 3](https://m3.material.io/styles/typography/type-scale-tokens) (corpo 16/14/12, rótulos 14/12/11, títulos 24 a 32), as [Human Interface Guidelines da Apple](https://developer.apple.com/design/human-interface-guidelines/typography) (corpo 17 pt, mínimo de 11 pt no iOS) e guias de painéis de dados (número principal de 36 a 44 px, textos de eixo de 10 a 12 px).

| Nível | Uso | Celular | Computador |
|---|---|---|---|
| 1 | Número principal (erro típico, nível convertido) | 36 a 41 px | 44 px |
| 2 | Título da tela | 20 px | 22 a 24 px |
| 3 | Valores de apoio (métricas, cartões) | 18 a 24 px | 18 a 28 px |
| 4 | Corpo e frases | 14 a 14,5 px | 15 px |
| 5 | Texto de apoio, legendas, botões | 12 a 13,5 px | 12,5 a 14 px |
| 6 | Rótulos em maiúsculas e eixos dos gráficos | 11 a 12 px | 11,5 a 12 px |

Mudanças principais: o número do erro típico caiu de 52–68 px para 36–44 px; os títulos de tela ficaram em 20–24 px (antes 17 px no celular); o subtítulo da marca subiu de 8 para 10 px; a barra de leitura do gráfico e os controles ficaram mais baixos, o que devolve cerca de 90 px de tela ao gráfico no celular. Nenhum texto fica abaixo de 11 px.

## Versão 2.6 (27/10/2026)
- **Previsto × observado:** o quadro "Marés do período" saiu. O botão de 1 dia entrou. O gráfico "Erro mês a mês" ganhou faixas de classificação (muito boa, boa, razoável, fraca), separadores de ano, linha do mês aberto e destaque do mês escolhido.
- **Previsão:** controles em 2 linhas e gráficos que se ajustam à altura da tela. No celular, a tela inteira cabe sem rolar (1 a 3 dias). Os cartões dos dias viraram uma faixa compacta.
- **Gráficos de todo o app:** resolução de 3 a 4 pixels por pixel de tela.
- **Textos:** revisão no estilo ASD-STE100 em português: frases de até 20 palavras e um termo por conceito (erro = previsto − observado).

## Correção (27/10/2026)
- **Previsto × observado não rolava.** Desde a atualização de 27/10, o painel dessa aba perdeu a regra de rolagem e o conteúdo abaixo da primeira tela ficava inacessível, no celular e no computador. A regra voltou e a aba Alturas também rola quando o conteúdo passa da tela.
- **Botão “Hoje”** na aba Previsto × observado: mostra o período que termina hoje (ou o último período com dados).
- O navegador de todo o registro aceita rolagem vertical sobre ele (antes bloqueava o toque).

## Versão 2.5 (27/10/2026)
- **Previsto × observado reescrito para o celular.** Ordem da tela: período (setas, primeiro dia e 3, 7, 15 ou 30 dias), resultado (erro típico em número grande, classificação e frase curta), gráficos (a) e (b) com leitura por toque, navegador de todo o registro, marés em cartões, erro mês a mês e CSV. Exemplos de período e referência (NR ou zero da régua) ficam em “Mais opções”. No computador, o mesmo conteúdo usa duas colunas. A lista de marés mostra, no máximo, as 400 mais recentes; o CSV traz todas.

## Versão 2.4 (27/10/2026)
- **Textos em português simplificado, no estilo da ASD-STE100.** A ASD-STE100 é uma norma de inglês técnico; aqui o app segue os mesmos princípios em português do Brasil: frases curtas (até 20 palavras nas instruções e 25 nas descrições), voz ativa, tempo presente, uma ideia por frase, um termo para cada conceito (nível de redução, NR; preamar; baixamar; zero da régua; previsto; observado; diferença = previsto − observado) e unidades abreviadas (m, cm, min). Os termos e os limites seguem a NORMAM-501/DHN e a IHO S-44 (6.1.0).
- **Previsão:** voltou ao modelo anterior ao estilo HIDRO-Telemetria (1, 2 ou 3 dias, referência NR ou zero da régua). O erro agora aparece em um gráfico auxiliar (b), logo abaixo do gráfico principal (a), com o mesmo eixo de tempo. A curva do erro no eixo direito saiu.
- **Gráficos:** resolução mínima de 2 pixels por pixel de tela, para linhas e textos nítidos.
- Revisão de todas as telas no computador e no celular; sem erros no console e sem rolagem lateral.

## Atualização da base (27/10/2026)
- **Previsão no estilo do HIDRO-Telemetria (ANA):** período De/A com atalhos (1, 2, 3, 7 dias, 1, 3 e 6 meses e Hoje), curva prevista e observada (pontos e linha), eixo direito invertido com **barras da diferença previsto − observado** (como a chuva no HIDRO), navegador inferior com alças, “Mostrar tudo”, leitura ao passar o cursor, tabela opcional e CSV. Acima de 62 dias o gráfico passa a médias diárias.
- **Referência das alturas:** a Previsão e o Previsto × observado têm o seletor “Acima do NR / Acima do zero da régua” (a escolha vale nas duas telas; a diferença é o NR de 66,3 cm). A Previsão passou a mostrar também a curva observada e, nas preamares e baixamares do dia, o horário e a altura observados.
- Série RLS atualizada até 27/10/2026 10:50 (arquivo .xls até 23/10 e .csv de 09 a 27/10; 186.332 leituras). Os valores repetidos nos dois arquivos são idênticos.
- **Previsto × observado com o mínimo de informação:** as preamares e baixamares observadas passaram a ser extraídas de todo o registro, também dos trechos curtos ou de amostragem irregular (antes só dos blocos contínuos de 32 dias). Sobem de 2.088 para 2.615; 68 são de registro irregular (amostras mais espaçadas, marcadas com ○) e têm incerteza maior.
- Picos espúrios do registro irregular (a partir de 01/08/2026) foram removidos pela diferença em relação à mediana local do resíduo (117 amostras). Scripts em `analise/atualizacao_2026-10-27/`.
- A calibração mensal de alturas (aba Alturas) não foi recalculada.

## Novidades da v2.2 (23/10/2026)
- **Somente esta versão é atualizada daqui em diante** (hidrometria-zp1/tideconversor). Horários remodelado (sizígia e quadratura sempre visíveis, cartões do mês, gráfico e tabela de todos os meses, resolução ampliada como padrão); Previsão por 1, 2 ou 3 dias sem campo de hora; unidades em “m”; Quadro com “Estação” e a Tabela 5 com Amplitude e Fase.
- **Telas simplificadas:** a Previsão virou uma curva do dia (toque ou arraste para escolher a hora) com a leitura do nível e as próximas preamar e baixamar, sem coluna d’água; o Previsto × observado cabe em quase uma tela, com todos os gráficos; a Série histórica foi removida; no Quadro de maré, a velocidade das constantes tem duas casas decimais e a Tabela 5 é centralizada.
- **Previsto × observado refeito:** visão geral de todo o registro (média diária, clique para escolher o período), resumo do erro de todo o registro, só do teste independente e do ajuste, curvas e pontos (preamares e baixamares observadas e previstas) no lugar de barras, erro de altura em pontos e curvas, erro mês a mês em pontos e curva, tabela com todas as 2.088 marés e CSV do período ou de todo o registro.
- **Aba Quadro de maré:** informações de maré no formato das cartas náuticas (alturas PMS, PMQ, NM, BMQ e BMS acima do NR e do zero da régua, esquema dos níveis, tipo de maré, estabelecimento do porto, amplitudes e constantes harmônicas principais), com botão para imprimir ou salvar em PDF.
- **Constantes do PACMARÉ:** a previsão de Fazendinha passou a usar as **113 constantes harmônicas geradas pelo PACMARÉ** para o bloco 02 (arquivos `AH_02` e `CH_B02`), incluindo Sa (21,6 cm) e Ssa (8,3 cm), no lugar das 57 do ajuste próprio. O erro caiu em todos os blocos (tabela abaixo). Quadro de marés, preamares/baixamares e curva previsto × observado foram recalculados. O NR foi alinhado às novas constantes: **66,3 cm** (era 66,7 cm).

## Novidades da v2.1
- **Previsão harmônica de Fazendinha** (aba Previsão): 57 constantes obtidas da série de 313 dias do bloco 02, com as componentes anuais **Sa (20,2 cm) e Ssa (8,6 cm)** (substituídas na v2.2 pelas do PACMARÉ); vale de 2024 a 2030. É a previsão que apresentou menos erros e a única usada para Fazendinha; para o Porto de Santana segue a tábua oficial.
- **Aba Previsto × observado:** uma janela de 3 a 30 dias (setas, data e 4 atalhos), com escala fixa que não muda de um período para outro. Mostra o resumo em linguagem direta (erro típico, tendência, 9 em cada 10 marés, horário da maré), calculado só nas preamares e baixamares, o gráfico observado × previsto com as diferenças hora a hora, a tabela de preamares e baixamares previstas e observadas, o erro mês a mês e a exportação em CSV. Indica se o período foi usado no ajuste ou é teste independente.
- **NR de trabalho = 66,3 cm acima do zero da régua** (RLS − 0,663 m), pelo método do Alte Franco (1997) com o nível médio anual S0 = 229,7 cm: NR = 229,7 − (M2 + S2 + N2 + K2) = 229,7 − 163,4. Substitui o RLS − 0,75 m. Todos os níveis acima do NR, inclusive o histórico, foram recalculados.
- **Quadro de marés** de Fazendinha: preamar e baixamar média de sizígia e de quadratura, nível médio e estabelecimento do porto (4 h 16 min).

## Desempenho (previsto − observado, RMSE horário em cm)
| Período | ajuste próprio (57 const.) | PACMARÉ (113 const.) |
|---|---|---|
| B03 jan–mar/2026 (independente) | 12,1 | **10,1** |
| B04 mar–jul/2026 (independente) | 11,8 | **9,5** |
| B01 nov–dez/2024 (seca, independente) | 26,3 | **24,1** |
| B02 (ajuste) | 11,6 | **8,7** |

Com o nível médio S0 anual (229,7 cm). Preamar/baixamar: desvio-padrão da altura de cerca de 8 cm (antes 10 a 11 cm); erro de horário médio de baixamar próximo de 0 min. Sa e Ssa vêm de menos de dois ciclos anuais e refletem o regime do rio de 2025–2026; fora dele o nível médio pode mudar até ±30 cm. Comparação completa em `data/comparacao_meu_vs_pacmare_*.csv`.

## Equações
R = leitura da régua; H = nível acima do NR; T = tábua de Santana (m). H = R − 0,663; T = a + bR com a e b locais no tempo (`data/calibracao_diaria.csv`). Previsão: nível = S0 + Σ f·H·cos(V0 + u − GW).

## Documentação e dados
- [ANALISE_HARMONICA.md](ANALISE_HARMONICA.md): análise harmônica, NR, previsão e erros (com figuras e scripts em `analise/harmonica/`).
- [ANALISE.md](ANALISE.md): reanálise da calibração e das defasagens com a série RLS.
- `data/`: constantes (`constantes_B02.csv`, `constantes_Sa_Ssa.csv`), erros (`erro_mensal.csv`, `previsao_vs_observado_PM_BM_eventos.csv`), previsão de preamares e baixamares de nov–dez/2026 e as tabelas anteriores.

## Aviso
Uso técnico e de apoio. Não substitui a Tábua de Marés oficial da DHN nem serve à navegação. O método de análise reproduz o descrito no manual do PACMARÉ 2003 e foi conferido contra a saída do próprio programa em um caso; o algoritmo exato do ANHAMA (Franco, 2009, cap. 8) ainda não foi aplicado.
