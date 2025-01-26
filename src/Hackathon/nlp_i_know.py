import iknowpy
import logging
logger = logging.getLogger(__name__)


def nlp_function():
    engine = iknowpy.iKnowEngine()

    # show supported languages
    print(engine.get_languages_set())

    # index some text
    text = ("Mr Tan Ah Kow was accompanied by his son, Mr Tan Ah Beng, for the examination. \
            Mr Tan is a 55 year old man, who is divorced, and unemployed. Mr Tan is currently living with his son, Ah Beng, \
            in Ah Beng’s flat. Mr Tan Ah Beng informed me that Mr Tan Ah Kow used to work as a cleaner. \
            Mr Tan Ah Kow has a history of medical conditions. He has had hypertension and \
            hyperlipidemia since 1990 and suffered several strokes in 2005. He subsequently \
            developed heart problems (cardiomyopathy), cardiac failure and chronic renal disease and was treated in ABC Hospital. \
    He was last admitted to the ABC Hospital on 1 April 2010 till 15 April 2010, during \
    which he was diagnosed to have suffered from a stroke. This was confirmed by CT \
                                                                                 and MRI brain scans. \
    Thereafter, he was transferred to XYZ Hospital for stroke rehabilitation on 15 April \
    2010. \
    After that, Mr Tan was referred to Blackacre Hospital follow-up treatment  \
    November 2010. The clinical impression was that he was manifesting behavioural \
    psychological symptoms secondary to Dementia")

    engine.index(text, 'en')

    # print the raw results
    print(engine.m_index)
    output = []

    # or make it a little nicer
    for s in engine.m_index['sentences']:
        for e in s['entities']:
            sentence = f"<'+{e}['type']+'>'+{e}['index']+'</'+{e}['type']+'>'s' \n"
            # print('<'+e['type']+'>'+e['index']+'</'+e['type']+'>', end=' ')
            output.append(sentence)
        print('\n')


    return output

if __name__ == "__main__":
    print("start run")
    result = nlp_function()
    open("log_nlp", "w", encoding="utf-8").close()
    logging.basicConfig(
        filename="log_nlp",
        format="%(levelname)s - %(asctime)s - %(message)s",
        level=logging.INFO,
        force=True,
    )

    logger.info("Finished nlp run")
    logger.info(result)