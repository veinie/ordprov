import os, sys, random

########################
###### FUNCTIONS #######
########################

def main(obj):
    # Main function does the following:
    # 1. Takes a key-value pair for comparison as a parameter
    # 2. Displays current stats
    # 3. Displays a finnish word and takes user input to correlate the swedish translation
    # 4. Decides if the translation is correct, and depending on the user input:
    #   - Closes program
    #   - Displays success message, increments "correct"-status and shuffles a new word
    #   - Displays false status, adds missed word to "missed_words" and increments "missed"
    # 5. Displays correct translation
    # 6. Takes user input to decide whether to move to next word or exit program
    global correct
    global incorrect
    global missed_words
    # Display current stats via UI-Class object
    UI.display_info(correct, incorrect, missed_words)
    # Take user input and give the finnish word as a clue
    user_input = input(f'{str(obj[1])}: ')
    # Validate user input and accomplish corresponding tasks
    if user_input == '9':
        exit()
    # User input is compared to current word's swedish translation
    elif user_input.upper() in [x.strip().upper() for x in obj[0].split(',')]:
        # If translation is correct:
        UI.display_succeed(True)
        correct += 1
        update_current_word()
    else:
        # If translation is incorrect:
        UI.display_succeed(False)
        add_missed_words(obj)
        incorrect += 1
        if 'debug' in sys.argv:
            UI.display_debug_translation(obj, user_input)
    # Display correct translation
    print(obj[0])
    # Select new word or exit program:
    user_input = UI.new_word_or_exit()
    if user_input == '9':
        exit()


def check_args():
    allowed = ['debug']
    invalid = [a for a in sys.argv[1::1] if a not in allowed]
    if invalid:
        UI.display_check_args(allowed, invalid)
        exit()


def select_wordlist(words1, words2, words3):
    # Select_wordlist does the following:
    # 1. Takes word-lists as parameters
    # 2. Takes user input to select word-list via UI-Class object
    # 3. Selects word-list for current session corresponding the user input
    while True:
        user_input = UI.select_wordslist()
        if user_input == '1':
            return words1
        elif user_input in ['2','3']:
            UI.display_gender_requirement()
            if user_input == '2': return words2
            return words3
        elif user_input == '9':
            exit()
        UI.display_check_input()  


def get_word(words):
    # Get_word selects a random key-value pair from dictionary given as parameter
    return random.choice(list(words.items()))


def update_current_word():
    # Update_current_word updates global current_word variable by
    # utilizing get_word() -function and word-list selected for current session
    global words
    global current_word
    current_word = get_word({k: v for k, v in words.items() if k != current_word[0]})

def add_missed_words(this_word):
    # Add_missed_words() validates if the key-value pair given in as parameter
    if this_word in missed_words.keys():
        missed_words[this_word] = missed_words[this_word] + 1
        return
    missed_words[this_word] = 1


def get_most_missed():
    # Returns a list of 3 most missed words and the corresponding amount of misses
    return_string = ''
    missed_list = sorted(list(missed_words.items()), key=lambda x: x[1], reverse=True)
    count = 0
    for elem in missed_list:
        if count < 3:
            return_string += f'{elem[1]} misses: {elem[0][1]} - {elem[0][0].upper()}\n'
            count += 1
    return return_string


########################
####### UI-Class #######
########################


class SanakoeUI:
    # UI-Class is built for this application for the sake of clarity of the program code.
    # This way print-statements are seperated from the logical functions for improved readability.

    def display_info(self, correct, incorrect, missed_words):
        # Display-info() clears shell, prints header and displays amount of correct and
        # incorrect translations in current session. If there are missed words, three
        # most missed words are displayed with translations to improve learning.
        os.system('CLS||clear')
        print('Sanakoeharjoitus - valitse (9) poistuaksesi\n')
        print(f'---Points---\nCorrect:{correct}\nIncorrect:{incorrect}\n')
        if missed_words:
            print('---Most missed---')
            print(f'{get_most_missed()}')

    def display_succeed(self, status):
        if status: print('Correctish?')
        else: print('WRONG!!')

    def new_word_or_exit(self):
        return input('Press any key for next word or (9) to exit ')
    
    def select_wordslist(self):
        return input('Select word list (1), (2) or (3) - or (9) to exit: ')
    
    def display_gender_requirement(self):
        os.system('CLS||clear')
        print('Gender (en, ett) required with these words.')
        input('Press any key to continue ')

    def display_check_input(self):
        print('Check input.')
        
    def display_check_args(self, allowed, invalid):
        print(f'Check call arguments - {", ".join(invalid)} not allowed.')
        print(f'Allowerd arguments: {", ".join(allowed)}.')

    def display_debug_translation(self, obj, user_input):
        # If debug is given as argument, display list of correct ASCII characters and their ordinal number
        # and those for user inputted translation.
        # 
        # It seems like sometimes python input() -function can't keep up with backspace during
        # keyboard input and thus the translation comparison can be evaluated as unsuccesfull even though
        # the correct translation is displayed in the shell.
        print('---------- Debug info ----------')
        print('Correct ASCII characters:')
        print(obj[0].split(",")[0])
        print([ord(c) for c in list(obj[0].split(",")[0])])
        print('Input ASCII characters:')
        print(user_input)
        print([ord(c) for c in list(user_input)])
        print('--------------------------------')


