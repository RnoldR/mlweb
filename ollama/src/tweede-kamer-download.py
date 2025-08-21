import os
import requests
import lxml.etree as etree
from xml.etree import ElementTree as ET

name_space_tag = '{http://www.tweedekamer.nl/ggm/vergaderverslag/v1.0}'
stopwords = ['De', 'De heer', 'Mevrouw', 'De Kamer,', 'gehoord de beraadslaging,',
             'Zij krijgt nr.', 'en gaat over tot de orde van de dag.',
             'Dank u wel, voorzitter.', 'Voorzitter, dank u wel.']

byte_limit = 2_500_000
max = 250
count = 1

pad = 'ollama/texts'
sprekers = 'ollama/sprekers'
tmp_file = os.path.join(pad, 'file.xml')
debate_file = os.path.join(pad, 'text-tk')
sprekers_file = os.path.join(sprekers, 'tk-spreker')

def show(obj, n):
    i = 0
    for key in obj.keys():
        print(key, obj[key])

        i += 1
        if i >= n:
            break

    return

### show ###


def demo_simple():
    response = requests.get('https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Document')

    print(response.status_code)
    print(response.headers)

    result = response.json()
    print(len(result))

    return

### demo_simple ###


def demo_tk():
    response = requests.get("https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Persoon?$filter=Verwijderd eq false and (Functie eq 'Tweede Kamerlid')")
    print(response.status_code)
    print(response.headers)

    result = response.json()
    print(len(result)) # 2
    print(result.keys()) # dict_keys(['@odata.context', 'value'])
    print(type(result['value'])) # <class 'list'>

    for value in result['value']:
        vn = value['Roepnaam']
        an = value['Achternaam']
        tv = value['Tussenvoegsel']
        
        if tv is None:
            print(vn, an)
        else:
            print(vn, tv, an)

        # if
    # for

    return
### demo_tk ###


def demo_plenair_debat():
    response = requests.get("https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Activiteit?$filter=contains(soort, 'plenair debat') and Status eq 'Uitgevoerd'&$count=true") #  and year(GewijzigdOp) eq 2022&$count=true")

    print(response.status_code)
    print(response.headers)

    result = response.json()
    debates = result['value']

    for value in debates:
        print('***', value['Onderwerp'].strip())

    # for

    print(len(debates))

    return

### demo_plenair_debat ###


def pp(element, **kwargs):
    xml = etree.tostring(element, pretty_print=True, **kwargs)
    print(xml.decode(), end='')

    return

### pp ###


def get_verslag(vergadering: str):
    id = vergadering['Id']

    # get report of meeting 'id'
    url = f"https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/verslag/{id}/resource"
    verslag = requests.get(url)

    # encoding of the documents is wrong, it is not utf-8. 
    # by setting it to apparent_encoding the correct encoding is applied
    verslag.encoding = verslag.apparent_encoding # 'ISO-8859-1'

    return verslag.text

### get_verslag ###


def create_speaker(sprekers, spreker):
    naam = spreker['verslagnaam']
    if 'voornaam' in spreker:
        # sometimes spreker['voornaam'] is None, hence the try..except block
        try:
            voornaam = spreker['voornaam']
            if not naam.startswith(voornaam):
                naam = voornaam + ' ' + naam
        except:
            pass

    spreker['id'] = naam
    if naam not in sprekers:
        sprekers[naam] = spreker

    else:
        existing = sprekers[naam]
        for txt in spreker['texts']:
            existing['texts'].append(txt)

    return sprekers

### create_speaker ###


def t(tg):
    return name_space_tag + tg

def nt(tg):
    return tg.split('}')[1]
    
def process_debate(filename: str, sprekers: dict, seq: int):
    # read and parse the xml file 
    doc = etree.parse(filename)
    spreker = None
    title = ''

    # write all elements to file
    # with open(text_file, mode = 'a') as outfile:
    # enumerate over all xml tags in document
    for elem in doc.iter():
        # get the tag
        tag = nt(elem.tag)
        if tag == 'titel' and len(title) == 0:
            title = elem.text
            omvang = os.path.getsize(filename)
            print(f'{seq:5} {omvang:12,}: {title}')
        
        # when is is a speaker, create new 'spreker' as a new dict
        if tag == 'spreker':
            # when a spreker exists, create one in sprekers and set 
            # spreker to None
            if spreker is not None:
                sprekers = create_speaker(sprekers, spreker)
                spreker = None

            # when None, create dict with one key: 'texts'
            else:
                spreker = {}
                spreker['texts'] = []

        # all other tags should be collected in a speaker
        else:
            # spreker is None, tag can't be associated with a speaker
            if spreker is None:
                pass

            # spreker is not None, collect tag in spreker
            else:
                # alineaitem is spoken text, collect in 'texts'
                if tag == 'alineaitem':
                    if spreker['texts'] is not None:
                        # negate in stopwords
                        if elem.text is not None \
                            and elem.text.strip() not in stopwords \
                            and not elem.text.strip().endswith(' ('):

                            spreker['texts'].append(elem.text + '\n\n')

                # some xml tag, just add to spreker
                else:
                    spreker[tag] = elem.text

                # if
            # if
        # if
    # for

    return sprekers

