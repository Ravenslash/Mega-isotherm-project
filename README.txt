Developing Standardized Isotherms for Gas Adsorption

Authors:

Noah Whelpley
nwhelpley@gmail.com

Gabrielle Magid
gkmagid@gmail.com

Daniel Coile
daniel.w.coile@gmail.com

Justin Chen
yeutyngchen@gmail.com

PLEASE REPORT ANY BUGS OR ANNOYANCES TO ONE OF THESE EMAILS

thank you

------------------------------------------------------------------------------------------------------------------------------

Outline:

The NIST/ARPA-E Database of Novel and Emerging Adsorbent Materials consists of 30,000 unique isotherms collected over the 
course of 4 years, spanning 6,426 adsorbent materials and 299 adsorbate gases.[1] However, many isotherms with the same 
adsorbent, adsorbate, and testing conditions contain wildly varying graphs. We attempt to address this problem by collecting 
and converting data from database isotherms into a large collated isotherm (colloquially referred to as a “mega-isotherm”) and  
using Langmuir (and if better optimized in the future other) isotherm models to create a single standardized and more 
generally representative graph.

main.py is a simple script for extracting data from the database

example contains a single example output from main.py and a compressed folder of a collection of them

scripts contains miscellaneous useful scripts for plotting, model fitting, working with lots of data at once, etc.

depreciated, true to its name, contains depreciated scripts


Plans/ideas for improvement:
  
  1. Finding a way to include liquid-phase adsorption
  2. Accounting for hysteresis in mesoporous materials
  3. Automating the identification of isotherms so far from the model as to warrant special attention
  
  

Common issues:

  pyIAST runtime error:
  
    one can change the starting guesses for the optimization algorithm with the optional parameter "param_guess" which takes a 
    dictionary of parameter names and starting guesses. Running through a few often fixes the issue, except on particularly 
    difficult to model datasets. This should be generally taken care of in graph_obtainer.py
    
  The model does not fit the data at all:
  
    The search for the cause of this issue is ongoing, but it is believed to be another problem with the optimization 
    algorithm used by pyIAST.
    
  

credit for pyiast module:

C. Simon, B. Smit, M. Haranczyk. (2016) pyIAST: Ideal Adsorbed Solution Theory (IAST) Python Package. Computer Physics
Communications. 200, pp.364-380.
