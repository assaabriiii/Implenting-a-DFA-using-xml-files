from bs4 import BeautifulSoup


class Automata:
    class __States:

        def __init__(self, isFinal=False, isInitial=False, name=None):
            self.isFinal = isFinal
            self.isInitial = isInitial
            self.name = name
            self.transitions = {}

        def setNextState(self, alph, state):
            self.transitions[alph] = state

        def getNextState(self, alph):
            return self.transitions[alph]

        def getName(self):
            return self.name

        def getFinalStatus(self):
            return self.isFinal

        def getInitialStatus(self):
            return self.isInitial

    def get_file(self, xml_file):
        with open(xml_file, 'r') as f:
            data = f.read()
        soup = BeautifulSoup(data, 'xml')
        self.__parse_and_create(soup)

    def check_input(self, string):
        self.__automata_acceptance(string, self.__initialState_obj, self.__alphabets)

    def __parse_and_create(self, file):
        self.__alphabets, number_of_alphabets = self.__extract_alphabets(file)
        states, number_of_states = self.__extract_states(file)
        initialState = self.__extract_initial_state(file)
        finalStates, number_of_final_states = self.__extract_final_states(file)
        stateObj, self.__initialState_obj = self.__create_state_objs(states, number_of_states, initialState, finalStates,
                                                                   number_of_final_states)
        self.__set_transitions(file, stateObj, number_of_states)

    def __extract_alphabets(self, file):
        Alphabets = file.find('Alphabets')
        number_of_alphabets = int(Alphabets.get('numberOfAlphabets'))
        alphabet_tags = Alphabets.find_all('alphabet')
        alphabets = []
        i = 0
        while i < number_of_alphabets:
            alphabets.append(alphabet_tags[i].get('letter'))
            i += 1

        return alphabets, number_of_alphabets

    def __extract_states(self, file):
        States_tag = file.find('States')
        number_of_states = int(States_tag.get('numberOfStates'))
        state_tags = States_tag.find_all('state')
        states = []
        i = 0
        while i < number_of_states:
            states.append(state_tags[i].get('name'))
            i += 1

        return states, number_of_states

    def __extract_initial_state(self, file):
        States_tag = file.find('States')
        initialState_tag = States_tag.find('initialState')
        initialState = initialState_tag.get('name')
        return initialState

    def __extract_final_states(self, file):
        FinalStates_tag = file.find('FinalStates')
        number_of_final_states = int(FinalStates_tag.get('numberOfFinalStates'))
        finalState_tags = FinalStates_tag.find_all('finalState')
        finalStates = []
        i = 0
        while i < number_of_final_states:
            finalStates.append(finalState_tags[i].get('name'))
            i += 1

        return finalStates, number_of_final_states

    def __create_state_objs(self, states, number_of_states, initialState, finalStates, number_of_final_states):
        stateObj = []
        initialState_obj = None
        i = 0
        while i < number_of_states:
            if states[i] == initialState:
                isInitial = True
            else:
                isInitial = False

            j = 0
            isFinal = False
            while j < number_of_final_states:
                if states[i] == finalStates[j]:
                    isFinal = True
                    break
                j += 1

            obj = self.__States(isFinal, isInitial, states[i])
            if obj.getInitialStatus():
                initialState_obj = obj
            stateObj.append(obj)
            i += 1

        return stateObj, initialState_obj

    def __set_transitions(self, file, stateObj, number_of_states):
        Transitions_tag = file.find('Transitions')
        number_of_trans = int(Transitions_tag.get('numberOfTrans'))
        transition_tags = Transitions_tag.find_all('transition')
        i = 0
        while i < number_of_trans:
            source = transition_tags[i].get('source')
            destination = transition_tags[i].get('destination')
            label = transition_tags[i].get('label')
            j = 0
            objs_found = 0
            destObj = self.__States()
            sourceObj = self.__States()
            while j < number_of_states and objs_found != 2:
                if stateObj[j].getName() == source:
                    sourceObj = stateObj[j]
                    objs_found += 1

                if stateObj[j].getName() == destination:
                    destObj = stateObj[j]
                    objs_found += 1
                j += 1

            sourceObj.setNextState(label, destObj)
            i += 1

    def __automata_acceptance(self, string, initialState_obj, alphabets):
        currentState = initialState_obj
        i = 0
        alph_exists = True
        trans_available = True
        while i < len(string):
            if string[i] not in alphabets:
                alph_exists = False
                break

            try:
                currentState = currentState.getNextState(string[i])

            except KeyError:
                trans_available = False
                break

            i += 1

        if currentState.getFinalStatus() and alph_exists and trans_available:
            print('The input string is accepted.')
        else:
            print('The input string is not accepted.')


automata = Automata()
automata.get_file('automata.xml')

while True:
    string = input('Enter a string(type "end" to exit): ')
    if string == 'end':
        break
    automata.check_input(string)
