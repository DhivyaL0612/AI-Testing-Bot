# testing_tool.py

# We import the prompt generators from the giskard library
from giskard.llm.generators.sycophancy import SycophancyDataGenerator
from giskard.llm.generators.toxicity import ToxicityDataGenerator
from giskard.llm.generators.prompt_injection import PromptInjectionDataGenerator

class ResponsibleAITestingTool:
    """
    This class is a toolkit for generating test prompts.
    Its only job is to create lists of prompts for different test types.
    """
    def generate_prompts(self, test_type: str, num_samples: int = 5):
        """
        The main function of this class.
        
        Args:
            test_type (str): The type of test (e.g., 'toxicity').
            num_samples (int): How many prompts to create.

        Returns:
            A list of prompt strings.
        """
        print(f"Generating {num_samples} prompts for '{test_type}' test...")

        # We select the correct generator based on the test_type
        if test_type == "toxicity":
            generator = ToxicityDataGenerator(num_samples=num_samples)
        elif test_type == "sycophancy":
            generator = SycophancyDataGenerator(num_samples=num_samples)
        elif test_type == "prompt_injection":
            generator = PromptInjectionDataGenerator(num_samples=num_samples)
        else:
            # If we ask for a test that doesn't exist, raise an error.
            raise ValueError(f"Unknown test type: {test_type}")
        
        # This runs the generator and creates a dataset object.
        dataset = generator.generate_dataset()
        
        # We extract just the 'prompt' column from the dataset and return it as a simple list.
        prompts = [item["prompt"] for item in dataset.df.to_dict(orient="records")]
        return prompts

