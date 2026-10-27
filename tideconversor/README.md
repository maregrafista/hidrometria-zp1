# TideConversor v2.2

Conversão entre a régua de Fazendinha e a tábua de Porto de Santana, horários, **previsão harmônica com componentes anuais** e **comparação previsto × observado**. Setor de Hidrografia da UNIPILOT. Aplicativo estático (HTML, CSS e JS), funciona offline após a primeira visita.

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
