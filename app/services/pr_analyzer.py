class PRContractAnalyzer:

    def __init__(self):
        self.loader = GitSchemaLoader()
        self.diff_engine = DiffEngine()

    def analyze(self):

        # 1. MAIN schema (baseline)
        base_schema = self.loader.load_main()

        # 2. PR schema (current state)
        pr_schema = self.loader.load_pr()

        # 3. Diff
        result = self.diff_engine.compare(base_schema, pr_schema)

        return result