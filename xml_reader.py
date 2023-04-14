import xml.etree.ElementTree as ET
import time
import os

class DFA:
    def __init__(self, filename):
        self.alphabets = []
        self.current_state = None
        self.final_states = []
        self.transitions = {}

        # Load the XML file
        tree = ET.parse(filename)
        root = tree.getroot()

        # Get the alphabets
        for elem in root.iter('alphabet'):
            self.alphabets.append(elem.attrib['letter'])

        # Get the initial state
        for elem in root.iter('initialState'):
            self.current_state = elem.attrib['name']

        # Get the final states
        for elem in root.iter('finalState'):
            self.final_states.append(elem.attrib['name'])

        # Get the transitions
        for elem in root.iter('transition'):
            source_state = elem.attrib['source']
            label = elem.attrib['label']
            destination_state = elem.attrib['destination']
            if source_state not in self.transitions:
                self.transitions[source_state] = {}
            self.transitions[source_state][label] = destination_state

    def simulate(self, input_str, verbose=True, animate=True):
        current_state = self.current_state
        for ch in input_str:
            if ch not in self.alphabets:
                return False
            if current_state not in self.transitions or ch not in self.transitions[current_state]:
                return False
            current_state = self.transitions[current_state][ch]
            if verbose:
                os.system('clear' if os.name == 'posix' else 'cls')  # Clear the screen
                print(f"Processing input string: {input_str}")
                print(f"Current state: {current_state}")
            if animate:
                print("\033[2J")  # Clear the screen
                print(f"Processing input string: {input_str}")
                print(f"Current state: {current_state}")
                time.sleep(0.5)  
        return current_state in self.final_states


    def print_table(self):
        print("{:<15}{:<15}{:<15}".format("", *self.alphabets))
        for state in self.transitions:
            row = "{:<15}".format(state)
            for alphabet in self.alphabets:
                row += "{:<15}".format(self.transitions[state].get(alphabet, "-"))
            if state in self.final_states:
                row += " Final"
            if state == self.current_state:
                row += " Current"
            print(row)

    def interactive_mode(self):
        print("Entering interactive mode...\n")
        while True:
            self.print_table()
            print("\nCurrent state:", self.current_state)
            user_input = input("Enter input string ('q' to quit): ")
            if user_input == 'q':
                break
            is_accepted = self.simulate(user_input)
            if is_accepted:
                print("\033[92m" + f"The '{user_input}' string is accepted." + "\033[0m")  # Print in green
            else:
                print("\033[91m" + f"The '{user_input}' string is not accepted." + "\033[0m")  # Print in red

    def batch_mode(self):
        input_strings = []
        while True: 
            inp = input("Enter your strings please : (write 'EXIT' to end) ")
            if inp == 'EXIT': 
                break
            else:
                input_strings.append(inp)

        print("Running DFA in batch mode...\n")
        for input_str in input_strings:
            is_accepted = self.simulate(input_str)
            if is_accepted:
                print("\033[92m" + f"The '{input_str}' string is accepted." + "\033[0m")  # Print in green
                time.sleep(1)
            else:
                print("\033[91m" + f"The '{input_str}' string is not accepted." + "\033[0m")  # Print in red
                time.sleep(1)
        
        
def hello_animation():
    print("\033[2J") # clear the screen
    print("\033[1;32;40m" + "     HELLO!" + "\033[0m") # print the text in green
    time.sleep(1) # pause for 1 second
    print("\033[2J") # clear the screen
    print("\033[1;33;40m" + "   WELCOME!" + "\033[0m") # print the text in yellow
    time.sleep(1) # pause for 1 second
    print("\033[2J") # clear the screen
    print("\033[1;34;40m" + "    TO " + "\033[0m") # print the text in blue
    time.sleep(1) # pause for 1 second
    print("\033[2J") # clear the screen
    print("\033[1;35;40m" + "   DFA IMPLANT" + "\033[0m") # print the text in magenta
    time.sleep(1) # pause for 1 second
    print("\033[2J") # clear the screen
    print("\033[1;36;40m" + "   USING .XML FILE!" + "\033[0m") # print the text in cyan
    time.sleep(1) # pause for 1 second
    print("\033[2J") # clear the screen
            
hello_animation()

x = DFA("example.xml")
x.batch_mode()


frames = [    "Goodbye!",    "Thank you for using my program",    "Made with ❤️",]

def animate():
    for frame in frames:
        print("\033c")  # Clear the screen
        print(frame.center(50))
        time.sleep(1)

animate()
