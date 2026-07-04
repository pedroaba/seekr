class UnknownOperationalSystemError(EnvironmentError):
    def __init__(self, operational_system):
        super().__init__(f"Failed to recognize the operational system "
                         f"({operational_system})")
