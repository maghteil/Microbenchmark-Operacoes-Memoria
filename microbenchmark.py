import csv
import platform
import time

sistema = platform.system()              # "Windows" ou "Linux"
arquivo_saida = f"logs_{sistema.lower()}.csv"

tamanhos_MB = range(100, 1001, 100)      # 100, 200, ..., 1000
repeticoes = 100

print(f"Sistema: {sistema} | Python: {platform.python_version()}")

with open(arquivo_saida, "w", newline="") as f:
    escritor = csv.writer(f)
    escritor.writerow(["bloco_MB", "teste", "alloc_ms", "write_ms", "read_ms", "free_ms"])

    for mb in tamanhos_MB:
        tamanho = mb * 1024 * 1024
        padrao = b"\xAA" * tamanho       # preparado fora da medição

        for teste in range(1, repeticoes + 1):
            # ALOCAÇÃO
            t0 = time.perf_counter_ns()
            bloco = bytearray(tamanho)
            t1 = time.perf_counter_ns()

            # ESCRITA
            t2 = time.perf_counter_ns()
            bloco[:] = padrao
            t3 = time.perf_counter_ns()

            # LEITURA
            t4 = time.perf_counter_ns()
            leitura = bloco[:]
            t5 = time.perf_counter_ns()

            # LIBERAÇÃO
            t6 = time.perf_counter_ns()
            bloco.clear()
            del bloco
            t7 = time.perf_counter_ns()

            del leitura                  # fora da medição, evita acumular cópias

            escritor.writerow([
                mb, teste,
                round((t1 - t0) / 1_000_000, 6),
                round((t3 - t2) / 1_000_000, 6),
                round((t5 - t4) / 1_000_000, 6),
                round((t7 - t6) / 1_000_000, 6),
            ])

        f.flush()                        # salva o progresso a cada tamanho
        del padrao
        print(f"Bloco de {mb} MB concluído")

print(f"Pronto! Arquivo gerado: {arquivo_saida}")