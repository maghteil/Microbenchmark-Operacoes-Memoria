# Microbenchmark de operações em memória: Windows vs. Linux

Experimento da disciplina Programação para Ciência de Dados (Unijuí, 2026). Compara o tempo de alocação, escrita, leitura e liberação de memória no Windows e no Linux.

## Estrutura
Todos os arquivos ficam na mesma pasta:
- `microbenchmark.py`: coleta dos tempos (mesmo código nos dois sistemas)
- `analise.py`: validação, estatísticas, teste de Mann-Whitney e gráficos
- `logs_windows.csv`, `logs_linux.csv`, `logs_combinados.csv`: dados coletados
- `estatisticas.csv`, `diferenca_linux_menos_windows.csv`, `resumo_comparacao.csv`: resultados da análise
- `grafico_operacoes.png`, `grafico_total.png`: gráficos
- `ambientes.md`: configuração de hardware e dos sistemas

## Como reproduzir
1. Use duas VMs (ou dual boot) equivalentes, uma por vez, com aplicações desnecessárias fechadas.
2. Em cada sistema, na pasta do projeto: `python microbenchmark.py` (Linux: `python3 microbenchmark.py`). Gera `logs_windows.csv` ou `logs_linux.csv` (1000 linhas cada).
3. Reúna os dois CSVs numa pasta e instale as dependências: `pip install pandas matplotlib seaborn scipy`.
4. Rode `python analise.py`.

## Condições do experimento
Blocos de 100 a 1000 MB (passo de 100 MB), 100 repetições por bloco, ordem alocar → escrever → ler → liberar, tempos em ms. Ordem de execução: **[sistema 1 → sistema 2]**.

## Limitações
Resultados válidos apenas para este hardware, para as VMs usadas, para o microbenchmark em Python e para as condições descritas.