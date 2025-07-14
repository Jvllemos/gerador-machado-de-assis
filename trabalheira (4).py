import os
from os.path import basename, exists
import string
import random
import re
import spacy
import requests

#Alunos: João Victor Barbosa, Joao Vitor Lemos, Bruno 
#pip install spacy no terminal 
#python -m spacy download pt_core_news_sm

# --- ETAPA 0: CONFIGURAÇÃO E CARREGAMENTO DE MODELOS ---
nlp = spacy.load("pt_core_news_sm")

# --- FUNÇÕES DE PRÉ-PROCESSAMENTO ---

def limpar_texto_original(caminho_arquivo):
    """Lê um arquivo, remove cabeçalhos/rodapés e retorna o conteúdo limpo como uma string."""
    with open(caminho_arquivo, 'r', encoding='utf-8-sig') as reader:
        linhas = reader.readlines()
    if not linhas: return ""
    indices_publicado = [i for i, linha in enumerate(linhas) if linha.strip().lower().startswith('publicado originalmente')]
    inicio_texto = indices_publicado[0] + 1 if indices_publicado else 0
    fim_texto = len(linhas)
    if inicio_texto >= fim_texto: return "".join(linhas)
    return "".join(linhas[inicio_texto:fim_texto])
def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve

        local, _ = urlretrieve(url, filename)
        print("Downloaded " + str(local))
    return filename

arquivos_machado = [
        "almada.txt", "americanas.txt", "aoAcaso.txt", "aquarelas.txt", "aventalLuva.txt", 
        "badaladas.txt", "balas.txt", "bonsDias.txt", "bote.txt", "caminhoProtocolo.txt", 
        "cantosFantasias.txt", "cartaBispoRJ.txt", "cartaImprensa.txt", "cartasFluminenses.txt", 
        "casaVelha.txt", "castroAlves.txt", "cenasVida.txt", "cherchez.txt", "colombo.txt", 
        "comentariosSemana.txt", "contituinteSombraLuz.txt", "contosFluminenses.txt", 
        "contosSeletos.txt", "crisalidas.txt", "criticaTeatral.txt", "cronicasFuturo.txt", 
        "cultoDever.txt", "desencantos.txt", "deuses.txt", "diarioRJ.txt", 
        "discursosAcademia.txt", "dispersas.txt", "domCasmurro.txt", "drSemana.txt", "ea.txt", 
        "eduardo.txt", "entre92-94.txt", "esau.txt", "estatua.txt", "fagundes.txt", "falenas.txt", 
        "floresFrutos.txt", "forcas.txt", "franciscoOtaviano.txt", "futuro.txt", "garrett.txt", 
        "gazeta.txt", "goncalvesDias.txt", "guarani.txt", "guilhermeMalta.txt", 
        "harmoniasErrantes.txt", "helena.txt", "henrique.txt", "henriqueChaves.txt", 
        "henriquieta.txt", "historia15dias.txt", "historia30dias.txt", "historiasMeiaNoite.txt", 
        "historiasSemData.txt", "iaia.txt", "idealCritico.txt", "ideiasTeatro.txt", "imortais.txt",
        "inspiracoesClaustro.txt", "instintoNacionalidade.txt", "iracema.txt", "joaquim.txt", 
        "jornalLivro.txt", "joseAlencar.txt", "licaoBotanica.txt", "lira20Anos.txt", "mae.txt", 
        "magalhaes.txt", "maoLuva.txt", "memorial-de-aires.txt", "memoriasBras.txt", 
        "meridionais.txt", "miragens.txt", "naoConsultesMedico.txt", "nevoasMatutinas.txt", 
        "notasSemanais.txt", "novaGeracao.txt", "ocidentais.txt", "oliveiraLimna.txt", 
        "oliverTwist.txt", "paginasRecolhidas.txt", "paixao.txt", "papeisAvulsos.txt", 
        "pareceresConservatorioDramatico.txt", "passadoPresenteFuturo.txt", "pedroLuis.txt", 
        "peregrinacao.txt", "primoBasilio.txt", "procelarias.txt", "proposito.txt", 
        "quaseMinistros.txt", "quedaMulheres.txt", "quincas.txt", "reforma.txt", "reliquias.txt", 
        "ressurreicao.txt", "revelacoes.txt", "revistaDramatica.txt", "revistaTeatros.txt", 
        "secretariaAgricultura.txt", "semana.txt", "sinfonias.txt", "suplicio.txt", 
        "suplicioMulher.txt", "tiposQuadros.txt", "trabalhadoresMar.txt", "tuAmor.txt", 
        "variasHistorias.txt", "velhoSenado.txt", "vicondeCastilho.txt"
    ]

