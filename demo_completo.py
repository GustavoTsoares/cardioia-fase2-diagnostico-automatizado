from pathlib import Path
import subprocess
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

BASE = Path(__file__).resolve().parent

print("\n================ CARDIOIA — DEMONSTRAÇÃO COMPLETA ================\n")
print("1) Executando a Parte 1...\n")
subprocess.run([sys.executable, str(BASE / "parte1_extracao.py")], check=True)

print("\n\n2) Treinando o classificador da Parte 2...\n")
dados = pd.read_csv(BASE / "dataset_risco.csv")
X_treino, X_teste, y_treino, y_teste = train_test_split(
    dados["frase"], dados["situacao"],
    test_size=0.25, random_state=1, stratify=dados["situacao"]
)
modelo = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 2),
        sublinear_tf=True
    )),
    ("classificador", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ))
])
modelo.fit(X_treino, y_treino)
pred = modelo.predict(X_teste)
print(f"Acurácia no teste: {accuracy_score(y_teste, pred):.2%}")

print("\n3) Testando duas frases novas:\n")
testes = [
    "Estou com dor forte no peito, suor frio e falta de ar.",
    "Tenho uma dor muscular leve depois do treino e ela já está melhorando."
]
for texto in testes:
    classe = modelo.predict([texto])[0]
    print(f"- {texto}\n  => {classe}\n")

print("AVISO: protótipo acadêmico. Não substitui avaliação médica.")
