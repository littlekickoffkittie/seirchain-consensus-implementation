import unittest
from two_phase_commit import Coordinator, Participant

class TestTwoPhaseCommit(unittest.TestCase):

    def test_successful_commit(self):
        participants = [Participant("p1"), Participant("p2")]
        coordinator = Coordinator(participants)
        result = coordinator.execute_transaction()
        self.assertEqual(result, "Commit")
        for p in participants:
            self.assertTrue(p.committed)
            self.assertFalse(p.aborted)

    def test_failed_prepare(self):
        class FailingParticipant(Participant):
            def prepare(self):
                return False

        participants = [Participant("p1"), FailingParticipant("p2")]
        coordinator = Coordinator(participants)
        result = coordinator.execute_transaction()
        self.assertEqual(result, "Abort")
        self.assertFalse(participants[0].committed)
        self.assertTrue(participants[0].aborted)
        self.assertFalse(participants[1].committed)
        self.assertTrue(participants[1].aborted)

if __name__ == '__main__':
    unittest.main()