SEU_NOME_DE_USUARIO_GITHUB = "Jvllemos" # Seu nome de usuário no GitHub
NOME_DO_SEU_REPOSITORIO = "livros-machado" 
url_base = f'https://raw.githubusercontent.com/Jvllemos/livros-machado/refs/heads/main/'
pasta_livros = 'livros_machado'

if not os.path.exists(pasta_livros):
    os.makedirs(pasta_livros)
for nome_arquivo in arquivos_machado:
    url_completa = url_base + nome_arquivo
    caminho_salvar = os.path.join(pasta_livros, nome_arquivo)

    resposta = requests.get(url_completa)
    resposta.raise_for_status() 

    with open(caminho_salvar, 'wb') as arquivo:
        arquivo.write(resposta.content)
        
    print(f"[OK] Baixado do seu GitHub: {nome_arquivo}")
 # ------------- PRINCIPAL -----------------------------
def rodar_projeto_completo(tamanho_texto=1000):
    
    # ETAPA 1: LEITURA E PRÉ-PROCESSAMENTO EM MEMÓRIA
    
    texto_completo = ""
    pasta_livros = 'livros_machado'
    print("Iniciando leitura e pré-processamento dos livros...")
    for nome_arquivo in arquivos_machado:
        caminho_original = os.path.join(pasta_livros, nome_arquivo)
        if os.path.exists(caminho_original):
            conteudo_limpo = limpar_texto_original(caminho_original)
            texto_completo += conteudo_limpo.replace('\n', ' ') + " "
    print("Leitura e pré-processamento concluídos.")

    # ETAPA 2: PROCESSAMENTO COM SPACY SEM LEMATIZAÇÃO
    print("Iniciando processamento com spaCy (sem lematização)...")
    texto_processado = texto_completo.replace('"', '') # Remove aspas
    texto_processado = re.sub(r'\s+', ' ', texto_completo) # Limpa espaços extras
    
    lista_de_palavras = []
    tamanho_lote = 1000000 
    for i in range(0, len(texto_processado), tamanho_lote):
        lote_texto = texto_processado[i:i + tamanho_lote]
        print(f"  - Processando lote de {len(lote_texto)} caracteres...")
        doc = nlp(lote_texto)
        
        # Lógica para usar a palavra real (token.text)
        tokens_do_lote = []
        for token in doc:
            if not token.is_space:
                tokens_do_lote.append(token.text.lower())
        
        lista_de_palavras.extend(tokens_do_lote)
    print(f"Processamento concluído. Total de tokens: {len(lista_de_palavras)}")

    # ETAPA 3: CONSTRUÇÃO DO CÉREBRO
    N_GRAM_SIZE = 4
    CONTEXT_SIZE = N_GRAM_SIZE - 1
    
    print(f"Iniciando a construção do cérebro (dicionário de {N_GRAM_SIZE}-grams)...")
    mapa_sucessores = {}
    for i in range(len(lista_de_palavras) - CONTEXT_SIZE):
        contexto = tuple(lista_de_palavras[i : i + CONTEXT_SIZE])
        proxima_palavra = lista_de_palavras[i + CONTEXT_SIZE]
        
        if contexto not in mapa_sucessores:
            mapa_sucessores[contexto] = {}
        
        mapa_sucessores[contexto][proxima_palavra] = mapa_sucessores[contexto].get(proxima_palavra, 0) + 1
        
    print(f"Cérebro construído. Total de chaves únicas: {len(mapa_sucessores)}")

    # ETAPA 4: GERAÇÃO DE TEXTO
    print(f"\nGerando texto com {tamanho_texto} palavras...")
    if not mapa_sucessores: return "O cérebro está vazio."

    #pequeno método para evitar pontuação no início do Texto
    chaves_iniciais = list(mapa_sucessores.keys())
    chaves_validas_para_inicio = [
        chave for chave in chaves_iniciais 
        if chave[0] not in string.punctuation
    ]
    if chaves_validas_para_inicio:
        contexto_atual = random.choice(chaves_validas_para_inicio)
    else:
        contexto_atual = random.choice(chaves_iniciais) 
    #volta à geração normal de texto 

    texto_gerado = list(contexto_atual)

    for i in range(tamanho_texto - CONTEXT_SIZE):
        sucessores = mapa_sucessores.get(contexto_atual)
        
        if not sucessores:
            contexto_atual = random.choice(chaves_iniciais)
            continue
        
        proximas_palavras = list(sucessores.keys())
        pesos = list(sucessores.values())
        
        proxima_palavra_escolhida = random.choices(proximas_palavras, weights=pesos, k=1)[0]
        texto_gerado.append(proxima_palavra_escolhida)
        contexto_atual = tuple(texto_gerado[-CONTEXT_SIZE:])
        
    texto_final = ""
    for i, palavra in enumerate(texto_gerado):
        if i == 0:
            texto_final += palavra.capitalize()
        elif palavra in string.punctuation:
            texto_final += palavra
        else:
            texto_final += " " + palavra
            
    return texto_final

