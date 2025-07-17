class Participant:
    def __init__(self, name):
        self.name = name
        self.prepared = False
        self.committed = False
        self.aborted = False

    def prepare(self):
        # In a real system, this would involve locking resources
        self.prepared = True
        return True

    def commit(self):
        if self.prepared:
            self.committed = True
            return True
        return False

    def abort(self):
        self.aborted = True
        return True

class Coordinator:
    def __init__(self, participants):
        self.participants = participants

    def execute_transaction(self):
        # Phase 1: Prepare
        prepared_participants = []
        try:
            for p in self.participants:
                if not p.prepare():
                    raise Exception("Participant failed to prepare")
                prepared_participants.append(p)
        except Exception:
            self.abort_transaction(self.participants)
            return "Abort"

        # Phase 2: Commit
        if len(prepared_participants) == len(self.participants):
            self.commit_transaction(prepared_participants)
            return "Commit"
        else:
            self.abort_transaction(prepared_participants)
            return "Abort"


    def commit_transaction(self, participants):
        for p in participants:
            p.commit()

    def abort_transaction(self, participants):
        for p in participants:
            p.abort()
