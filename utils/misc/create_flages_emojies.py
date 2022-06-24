import pycountry
import translate


async def create_flag(name_country):
    translator = translate.Translator(to_lang="en", from_lang="ru")
    name_country = translator.translate(name_country)

    try:
        flag_country = pycountry.countries.search_fuzzy(name_country)
    except:
        return ""
    else:
        return flag_country[0].flag