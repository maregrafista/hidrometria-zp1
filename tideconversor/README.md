# TideConversor

Conversão entre a régua de Fazendinha e a tábua de Porto de Santana, horários, série histórica, **previsão harmônica com componentes anuais** e **comparação previsto × observado**. Setor de Hidrografia da UNIPILOT. Página única, funciona offline ao salvar a página.

## Atualização de 23/10/2026
- **Previsão harmônica de Fazendinha** (aba Previsão): 57 constantes da série de 313 dias do bloco 02, mais as componentes anuais **Sa (20,2 cm) e Ssa (8,6 cm)**; vale de 2024 a 2030. É a previsão que apresentou menos erros e a única usada para Fazendinha; para o Porto de Santana segue a tábua oficial de 2026.
- **Aba Previsto × observado:** uma janela de 3 a 30 dias (setas, data e 4 atalhos), com escala fixa que não muda de um período para outro. Mostra o resumo em linguagem direta (erro típico, tendência, 9 em cada 10 horas, horário da maré), o gráfico observado × previsto com as diferenças hora a hora, a tabela de preamares e baixamares previstas e observadas, o erro mês a mês e a exportação em CSV. Indica se o período foi usado no ajuste ou é teste independente.
- **NR de trabalho = 66,7 cm acima do zero da régua** (RLS − 0,667 m) pelo método do Alte Franco (1997): NR = S0 anual − (M2 + S2 + N2 + K2) = 229,7 − 163,0. Substitui RLS − 0,75 m; os níveis acima do NR foram recalculados em todas as abas.
- **Quadro de marés** (aba Previsão): preamar e baixamar médias de sizígia e quadratura, nível médio e estabelecimento do porto (4 h 16 min).
- **Calibração, defasagens e histórico recalculados** com a série RLS de 07/11/2024 a 23/10/2026: 972 pares de calibração, 1.001 extremos pareados, médias diárias até outubro/2026.

## Desempenho da previsão (previsto − observado, RMSE horário em cm)
| Período | só marés | com Sa/Ssa |
|---|---|---|
| B03 jan–mar/2026 (independente) | 17,7 | **12,1** |
| B01 nov–dez/2024 (seca, independente) | 52,0 | **26,2** |
| B02 (ajuste) | 20,8 | 11,6 |
| B04 (ajuste) | 15,7 | 11,9 |

Erro de horário de preamar e baixamar: +9 e −6 min em média (absoluto ≈ 11 a 12 min). Sa e Ssa vêm de menos de dois ciclos anuais; fora do regime de 2025–2026 o nível médio pode mudar até ±30 cm.

## Equações
R = leitura da régua; H = nível acima do NR; T = tábua de Santana. H = R − 0,667; T = a + bR (ajuste mensal); R = (T − a)/b. Previsão harmônica: nível = S0 + Σ f·H·cos(V0 + u − GW).

## Documentação e dados
- [ANALISE_HARMONICA.md](ANALISE_HARMONICA.md): análise harmônica, NR, previsão e erros (figuras e scripts em `analise/harmonica/`).
- [ANALISE.md](ANALISE.md): reanálise da calibração e das defasagens com a série RLS.
- `data/`: constantes harmônicas, erros e previsão de preamares e baixamares de nov–dez/2026. `calibracao_mensal.csv`, `defasagens_mensais.csv`, `medias_historicas.csv` e `auditoria.json` foram atualizados.

## Aviso
Uso técnico e de apoio. Não substitui a Tábua de Marés oficial da DHN nem serve à navegação. A análise reproduz o método descrito no manual do PACMARÉ 2003 e foi conferida contra a saída do próprio programa em um caso; o algoritmo exato do ANHAMA (Franco, 2009, cap. 8) ainda não foi aplicado.
