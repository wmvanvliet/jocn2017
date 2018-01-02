# Exploring the organization of semantic memory through unsupervised analysis of event-related potentials

Analysis code for:

[Marijn van Vliet, Marc M. Van Hulle and Riitta Salmelin, "Exploring the organization of semantic memory through unsupervised analysis of event-related potentials", Journal of Cognitive Neuroscience](https://www.mitpressjournals.org/doi/abs/10.1162/jocn_a_01211).

## Data

The main data used for the analysis in the notebooks is stored in this repository as [`data.csv`](data.csv). In addition, some psycho-linguistic data for the stimuli is available in [`psycho_linguistic_variables.csv`](psycho_linguistic_variables.csv).

For access to the EEG data and the N400 template, please contact [Marijn van Vliet](mailto:w.m.vanvliet@gmail.com).

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
