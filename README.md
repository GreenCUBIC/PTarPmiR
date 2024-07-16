# PTarPmiR

P-TarPmiR is a plant microRNA target prediction software.

Upon submitting a list of miRNAs and mRNAs P-TarPmiR will extract features from all possible miRNA and mRNA pairings. These features will be sent to a classifier trained on thousands of plant miRNA:mRNA interactions, resulting in a target prediction confidence for each pairing.

## Abstract
microRNAs (miRNAs) are small non-coding ribonucleic acids that post-transcriptionally regulate gene expression through the targeting of messenger RNA (mRNAs). Most miRNA target predictors have focused on animal species and prediction performance drops substantially when applied to plant species. Several rule-based miRNA target predictors have been developed in plant species, but they often fail to discover new miRNA targets with non-canonical miRNA-mRNA binding. Here, the recently published TarDB database of plant miRNA-mRNA data is leveraged to retrain the TarPmiR miRNA target predictor for application on plant species. Rigorous experiment design across four plant test species demonstrates that animal-trained predictors fail to sustain performance on plant species, and that the use of plant-specific training data improves accuracy depending on the quantity of plant training data used. Surprisingly, our results indicate that the complete exclusion of animal training data leads to the most accurate plant-specific miRNA target predictor indicating that animal-based data may detract from miRNA target prediction in plants. Our final plant-specific miRNA prediction method, dubbed P-TarPmiR, is freely available for use at here. The final P-TarPmiR method is used to predict targets for all miRNA within the soybean genome. Those ranked predictions, together with GO term enrichment, are shared with the research community.

## Getting Started

### Dependencies and Installing

* See the original [TarPmiR Manual](http://hulab.ucf.edu/research/projects/miRNA/TarPmiR) for dowload, setup and installation
  * Note that the PTarPmiR was built on top of TarPmiR Linux. Compatability with windows operating systems cannot be garunteed
  * Note that their document may indicate that Python 2.7 is required; instead, Python 3.8 is actually required.
  * Note also that the pickled model files require downgrading to sklearn version 1.0.2. Otherwise, errors will be thrown when loading the pre-trained models and correct execution is not guaranteed.
  * (Thank you to Filippo Bergeretti for pointing out these discrepancies)
* Then replace the existing `TarPmiR.py` file with the one in this repo.
* Add the `parallel_TarPmiR.py` file to the same directory as the `TarPmiR.py` 
* Copy all models in the `models` directory of this repo to the TarPmiR models directory
    * Some models may require unzip-ing before use  

### Executing program

* The program can be run using the original TarPmiR Interface:
```
TarPmiR.py -a example/miR -b example/mRNAs -m models/Human.pkl -p 0.5
```
* Or using the Parrallellized interface:

```
parallel_TarPmiR.py -a example/miR -b example/mRNAs -c models/Human.pkl -p 0.5 -n number_of_threads
```

### Available Models
* Plant model trained on TarDB -> plant_Dec_4_2022.pkl
* Plant + Human model trained on TarDB and avallable human data (See journal) -> plant_Human_Dec_4_2022.pkl
* ath + Human model trained avallable human data and A. thaliana (See journal) -> ath_human.pkl

### Webserver 
A weserver is also avalible for use: [PTarPmiR](https://ptarpmir.cu-bic.ca/)

Note: Maximum file size is 100 KB or 100 000 characters

## Authors

Contributors names and contact info

* Victoria Ajila
* [James R. Green](http://www.sce.carleton.ca/faculty/green/green.php)

## Version History
* 0.1
    * Initial Release

## License
The software is a freely available for academic use.

## Citation
TBD

## Acknowledgments
* [Hu Lab - University of Central Florida](https://hulab.ucf.edu/)
