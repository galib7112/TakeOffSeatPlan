## Script for making seating plans of Take Off Programming Contest.

### Requirement
* Python 3.6

### Installation
* Download the repository from git using git
> `git clone https://github.com/mehedi-shafi/TakeOffSeatPlan.git`
* or Download as zip.
* Installed required libraries using pip
> `pip install -r requirements.txt`

### Usage 
* Copy the response data csv to _raw/_ directory
* Open __conf.json__ file and edit necessary variables. Required ones are
    * `semester` [current semester id]
    * `participant_count` [total number of participant confirmed]
    * `input` [input csv path]
    * `number_rooms` [Number of rooms required]
    * `number_seat_per_room` [Number of marked computers each room]
    * > make sure you maintain the required room and computer count accordingly
* You can leave the non-required configurations in __conf.json__ as they are.
* > MAKE SURE NO FIELDS ARE NAN. If you leave them they will be defined as 'UD' by the system.
* Rename the headers in of the __csv__ files to following
    * time
    * name
    * email
    * mobile
    * mobile2
    * campus
    * department
    * semester
    * section
    * tshirt
    * id
    * payment
    * token
* **This step is important. If you don't rename the header accordingly script will fail**
* Run the script.
> `python main.py`
* After running you should find necessary output files in _outputs_ folder.