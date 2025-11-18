// Transpositor Musical - Frontend JavaScript
class TranspositorFrontend {
    constructor() {
        this.instruments = {
            violao: { nome: "Violão", afinacao: "E-A-D-G-B-E", tonalidade: "C" },
            guitarra: { nome: "Guitarra", afinacao: "E-A-D-G-B-E", tonalidade: "C" },
            baixo: { nome: "Baixo", afinacao: "E-A-D-G", tonalidade: "C" },
            ukulele: { nome: "Ukulele", afinacao: "G-C-E-A", tonalidade: "C" },
            violino: { nome: "Violino", afinacao: "G-D-A-E", tonalidade: "C" },
            flauta: { nome: "Flauta", afinacao: "C", tonalidade: "C" },
            clarineta: { nome: "Clarineta", afinacao: "D", tonalidade: "Bb" },
            sax_alto: { nome: "Saxofone Alto", afinacao: "Db", tonalidade: "Eb" },
            sax_tenor: { nome: "Saxofone Tenor", afinacao: "Ab", tonalidade: "Bb" },
            trompete: { nome: "Trompete", afinacao: "C", tonalidade: "Bb" },
            trombone: { nome: "Trombone", afinacao: "E", tonalidade: "C" }
            tuba: { nome : "tuba", afinacao: "Bb-F-Eb-C", tonalidade "Bb"}
        };

        this.transposicoes = {
            'C': 0, 'Bb': -2, 'Eb': -9, 'F': -7
        };

        this.notas = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.hideLoading();
        this.updateInstrumentInfo();
    }

