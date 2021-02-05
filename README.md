# machine-translation-scraping
This Python script scrapes Machine Translation sites based on input in Source.xlsx

## TO DO
* [x] Count characters from DF
* Function-ify everything
    * Google
        * "Your client made a request that's too long"
    * [x] Baidu
    * QQ 
        * Sometimes erroneously replaces commas before capital letters with '.\n'
            * Causes the resulting list to be too long
    * [x] DeepL
        * [x] Implement pauses for the progress popup
            * [x] xpath: //*[@id="dl_translator"]/div[5]/div[1]
            * [x] May be able to just have it pause every 1000 characters 
    * [x] SoGou
    * Put it all into an Excel sheet
    * Bugs
        * [x] Replace \n with a space