# Atualização automática dos dados (Fazendinha e Curuá)

O fluxo roda no GitHub Actions a cada 6 horas (`.github/workflows/atualizar-dados.yml`) e também sob demanda (aba Actions → Atualizar dados da maré → Run workflow).

1. `baixar_hydromet.py` entra no Hydromet Cloud, baixa o Excel do sensor RLS de cada estação e salva em `entrada/<estacao>/`.
2. `atualizar_dados.py` junta com `dados/serie_<estacao>.csv`, aplica o controle de qualidade, recalcula marés e série horária e reescreve o bloco `TC_HARM` da página.
3. O fluxo grava o resultado no repositório. O GitHub Pages publica em seguida.

## Segredos (você cria; nunca no código)
Repositório → Settings → Secrets and variables → Actions → New repository secret:
- `HYDROMET_USER`
- `HYDROMET_PASS`

## Pontos a confirmar na primeira execução
- Fazendinha: estação `Atalaia_Fazendinha`, sensor `RLS` (confirmado na tela do Hydromet Cloud).
- Curuá: estação `PONTA_DO_CÉU_I`. Os sensores dessa estação são Bateria, BOIA (SE200), RADAR e Temp, sem sensor chamado RLS. O fluxo usa `RADAR`. Em consultas de teste, o RADAR e a BOIA não devolveram dados para 28/03/2026 nem para outubro/2026. Se for outro sensor, defina a variável `HYDROMET_SENSOR_CURUA`.
- Se um download falhar, o fluxo guarda tela e HTML em "diagnostico" (aba Actions → execução → Artifacts).

## Teste local
`pip install numpy pandas playwright && python3 -m playwright install chromium`
`HYDROMET_USER=... HYDROMET_PASS=... python3 baixar_hydromet.py --inspecionar`
`python3 atualizar_dados.py`
