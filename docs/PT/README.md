# CESS-UFF — Avaliação prática com ESP32 e MicroPython

**Language / Idioma:** [English](../../README.md) | [Português](README.md)

Este repositório contém um projeto completo de simulação no Wokwi para uma
avaliação prática envolvendo instrumentação, eletrônica e lógica de programação.
A aplicação utiliza uma placa ESP32, dois LEDs, um botão pulsador normalmente
aberto e um display OLED SSD1306.

## Comportamento do projeto

| Entrada ou tarefa | Saída esperada |
|---|---|
| Tarefa independente do LED vermelho | O GPIO 2 alterna de estado a cada 500 ms |
| Botão solto | O GPIO 17 permanece em nível baixo, o LED verde fica apagado e o OLED mostra `Boa sorte!!` |
| Botão pressionado | O GPIO 17 passa ao nível alto, o LED verde acende e o OLED mostra `Consegui!` |

O botão utiliza o resistor interno de redução (`pull-down`) do ESP32 e um
tratamento de antirrepique por software, não bloqueante, de 30 ms. O OLED é
atualizado apenas na inicialização e após uma transição estável do estado do
botão. Essa estratégia evita tráfego I2C desnecessário e cintilação visível.

## Mapeamento obrigatório dos GPIOs

| Componente | Identificador no Wokwi | Conexão no ESP32 |
|---|---|---:|
| LED vermelho | `red-led` | GPIO 2 |
| LED verde | `green-led` | GPIO 4 |
| Botão pulsador normalmente aberto | `push-button` | GPIO 17, ativo em nível alto |
| Relógio do OLED | `oled-display` / SCL | GPIO 25 |
| Dados do OLED | `oled-display` / SDA | GPIO 16 |

O mapeamento I2C do OLED é uma predefinição do projeto. O GPIO 25 deve ser
utilizado como SCL e o GPIO 16 como SDA. Esse mapeamento não resulta de um
estudo de otimização da interface e não deve ser alterado silenciosamente.

## Placa-alvo

| Campo | Definição |
|---|---|
| Placa | Espressif ESP32-DevKitC V4 |
| Identificador no Wokwi | `board-esp32-devkit-c-v4` |
| Perfil físico recomendado | ESP32-DevKitC V4 com módulo ESP32-WROOM-32E |
| Convenção de pinagem | Números dos GPIOs do ESP32, não posições sequenciais dos conectores |

A denominação genérica “ESP32” não é suficiente para documentar a montagem
física, pois diferentes placas podem apresentar quantidade e disposição de
terminais distintas.

## Estrutura do repositório

```text
cess-uff/
├── main.py                          # ponto de entrada (MicroPython)
├── ssd1306.py                       # driver do OLED SSD1306
├── diagram.json                     # circuito do Wokwi (componentes + conexões)
├── wokwi.toml                       # configuração do simulador Wokwi (VS Code)
├── README.md                        # README principal do repositório (Inglês)
├── LICENSE                          # CC0 1.0 Universal
├── .gitignore
├── docs/
│   ├── EN/                          # documentação em Inglês
│   │   ├── README.md
│   │   ├── technical-specification.md
│   │   ├── component-specifications.md
│   │   └── hardware-reference.md
│   └── PT/                          # documentação em Português
│       ├── README.md
│       ├── technical-specification.md
│       ├── component-specifications.md
│       └── hardware-reference.md
└── tests/                           # scripts de diagnóstico isolado
    ├── README.md
    ├── 01_red_led_basic.py
    ├── 02_red_led_blink.py
    ├── 03_red_led_asyncio.py
    ├── 04_push_button_green_led.py
    ├── 05_oled_basic.py
    └── 06_oled_full_diagnostic.py
```

## Links da documentação em Português

- [Especificação Técnica](technical-specification.md)
- [Especificações dos Componentes](component-specifications.md)
- [Referência de Hardware](hardware-reference.md)

## Endereços do projeto

Substitua os marcadores após publicar o projeto:

- Repositório GitHub: `<GITHUB_REPOSITORY_URL>`
- Simulação do circuito no Wokwi: `<WOKWI_PROJECT_URL>`

São dois entregáveis diferentes. O endereço do GitHub disponibiliza o
código-fonte versionado e a documentação. O endereço do Wokwi abre o circuito
interativo e permite executar a simulação diretamente no navegador.

## Executar no Wokwi pelo navegador

1. Entre no Wokwi e crie um projeto **ESP32 MicroPython**.
2. Substitua o `main.py` gerado pelo `main.py` deste repositório.
3. Adicione o arquivo `ssd1306.py` ao projeto on-line.
4. Substitua o `diagram.json` on-line pelo arquivo deste repositório.
5. Inicie a simulação.
6. Pressione o botão do circuito ou mantenha a tecla **Espaço** pressionada
   enquanto o diagrama estiver com foco.
