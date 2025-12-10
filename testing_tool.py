# FILE: testing_tool.py

# We need to import the specific prompt-generating tools from the Giskard library.
from giskard.llm.generators.sycophancy import SycophancyDataGenerator
from giskard.llm.generators.toxicity import ToxicityDataGenerator
from giskard.llm.generators.prompt_injection import PromptInjectionDataGenerator

# We will structure our code inside a class to keep it organized.
class ResponsibleAITestingTool:
    """
    This class acts as a dedicated tool for generating test prompts.
    It does not know about browsers or AI models; it only creates prompts.
    """

    # This is the main function of our class. It will be called by our orchestrator.
    def generate_prompts(self, test_type: str, num_samples: int = 5) -> list[str]:
        """
        Creates a list of test prompts for a specified test type.

        Args:
            test_type: The name of the test to run (e.g., 'toxicity').
            num_samples: The number of unique prompts to generate.

        Returns:
            A list of strings, where each string is a ready-to-use prompt.
        """
        print(f"Generating {num_samples} prompts for '{test_type}' test...")

        # This 'if/elif/else' block acts as a switch to select the correct
        # generator tool from Giskard based on the input 'test_type'.
        if test_type == "toxicity":
            generator = ToxicityDataGenerator(num_samples=num_samples)
        elif test_type == "sycophancy":
            generator = SycophancyDataGenerator(num_samples=num_samples)
        elif test_type == "prompt_injection":
            generator = PromptInjectionDataGenerator(num_samples=num_samples)
        else:
            # It's good practice to handle unknown inputs to prevent errors.
            raise ValueError(f"The test type '{test_type}' is not supported.")

        # This line tells the selected Giskard generator to do its work.
        dataset = generator.generate_dataset()

        # The result from Giskard is a dataset object. We need to extract just the
        # prompts from it and return them as a simple Python list of strings.
        prompts = [item["prompt"] for item in dataset.df.to_dict(orient="records")]
        return prompts
