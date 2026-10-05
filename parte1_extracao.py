from pathlib import Path
import csv
import re
import unicodedata
from collections import Counter, defaultdict

BASE = Path(__file__).resolve().parent

def normalizar(texto: str) -> str:
    """Converte para minúsculas, remove acentos e normaliza espaços."""
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    return re.sub(r"\s+", " ", texto).strip()

def carregar_mapa(caminho):
    regras = []
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        for linha in csv.DictReader(f):
            regras.append(linha)
    return regras

def diagnosticar(frase, regras):
    texto = normalizar(frase)
    pontuacao = Counter()
    encontrados = defaultdict(list)

    for regra in regras:
        doenca = regra["doenca_associada"]
        for coluna in ("sintoma_1", "sintoma_2"):
            sintoma = regra[coluna].strip()
            if sintoma and normalizar(sintoma) in texto:
                pontuacao[doenca] += 1
                encontrados[doenca].append(sintoma)

    if not pontuacao:
        return "Não identificado", []

    doenca, _ = pontuacao.most_common(1)[0]
    # remove duplicatas mantendo ordem
    sintomas = list(dict.fromkeys(encontrados[doenca]))
    return doenca, sintomas

def main():
    regras = carregar_mapa(BASE / "mapa_conhecimento.csv")
    frases = [
        linha.strip()
        for linha in (BASE / "frases_sintomas.txt").read_text(encoding="utf-8").splitlines()
        if linha.strip()
    ]

    resultados = []
    print("=" * 78)
    print("CARDIOIA — EXTRAÇÃO DE SINTOMAS E DIAGNÓSTICO ASSISTIDO (SIMULAÇÃO)")
    print("=" * 78)

    for i, frase in enumerate(frases, start=1):
        diagnostico, sintomas = diagnosticar(frase, regras)
        resultados.append([i, frase, "; ".join(sintomas), diagnostico])
        print(f"\nPaciente {i}")
        print(f"Relato: {frase}")
        print(f"Sintomas identificados: {', '.join(sintomas) if sintomas else 'nenhum'}")
        print(f"Diagnóstico sugerido: {diagnostico}")

    with open(BASE / "resultados_parte1.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["paciente", "frase", "sintomas_identificados", "diagnostico_sugerido"])
        w.writerows(resultados)

    print("\nArquivo 'resultados_parte1.csv' gerado com sucesso.")
    print("\nAVISO: projeto acadêmico e demonstrativo; não substitui avaliação médica.")

if __name__ == "__main__":
    main()