7. Salve o projeto e use a função de compartilhamento do Wokwi para obter o
   endereço público da plataforma.
8. Insira o endereço na seção **Endereços do projeto** e registre a alteração
   no Git.

O projeto on-line do Wokwi não utiliza `wokwi.toml`. Esse arquivo é empregado
pela extensão do Wokwi no VS Code.

## Executar no VS Code com o Wokwi

### 1. Pré-requisitos

Instale:

- Git;
- Visual Studio Code;
- a extensão oficial **Wokwi Simulator** para VS Code;
- Python 3 e `pip`;
- o utilitário `mpremote` do MicroPython.

Clone o repositório e abra a pasta:

```bash
git clone <GITHUB_REPOSITORY_URL>
cd cess-uff
code .
```

### 2. Adicionar o firmware MicroPython

Baixe um firmware genérico do MicroPython para ESP32, no formato `.bin`, e
salve-o na raiz do repositório com o nome:

```text
firmware.bin
```

O arquivo `firmware.bin` deve permanecer excluído do Git pelo `.gitignore`.
Quando possível, utilize uma versão do `mpremote` compatível com o firmware
selecionado:

```bash
python -m pip install "mpremote==<FIRMWARE_VERSION>"
```

### 3. Iniciar o simulador

Abra `diagram.json` no VS Code e use o botão de execução, ou:

1. pressione `Ctrl+Shift+P`;
2. execute **Wokwi: Start Simulator**.

O `wokwi.toml` carrega `firmware.bin` e disponibiliza a porta serial simulada
por RFC2217 na porta TCP 4000.

### 4. Enviar os arquivos ao sistema MicroPython simulado

Mantenha o simulador em execução. Em outro terminal, execute:

```bash
mpremote connect port:rfc2217://localhost:4000 fs cp ssd1306.py :ssd1306.py
mpremote connect port:rfc2217://localhost:4000 fs cp main.py :main.py
mpremote connect port:rfc2217://localhost:4000 reset
```

O sistema de arquivos MicroPython simulado não é persistente entre sessões.
Repita o envio dos arquivos após iniciar uma nova sessão do simulador.

## Publicar no GitHub

Depois de criar um repositório vazio no GitHub:

```bash
git init
git add .
git commit -m "Create ESP32 MicroPython Wokwi assessment project"
git branch -M main
git remote add origin <GITHUB_REPOSITORY_URL>
git push -u origin main
```

Utilize mensagens de confirmação de alteração claras ao incorporar revisões ou
comentários complementares de outros projetistas.

## Resumo das decisões de projeto

- O Wokwi foi adotado no lugar do Tinkercad porque oferece suporte nativo ao
  ESP32, ao arquivo `main.py` em MicroPython, ao OLED SSD1306, ao circuito
  definido em `diagram.json` e ao compartilhamento da simulação.
- A aplicação utiliza exclusivamente tarefas cooperativas com `asyncio`.
  Atrasos bloqueantes com `time.sleep()` e um superlaço temporizado manualmente
  foram rejeitados para melhorar a separação de responsabilidades e a
  escalabilidade.
- O LED vermelho alterna de estado a cada 500 ms sem impedir a leitura do botão
  ou a atualização do OLED.
- O botão usa `Pin.PULL_DOWN`; não há resistor externo de redução nem filtro RC.
- O antirrepique é realizado por software durante 30 ms.
- O OLED é atualizado por evento, e não continuamente.
- GPIO 25 como SCL e GPIO 16 como SDA são atribuições predefinidas.
- A placa virtual é a ESP32-DevKitC V4 oficial da Espressif.

Consulte os arquivos em [`docs/PT/`](technical-specification.md) para requisitos, decisões, restrições elétricas,
identificação dos componentes e plano de validação.

## Licença

O projeto é dedicado ao domínio público sob a licença **CC0 1.0 Universal**.
Consulte o arquivo [`LICENSE`](../../LICENSE).

## Referências oficiais

- Wokwi: <https://docs.wokwi.com/>
- Formato `diagram.json`: <https://docs.wokwi.com/diagram-format>
- MicroPython no Wokwi para VS Code:
  <https://docs.wokwi.com/vscode/vscode-micropython>
- Configuração de projetos Wokwi:
  <https://docs.wokwi.com/vscode/project-config>
- Firmware MicroPython para ESP32:
  <https://micropython.org/download/ESP32_GENERIC/>