########################
###### Word-lists ######
########################


words1 = {
    'avl??gga, avl??gger, avlade, avlagt, ta examen': "suorittaa tutkinto",
    'betyg, -et, -, -en': 'arvosana (rr), todistus (sr)',
    'bli f??rdig med studierna, bli f??rdig, blir, blev, blivit': 'valmistua',
    'deltidsstudier, -na': 'osa-aikaiset opinnot',
    'distansstudier': 'et??opinnot',
    'dubbelexamen': 'kaksoistutkinto',
    'examensarbete, -t, -n, -na, l??rdomsprov, -et, -, -en': 'opinn??ytety??',
    'examensbetyg, -et, -, -en': 'tutkintotodistus',
    'godk??n, godk??nd, -t, -a': 'hyv??ksytty',
    'grundskola, -n, -or, -orna': 'peruskoulu',
    'grundstudier, -na': 'perusopinnot',
    'gymnasium, -et, -er, -erna': 'lukio',
    'heltidsstudier, -na': 'p????toimiset opinnot',
    'h??gskola, -n, -or, -orna': 'korkeakoulu',
    'h??gskoleexamen, -, -examina': 'korkeakoulututkinto',
    'inriktning, -en, -ar, -arna': 'suuntautuminen',
    'intr??desprov, -et, -, -en': 'p????sykoe',
    'komma in, kommer, kom, kommit': 'p????st?? sis????n, tulla hyv??ksytyksi',
    'kurs, -en, -er, -erna': 'kurssi',
    'lektion, -ern, -er, -erna': 'oppitunti',
    'n??rundervisning, kontaktundervisning, -en': 'l??hiopetus',
    'obligatorisk, -t, -a': 'pakollinen',
    'praktik, -en': 'harjoittelu',
    'praktikant, -en, -er, -erna': 'harjoittelija',
    'praktiser, praktisera, -ar, -ade, -at': 'harjoitella',
    'prov, -et, -, -en': 'koe',
    'sj??lvstudier, -na': 'itseopiskelu',
    'student, -en, -er, -erna': 'ylioppilas (sr), opiskelija (rr)',
    'studentexamen, -, examina': 'ylioppilastutkinto',
    'studiepo??ng, -et, -, -en': 'opintopiste',
    's??k in, s??ka in, -er, -te, -t, sig in': 'pyrki?? sis????n',
    'tent, tenta, -an, -or, -orna': 'tentti',
    'termin, -en, -or- orna': 'lukukausi',
    'universitet, -et, -, -en': 'yliopisto',
    'utbildning, -en, -ar, -arna': 'koulutus',
    'utbildningsprogram, -met, -, -en': 'koulutusohjelma',
    'utexaminer, -as, -ades, -ats': 'valmistua',
    'vitsord, -et, -, -en': 'arvosana (sr)',
    'yrkesh??gskol, yrkesh??gskola, -n, -or, -orna': 'ammattikorkeakoulu',
    'yrkesh??gskoleexamen, -, -examina': 'ammattikorkeakoulututkinto',
    'yrkesinstitut, -et, -, -en': 'ammattiopisto',
    'yrkesstudier, -na': 'ammattiopinnot',
}


