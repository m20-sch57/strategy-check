import server.structures as structures
import sqlite3

DatabasePath = 'database.db'

class Storage:
    def __init__(self):
        self.connection = sqlite3.connect(DatabasePath, check_same_thread=False)
        self.cursor = self.connection.cursor()
        structures.createUsersTable(self.cursor)
        structures.createProblemsTable(self.cursor)
        structures.createSubmissionsTable(self.cursor)
        structures.createTournamentsTable(self.cursor)
        structures.createMessagesTable(self.cursor)
        self.connection.commit()

    def getSize(self, tableName):
        self.cursor.execute('SELECT COUNT (*) FROM ' + tableName)
        size = self.cursor.fetchone()
        return size[0]

    def getUsersCount(self):
        return self.getSize('users')

    def getProblemsCount(self):
        return self.getSize('problems')

    def getSubmissionsCount(self):
        return self.getSize('submissions')

    def getTournamentsCount(self):
        return self.getSize('tournaments')

    def getMessagesCount(self):
        return self.getSize('messages')

    def updateId(self, obj, tableName):
        if (obj.id == -1):
            size = self.getSize(tableName)
            obj.id = size

    def getUser(self, id):
        return structures.getUser(self.cursor, id)

    def getProblem(self, id):
        return structures.getProblem(self.cursor, id)

    def getSubmission(self, id):
        return structures.getSubmission(self.cursor, id)

    def getTournament(self, id):
        return structures.getTournament(self.cursor, id)

    def getMessage(self, id):
        return structures.getMessage(self.cursor, id)

    def getUserByName(self, username):
        return structures.getUserByName(self.cursor, username)

    def getProblemByName(self, name):
        return structures.getProblemByName(self.cursor, name)

    def getAllUsers(self):
        return structures.getAllUsers(self.cursor)

    def saveUser(self, user):
        self.updateId(user, 'users')
        user.save(self.cursor)
        self.connection.commit()
        return user.id

    def saveProblem(self, problem):
        self.updateId(problem, 'problems')
        problem.save(self.cursor)
        self.connection.commit()
        return problem.id

    def saveSubmission(self, submission):
        self.updateId(submission, 'submissions')
        submission.save(self.cursor)
        self.connection.commit()
        return submission.id

    def saveTournament(self, tournament):
        self.updateId(tournament, 'tournaments')
        tournament.save(self.cursor)
        self.connection.commit()
        return tournament.id

    def saveMessage(self, message):
        self.updateId(message, 'messages')
        message.save(self.cursor)
        self.connection.commit()
        return message.id

    def getProblemset(self):
        response = structures.getProblemset(self.cursor)
        dictResponse = [
            {'id' : response[i][0], 'name' : response[i][1]}
            for i in range(len(response))
        ]
        return dictResponse

    def getSubmissionListU(self, userId):
        return structures.getSubmissionListU(self.cursor, userId)

    def getSubmissionListUP(self, userId, probId):
        return structures.getSubmissionListUP(self.cursor, userId, probId)

    def getCertainField(self, tableName, id, fieldName):
        return structures.getCertainField(self.cursor, tableName, id, fieldName)

    def getSubDict(subId, probName):
        return structures.getSubDict(self.cursor, subId, probName)

class Status:
    def __init__(self):
        self.runningTournament = False # don't change them manually, call special functions
        self.runningTournamentId = -1
    
    def tournamentStarted(self, tournamentId: int) -> None:
        self.runningTournament = True
        self.runningTournamentId = tournamentId

    def tournamentStopped(self, tournamentId: int) -> None:
        if self.runningTournamentId == tournamentId:
            self.runningTournament = False
            self.runningTournamentId = -1
        else:
            raise ValueError("Invalid tournament Id")

    def RunningTournament(self) -> bool:
        return self.runningTournament

storage = Storage()
status = Status()
