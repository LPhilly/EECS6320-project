import os
import sys

path = "/home/frabbi/Desktop/projects/fairness_testing_code_generation/fairness_test/test_suites"

for filename in os.listdir(path):
    if filename.endswith('.py'):
        print(filename)
        with open(os.path.join(path, filename), 'r') as file:
            content = file.read()
            content = content.replace("indian", "american indian")
            print(content)
            print("---------------------------------------------------")
        with open(os.path.join(path, filename), 'w') as file:
            file.write(content)