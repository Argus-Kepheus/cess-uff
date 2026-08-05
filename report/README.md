# Relatório LaTeX

Esta pasta contém o relatório técnico resumido do projeto CESS-UFF / SGIMP.

## Estrutura

```text
report/
├── relatorio.tex
├── relatorio.pdf
├── build.ps1
├── README.md
└── figures/
    └── circuito-wokwi.png
```

## Compilação automatizada (PowerShell)

A partir da pasta `report/` (ou de qualquer lugar — o script sempre opera
na sua própria pasta):

```powershell
.\build.ps1
```

Isso compila `relatorio.tex` em `relatorio.pdf` e remove automaticamente
os arquivos temporários gerados (`.aux`, `.log`, `.out`, `.toc`, `.fls`,
`.fdb_latexmk`, `.synctex.gz`, etc.) ao final. `relatorio.pdf` nunca é
apagado.

Usa `latexmk -lualatex` quando disponível (resolve sozinho quantas
passagens são necessárias); se `latexmk` não estiver instalado, ou falhar
por falta do interpretador `perl` (comum em instalações MiKTeX sem o
componente Perl), o script cai automaticamente para duas passagens
manuais de `lualatex`, que é o suficiente para este documento.

Outras opções:

```powershell
.\build.ps1 -Clean       # só remove os temporários, sem compilar
.\build.ps1 -KeepTemp    # compila mas mantém os temporários (útil para depurar o .log)
.\build.ps1 -Open        # compila e abre o PDF resultante ao final
```

Se a compilação falhar, o script preserva os arquivos temporários (mesmo
sem `-KeepTemp`) para permitir inspecionar `relatorio.log`.

## Compilação no TeXstudio

1. Abra `relatorio.tex` no TeXstudio.
2. Em **Opções > Configurar TeXstudio > Compilação**, selecione **LuaLaTeX** como compilador padrão.
3. Compile o documento duas vezes para atualizar o sumário, as referências internas e o número total de páginas.

O arquivo também contém a diretiva:

```tex
% !TeX program = lualatex
```

Em instalações nas quais o TeXstudio respeita diretivas mágicas, essa linha já seleciona o compilador correto.

## Campo a revisar

Antes da entrega, substitua no preâmbulo:

```tex
\newcommand{\CandidateName}{\textit{preencher antes da entrega}}
```

pelo nome do candidato.
