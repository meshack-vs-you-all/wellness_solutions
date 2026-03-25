#!/bin/bash

# Compile the LaTeX document
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex  # Run twice for TOC

# Clean up auxiliary files
rm -f *.aux *.log *.out *.toc

echo "PDF compilation complete!"