    setupEventListeners() {
        // Listeners para instrumentos
        document.getElementById('instrument-origin').addEventListener('change', () => this.updateInstrumentInfo());
        document.getElementById('instrument-destination').addEventListener('change', () => this.updateInstrumentInfo());

        // Listener para transposição automática
        document.getElementById('auto-transpose').addEventListener('change', (e) => {
            if (e.target.checked) {
                this.autoTranspose();
            }
        });

        // Listener para input de cifra com debounce
        let timeout;
        document.getElementById('chord-input').addEventListener('input', (e) => {
            clearTimeout(timeout);
            if (document.getElementById('auto-transpose').checked) {
                timeout = setTimeout(() => this.autoTranspose(), 500);
            }
        });

        // Atalhos de teclado
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 'Enter':
                        e.preventDefault();
                        this.transposeMusic();
                        break;
                    case 'l':
                        e.preventDefault();
                        this.clearText();
                        break;
                    case 'e':
                        e.preventDefault();
                        this.showExamples();
                        break;
                }
            }
        });
    }

    hideLoading() {
        setTimeout(() => {
            document.getElementById('loading').style.display = 'none';
        }, 2000);
    }

    updateInstrumentInfo() {
        const origin = document.getElementById('instrument-origin').value;
        const destination = document.getElementById('instrument-destination').value;

        document.getElementById('origin-info').innerHTML = 
            `<span class="tuning">Afinação: ${this.instruments[origin].afinacao}</span>`;
        
        document.getElementById('destination-info').innerHTML = 
            `<span class="tuning">Afinação: ${this.instruments[destination].afinacao}</span>`;
    }

    async transposeMusic() {
        const chordInput = document.getElementById('chord-input').value.trim();
        if (!chordInput) {
            this.showToast('Digite uma cifra musical!', 'warning');
            return;
        }

        const origin = document.getElementById('instrument-origin').value;
        const destination = document.getElementById('instrument-destination').value;
        const useFlats = document.getElementById('use-flats').checked;
        const showPortuguese = document.getElementById('show-portuguese').checked;

        // Simular processamento
        this.showToast('Processando transposição...', 'info');

        try {
            // Simular delay de processamento
            await new Promise(resolve => setTimeout(resolve, 1000));

            const resultado = this.calcularTransposicao(chordInput, origin, destination, useFlats);
            this.mostrarResultado(resultado, showPortuguese);
            
            this.showToast('Transposição concluída!', 'success');
        } catch (error) {
            this.showToast('Erro na transposição: ' + error.message, 'error');
        }
    }

    calcularTransposicao(cifra, origem, destino, usarBemois) {
        const semitons = this.calcularDiferencaInstrumentos(origem, destino);
        
        // Converter cifra para inglês se estiver em português
        let cifraIngles = this.converterParaIngles(cifra);
        
        // Transpor acordes
        const palavras = cifraIngles.split(/\s+/);
        const resultado = palavras.map(palavra => {
            if (this.eAcorde(palavra)) {
                return this.transporAcorde(palavra, semitons, usarBemois);
            }
            return palavra;
        }).join(' ');

        return resultado;
    }

    converterParaIngles(cifra) {
        const conversoes = {
            'Dó': 'C', 'Ré': 'D', 'Mi': 'E', 'Fá': 'F', 
            'Sol': 'G', 'Lá': 'A', 'Si': 'B',
            'Dóm': 'Cm', 'Rém': 'Dm', 'Mim': 'Em', 'Fám': 'Fm',
            'Solm': 'Gm', 'Lám': 'Am', 'Sim': 'Bm'
        };

        let cifraIngles = cifra;
        for (const [pt, en] of Object.entries(conversoes)) {
            const regex = new RegExp(pt, 'gi');
            cifraIngles = cifraIngles.replace(regex, en);
        }

        return cifraIngles;
    }

    eAcorde(palavra) {
        return /^[A-G][#b]?(m|7|m7|maj7|dim|aug|sus2|sus4|6|9)?(\/[A-G][#b]?)?$/.test(palavra);
    }

    transporAcorde(acorde, semitons, usarBemois) {
        // Encontrar nota base
        const match = acorde.match(/^([A-G][#b]?)/);
        if (!match) return acorde;

        const notaBase = match[1];
        const resto = acorde.slice(notaBase.length);

        try {
            const notaCompleta = notaBase + '4'; // Oitava de referência
            const novaNota = this.transporNota(notaCompleta, semitons, usarBemois);
            const novaNotaBase = novaNota.slice(0, -1); // Remove oitava

            return novaNotaBase + resto;
        } catch (error) {
            return acorde;
        }
    }

    transporNota(nota, semitons, usarBemois) {
        // Implementação simplificada da transposição
        const idx = this.notas.indexOf(nota.slice(0, -1));
        if (idx === -1) return nota;

        const novaIdx = (idx + semitons + 12) % 12;
        let novaNota = this.notas[novaIdx];

        if (usarBemois) {
            const bemols = {'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'};
            novaNota = bemols[novaNota] || novaNota;
        }

        return novaNota + nota.slice(-1);
    }

    calcularDiferencaInstrumentos(origem, destino) {
        const instrOrigem = this.instruments[origem];
        const instrDestino = this.instruments[destino];
        
        const transOrigem = this.transposicoes[instrOrigem.tonalidade] || 0;
        const transDestino = this.transposicoes[instrDestino.tonalidade] || 0;
        
        return transDestino - transOrigem;
    }

    mostrarResultado(resultado, showPortuguese) {
        document.getElementById('results-section').style.display = 'block';
        
        // Cifra transposta
        document.getElementById('transposed-chords').textContent = resultado;
        
        // Explicação em português
        const explicacao = showPortuguese ? this.converterParaPortugues(resultado) : resultado;
        document.getElementById('portuguese-explanation').textContent = explicacao;
        
        // Detalhes
        const origem = document.getElementById('instrument-origin').value;
        const destino = document.getElementById('instrument-destination').value;
        const semitons = this.calcularDiferencaInstrumentos(origem, destino);
        
        document.getElementById('transposition-details').innerHTML = `
            <p><strong>Origem:</strong> ${this.instruments[origem].nome}</p>
            <p><strong>Destino:</strong> ${this.instruments[destino].nome}</p>
            <p><strong>Diferença:</strong> ${semitons} semitons</p>
            <p><strong>Afinação origem:</strong> ${this.instruments[origem].afinacao}</p>
            <p><strong>Afinação destino:</strong> ${this.instruments[destino].afinacao}</p>
        `;

        // Scroll para resultados
        document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
    }

    converterParaPortugues(cifra) {
        const conversoes = {
            'C': 'Dó', 'D': 'Ré', 'E': 'Mi', 'F': 'Fá', 'G': 'Sol', 'A': 'Lá', 'B': 'Si',
            'Cm': 'Dó m', 'Dm': 'Ré m', 'Em': 'Mi m', 'Fm': 'Fá m', 'Gm': 'Sol m', 'Am': 'Lá m', 'Bm': 'Si m',
            'C#': 'Dó#', 'D#': 'Ré#', 'F#': 'Fá#', 'G#': 'Sol#', 'A#': 'Lá#',
            'Db': 'Réb', 'Eb': 'Mib', 'Gb': 'Solb', 'Ab': 'Láb', 'Bb': 'Sib'
        };

        let cifraPortugues = cifra;
        for (const [en, pt] of Object.entries(conversoes)) {
            const regex = new RegExp('\\b' + en + '\\b', 'g');
            cifraPortugues = cifraPortugues.replace(regex, pt);
        }

        return cifraPortugues;
    }

    autoTranspose() {
        const chordInput = document.getElementById('chord-input').value.trim();
        if (chordInput && document.getElementById('auto-transpose').checked) {
            this.transposeMusic();
        }
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = 'toast show';
        
        // Cores por tipo
        const colors = {
            success: '#4cc9f0',
            error: '#f72585',
            warning: '#ffaa00',
            info: '#4361ee'
        };
        
        toast.style.background = colors[type] || colors.info;
        
        setTimeout(() => {
            toast.className = 'toast';
        }, 3000);
    }
}

// Funções Globais
let transpositor;

function addChord(chord) {
    const textarea = document.getElementById('chord-input');
    const current = textarea.value;
    textarea.value = current + (current ? ' ' : '') + chord;
    
    // Disparar evento de input para auto-transpose
    textarea.dispatchEvent(new Event('input'));
}

function clearText() {
    document.getElementById('chord-input').value = '';
    document.getElementById('results-section').style.display = 'none';
    transpositor.showToast('Texto limpo!', 'info');
}

function pasteText() {
    navigator.clipboard.readText().then(text => {
        document.getElementById('chord-input').value = text;
        transpositor.showToast('Texto colado!', 'success');
    }).catch(err => {
        transpositor.showToast('Erro ao colar texto', 'error');
    });
}

function copyResult() {
    const result = document.getElementById('transposed-chords').textContent;
    navigator.clipboard.writeText(result).then(() => {
        transpositor.showToast('Resultado copiado!', 'success');
    });
}

function showExamples() {
    document.getElementById('examples-modal').style.display = 'block';
}

function showHelp() {
    document.getElementById('help-modal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.body.setAttribute('data-theme', newTheme);
    
    // Salvar preferência
    localStorage.setItem('theme', newTheme);
    transpositor.showToast(`Tema ${newTheme === 'dark' ? 'escuro' : 'claro'} ativado`, 'info');
}

function updateOptions() {
    if (document.getElementById('auto-transpose').checked) {
        transpositor.autoTranspose();
    }
}

function loadExample(exampleId) {
    const examples = {
        example1: 'C Cmaj7 C7 F Fm C G Am',
        example2: 'C Am F G',
        example3: 'C G Am F C G F C',
        example4: 'C G Am F',
        example5: 'Am F C G',
        example6: 'A7 D7 E7'
    };
    
    document.getElementById('chord-input').value = examples[exampleId];
    document.getElementById('examples-modal').style.display = 'none';
    
    if (document.getElementById('auto-transpose').checked) {
        transpositor.autoTranspose();
    }
}

function showAbout() {
    alert(`🎵 Transpositor Musical v1.0\n\nDesenvolvido para músicos que precisam transpor cifras entre diferentes instrumentos.\n\nFuncionalidades:\n• Transposição entre 10+ instrumentos\n• Suporte a acordes complexos\n• Interface moderna e responsiva\n• Trabalha 100% no navegador\n• Totalmente gratuito!`);
}

function showShortcuts() {
    alert(`⌨️ Atalhos do Teclado:\n\nCtrl+Enter - Transpor música\nCtrl+L - Limpar texto\nCtrl+E - Mostrar exemplos\n\nDica: Ative "Transposição Automática" para ver resultados instantâneos!`);
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    transpositor = new TranspositorFrontend();
    
    // Carregar tema salvo
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
});

// Fechar modal clicando fora
window.onclick = function(event) {
    const modals = document.getElementsByClassName('modal');
    for (let modal of modals) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }
}