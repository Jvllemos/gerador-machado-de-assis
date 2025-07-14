# gerador-machado-de-assis
Projeto acadêmico que utiliza Processamento de Linguagem Natural para criar textos inéditos no estilo machadiano.

# Gerador de Textos no Estilo de Machado de Assis

Este projeto foi desenvolvido como um trabalho para a disciplina de Algoritmos e Lógica de Programação do curso de Engenharia de Controle e Automação.

O objetivo é um programa que "aprende" o estilo de escrita de Machado de Assis a partir de suas obras e, em seguida, gera textos inéditos que imitam esse mesmo estilo.

---

## ✒️ Sobre o Projeto

Imagine alimentar um computador com dezenas de livros de um dos maiores escritores da língua portuguesa e depois pedir a ele: "Agora, escreva algo novo, mas com a alma de Machado". É exatamente isso que este projeto faz.

Ele não copia e cola trechos, mas sim constrói frases do zero, palavra por palavra, tentando seguir a mesma cadência, vocabulário e estrutura que Machado de Assis usava em clássicos como "Dom Casmurro" e "Memórias Póstumas de Brás Cubas".

### Exemplo de Texto Gerado

> “A alma dos outros é um mistério que a nossa não penetra, e a vida, meus amigos, não passa de uma série de observações irônicas sobre a vaidade humana. Não era o amor, mas a falta dele que o fazia suspirar. Cada época tem os seus velhos, como cada noite tem a sua lua; era a única filosofia que consolava o coração daquele homem, que via no espelho não um rosto, mas um argumento.”

---

## ⚙️ Como Funciona (De Forma Simples)

Para conseguir imitar o autor, o programa segue três passos principais:

1.  **Leitura e Aprendizado:** Primeiro, o código lê uma vasta coleção de obras de Machado de Assis. Ele analisa as sequências de palavras para entender quais palavras o autor costumava usar depois de outras. Por exemplo, depois da expressão "Os olhos de Capitu...", quais eram as palavras mais prováveis?

2.  **Construção da Memória:** Com base nessa análise, ele cria um grande "mapa mental" (tecnicamente um dicionário de N-gramas) que associa sequências de palavras com suas possíveis continuações, guardando as probabilidades de cada uma.

3.  **Criação do Texto:** O programa escolhe um ponto de partida aleatório e começa a escrever. A cada passo, ele olha para as últimas palavras que escreveu, consulta seu "mapa mental" e escolhe a próxima palavra, tentando sempre tomar as decisões que o próprio Machado tomaria. Ao final, ele ainda faz ajustes para garantir que as frases comecem com letra maiúscula.

---

## 🚀 Como Executar o Projeto

Se você quiser ver a mágica acontecer no seu próprio computador, siga os passos abaixo.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
    cd SEU_REPOSITORIO
    ```

2.  **Instale as dependências necessárias:**
    O projeto usa a biblioteca `spaCy` para processamento de linguagem.
    ```bash
    pip install spacy requests
    ```

3.  **Baixe o modelo de língua portuguesa:**
    ```bash
    python -m spacy download pt_core_news_sm
    ```

4.  **Execute o script principal:**
    ```bash
    python nome_do_seu_arquivo.py
    ```
    Ao final, um arquivo chamado `texto_gerado_final_otimizado.txt` será criado com o texto inédito.

### Análise e Melhorias

Durante o desenvolvimento, diversas abordagens foram testadas para melhorar a qualidade do texto gerado, como o uso de *lematização* (para entender a conjugação de verbos), *stemming* (para simplificar as palavras à sua raiz) e o cálculo de *perplexidade* para encontrar o tamanho ideal da "memória" do nosso robô-escritor. Após testes, o modelo de **Quadrigrama (N=4)** foi o que apresentou os resultados mais coesos e interessantes.

---

## 👨‍💻 Autores

* João Victor Barbosa
* João Vitor Lemos (@Jvllemos)
* Bruno Ramos (@bruno-hessmann)