### process_debate ###


def create_md_file(filename: str, sprekers: dict):
    filename = filename + '.md'
    print(f'{len(sprekers)} sprekers gevonden, sriting to: {filename}')

    with open(filename, mode = 'a') as outfile:
        # write file header
        outfile.write('[[_TOC_]]\n')
        outfile.write('\n# Texts\n')

        # iterate over all speakers
        for key, value in sprekers.items():
            # write the texts
            if 'texts' in value.keys() \
                and len(value['texts']) > 1:

                # write speaker identification
                outfile.write(f'\n## {key} \n\n')

                for txt in value['texts']:
                    outfile.write(f'{txt}\n')

            else:
                pass
                # outfile.write('No text for speaker')

            # if
        # for
    # with

    return

### create_md_file ###


def create_txt_file(filename: str, sprekers: dict):
    """ A text file is generated with the name of each member preceding a sentence he/she said.

    Args:
        filename (str): namne of the file
        sprekers (dict): list of speakers and their text
    """

    m = 1
    n = 0
    bytes = 0
    outfile = None
    print(f'{len(sprekers)} sprekers gevonden, sriting to: {filename}')

    textfile = f'{filename}-{max:03d}-{m:02d}.txt'
    outfile = open(textfile, mode = 'w', encoding = 'UTF8')
    # iterate over all speakers
    for key, value in sprekers.items():
        if bytes > byte_limit: # n % split == 0:
            bytes = 0

            m += 1
            textfile = f'{filename}-{max:03d}-{m:02d}.txt'

            outfile.close()
            outfile = open(textfile, mode = 'w', encoding = 'UTF8')
        # if

        # write the texts
        if 'texts' in value.keys() \
            and len(value['texts']) > 1:

            for txt in value['texts']:
                bytes += len(txt.encode('utf-8')) # len(txt)
                outfile.write(f'Het Tweede Kamer lid {key} zegt: ')
                outfile.write(f'{txt}\n')

        else:
            pass # No text for speaker

        # if

        n += 1

    # for

    outfile.close()

    return

### create_txt_file ###


def create_sprekers_files(filename: str, sprekers: dict):
    """ A text file is generated with the name of each member preceding a sentence he/she said.

    Args:
        filename (str): namne of the file
        sprekers (dict): list of speakers and their text
    """

    print(f'{len(sprekers)} sprekers gevonden, sriting to: {filename}')

    # iterate over all speakers
    for key, value in sprekers.items():
        """
        if bytes > byte_limit: # n % split == 0:
            bytes = 0

            m += 1
            textfile = f'{filename}-{max:03d}-{m:02d}.txt'

            outfile.close()
            outfile = open(textfile, mode = 'w', encoding = 'UTF8')
        # if
        """

        # write the texts
        if 'texts' in value.keys() \
            and len(value['texts']) > 1:

            # create sprekers file
            unspaced = key.replace(' ', '_')
            textfile = f'{filename}-{unspaced}.txt'
            outfile = open(textfile, mode = 'w', encoding = 'UTF8')

            for txt in value['texts']:
                outfile.write(f'Het Tweede Kamer lid {key} zegt: ')
                outfile.write(f'{txt}\n')

            outfile.close()

        else:
            pass # No text for speaker

        # if

    # for

    return

### create_sprekers_files ###


def verwerk_alle_verslagen():
    # get all parlimentary resumee's
    response = requests.get("https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/Verslag?$filter=contains(soort, 'Eindpublicatie')") # and Status eq 'Uitgevoerd'&$count=true")

    print(f'\nGot documents, response code is: {response.status_code}\n')

    # convert to json, extract xml text
    result = response.json()
    debates = result['value']
    print(len(debates), 'plenaire debatten gevonden')

    # initialize existing text bases
    with open(debate_file, 'w', encoding = 'UTF8') as outfile:
        outfile.write('\n')

    # get speakers from all debates    
    sprekers = {}
    print('')
    count = 0
    for value in debates:
        count += 1
        # print('***', value['Vergadering_Id'], value['ContentLength'])

        xml_doc = get_verslag(value)

        with open(tmp_file, 'w', encoding = 'UTF8') as outfile:
            outfile.write(xml_doc)
        
        sprekers = process_debate(tmp_file, sprekers, count)

        if count >= max:
            break

    # for
    print('')

    create_md_file(debate_file, sprekers)
    # create_txt_file(debate_file, sprekers)
    create_sprekers_files(sprekers_file, sprekers)
    return

### verwerk_alle_verslagen ###

if __name__ == "__main__":
    verwerk_alle_verslagen()
