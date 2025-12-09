#where main testing happens using giskard

from giskard.llm.generators.sycophancy import SycophancyDataGenerator
from giskard.llm.generators.toxicity import ToxicityDataGenerator
from giskard.llm.generators.prompt_injection import PromptInjectionDataGenerator

class ResponsibleAITestingTool:
    def generate_prompts(test_type: str, num_samples: int )-> list[str]:
        if test_type == "toxicity":
            generator = ToxicityDataGenerator(num_samples)
        elif test_type == "sycophancy":
            generator = SycophancyDataGenerator(num_samples)
        elif test_type == "prompt_injection":
            generator = PromptInjectionDataGenerator(num_samples)
        else:
            raise ValueError(f"The test type '{test_type}' is not supported.")
        
        dataset = generator.generate_dataset()

        prompts = [items["prompt"] for items in dataset.df.to_dict(orient="records")]

        return prompts
 