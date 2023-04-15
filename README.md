# WIP2022-GitHub_Readme-code
## Dependencies
When determining common traits that exist within README files, our program uses the spacy library to determine
similarities between headers. This must be downloaded via:

    pip install spacy
    pip install git+https://github.com/MartinoMensio/spacy-universal-sentence-encoder.git

Optionally, a parameter is also provided USE_LARGE_MODEL under traitFinder.py.
As well as USE_UNIV_SENTENCE_ENCODER, which when set to 0 will not use a sentence encoder, 
and instead use Spacy's large or small core datasets.
USE_LARGE_MODEL may be set to 0 if you wish to use the small model, which will improve performance although provide less accurate results.

In our paper, we USE_UNIV_SENTENCE_ENCODER, given in the first download link.
The small model must be downloaded via:

    pip install spacy
    python -m spacy download en_core_web_lg

    pip install spacy
    python -m spacy download en_core_web_sm

If you still receive a problem with finding the packages after installing, try:

    python -m spacy download en

and restart your IDE.

## Data:
The data for RQ1 and RQ2 are packaged in ```data/all_in_one_data.csv```

## RQs

### RQ1
run 
```python Wilcoxon&Cliffs_delta.py```

### RQ2 
run 
```python Feature_importance.py```

### RQ3

The labeled data located in ```/date/popular vs non_popular_commits 100 samples published.xlsx```

## Collect data from GitHub
### Config.properties Format
You will need a `Config.properties` file in the root of the project to extract data from GitHub API in the following format
```python
token= your_token_goes_here
user= your_GitHub_username_goes_here
```
For more token information, please refer to: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token



### Tips on running the code
- Most data collection/retrieval files can be found under data_retrieval
- Most `pandas.read_csv()` file name is hardcoded, feel free to change __file_name and __save_name in main as needed.
- Save a copy of your current data when you are adding new columns to the data in case of failure
- For most files does not need arguments, so you can simply click run.
