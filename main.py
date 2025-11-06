#!/usr/bin/env python3
"""
Sistema de Transposição Musical Offline
Controle totalmente local sem dependências externas
"""

import json
import os
from datetime import datetime

class TranspositorMusical:
    def __init__(self):
        # Notas musicais naturais e acidentadas
        self.notas = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.notas_naturais = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.notas_portugues = {
            'C': 'Dó', 'D': 'Ré', 'E': 'Mi', 'F': 'Fá', 
            'G': 'Sol', 'A': 'Lá', 'B': 'Si',
            'C#': 'Dó#', 'D#': 'Ré#', 'F#': 'Fá#', 'G#': 'Sol#', 'A#': 'Lá#',
            'Db': 'Réb', 'Eb': 'Mib', 'Gb': 'Solb', 'Ab': 'Láb', 'Bb': 'Sib'
        }
        
        # Tipos de acordes suportados
        self.tipos_acordes = {
            '': 'maior',
            'm': 'menor',
            '7': 'sétima',
            'm7': 'menor sétima',
            'maj7': 'sétima maior',
            'dim': 'diminuto',
            'aug': 'aumentado',
            'sus2': 'suspenso 2ª',
            'sus4': 'suspenso 4ª',
            '6': 'sexta',
            '9': 'nona'
        }
        
        self.instrumentos = {
            # Cordas
            "violao": {"nome": "Violão", "afinacao": ["E2", "A2", "D3", "G3", "B3", "E4"], "tonalidade": "C"},
            "guitarra": {"nome": "Guitarra", "afinacao": ["E2", "A2", "D3", "G3", "B3", "E4"], "tonalidade": "C"},
            "baixo": {"nome": "Baixo", "afinacao": ["E1", "A1", "D2", "G2"], "tonalidade": "C"},
            "ukulele_soprano": {"nome": "Ukulele Soprano", "afinacao": ["G4", "C4", "E4", "A4"], "tonalidade": "C"},
            "violino": {"nome": "Violino", "afinacao": ["G3", "D4", "A4", "E5"], "tonalidade": "C"},
            
            # Madeiras
            "flauta_transversal": {"nome": "Flauta Transversal", "afinacao": ["C4"], "tonalidade": "C"},
            "clarineta_sib": {"nome": "Clarineta Sib", "afinacao": ["D3"], "tonalidade": "Bb"},
            "saxofone_alto": {"nome": "Saxofone Alto", "afinacao": ["Db3"], "tonalidade": "Eb"},
            "saxofone_tenor": {"nome": "Saxofone Tenor", "afinacao": ["Ab2"], "tonalidade": "Bb"},
            "oboe": {"nome": "Oboé", "afinacao": ["C4"], "tonalidade": "C"},
            
            # Metais
            "trompete_sib": {"nome": "Trompete Sib", "afinacao": ["C4"], "tonalidade": "Bb"},
            "trompa_fa": {"nome": "Trompa em Fá", "afinacao": ["F2"], "tonalidade": "F"},
            "trombone": {"nome": "Trombone", "afinacao": ["E2"], "tonalidade": "C"},
            "tuba_sib": {"nome": "Tuba Sib", "afinacao": ["Bb1"], "tonalidade": "Bb"},
        }
        
        self.transposicoes = {
            'C': 0,   # Não transpositor
            'Bb': -2, # Soa 1 tom abaixo
            'Eb': -9, # Soa 1 tom e meio abaixo
            'F': -7,  # Soa 5ª justa abaixo
            'A': -3   # Soa 1 tom e meio abaixo
        }

    def nota_para_numero(self, nota):
        """Converte nota para número sequencial"""
        nota = self._converter_bemol_para_sustenido(nota)
        
        # Extrai nome da nota e oitava
        nome_nota = ""
        oitava = ""
        
        for char in nota:
            if char.isdigit() or char == '-':
                oitava += char
            else:
                nome_nota += char
        
        if not oitava:
            raise ValueError(f"Nota inválida: {nota}")
        
        oitava = int(oitava)
        
        try:
            indice_nota = self.notas.index(nome_nota)
        except ValueError:
            raise ValueError(f"Nota inválida: {nome_nota}")
        
        return oitava * 12 + indice_nota

    def _converter_bemol_para_sustenido(self, nota):
        """Converte bemóis para sustenidos equivalentes"""
        conversoes = {
            'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'
        }
        for bemol, sustenido in conversoes.items():
            if bemol in nota:
                return nota.replace(bemol, sustenido)
        return nota

    def _converter_sustenido_para_bemol(self, nota):
        """Converte sustenidos para bemóis equivalentes"""
        conversoes = {
            'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'
        }
        for sustenido, bemol in conversoes.items():
            if sustenido in nota:
                return nota.replace(sustenido, bemol)
        return nota

    def numero_para_nota(self, numero, usar_bemois=False):
        """Converte número sequencial para nota"""
        oitava = numero // 12
        indice_nota = numero % 12
        
        nota = self.notas[indice_nota]
        if usar_bemois:
            nota = self._converter_sustenido_para_bemol(nota)
        
        return f"{nota}{oitava}"

    def converter_nota_portugues(self, nota_ingles):
        """Converte nota do inglês para português"""
        # Remove a oitava se existir
        nota_base = ''.join([c for c in nota_ingles if not c.isdigit() and c != '-'])
        return self.notas_portugues.get(nota_base, nota_ingles)

    def explicar_acorde(self, acorde):
        """Explica a composição de um acorde"""
        if not any(note in acorde for note in self.notas_naturais):
            return None
        
        # Encontra a nota base
        nota_base = ""
        resto = acorde
        for i in range(min(2, len(acorde))):
            if acorde[i] in self.notas_naturais:
                if i + 1 < len(acorde) and acorde[i + 1] in ['#', 'b']:
                    nota_base = acorde[i:i+2]
                    resto = acorde[i+2:]
                else:
                    nota_base = acorde[i]
                    resto = acorde[i+1:]
                break
        
        if not nota_base:
            return None
        
        # Identifica o tipo de acorde
        tipo_acorde = ""
        for tipo in self.tipos_acordes.keys():
            if resto.startswith(tipo):
                tipo_acorde = tipo
                break
        
        explicacao = self.tipos_acordes.get(tipo_acorde, "desconhecido")
        nota_pt = self.converter_nota_portugues(nota_base)
        
        return f"{nota_pt} {explicacao}"

    def transpor_nota(self, nota, semitons, usar_bemois=False):
        """Transpõe uma nota individual"""
        numero = self.nota_para_numero(nota)
        nova_nota_numero = numero + semitons
        
        if nova_nota_numero < 0:
            raise ValueError("Transposição resulta em nota abaixo do limite")
        
        return self.numero_para_nota(nova_nota_numero, usar_bemois)

    def calcular_transposicao_instrumento(self, instrumento_id):
        """Calcula semitons de transposição para instrumento"""
        instrumento = self.instrumentos[instrumento_id]
        tonalidade = instrumento["tonalidade"]
        return self.transposicoes.get(tonalidade, 0)

    def calcular_diferenca_afinacao(self, instrumento_origem_id, instrumento_destino_id):
        """Calcula diferença em semitons entre instrumentos"""
        trans_origem = self.calcular_transposicao_instrumento(instrumento_origem_id)
        trans_destino = self.calcular_transposicao_instrumento(instrumento_destino_id)
        
        # Usa primeira corda/nota como referência
        instr_origem = self.instrumentos[instrumento_origem_id]
        instr_destino = self.instrumentos[instrumento_destino_id]
        
        if instr_origem["afinacao"] and instr_destino["afinacao"]:
            corda_origem = instr_origem["afinacao"][0]
            corda_destino = instr_destino["afinacao"][0]
            
            num_origem = self.nota_para_numero(corda_origem)
            num_destino = self.nota_para_numero(corda_destino)
            
            diferenca_afinacao = num_destino - num_origem
        else:
            diferenca_afinacao = 0
        
        return diferenca_afinacao + (trans_destino - trans_origem)

    def transpor_acorde(self, acorde, semitons, usar_bemois=False):
        """Transpõe um acorde"""
        # Padrão para acordes complexos
        if '/' in acorde:
            partes = acorde.split('/')
            acorde_base = self._transpor_acorde_simples(partes[0], semitons, usar_bemois)
            baixo = self._transpor_acorde_simples(partes[1], semitons, usar_bemois)
            return f"{acorde_base}/{baixo}"
        else:
            return self._transpor_acorde_simples(acorde, semitons, usar_bemois)

    def _transpor_acorde_simples(self, acorde, semitons, usar_bemois):
        """Transpõe um acorde simples (sem baixo)"""
        if not any(note in acorde for note in self.notas_naturais):
            return acorde
        
        # Encontra a nota base do acorde
        nota_base = ""
        resto = acorde
        
        for i in range(min(3, len(acorde))):
            if acorde[i] in self.notas_naturais:
                if i + 1 < len(acorde) and acorde[i + 1] in ['#', 'b']:
                    nota_base = acorde[i:i+2]
                    resto = acorde[i+2:]
                else:
                    nota_base = acorde[i]
                    resto = acorde[i+1:]
                break
        
        if not nota_base:
            return acorde
        
        try:
            # Transpõe a nota base
            nota_completa = f"{nota_base}4"  # Usa oitava 4 como referência
            nova_nota = self.transpor_nota(nota_completa, semitons, usar_bemois)
            nova_nota_base = nova_nota[:-1]  # Remove a oitava
            
            return nova_nota_base + resto
        except:
            return acorde

    def transpor_cifra(self, cifra, instrumento_origem_id, instrumento_destino_id, usar_bemois=False):
        """Transpõe cifra completa entre instrumentos"""
        semitons = self.calcular_diferenca_afinacao(instrumento_origem_id, instrumento_destino_id)
        
        # Divide a cifra em palavras e processa cada uma
        palavras = cifra.split()
        resultado = []
        
        for palavra in palavras:
            # Tenta transpor se parece com um acorde
            if any(note in palavra for note in self.notas_naturais):
                acorde_transposto = self.transpor_acorde(palavra, semitons, usar_bemois)
                resultado.append(acorde_transposto)
            else:
                resultado.append(palavra)
        
        return ' '.join(resultado)

    def listar_instrumentos(self):
        """Lista todos os instrumentos disponíveis"""
        return [
            {"id": id, **info} 
            for id, info in self.instrumentos.items()
        ]

    def mostrar_info_instrumento(self, instrumento_id):
        """Mostra informações do instrumento"""
        if instrumento_id not in self.instrumentos:
            return None
        
        instrumento = self.instrumentos[instrumento_id]
        transposicao = self.calcular_transposicao_instrumento(instrumento_id)
        
        return {
            "nome": instrumento["nome"],
            "tonalidade": instrumento["tonalidade"],
            "afinacao": instrumento["afinacao"],
            "transposicao": transposicao
        }

    def mostrar_escala_natural(self, nota_base="C"):
        """Mostra as 7 notas musicais naturais a partir de uma nota base"""
        try:
            idx_base = self.notas.index(nota_base)
            escala = []
            for i in range(7):
                nota_idx = (idx_base + i) % 12
                escala.append(self.notas[nota_idx])
            return escala
        except:
            return None

    def converter_cifra_portugues(self, cifra):
        """Converte cifra inteira para nomenclatura portuguesa"""
        palavras = cifra.split()
        resultado_pt = []
        
        for palavra in palavras:
            explicacao = self.explicar_acorde(palavra)
            if explicacao:
                resultado_pt.append(explicacao)
            else:
                resultado_pt.append(palavra)
        
        return ' | '.join(resultado_pt)

