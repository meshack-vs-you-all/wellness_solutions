#!/bin/bash

# Compile the LaTeX document
pdflatex -interaction=nonstopmode JPF_Stretch_Hub_Final_Report.tex
pdflatex -interaction=nonstopmode JPF_Stretch_Hub_Final_Report.tex  # Run twice for TOC

# Clean up auxiliary files
rm -f *.aux *.log *.out *.toc

echo "PDF compilation complete!"