def capitalizar_frases(texto):
    """
    Capitaliza a primeira letra do texto e a primeira letra após cada ponto final,
    ponto de interrogação ou ponto de exclamação.
    """
    if not texto:
        return ""

    resultado_lista = list(texto)  
    capitalizar_proxima = True  # Começamos com True para capitalizar a primeira letra do texto

    for i, char in enumerate(resultado_lista):
        # Se a bandeira for True e o caractere atual for uma letra...
        if capitalizar_proxima and char.isalpha():
            resultado_lista[i] = char.upper()
            capitalizar_proxima = False  # Desativa a bandeira após capitalizar

        # Se encontrarmos um ponto final, ativamos a bandeira para a próxima letra
        elif char in '.?!':
            capitalizar_proxima = True

    retornado =  "".join(resultado_lista)
    if retornado.strip() and retornado.strip()[-1] not in '.?!':
        retornado += '.'
    return retornado

# --- BLOCO DE EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    texto_no_final = rodar_projeto_completo(tamanho_texto=1000)
    
    print("\n--- TEXTO GERADO (VERSÃO OTIMIZADA) ---")
    texto_final_correto = capitalizar_frases(texto_no_final)
    print(texto_final_correto)
    
    # Salva o resultado final no arquivo
    with open("texto_gerado_final_otimizado.txt", 'w', encoding='utf-8') as f:
        f.write(texto_final_correto)
    print("\nTexto final salvo em 'texto_gerado_final_otimizado.txt'")



    # """Respostas e depósito de código """

    # USO DA CONJUGAÇÃO DE VERBOS USANDO LEMATIZAÇÃO:

        #  # ETAPA 4: GERAÇÃO COM FILTRO DE SINTAXE
        # print(f"\nGerando texto com {tamanho_texto} palavras e filtro de sintaxe...")
        # if not mapa_sucessores: return "O cérebro está vazio."
        
        # chaves_iniciais = list(mapa_sucessores.keys())
        # quadrigrama_atual = random.choice(chaves_iniciais)
        # texto_gerado = list(quadrigrama_atual)

        # for i in range(tamanho_texto - 3):
        #     sucessores = mapa_sucessores.get(quadrigrama_atual)
        #     if not sucessores:
        #         quadrigrama_atual = random.choice(chaves_iniciais)
        #         continue
            
        #     palavra_anterior = quadrigrama_atual[-1]
        #     info_anterior = obter_info_gramatical(palavra_anterior, nlp)
            
        #     candidatos_validos = {}
        #     # Aplica o filtro de concordância de gênero
        #     if info_anterior and info_anterior["pos"] == "DET" and info_anterior["gender"]:
        #         genero_artigo = info_anterior["gender"][0]
        #         for palavra, peso in sucessores.items():
        #             info_candidato = obter_info_gramatical(palavra, nlp)
        #             # Permite a palavra se ela concordar com o gênero ou se não for um substantivo
        #             if not info_candidato or info_candidato["pos"] != "NOUN" or not info_candidato["gender"] or info_candidato["gender"][0] == genero_artigo:
        #                 candidatos_validos[palavra] = peso
        #     else:
        #         candidatos_validos = sucessores

        #     # Se o filtro removeu todas as opções, usa as originais para não travar
        #     if not candidatos_validos:
        #         candidatos_validos = sucessores

        #     proximas_palavras = list(candidatos_validos.keys())
        #     pesos = list(candidatos_validos.values())
            
        #     if not proximas_palavras: # Se mesmo assim não houver candidatos, reinicia
        #         quadrigrama_atual = random.choice(chaves_iniciais)
        #         continue

        #     proxima_palavra_escolhida_lema = random.choices(proximas_palavras, weights=pesos, k=1)[0]
        #     palavra_anterior_no_texto = texto_gerado[-1]
        #     proxima_palavra_escolhida = conjugar_verbo_simples(proxima_palavra_escolhida_lema, palavra_anterior_no_texto, nlp)
        #     texto_gerado.append(proxima_palavra_escolhida)
        #     quadrigrama_atual = (quadrigrama_atual[1], quadrigrama_atual[2], quadrigrama_atual[3], proxima_palavra_escolhida)
            
        # return ' '.join(texto_gerado)

    # USO DE PERPLEXIDADE PARA DETERMINAR O N: 
    # import numpy as np
    # from collections import defaultdict, Counter
    # import os
    # import re
    # import random
    # import spacy

    # # === 1. Carregamento do modelo spaCy ===
    # nlp = spacy.load("pt_core_news_sm")

    # # === 2. Limpeza e leitura dos arquivos ===
    # def limpar_texto_original(caminho_arquivo):
    #     try:
    #         with open(caminho_arquivo, 'r', encoding='utf-8-sig') as reader:
    #             linhas = reader.readlines()
    #         if not linhas:
    #             return ""
    #         indices_publicado = [i for i, linha in enumerate(linhas) if linha.strip().lower().startswith('publicado originalmente')]
    #         inicio = indices_publicado[0] + 1 if indices_publicado else 0
    #         return "".join(linhas[inicio:])
    #     except:
    #         return ""

    # pasta_livros = 'livros_machado'
    # arquivos = [f for f in os.listdir(pasta_livros) if f.endswith('.txt')]
    # texto = ""
    # for nome in arquivos:
    #     caminho = os.path.join(pasta_livros, nome)
    #     texto += limpar_texto_original(caminho).replace('\n', ' ') + " "

    # # === 3. Pré-processamento ===
    # texto = texto.lower().replace("'", "")
    # texto = re.sub(r'\s+', ' ', texto)
    # tokens = []
    # tamanho_lote = 500000
    # for i in range(0, len(texto), tamanho_lote):
    #     doc = nlp(texto[i:i+tamanho_lote])
    #     tokens.extend([t.text.lower() for t in doc if not t.is_punct and not t.is_space and not t.like_num])

    # # === 4. Funções de avaliação ===
    # def gerar_texto(model, n, tamanho=40, contexto_inicial=None):
    #     if not contexto_inicial:
    #         contexto_inicial = random.choice(list(model.keys()))
    #     contexto = list(contexto_inicial)
    #     resultado = list(contexto)

    #     for _ in range(tamanho - len(contexto)):
    #         contexto_tuple = tuple(contexto)
    #         if contexto_tuple in model:
    #             proximas = model[contexto_tuple]
    #             total = sum(proximas.values())
    #             palavras = list(proximas.keys())
    #             pesos = [proximas[p] / total for p in palavras]
    #             proxima = random.choices(palavras, weights=pesos, k=1)[0]
    #         else:
    #             proxima = random.choice(random.choice(list(model.values())).keys())
    #         resultado.append(proxima)
    #         contexto = resultado[-(n - 1):]
    #     return ' '.join(resultado)

    # def avaliar_e_gerar(tokens, n):
    #     split_index = int(len(tokens) * 0.8)
    #     train, test = tokens[:split_index], tokens[split_index:]
    #     model = defaultdict(Counter)
    #     contexto_len = n - 1

    #     for i in range(len(train) - contexto_len):
    #         contexto = tuple(train[i:i+contexto_len])
    #         proxima = train[i + contexto_len]
    #         model[contexto][proxima] += 1

    #     vocab = set(train)
    #     V = len(vocab)
    #     log_prob = 0.0
    #     N = 0

    #     for i in range(len(test) - contexto_len):
    #         contexto = tuple(test[i:i+contexto_len])
    #         proxima = test[i + contexto_len]
    #         count_context = sum(model[contexto].values()) if contexto in model else 0
    #         count_ngram = model[contexto][proxima] if contexto in model else 0
    #         prob = (count_ngram + 1) / (count_context + V)
    #         log_prob += np.log2(prob)
    #         N += 1

    #     perplexidade = np.power(2, - (1/N) * log_prob) if N > 0 else float('inf')
    #     texto_gerado = gerar_texto(model, n=n)
    #     return perplexidade, texto_gerado

    # for n in [2, 7]:
    #     ppl, texto = avaliar_e_gerar(tokens, n)
    #     print(f"\n=== n = {n} ===")
    #     print(f"Perplexidade: {ppl:.2f}")
    #     print(f"Texto gerado:\n{texto}\n")

# EXEMPLO DE ADOÇÃO DE STEMMING:
    # from nltk.stem import RSLPStemmer
    # stemmer = RSLPStemmer()

    # # Dentro do  loop de processamento do spaCy na ETAPA 2...
    #  (...)
    # tokens_do_lote = []
    # for token in doc:
    #     if not token.is_space:
    #         # Em vez de pegar o lema ou o texto, pegaríamos o radical
    #         palavra_processada = stemmer.stem(token.text.lower())
    #         tokens_do_lote.append(palavra_processada)
    #  (...)

    # N-GRAMAS E SUA ANÁLISE:
    # pelo calculo da perplexidade (código acima comentado) chegamos à conclusão de que 
    # os numéros que melhor atendem são 2, 3, 4 (os demais apresentam uma perplexidade muito elevada)
    # Contudo, sabendo que perplexidade não indica necessariamente melhor compreensão do texto
    # testamos as opções por meio de filtros de IA e leitores humanos e chegamos à conclusão 
    #de que o melhor N = 4 (quadrigrama)