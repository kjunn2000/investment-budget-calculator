from engine_lambda.main import handler
import json
import os

def main():
    input_path = os.path.join(os.path.dirname(__file__), 'input.json')
    with open(input_path, "r") as file:
        input_data = json.load(file)

    event = {"body": input_data}
    response = handler(event, {})
    
    output_path = os.path.join(os.path.dirname(__file__), 'output.json')
    with open(output_path, "w") as file:
        json.dump(response, file, indent=4)

    print(f"Response written to {output_path}")

if __name__ == "__main__":
    main()
    