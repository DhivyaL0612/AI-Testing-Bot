# FILE: testing_tool.py

# Import the main Harness class from langtest
from langtest import Harness

class ResponsibleAITestingTool:
    """
    This class now uses the 'langtest' library to generate test prompts.
    It's lighter and more reliable for deployment.
    """

    def generate_prompts(self, test_type: str, num_samples: int = 5) -> list[str]:
        """
        Creates a list of test prompts for a specified test type using langtest.

        Args:
            test_type: The name of the test to run (e.g., 'toxicity').
            num_samples: The number of unique prompts to generate.

        Returns:
            A list of strings, where each string is a ready-to-use prompt.
        """
        print(f"Generating prompts for '{test_type}' test using langtest...")

        # 1. Create a langtest "Harness". This is the main object.
        # We point it to a dummy task and model since we only want to generate prompts.
        harness = Harness(
            task="text-generation",
            model={"model": "gpt-3.5-turbo", "hub": "openai"},
            data=[{"text": "dummy"}] # Dummy data
        )

        # 2. Configure the test we want to run.
        # Langtest uses the .configure() method to set up the test.
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

        # 3. Generate the test cases.
        harness.generate()

        # 4. Extract the prompts from the generated data.
        # Langtest stores the generated prompts in a slightly different structure.
        # The .generated_results attribute holds the results.
        test_results = harness.generated_results()

        prompts = []
        # We loop through the results to find our specific test type.
        for result in test_results:
            if result['test_type'] == test_type:
                # 'test_cases' is a list of dictionaries. We want the 'test_case' value.
                for item in result['test_cases']:
                    prompts.append(item['test_case'])
        
        # We only need the number of samples requested.
        return prompts[:num_samples]

