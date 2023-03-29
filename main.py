from xml_reader import simulate_dfa 
from os import system


while True : 
    input_str = str(input("Enter your string -> "))
    if simulate_dfa(input_str):
        print(f"'{input_str}' is ACCEPTED by the given DFA")
        system("sleep 2")
        system("clear")
    elif input_str == "exit":
        print("Goodbye ")
        break  
    else:
        print(f"'{input_str}' is NOT ACCEPTED by the given DFA")
        system("sleep 2")
        system("clear")