def menu_principal():
    print("\n" + "="*60)
    print("           🎵 SISTEMA DE TRANSPOSIÇÃO MUSICAL OFFLINE")
    print("="*60)
    print("1. 🎸 Transpor entre instrumentos")
    print("2. 🎹 Transpor por semitons") 
    print("3. 📋 Listar instrumentos")
    print("4. 🔍 Informações do instrumento")
    print("5. 🎼 Transpor nota individual")
    print("6. 🎶 Mostrar escala natural")
    print("7. 🇧🇷 Explicar cifra em português")
    print("8. 🎼 Mostrar todas as notas musicais")
    print("9. 🚪 Sair")
    print("="*60)

def mostrar_notas_musicais():
    """Mostra todas as notas musicais com explicação"""
    print("\n" + "="*50)
    print("           🎼 NOTAS MUSICAIS - 7 NATURAIS")
    print("="*50)
    
    notas_info = [
        ("C", "Dó", "Primeira nota da escala"),
        ("D", "Ré", "Segunda nota da escala"), 
        ("E", "Mi", "Terceira nota da escala"),
        ("F", "Fá", "Quarta nota da escala"),
        ("G", "Sol", "Quinta nota da escala"),
        ("A", "Lá", "Sexta nota da escala"),
        ("B", "Si", "Sétima nota da escala")
    ]
    
    for simbolo, nome, explicacao in notas_info:
        print(f"  {simbolo:<2} = {nome:<4} - {explicacao}")
    
    print("\n🎵 Notas com acidentes:")
    acidentes_info = [
        ("C#/Db", "Dó sustenido / Ré bemol"),
        ("D#/Eb", "Ré sustenido / Mi bemol"), 
        ("F#/Gb", "Fá sustenido / Sol bemol"),
        ("G#/Ab", "Sol sustenido / Lá bemol"),
        ("A#/Bb", "Lá sustenido / Si bemol")
    ]
    
    for notas, explicacao in acidentes_info:
        print(f"  {notas:<8} - {explicacao}")

