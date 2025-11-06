#!/usr/bin/env python3
"""
Testes unitários para o Transpositor Musical
Com testes para notas naturais e cifras em português
"""

import sys
import os

# Adiciona o diretório atual ao path para importar o main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import TranspositorMusical

def test_notas_naturais():
    """Testa as 7 notas musicais naturais"""
    print("🎼 Testando as 7 notas musicais naturais...")
    
    transpositor = TranspositorMusical()
    
    # Teste das notas naturais
    notas_naturais = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    nomes_portugues = ['Dó', 'Ré', 'Mi', 'Fá', 'Sol', 'Lá', 'Si']
    
    for i, nota in enumerate(notas_naturais):
        nome_pt = transpositor.converter_nota_portugues(nota)
        esperado = nomes_portugues[i]
        status = "✅" if nome_pt == esperado else "❌"
        print(f"   {status} {nota} = {nome_pt} (esperado: {esperado})")
    
    # Teste de escalas naturais
    print("\n🎹 Testando escalas naturais...")
    escalas_testes = [
        ("C", ['C', 'D', 'E', 'F', 'G', 'A', 'B']),
        ("G", ['G', 'A', 'B', 'C', 'D', 'E', 'F#']),
        ("F", ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'])
    ]
    
    for nota_base, esperado in escalas_testes:
        escala = transpositor.mostrar_escala_natural(nota_base)
        status = "✅" if escala == esperado else "❌"
        print(f"   {status} Escala de {nota_base}: {escala}")

def test_explicacao_acordes():
    """Testa a explicação de acordes em português"""
    print("\n🇧🇷 Testando explicação de acordes em português...")
    
    transpositor = TranspositorMusical()
    
    testes_acordes = [
        ("C", "Dó maior"),
        ("Cm", "Dó menor"), 
        ("C7", "Dó sétima"),
        ("Cm7", "Dó menor sétima"),
        ("Gsus4", "Sol suspenso 4ª"),
        ("Dm", "Ré menor")
    ]
    
    for acorde, esperado in testes_acordes:
        explicacao = transpositor.explicar_acorde(acorde)
        status = "✅" if explicacao == esperado else "❌"
        print(f"   {status} {acorde} = {explicacao} (esperado: {esperado})")

def test_transpositor():
    """Testes básicos do sistema de transposição"""
    print("\n🧪 Iniciando testes do Transpositor Musical...")
    
    transpositor = TranspositorMusical()
    
    # Teste 1: Transposição de notas simples
    print("\n1. Testando transposição de notas...")
    testes_notas = [
        ("C4", 2, "D4"),
        ("A4", -2, "G4"), 
        ("C4", 12, "C5"),  # Oitava acima
        ("E4", -12, "E3"), # Oitava abaixo
    ]
    
    for nota, semitons, esperado in testes_notas:
        resultado = transpositor.transpor_nota(nota, semitons)
        status = "✅" if resultado == esperado else "❌"
        print(f"   {status} {nota} + {semitons} = {resultado} (esperado: {esperado})")
    
    # Teste 2: Transposição de acordes
    print("\n2. Testando transposição de acordes...")
    testes_acordes = [
        ("C", 2, "D"),
        ("Am", 2, "Bm"),
        ("F#7", -1, "F7"),
        ("G/B", 2, "A/C#"),
    ]
    
    for acorde, semitons, esperado in testes_acordes:
        resultado = transpositor.transpor_acorde(acorde, semitons)
        status = "✅" if resultado == esperado else "❌"
        print(f"   {status} {acorde} + {semitons} = {resultado} (esperado: {esperado})")
    
    # Teste 3: Transposição entre instrumentos
    print("\n3. Testando transposição entre instrumentos...")
    try:
        cifra = "C G Am F"
        resultado = transpositor.transpor_cifra(cifra, "violao", "ukulele_soprano")
        print(f"   ✅ Violão → Ukulele: {cifra} → {resultado}")
        
        # Teste com explicação em português
        explicacao = transpositor.converter_cifra_portugues(resultado)
        print(f"   🇧🇷 Explicação: {explicacao}")
    except Exception as e:
        print(f"   ❌ Erro na transposição: {e}")
    
    # Teste 4: Listagem de instrumentos
    print("\n4. Testando listagem de instrumentos...")
    instrumentos = transpositor.listar_instrumentos()
    print(f"   ✅ {len(instrumentos)} instrumentos carregados")
    for instr in instrumentos[:3]:  # Mostra apenas os 3 primeiros
        print(f"      🎹 {instr['nome']}")
    
    print("\n🎉 Todos os testes concluídos!")

def test_exemplos_praticos():
    """Exemplos práticos de uso com notas em português"""
    print("\n🎵 EXEMPLOS PRÁTICOS COM NOTAS EM PORTUGUÊS:")
    
    transpositor = TranspositorMusical()
    
    # Exemplo 1: Música popular com explicação
    print("\n1. Música popular (Violão → Ukulele):")
    cifra = "C G Am F"
    resultado = transpositor.transpor_cifra(cifra, "violao", "ukulele_soprano")
    explicacao_orig = transpositor.converter_cifra_portugues(cifra)
    explicacao_dest = transpositor.converter_cifra_portugues(resultado)
    
    print(f"   Original: {cifra}")
    print(f"   Em português: {explicacao_orig}")
    print(f"   Ukulele: {resultado}") 
    print(f"   Em português: {explicacao_dest}")
    
    # Exemplo 2: Notas individuais
    print("\n2. Conversão de notas individuais:")
    notas_teste = ["C", "D", "E", "F", "G", "A", "B", "C#", "Eb"]
    for nota in notas_teste:
        nota_pt = transpositor.converter_nota_portugues(nota)
        print(f"   {nota} = {nota_pt}")
    
    # Exemplo 3: Escalas
    print("\n3. Escalas naturais:")
    for nota_base in ["C", "G", "F"]:
        escala = transpositor.mostrar_escala_natural(nota_base)
        if escala:
            escala_pt = [transpositor.converter_nota_portugues(n) for n in escala]
            print(f"   Escala de {nota_base}: {' - '.join(escala)}")
            print(f"   Em português: {' - '.join(escala_pt)}")

if __name__ == "__main__":
    test_notas_naturais()
    test_explicacao_acordes() 
    test_transpositor()
    test_exemplos_praticos()