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
    new_word = get_word(words)
    while new_word == current_word:
        new_word = get_word(words)
    current_word = new_word


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
    'avlägga, avlägger, avlade, avlagt, ta examen': "suorittaa tutkinto",
    'betyg, -et, -, -en': 'arvosana (rr), todistus (sr)',
    'bli färdig med studierna, bli färdig, blir, blev, blivit': 'valmistua',
    'deltidsstudier, -na': 'osa-aikaiset opinnot',
    'distansstudier': 'etäopinnot',
    'dubbelexamen': 'kaksoistutkinto',
    'examensarbete, -t, -n, -na, lärdomsprov, -et, -, -en': 'opinnäytetyö',
    'examensbetyg, -et, -, -en': 'tutkintotodistus',
    'godkän, godkänd, -t, -a': 'hyväksytty',
    'grundskola, -n, -or, -orna': 'peruskoulu',
    'grundstudier, -na': 'perusopinnot',
    'gymnasium, -et, -er, -erna': 'lukio',
    'heltidsstudier, -na': 'päätoimiset opinnot',
    'högskola, -n, -or, -orna': 'korkeakoulu',
    'högskoleexamen, -, -examina': 'korkeakoulututkinto',
    'inriktning, -en, -ar, -arna': 'suuntautuminen',
    'inträdesprov, -et, -, -en': 'pääsykoe',
    'komma in, kommer, kom, kommit': 'päästä sisään, tulla hyväksytyksi',
    'kurs, -en, -er, -erna': 'kurssi',
    'lektion, -ern, -er, -erna': 'oppitunti',
    'närundervisning, kontaktundervisning, -en': 'lähiopetus',
    'obligatorisk, -t, -a': 'pakollinen',
    'praktik, -en': 'harjoittelu',
    'praktikant, -en, -er, -erna': 'harjoittelija',
    'praktiser, praktisera, -ar, -ade, -at': 'harjoitella',
    'prov, -et, -, -en': 'koe',
    'självstudier, -na': 'itseopiskelu',
    'student, -en, -er, -erna': 'ylioppilas (sr), opiskelija (rr)',
    'studentexamen, -, examina': 'ylioppilastutkinto',
    'studiepoäng, -et, -, -en': 'opintopiste',
    'sök in, söka in, -er, -te, -t, sig in': 'pyrkiä sisään',
    'tent, tenta, -an, -or, -orna': 'tentti',
    'termin, -en, -or- orna': 'lukukausi',
    'universitet, -et, -, -en': 'yliopisto',
    'utbildning, -en, -ar, -arna': 'koulutus',
    'utbildningsprogram, -met, -, -en': 'koulutusohjelma',
    'utexaminer, -as, -ades, -ats': 'valmistua',
    'vitsord, -et, -, -en': 'arvosana (sr)',
    'yrkeshögskol, yrkeshögskola, -n, -or, -orna': 'ammattikorkeakoulu',
    'yrkeshögskoleexamen, -, -examina': 'ammattikorkeakoulututkinto',
    'yrkesinstitut, -et, -, -en': 'ammattiopisto',
    'yrkesstudier, -na': 'ammattiopinnot',
}


words2 = {
    'anställa': 'palkata',
    'en annons': 'ilmoitus',
    'en anställd, en arbetstagare': 'työntekijä',
    'en anställning ': 'työsuhde',
    'en ansökan': 'hakemus',
    'en arbetsdag': 'työpäivä',
    'en arbetsgivare': 'työnantaja',
    'en bransch': '(ammatti)ala',
    'en chef': 'johtaja, päällikkö',
    'en erfarenhet': 'kokemus (vrt. arbetserfarenhet = työkokemus)',
    'en egenskap': 'ominaisuus',
    'en förmån': 'etu',
    'en intervju': 'haastattelu',
    'en kollega': 'kollega, työtoveri',
    'en kunskap': 'osaaminen, taito',
    'en lön': 'palkka (vrt. en timlön = tuntipalkka, en månadslön = kuukausipalkka)',
    'en semester': 'loma',
    'en uppgift': 'tehtävä',
    'en utbildning': 'koulutus',
    'en utmaning': 'haaste',
    'ett arbete, ett jobb': 'työ',
    'ett arbetsintyg': 'työtodistus',
    'ett avtal': 'sopimus',
    'ett CV': 'ansioluettelo',
    'ett fast jobb': 'vakituinen työ',
    'ett företag': 'yritys',
    'ett skiftarbete': 'vuorotyö',
    'ett team': 'tiimi',
    'flexibel': 'joustava',
    'flitig': 'ahkera',
    'flytande': 'sujuva',
    'glad': 'iloinen',
    'information': 'tieto',
    'jobba deltid': 'työskennellä osa-aikaisesti',
    'jobba heltid': 'työskennellä kokoaikaisesti',
    'jobba, arbeta': 'työskennellä',
    'planera': 'suunnitella',
    'samarbetskunnig': 'yhteistyötaitoinen',
    'pålitlig': 'luotettava',
    'språkkunskaper': 'kielitaito (kielitaidot)',
    'starka sidor': 'vahvat puolet',
    'svaga sidor': 'heikot puolet',
    'söka': 'hakea (vrt. söka jobb = hakea työtä)',
    'vänlig': 'ystävällinen',
}


words3 = {
    'ansluta, anslutar, anslutade, anslutat': 'liittää',
    'dela, delar, delade, delat': 'jakaa',
    'en analytik': 'analytiikka',
    'en användare': 'käyttäjä',
    'en applikation': 'sovellus',
    'en artificiell intelligens': 'tekoäly',
    'en databas': 'tietokanta',
    'en databehandling': 'tietojenkäsittely',
    'en datasäkerhet': 'tietoturva',
    'en dataöverföring': 'tiedonsiirto',
    'en dator': 'tietokone',
    'en datormus': 'hiiri (tietokoneen)',
    'en fil': 'tiedosto',
    'en klient, en kund': 'asiakas',
    'en molntjänst': 'pilvipalvelu',
    'en server': 'palvelin',
    'en skärm': 'näyttö',
    'en sladd': 'johto',
    'en strömkälla': 'virtalähde',
    'en uppdatering': 'päivitys',
    'en webbläsare': 'verkkoselain',
    'ett avbrott': 'katkos',
    'ett lösenord': 'salasana',
    'ett system': 'järjestelmä',
    'ett tangentbord': 'näppäimistö',
    'ett tråd': 'lanka',
    'hämta, hämtar, hämtade, hämtat': 'ladata (esim. tiedosto)',
    'internet': 'internetti (vrt. nätet = netti)',
    'konfidentiell': 'luottamuksellinen',
    'planera, planerar, planerade, planerat': 'suunnitella',
    'programmera, programmerar, programmerade, programmerat': 'ohjelmoida',
    'sprida, sprider, spred, spridit': 'levittää',
    'stänga av, stänger av, stängde av, stängt av': 'sulkea',
    'trådlös': 'langaton',
    'utveckla, utvecklar, utvecklade, utvecklat': 'kehittää',
    'överföra, överför, överförde, överfört': 'siirtää'
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