def main():
    transpositor = TranspositorMusical()
    
    while True:
        menu_principal()
        opcao = input("\n🎹 Digite sua opção: ").strip()
        
        try:
            if opcao == "1":
                print("\n🎷 Instrumentos disponíveis:")
                instrumentos = transpositor.listar_instrumentos()
                for i, instr in enumerate(instrumentos, 1):
                    print(f"{i}. {instr['nome']} ({instr['id']})")
                
                orig_idx = int(input("\n🎯 Número do instrumento de origem: ")) - 1
                dest_idx = int(input("🎯 Número do instrumento de destino: ")) - 1
                
                if 0 <= orig_idx < len(instrumentos) and 0 <= dest_idx < len(instrumentos):
                    instrumento_origem = instrumentos[orig_idx]['id']
                    instrumento_destino = instrumentos[dest_idx]['id']
                    
                    cifra = input("\n🎼 Digite a cifra: ")
                    usar_bemois = input("🎹 Usar bemóis? (s/n): ").lower().startswith('s')
                    
                    resultado = transpositor.transpor_cifra(cifra, instrumento_origem, instrumento_destino, usar_bemois)
                    
                    print(f"\n🎵 Resultado: {resultado}")
                    semitons = transpositor.calcular_diferenca_afinacao(instrumento_origem, instrumento_destino)
                    print(f"🎼 Diferença: {semitons} semitons")
                    
                    # Mostra explicação em português
                    explicacao_pt = transpositor.converter_cifra_portugues(resultado)
                    print(f"🇧🇷 Explicação: {explicacao_pt}")
                else:
                    print("❌ Números inválidos!")
            
            elif opcao == "2":
                cifra = input("\n🎼 Digite a cifra: ")
                semitons = int(input("🎹 Semitons para transpor (+ para cima, - para baixo): "))
                usar_bemois = input("🎵 Usar bemóis? (s/n): ").lower().startswith('s')
                
                resultado = ""
                palavras = cifra.split()
                for palavra in palavras:
                    acorde_transposto = transpositor.transpor_acorde(palavra, semitons, usar_bemois)
                    resultado += acorde_transposto + " "
                
                print(f"\n🎵 Resultado: {resultado.strip()}")
                explicacao_pt = transpositor.converter_cifra_portugues(resultado.strip())
                print(f"🇧🇷 Explicação: {explicacao_pt}")
            
            elif opcao == "3":
                print("\n📋 Instrumentos disponíveis:")
                instrumentos = transpositor.listar_instrumentos()
                for instr in instrumentos:
                    print(f"  🎹 {instr['nome']} - {instr['id']}")
            
            elif opcao == "4":
                instrumento_id = input("\n🔍 Digite o ID do instrumento: ")
                info = transpositor.mostrar_info_instrumento(instrumento_id)
                
                if info:
                    print(f"\n📊 {info['nome']}:")
                    print(f"  🎼 Tonalidade: {info['tonalidade']}")
                    print(f"  🎵 Afinação: {', '.join(info['afinacao'])}")
                    print(f"  🎚️  Transposição: {info['transposicao']} semitons")
                else:
                    print("❌ Instrumento não encontrado!")
            
            elif opcao == "5":
                nota = input("\n🎼 Digite a nota (ex: C4, A#3, Bb5): ")
                semitons = int(input("🎹 Semitons para transpor: "))
                usar_bemois = input("🎵 Usar bemóis? (s/n): ").lower().startswith('s')
                
                resultado = transpositor.transpor_nota(nota, semitons, usar_bemois)
                nota_pt = transpositor.converter_nota_portugues(nota)
                resultado_pt = transpositor.converter_nota_portugues(resultado)
                print(f"\n🎵 {nota} ({nota_pt}) → {resultado} ({resultado_pt})")
                print(f"🎼 {semitons} semitons")
            
            elif opcao == "6":
                nota_base = input("\n🎹 Digite a nota base (ex: C, D, F#): ").upper()
                escala = transpositor.mostrar_escala_natural(nota_base)
                
                if escala:
                    print(f"\n🎼 Escala natural de {nota_base}:")
                    escala_pt = [transpositor.converter_nota_portugues(nota) for nota in escala]
                    print(f"  Notas: {' - '.join(escala)}")
                    print(f"  Nomes: {' - '.join(escala_pt)}")
                else:
                    print("❌ Nota base inválida!")
            
            elif opcao == "7":
                cifra = input("\n🎼 Digite a cifra para explicar: ")
                explicacao = transpositor.converter_cifra_portugues(cifra)
                print(f"\n🇧🇷 Explicação: {explicacao}")
            
            elif opcao == "8":
                mostrar_notas_musicais()
            
            elif opcao == "9":
                print("\n🎶 Obrigado por usar o Transpositor Musical!")
                break
            
            else:
                print("❌ Opção inválida!")
        
        except ValueError as e:
            print(f"❌ Erro: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
        
        input("\n📝 Pressione Enter para continuar...")

if __name__ == "__main__":
    main()