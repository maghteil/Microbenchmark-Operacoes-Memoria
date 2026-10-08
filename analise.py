import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu

OPS = ["alloc_ms", "write_ms", "read_ms", "free_ms"]
NOMES = ["Alocação", "Escrita", "Leitura", "Liberação"]

# 1) Leitura e validação
def carregar(caminho, sistema):
    df = pd.read_csv(caminho)
    assert list(df.columns) == ["bloco_MB", "teste"] + OPS, "Cabeçalho incorreto"
    df["bloco_MB"] = df["bloco_MB"].astype(int)
    df["teste"] = df["teste"].astype(int)
    df["sistema"] = sistema
    erros = []
    if len(df) != 1000: erros.append(f"{len(df)} registros (esperado 1000)")
    if df.isna().any().any(): erros.append("valores ausentes")
    if df.duplicated(["bloco_MB", "teste"]).any(): erros.append("duplicidades")
    if sorted(df["bloco_MB"].unique()) != list(range(100, 1001, 100)): erros.append("tamanhos de bloco incorretos")
    if not (df.groupby("bloco_MB")["teste"].apply(lambda s: sorted(s) == list(range(1, 101)))).all(): erros.append("testes 1-100 incompletos")
    if (df[OPS] < 0).any().any(): erros.append("tempos negativos")
    if erros:
        raise SystemExit(f"ERRO em {sistema}: " + "; ".join(erros))
    print(f"{sistema}: validação OK")
    return df

df = pd.concat([carregar("logs_windows.csv", "Windows"),
                carregar("logs_linux.csv", "Linux")], ignore_index=True)
df["total_ms"] = df[OPS].sum(axis=1)
df.to_csv("logs_combinados.csv", index=False)

# 2) Estatísticas por sistema, bloco e operação
cols = OPS + ["total_ms"]
agg = df.groupby(["sistema", "bloco_MB"])[cols].agg(["median", "mean", "std"])
agg.to_csv("estatisticas.csv")

# 3) Diferença Linux - Windows (medianas) e teste de Mann-Whitney
med = df.groupby(["sistema", "bloco_MB"])[cols].median()
dif = med.loc["Linux"] - med.loc["Windows"]
dif.to_csv("diferenca_linux_menos_windows.csv")
print("\nMedianas em 100 MB e 1000 MB:")
print(med.loc[(slice(None), [100, 1000]), :].round(2))

print("\nBlocos (de 10) em que cada sistema teve a menor mediana, e blocos com p < 0,05:")
linhas = []
for op in cols:
    win_menor = int((dif[op] > 0).sum())
    sig = 0
    for mb in range(100, 1001, 100):
        w = df[(df.sistema == "Windows") & (df.bloco_MB == mb)][op]
        l = df[(df.sistema == "Linux") & (df.bloco_MB == mb)][op]
        if mannwhitneyu(w, l).pvalue < 0.05: sig += 1
    linhas.append([op, win_menor, 10 - win_menor, sig])
resumo = pd.DataFrame(linhas, columns=["operacao", "blocos_Windows_menor", "blocos_Linux_menor", "blocos_p<0,05"])
resumo.to_csv("resumo_comparacao.csv", index=False)
print(resumo)

# 4) Gráficos: um por operação + total
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, op, nome in zip(axes.flatten(), OPS, NOMES):
    sns.lineplot(data=df, x="bloco_MB", y=op, hue="sistema", estimator="median",
                 errorbar="sd", marker="o", ax=ax)
    ax.set_title(f"Tempo de {nome} (mediana)")
    ax.set_xlabel("Tamanho do bloco (MB)"); ax.set_ylabel("Tempo (ms)")
plt.tight_layout(); plt.savefig("grafico_operacoes.png", dpi=300)

plt.figure(figsize=(9, 5))
sns.lineplot(data=df, x="bloco_MB", y="total_ms", hue="sistema", estimator="median",
             errorbar="sd", marker="o")
plt.title("Tempo total do ciclo de memória (mediana)")
plt.xlabel("Tamanho do bloco (MB)"); plt.ylabel("Tempo total (ms)")
plt.tight_layout(); plt.savefig("grafico_total.png", dpi=300)
print("Gráficos salvos.")