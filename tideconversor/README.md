# TideConversor

Desenvolvido pelo Setor de Hidrografia da UNIPILOT.

Conversão sazonal entre a régua de Fazendinha e a altura prevista na tábua do Porto de Santana, com análise descritiva dos horários e do nível médio.

## Uso

Abra `index.html` ou acesse a página publicada. O aplicativo é autocontido, inclui seu logotipo e funciona offline ao salvar a página.

- **Alturas:** selecione a referência, informe a altura em metros e o mês. Para entrada na régua, apresenta H acima do NR e equivalente na tábua. Para entrada na tábua, apresenta H estimado em Fazendinha e equivalente na régua.
- **Horários:** diferença entre extremo observado em Fazendinha e previsão de Santana. Negativo significa antes da previsão; positivo, depois. Não equivale, isoladamente, à propagação física entre duas estações observadas.
- **Série histórica:** médias mensais e cobertura de 2024–2026. 2024 é mostrado separadamente por ter ocorrido seca extrema regional. 2025 é um comparador, não normal climatológica.

## Equações e validação

R = altura acima do zero da régua, H = altura em Fazendinha acima do NR, T = altura da tábua de Santana. Todas em metros.

H = R − 0,75. T = a + bR. No sentido inverso: R = (T − a)/b.

A calibração mensal usa somente dados de 2026, pareados nos horários oficiais de preamar e baixamar. 66.419 leituras válidas e 1.003 pares. Validação por retirada de semanas inteiras: RMSE 8,30 cm para T e 7,94 cm para R. Trata-se de validação temporal interna, não validação em outro ano nem intervalo de confiança. Alturas intermediárias não foram validadas separadamente.

Pressupõe-se o mesmo zero entre a régua física e as séries, sem nivelamento independente fornecido. O valor de NR foi informado pelo usuário e é aplicado uma vez. Os relógios foram mantidos conforme os arquivos, sem deslocamento inferido.

## Novo arquivo

`atalaia_loggrp_20260728_20260803.xlsx` contém 186.510 linhas, de 30/09/2024 16:20 a 14/07/2026 06:30. Seus gráficos internos identificam a coluna E como altura acima do zero e F = E − 0,75. A coluna D, com longos trechos quase constantes, não foi usada. O nome do sensor da coluna E não foi presumido.

Nas coincidências de 2026, a coluna E tem preferência sobre os arquivos Report; não se calculou média de fontes nem se duplicaram horários. Há 55.254 coincidências válidas e 19.472 valores idênticos. Um pico isolado em 09/06/2026 10:30, +0,65/−0,66 m em cinco minutos, foi retirado apenas da análise e preservado na auditoria original. A nova série permite recuperar o trecho de 06/01 que era suspeito nos Reports.

As médias diárias históricas exigem ≥260 amostras e intervalo máximo no dia ≤60 minutos. Médias mensais dão peso igual a cada dia qualificado. Meses parciais são identificados. A comparação de outubro–dezembro 2024 × 2025 usa meses completos: diferenças observadas de −30,24; −23,58 e −23,09 cm. Essas diferenças não isolam causalmente o efeito da seca.

## Ciclo lunar e extremos

Fases do U.S. Naval Observatory em UTC, convertidas para UTC−03. Janela padrão ±2 dias, ajustável a ±1 ou ±3. Lua nova/cheia: sizígia; quartos: quadratura. Eventos fora da janela não entram nas médias. A classificação astronômica não pressupõe coincidência exata com máximos e mínimos da amplitude local.

Extremos detectados independentemente, por segmento, proeminência 0,50 m. Candidatos do mesmo tipo a menos de 3h são agrupados. Horário de patamar = centro da primeira à última ocorrência do extremo. Pareamento um a um do mesmo tipo, distância máxima 180 min, sem atravessar lacunas >90 min. Suporte padrão ≤20 min e patamar ≤40 min; opção ampliada ≤65 min. 970 extremos antes dos filtros. n<3: média não mostrada; n=3–9: poucos pares. DP é dispersão dos eventos, não incerteza da média.

## Fontes

- Dados locais fornecidos pelo usuário: XLSX Atalaia e arquivos Report.
- Tábua oficial Porto de Santana 2026, PDF fornecido pelo usuário.
- Fases lunares: https://aa.usno.navy.mil/api/moon/phases/year?year=2026
- Contexto da seca de 2024: https://www.sgb.gov.br/sala-de-imprensa/-/asset_publisher/ujyx/content/monitoramento-hidrologico-permite-acompanhar-evolucao-da-estiagem-na-regiao-norte
- Logotipo: https://unipilot.com/imagens/site/icones/logo.png

Não se publicaram as planilhas originais neste diretório. Os dados derivados, coeficientes, fases e estatísticas usados pela interface estão incorporados no HTML. As tabelas CSV acompanham a página. Atualização: 23/10/2026.