words2 = {
    'anst??lla': 'palkata',
    'en annons': 'ilmoitus',
    'en anst??lld, en arbetstagare': 'ty??ntekij??',
    'en anst??llning ': 'ty??suhde',
    'en ans??kan': 'hakemus',
    'en arbetsdag': 'ty??p??iv??',
    'en arbetsgivare': 'ty??nantaja',
    'en bransch': '(ammatti)ala',
    'en chef': 'johtaja, p????llikk??',
    'en erfarenhet': 'kokemus (vrt. arbetserfarenhet = ty??kokemus)',
    'en egenskap': 'ominaisuus',
    'en f??rm??n': 'etu',
    'en intervju': 'haastattelu',
    'en kollega': 'kollega, ty??toveri',
    'en kunskap': 'osaaminen, taito',
    'en l??n': 'palkka (vrt. en timl??n = tuntipalkka, en m??nadsl??n = kuukausipalkka)',
    'en semester': 'loma',
    'en uppgift': 'teht??v??',
    'en utbildning': 'koulutus',
    'en utmaning': 'haaste',
    'ett arbete, ett jobb': 'ty??',
    'ett arbetsintyg': 'ty??todistus',
    'ett avtal': 'sopimus',
    'ett CV': 'ansioluettelo',
    'ett fast jobb': 'vakituinen ty??',
    'ett f??retag': 'yritys',
    'ett skiftarbete': 'vuoroty??',
    'ett team': 'tiimi',
    'flexibel': 'joustava',
    'flitig': 'ahkera',
    'flytande': 'sujuva',
    'glad': 'iloinen',
    'information': 'tieto',
    'jobba deltid': 'ty??skennell?? osa-aikaisesti',
    'jobba heltid': 'ty??skennell?? kokoaikaisesti',
    'jobba, arbeta': 'ty??skennell??',
    'planera': 'suunnitella',
    'samarbetskunnig': 'yhteisty??taitoinen',
    'p??litlig': 'luotettava',
    'spr??kkunskaper': 'kielitaito (kielitaidot)',
    'starka sidor': 'vahvat puolet',
    'svaga sidor': 'heikot puolet',
    's??ka': 'hakea (vrt. s??ka jobb = hakea ty??t??)',
    'v??nlig': 'yst??v??llinen',
}


words3 = {
    'ansluta, anslutar, anslutade, anslutat': 'liitt????',
    'dela, delar, delade, delat': 'jakaa',
    'en analytik': 'analytiikka',
    'en anv??ndare': 'k??ytt??j??',
    'en applikation': 'sovellus',
    'en artificiell intelligens': 'teko??ly',
    'en databas': 'tietokanta',
    'en databehandling': 'tietojenk??sittely',
    'en datas??kerhet': 'tietoturva',
    'en data??verf??ring': 'tiedonsiirto',
    'en dator': 'tietokone',
    'en datormus': 'hiiri (tietokoneen)',
    'en fil': 'tiedosto',
    'en klient, en kund': 'asiakas',
    'en molntj??nst': 'pilvipalvelu',
    'en server': 'palvelin',
    'en sk??rm': 'n??ytt??',
    'en sladd': 'johto',
    'en str??mk??lla': 'virtal??hde',
    'en uppdatering': 'p??ivitys',
    'en webbl??sare': 'verkkoselain',
    'ett avbrott': 'katkos',
    'ett l??senord': 'salasana',
    'ett system': 'j??rjestelm??',
    'ett tangentbord': 'n??pp??imist??',
    'ett tr??d': 'lanka',
    'h??mta, h??mtar, h??mtade, h??mtat': 'ladata (esim. tiedosto)',
    'internet': 'internetti (vrt. n??tet = netti)',
    'konfidentiell': 'luottamuksellinen',
    'planera, planerar, planerade, planerat': 'suunnitella',
    'programmera, programmerar, programmerade, programmerat': 'ohjelmoida',
    'sprida, sprider, spred, spridit': 'levitt????',
    'st??nga av, st??nger av, st??ngde av, st??ngt av': 'sulkea',
    'tr??dl??s': 'langaton',
    'utveckla, utvecklar, utvecklade, utvecklat': 'kehitt????',
    '??verf??ra, ??verf??r, ??verf??rde, ??verf??rt': 'siirt????'
}


#########################
######### MAIN ##########
#########################


if __name__ == '__main__':
    correct = 0
    incorrect = 0
    missed_words = {}
    UI = SanakoeUI()
    check_args()
    words = select_wordlist(words1, words2, words3)
    current_word = get_word(words)
    while True:
        main(current_word)