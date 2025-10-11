# User Manual / Manual do Usuário - Image Overlay Z

<h3 align="center">
  <a href="#english">English</a> • <a href="#português-brasil">Português (Brasil)</a>
</h3>

---

## English

Welcome to the user manual for **Image Overlay Z**! This guide provides a step-by-step walkthrough of how to use the graphical application to apply overlays to your images efficiently.

### Table of Contents

1.  [Introduction](#1-introduction)
2.  [System Requirements](#2-system-requirements)
3.  [Step-by-Step Guide](#3-step-by-step-guide)
    -   [Step 1: Language Selection](#step-1-language-selection)
    -   [Step 2: Select the Overlay Image](#step-2-select-the-overlay-image)
    -   [Step 3: Select the Target Images](#step-3-select-the-target-images)
    -   [Step 4: Select the Output Folder](#step-4-select-the-output-folder)
    -   [Step 5: Configure Options](#step-5-configure-options)
    -   [Step 6: Processing](#step-6-processing)
4.  [Explanation of Options](#4-explanation-of-options)
    -   [Auto-Recolor for Contrast](#auto-recolor-for-contrast)
    -   [Overlay Size](#overlay-size)
    -   [Opacity](#opacity)
    -   [Position](#position)
5.  [Troubleshooting](#5-troubleshooting)

---

### 1. Introduction

**Image Overlay Z** is a graphical tool designed to apply an image overlay to multiple images at once. It simplifies the process with a user-friendly interface, eliminating the need for command-line operations. Its standout feature is the ability to intelligently adjust the overlay's tone to ensure it is always visible, whether the background is light or dark.

### 2. System Requirements

To run the application, you will need:
-   **Python 3.8 or higher**.
-   The following Python libraries: **pillow** and **Numpy**. You can install them with this command:
    ```bash
    pip install pillow numpy
    ```

### 3. Step-by-Step Guide

#### Step 1: Language Selection
When you first run the script, a window will appear asking you to choose your preferred language. Click **"Continue in English"** or **"Continuar em Português Brasileiro"** to proceed.

#### Step 2: Select the Overlay Image
A file dialog will open. Navigate to and select the image file you want to use as your overlay (e.g., your logo). This image should ideally have a transparent background for the best results.

#### Step 3: Select the Target Images
Next, another file dialog will open. Here, you can select one or more images that you want to apply the overlay to. You can select multiple files at once by holding down **Ctrl** (Windows/Linux) or **Cmd** (Mac) while clicking.

#### Step 4: Select the Output Folder
After selecting your images, you will be prompted to choose a folder where the new, processed images will be saved.

#### Step 5: Configure Options
A series of dialog boxes will appear, allowing you to customize how the overlay is applied:
1.  **Auto-recolor for contrast:** You will be asked if you want to automatically adjust the overlay's tone based on the background. **Answering "Yes" is highly recommended.**
2.  **Overlay Size:** Enter a value to set the overlay's height. You can use pixels (e.g., `150`) or a percentage of the target image's height (e.g., `10%`). Leave it blank to use a default size.
3.  **Opacity:** Enter a percentage from 0 to 100 to set the transparency. `100` is fully opaque, while `50` is semi-transparent.
4.  **Position:** Enter where you want the overlay to be placed. Options are: `top left`, `top right`, `bottom left`, or `bottom right`.

#### Step 6: Processing
Once all options are set, a progress window will appear, showing the status as each image is processed. When the process is complete, a success message will be displayed, and the application will close. Your new images will be in the output folder you selected.

### 4. Explanation of Options

#### Auto-Recolor for Contrast
This is the application's most powerful feature. When enabled, it analyzes the area behind the overlay on each image.
-   If the area is **dark**, the overlay is automatically made **lighter**.
-   If the area is **light**, the overlay is automatically made **darker**.
This ensures your overlay is always easy to see.

#### Overlay Size
You can define the size in two ways:
-   **Pixels (e.g., `150`):** Sets a fixed height in pixels.
-   **Percentage (e.g., `10%`):** Makes the overlay's height a percentage of the target image's height. This is great for maintaining a consistent relative size across images of different dimensions.

#### Opacity
This controls how transparent the overlay is. A value of `100` (or `100%`) means it's fully visible, while lower values make it more subtle.

#### Position
You can place the overlay in any of the four corners of the image. If you enter an invalid option or leave it blank, it will default to the bottom right.

### 5. Troubleshooting

-   **Error: "File or directory not found"**
    -   **Solution:** Ensure that the file paths selected for the overlay and target images are correct and that you have permission to save files in the chosen output folder.

-   **Application closes unexpectedly:**
    -   **Solution:** If you close any of the initial file or option dialogs, the application will exit by design. To complete the process, you must provide input for all steps.

For other issues, please open an *issue* on our GitHub repository.

---

## Português (Brasil)

Bem-vindo ao manual do usuário do **Image Overlay Z**! Este guia oferece um passo a passo detalhado de como usar a aplicação gráfica para aplicar sobreposições em suas imagens de forma eficiente.

### Índice

1.  [Introdução](#1-introdução-1)
2.  [Requisitos do Sistema](#2-requisitos-do-sistema-1)
3.  [Guia Passo a Passo](#3-guia-passo-a-passo)
    -   [Passo 1: Seleção de Idioma](#passo-1-seleção-de-idioma)
    -   [Passo 2: Selecione a Imagem de Sobreposição](#passo-2-selecione-a-imagem-de-sobreposição)
    -   [Passo 3: Selecione as Imagens de Destino](#passo-3-selecione-as-imagens-de-destino)
    -   [Passo 4: Selecione a Pasta de Saída](#passo-4-selecione-a-pasta-de-saída)
    -   [Passo 5: Configure as Opções](#passo-5-configure-as-opções)
    -   [Passo 6: Processamento](#passo-6-processamento)
4.  [Explicação das Opções](#4-explicação-das-opções)
    -   [Ajuste de Cor Automático para Contraste](#ajuste-de-cor-automático-para-contraste)
    -   [Tamanho da Sobreposição](#tamanho-da-sobreposição)
    -   [Opacidade](#opacidade)
    -   [Posição](#posição)
5.  [Solução de Problemas](#5-solução-de-problemas)

---

### 1. Introdução

O **Image Overlay Z** é uma ferramenta gráfica projetada para aplicar uma sobreposição de imagem em múltiplos arquivos de uma só vez. Ele simplifica o processo com uma interface amigável, eliminando a necessidade de operações de linha de comando. Sua principal funcionalidade é a capacidade de ajustar inteligentemente o tom da sobreposição para garantir que ela esteja sempre visível, seja o fundo claro ou escuro.

### 2. Requisitos do Sistema

Para executar a aplicação, você precisará de:
-   **Python 3.8 ou superior**.
-   As seguintes bibliotecas Python: **pillow** e **Numpy**. Você pode instalá-las com este comando:
    ```bash
    pip install pillow numpy
    ```

### 3. Guia Passo a Passo

#### Passo 1: Seleção de Idioma
Ao executar o script pela primeira vez, uma janela aparecerá pedindo para você escolher seu idioma de preferência. Clique em **"Continuar em Português Brasileiro"** ou **"Continue in English"** para prosseguir.

#### Passo 2: Selecione a Imagem de Sobreposição
Uma janela de seleção de arquivo será aberta. Navegue e selecione o arquivo de imagem que você deseja usar como sua sobreposição (por exemplo, seu logo). Para melhores resultados, essa imagem deve ter um fundo transparente.

#### Passo 3: Selecione as Imagens de Destino
Em seguida, outra janela de seleção de arquivo será aberta. Aqui, você pode selecionar uma ou mais imagens nas quais deseja aplicar a sobreposição. Você pode selecionar vários arquivos de uma vez segurando **Ctrl** (Windows/Linux) ou **Cmd** (Mac) enquanto clica.

#### Passo 4: Selecione a Pasta de Saída
Após selecionar suas imagens, você será solicitado a escolher uma pasta onde as novas imagens processadas serão salvas.

#### Passo 5: Configure as Opções
Uma série de caixas de diálogo aparecerá, permitindo que você personalize como a sobreposição será aplicada:
1.  **Ajuste de cor para contraste:** Será perguntado se você deseja ajustar automaticamente o tom da sobreposição com base no fundo. **Responder "Sim" é altamente recomendado.**
2.  **Tamanho da Sobreposição:** Digite um valor para definir a altura da sobreposição. Você pode usar pixels (ex: `150`) ou uma porcentagem da altura da imagem de destino (ex: `10%`). Deixe em branco para usar um tamanho padrão.
3.  **Opacidade:** Digite uma porcentagem de 0 a 100 para definir a transparência. `100` é totalmente opaco, enquanto `50` é semitransparente.
4.  **Posição:** Digite onde você deseja que a sobreposição seja posicionada. As opções são: `superior esquerdo`, `superior direito`, `inferior esquerdo` ou `inferior direito`.

#### Passo 6: Processamento
Assim que todas as opções forem definidas, uma janela de progresso aparecerá, mostrando o status enquanto cada imagem é processada. Quando o processo for concluído, uma mensagem de sucesso será exibida, e a aplicação será fechada. Suas novas imagens estarão na pasta de saída que você selecionou.

### 4. Explicação das Opções

#### Ajuste de Cor Automático para Contraste
Esta é a funcionalidade mais poderosa da aplicação. Quando ativada, ela analisa a área atrás da sobreposição em cada imagem.
-   Se a área for **escura**, a sobreposição é automaticamente tornada mais **clara**.
-   Se a área for **clara**, a sobreposição é automaticamente tornada mais **escura**.
Isso garante que sua sobreposição seja sempre fácil de ver.

#### Tamanho da Sobreposição
Você pode definir o tamanho de duas maneiras:
-   **Pixels (ex: `150`):** Define uma altura fixa em pixels.
-   **Porcentagem (ex: `10%`):** Torna a altura da sobreposição uma porcentagem da altura da imagem de destino. Isso é ótimo para manter um tamanho relativo consistente em imagens de diferentes dimensões.

#### Opacidade
Isso controla o quão transparente a sobreposição é. Um valor de `100` (ou `100%`) significa que ela está totalmente visível, enquanto valores mais baixos a tornam mais sutil.

#### Posição
Você pode posicionar a sobreposição em qualquer um dos quatro cantos da imagem. Se você digitar uma opção inválida ou deixar em branco, o padrão será o canto inferior direito.

### 5. Solução de Problemas

-   **Erro: "Arquivo ou diretório não encontrado"**
    -   **Solução:** Certifique-se de que os caminhos dos arquivos selecionados para a sobreposição e as imagens de destino estão corretos e que você tem permissão para salvar arquivos na pasta de saída escolhida.

-   **A aplicação fecha inesperadamente:**
    -   **Solution:** Se você fechar qualquer uma das janelas de seleção de arquivo ou de opções, a aplicação será encerrada. Para concluir o processo, você deve fornecer as informações em todos os passos.

For other issues, please open an *issue* on our GitHub repository.
```
