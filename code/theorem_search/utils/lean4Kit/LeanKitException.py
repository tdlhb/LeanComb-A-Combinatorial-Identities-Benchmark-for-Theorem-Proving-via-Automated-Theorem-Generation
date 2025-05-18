

class TheoremInitException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class TacticApplyException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class ProofStateException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class InteractiveTimeoutException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class VerificationFailedException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class InteractiveEOFException(Exception):
    def __init__(self, *args):
        super().__init__(*args)