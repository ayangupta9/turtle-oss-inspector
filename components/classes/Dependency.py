class Dependency:
    def __init__(
        self,
        file_path: str = None,
        package_name: str = None,
        package_url: str = None,
        vulnerabilities: list = [],
    ):
        self.file_path = file_path
        self.package_name = package_name
        self.package_url = package_url
        self.vulnerabilities = vulnerabilities
