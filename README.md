# Exploring the organization of semantic memory through unsupervised analysis of event-related potentials

Analysis code for:

Marijn van Vliet, Marc M. Van Hulle and Riitta Salmelin, "Exploring the organization of semantic memory through unsupervised analysis of event-related potentials", Journal of Cognitive Neuroscience, submitted, aimed for publication in 2017.

## Data

The main data used for the analysis in the notebooks is stored in this repository as [`data.csv`](data.csv). In addition, some psycho-linguistic data for the stimuli is available in [`psycho-linguistic-variables.csv`](psycho-linguistic-variables.csv).

## Notebooks

 1. [Hierarchical clustering based on N400 amplitude](clustering.ipynb)
 2. [Exploration of possible confounding psycho-linguistic variables](confounds.ipynb)
 3. [Effect of the judgement-of-association task](task.ipynb)
 
## Requirements

To run the notebooks, the following Python packages are required:

 - numpy
 - scipy
 - pandas
 - matplotlib
 - rpy2

And the following R packages:

 - lme4
 - lmerTest
