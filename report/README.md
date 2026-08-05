# Relatório LaTeX

Esta pasta contém o relatório técnico resumido do projeto CESS-UFF / SGIMP.

## Estrutura

```text
report/
├── relatorio.tex
├── relatorio.pdf
├── README.md
└── figures/
    └── circuito-wokwi.png
```

## Compilação no TeXstudio

1. Abra `relatorio.tex` no TeXstudio.
2. Em **Opções > Configurar TeXstudio > Compilação**, selecione **LuaLaTeX** como compilador padrão.
3. Compile o documento duas vezes para atualizar o sumário, as referências internas e o número total de páginas.

O arquivo também contém a diretiva:

```tex
% !TeX program = lualatex
```

Em instalações nas quais o TeXstudio respeita diretivas mágicas, essa linha já seleciona o compilador correto.

## Compilação pelo terminal

A partir da pasta `report/`:

```bash
lualatex -interaction=nonstopmode -halt-on-error relatorio.tex
lualatex -interaction=nonstopmode -halt-on-error relatorio.tex
```

Também é possível usar:

```bash
latexmk -lualatex relatorio.tex
```

## Campo a revisar

Antes da entrega, substitua no preâmbulo:

```tex
\newcommand{\CandidateName}{\textit{preencher antes da entrega}}
```

pelo nome do candidato.
