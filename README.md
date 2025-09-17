# Gui_Translate

## Descrição do Projeto

Este é um projeto de aprendizado com uma interface gráfica (GUI) de tradução. O repositório contém os scripts e notebooks usados para criar o backend e a interface, com o objetivo de praticar o uso de classes e aprimorar as habilidades de desenvolvimento.

O projeto ainda está em desenvolvimento e o código pode conter bugs.

## Estrutura do Projeto

O repositório contém arquivos com propósitos diferentes:

-   **Arquivos do Google Colab (.ipynb):** Localizados na pasta `colab/`, esses notebooks foram criados para serem executados diretamente no Google Colab, onde os modelos de IA e os recursos de computação são otimizados. Eles são a base do projeto.

-   **Scripts Python (.py):** O arquivo `api_gui_translate.py` é uma versão ajustada para ser hospedada como backend. Embora seja funcional, ele foi adaptado a partir do código do Colab, e podem ser necessários ajustes para rodá-lo em ambientes locais.

## Como Rodar o Projeto

Para executar o projeto, siga os passos abaixo:

1.  **Crie e ative o ambiente virtual:**

    -   **Crie o ambiente:**
        ```bash
        python -m venv venv
        ```

    -   **Ative o ambiente:**
        -   No Windows:
            ```bash
            .\venv\Scripts\activate
            ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute o script principal:**
    ```bash
    python seu_arquivo.py
    ```
