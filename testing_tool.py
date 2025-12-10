# FILE: testing_tool.py

from langtest import Harness

class ResponsibleAITestingTool:
    """
    This class uses the 'langtest' library to generate test prompts.
    It is lighter and more reliable for deployment than Giskard.
    """

    def generate_prompts(self, test_type: str, num_samples: int = 5) -> list[str]:
        """
        Creates a list of test prompts using langtest.
        """
        print(f"Generating prompts for '{test_type}' test using langtest...")

        # Create a langtest "Harness".
        # The model and data are just placeholders to satisfy the constructor.
        # We never actually run the model here, so no API keys are used.
        harness = Harness(
            task="text-generation",
            model={"model": "bert-base-uncased", "hub": "huggingface"},
            data=[{"text": "dummy"}]
        )

        # Configure the test we want to run.
        harness.configure(
            {
                "tests": {
                    "defaults": {"min_pass_rate": 1.0},
                    "robustness": {
                        test_type: {"min_pass_rate": 1.0}
                    }
                }
            }
        )

        # Generate the test cases.
        harness.generate()

        # Extract the prompts from the generated data.
        test_results = harness.generated_results()

        prompts = []
        for result in test_results:
            if result['test_type'] == test_type:
                for item in result['test_cases']:
                    prompts.append(item['test_case'])
        
        # Return the requested number of samples.
        return prompts[:num_samples]

