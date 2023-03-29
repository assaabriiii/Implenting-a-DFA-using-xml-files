import xml.etree.ElementTree as ET

# Load the XML file
tree = ET.parse('example.xml')
root = tree.getroot()

# Get the alphabets
alphabets = []
for elem in root.iter('alphabet'):
    alphabets.append(elem.attrib['letter'])

# Get the initial state
current_state = None
for elem in root.iter('initialState'):
    current_state = elem.attrib['name']

# Get the final states
final_states = []
for elem in root.iter('finalState'):
    final_states.append(elem.attrib['name'])

# Get the transitions
transitions = {}
for elem in root.iter('transition'):
    source_state = elem.attrib['source']
    label = elem.attrib['label']
    destination_state = elem.attrib['destination']
    if source_state not in transitions:
        transitions[source_state] = {}
    transitions[source_state][label] = destination_state

# Define a function to simulate the DFA on a string input
def simulate_dfa(input_str):
    global current_state
    for ch in input_str:
        if ch not in alphabets:
            return False
        if current_state not in transitions or ch not in transitions[current_state]:
            return False
        current_state = transitions[current_state][ch]
    return current_state in final_states




