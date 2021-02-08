# machine-translation-scraping
This Python script scrapes Machine Translation sites based on input in Source.xlsx

## TO DO
* [x] Count characters from DF
* Function-ify everything
    1. Websites 
        * [x] Google
            * [x] "413. That’s an error. Your client issued a request that was too large. That’s all we know."
                * [x] Likely due to the page not refreshing every 4500 characters
        * [x] Baidu
        * QQ
            * Sometimes erroneously replaces commas before capital letters with '.\n'
                * Causes the resulting list to be too long
        * [x] DeepL
            * [x] Implement pauses for the progress popup
                * [x] xpath: //*[@id="dl_translator"]/div[5]/div[1]
                * [x] May be able to just have it pause every 1000 characters 
        * [x] SoGou
    2. [x] Put it all into an Excel sheet
    3. Global Bugs
        * [x] Replace \n with a space
        * [x] Omit empty strings in the final list