import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import random

class Arrange:
    def __init__ (self, filepath, semestercode, outpath):
        self.filepath       = filepath
        self.semestercode   = semestercode
        self.outpath        = outpath
        self.dataframe      = pd.read_csv(filepath)
        self.cleandata()
        self.semester1      = self.dataframe[self.dataframe['semester'].str.contains('1st')]
        self.semester2      = self.dataframe[self.dataframe['semester'].str.contains('2nd')]

    def cleandata(self):
        print("Cleaning Data... ")
        df  = self.getdataframe()
        
        df = df.fillna('undefined')

        df  = df[(df.payment == 'OK') | (df.payment == 'ok')]

        df = df.sort_values('token')
        df = df.reset_index()
        
        if not ('pc'        in df.columns):
            df['pc']        = ''
        if not('userid'     in df.columns):
            df['userid']    = ''
        if not('password'   in df.columns):
            df['password']  = ''
        if not('serial'     in df.columns):
            df['serial']    = range(1, len(df) + 1)
        if not('id'         in df.columns):
            print('There is not ID column present. Please reformat and try again.')
            exit(1)

        self.setdataframe(df)

    def getsectionwiseregistration(self):
        df1 = self.get1stsemester()
        df2 = self.get2ndsemester()
        print(len(df1))
        print(len(df2))
        print(len(self.dataframe))
        f, (ax1, ax2) = plt.subplots(ncols=2)
        f.suptitle('Section vs Registration ratio.', fontsize='16')
        
        df1.groupby('section').section.count().plot(ax=ax1, color='#1976D2', kind='bar')
        ax1.set_title('1st Semester (total: ' + str(df1.id.count()) + ')')

        df2.groupby('section').section.count().plot(ax=ax2, color='#1976D2', kind='bar')        
        ax2.set_title('2nd Semester (total: ' + str(df2.id.count()) + ')')
        
        plt.savefig(self.outpath + self.semestercode + '_registration_graph.png',
                    format='png')

    def planseat(self, nocomputer, roomcount, rooms, params, columncount=8, rowcount=5):
        print("Processing Data.. ")
        # distribute the students token wise without shuffling
        roomwisetoken = self.distributetoken(nocomputer, roomcount)
        
        # section wise registratin graph
        if 'registrationgraph' in params:
            self.getsectionwiseregistration()

        # make the seatrange csv
        if 'seatplanrange' in params:
            self.saveseatplanrange(roomwisetoken, rooms)

        # make tshirt room wise count
        if 'tshirtcount' in params:
            self.tshirtcountsave(roomwisetoken, rooms)
   
        # save roomwise seatplan
        if 'roomwise' in params:            
            self.shuffleseatarrangement(nocomputer, roomwisetoken)
            self.saveseatplanindividual(rooms, roomwisetoken)

        # return roomwisetoken

    def saveseatplanindividual(self, rooms, roomwisetoken):
        print("Saving seatplan for rooms.")
        with open(self.outpath + self.semestercode + '_seatplan.csv', 
                'w+', 
                newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            roomno = 0
            for room in roomwisetoken:
                writer.writerow([rooms[roomno]])
                roomno += 1
                writer.writerow(['Handle', 'Name', 'ID', 'Semester', 'Section', 'Token', 'Tshirt_Size', 'PC', 'USERID', 'PASSWORD'])
                for index, row in room.iterrows():
                    writer.writerow([str(room.loc[index]['name'])+'['+str(room.loc[index].id)+ ', ' + str(room.loc[index].semester)+'-'+str(room.loc[index].section) +'](' + str(room.loc[index].token) + ')',
                    room.loc[index]['name'], 
                    room.loc[index].id, 
                    room.loc[index].semester, 
                    room.loc[index].section, 
                    room.loc[index].token, 
                    room.loc[index].tshirt, 
                    room.loc[index].pc,
                    room.loc[index].userid,
                    room.loc[index].password])
    

    def sequential(self, rand, room, index):
        #there might be previous index might not be
        if int(room.iloc[0].name) < int(index):
            previousindex = index-1
            if previousindex in room.index and (int(room.loc[previousindex].pc) == rand+1 or int(room.loc[previousindex].pc) == rand-1):                
                return True
            #same semester and section
            # if previousindex in room.index and room.loc[previousindex].semester == room.loc[index].semester and room.loc[previousindex].section == room.loc[index].section:                
            #     return True
        return False


    def shuffleseatarrangement(self, computernumber, roomwisetoken):
        print("Re-arranging seating arrangement")
        roomno = 1 
        for room in roomwisetoken:
            assigned = []
            print("Working on room: " + str(roomno))
            roomno += 1
            # pcs = random.sample(range(1, computernumber+1), computernumber)
            # print(len(pcs))
            # i = 0            
            for index, row in room.iterrows():
                rand = random.randint(1, computernumber)
                sequencecount = 1
                while rand in assigned:
                    sequencecount += 1
                    rand = random.randint(1, computernumber)
                #     # print(assigned)
                #     # print(len(assigned))  
                #     # print(rand)
                #     # llln = input()
                room.at[index, 'pc'] = rand
                # i += 1
                assigned.append(rand)

    def distributetoken(self, nocomputer, roomcount):
        print("Distributing students to room according to number of rooms and number of computer per room.")
        df = self.getdataframe()
        roomwisetoken = []
        for i in range(roomcount):
            room = df[df.serial > i*nocomputer]
            room = room.loc[:(((i+1)*nocomputer)-1), :]
            roomwisetoken.append(room)
        return roomwisetoken


    def tshirtcountsave(self, roomwisetoken, rooms):
        print("Counting number of tshirt per room and save them.")
        with open(self.outpath + self.semestercode + '_tshirtcount.csv', 
                'w+', 
                newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(['Room', 'S', 'M', 'L', 'XL', 'XXL', 'Others', 'Total'])
            roomno = 0            
            for room in roomwisetoken:
                otherCount = room.serial.count() - (room.tshirt[room.tshirt == 'S'].count() + room.tshirt[room.tshirt == 'M'].count() + room.tshirt[room.tshirt == 'L'].count() + room.tshirt[room.tshirt == 'XL'].count() + room.tshirt[room.tshirt == 'XXL'].count())
                writer.writerow([rooms[roomno], room.tshirt[room.tshirt == 'S'].count(),
                 room.tshirt[room.tshirt == 'M'].count(),
                 room.tshirt[room.tshirt == 'L'].count(),
                 room.tshirt[room.tshirt == 'XL'].count(),
                 room.tshirt[room.tshirt == 'XXL'].count(),
                 otherCount,
                 room.id.count()])
                roomno += 1

    def saveseatplanrange(self, roomwisetoken, rooms):
        print("Saving seating range.")
        with open(self.outpath + self.semestercode + '_seat_rangeplan.csv', 
                'w+', 
                newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            roomno = 0
            writer.writerow(["Room", "From", "To"])
            for room in roomwisetoken:                              
                writer.writerow([rooms[roomno], room.iloc[0].token, room.iloc[-1].token])
                roomno += 1

    def getdataframe(self):
        return pd.DataFrame(self.dataframe)
    
    def get1stsemester(self):
        return pd.DataFrame(self.semester1)
    
    def get2ndsemester(self):
        return pd.DataFrame(self.semester2)

    def setdataframe(self, dataframe):
        self.dataframe = dataframe
    
    def set1stsemester(self, dataframe):
        self.semester1 = dataframe
    
    def set2ndsemester(self, dataframe):
        self.semester2 = dataframe
