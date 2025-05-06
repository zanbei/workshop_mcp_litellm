

from dotenv import load_dotenv
from crewai_tools.crew import SimpleCrew

load_dotenv()

def get_travel_advice(city):
    action_input = {"query": f"I want to travel to {city} on May 1st, 2025, what is the travel advice?"}
    try:
        response = SimpleCrew().crew().kickoff(inputs=action_input)
        print(f"Travel advice for {city}:", response)
    except Exception as e:
        print(f"Error running crew for {city}: {e}")

def run():
    cities = ["Copenhagen", "Beijing", "Berlin", "Paris", "Phuket", "Shanghai"]
    print("Please select a city from the following list:")
    for i, city in enumerate(cities, 1):
        print(f"{i}. {city}")

    choice = input("Enter the number of your choice: ")
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(cities):
            selected_city = cities[choice_index]
            get_travel_advice(selected_city)
        else:
            print("Invalid selection. Please run the program again and select a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number corresponding to the city.")

if __name__ == "__main__":
    run()
