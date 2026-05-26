"""
r"/home/andrey/SecLists/Usernames/Names/names-brazil-top100000.txt"
r"/home/andrey/Documentos/usernames_pt.txt"

"""

import enchant
import re
import os

# 1. Configuração do Idioma e Caminhos
# Use "pt_BR" para Português do Brasil ou "pt_PT" para Portugal
try:
    d = enchant.Dict("pt_PT")
except:
    print("Erro: Dicionário não encontrado. Verifique a instalação do PyEnchant.")
    exit()

source_file = r"/home/andrey/SecLists/Usernames/xato-net-10-million-usernames.txt"
output_file = r"/home/andrey/Documentos/usernames_pt.txt"

unique_entries = set()
checked_cache = {}  # Acelera o processo ignorando palavras já validadas

# 2. Carregar o dicionário atual para a memória
# Isso garante que o contador final seja a soma de TUDO (antigo + novo)
if os.path.exists(output_file):
    print(f"Lendo dicionário existente: {output_file}...")
    with open(output_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            content = line.strip()
            # Ignora linhas vazias e o contador anterior
            if content and not content.startswith("TOTAL:"):
                unique_entries.add(content)

# 3. Processar o novo arquivo fonte
if os.path.exists(source_file):
    print(f"Processando novas palavras de: {source_file}...")
    regex_pt = re.compile(r'^([a-zA-ZÀ-ÿ-]+)')

    with open(source_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            clean_line = line.strip()
            if not clean_line:
                continue

            match = regex_pt.match(clean_line)
            if match:
                # Extrai a parte textual e limpa hifens
                pure_word = match.group(1).rstrip('-').lower()

                # CORREÇÃO: Verifica se a string não está vazia antes de validar
                if pure_word:
                    if pure_word not in checked_cache:
                        checked_cache[pure_word] = d.check(pure_word)

                    if checked_cache[pure_word]:
                        unique_entries.add(clean_line)

# 4. Salvar tudo ordenado por ordem alfabética com contador no fim
print("Ordenando e salvando arquivo final...")
final_list = sorted(list(unique_entries))

with open(output_file, "w", encoding="utf-8") as out:
    for item in final_list:
        out.write(item + "\n")

    # O contador reflete o total de entradas únicas no arquivo final
    out.write(f"TOTAL: {len(final_list)}\n")

print("-" * 30)
print(f"CONCLUÍDO!")
print(f"Total de palavras no dicionário: {len(final_list)}")
print("-" * 30)