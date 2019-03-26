import json
from src.arrange import Arrange
import os.path

def validateconfiguration(config):
    validated = True
    if not os.path.isfile(config['input']):
        print('Input file does not exist')
        validated = False
    if (config['number_rooms'] - 1) * config['number_seat_per_room'] > config['participant_count']:
        validated = False
        print('Number of room allocated according to number of seat per room exceeds requirement')
        print('Please adjust the number of rooms and number of seat per room')
    if len(config["params"]) < 1:
        print('Add at least one parameter in configuration')
        validated = False
    if not validated:
        exit(1)

if __name__ == '__main__':    
    with open('conf.json', 'r') as file:
        configuration = json.load(file)
    validateconfiguration(configuration)
    planner = Arrange(configuration['input'],
                    configuration['semester'],
                    configuration['outpath'])
    planner.planseat(configuration['number_seat_per_room'],
                    configuration['number_rooms'],
                    configuration['room_numbers'],
                    configuration['params'])
