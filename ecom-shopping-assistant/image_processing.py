from agno.media import Image
from agno.agent import Agent, RunResponse
from instructions import Instructions
from utils import getModel
from agno.utils.log import logger


class ProductImageProcessingAgent(Agent):
    """
    Agent responsible for identifying the product in an image and generating a text query.
    """

    def __init__(self, api_key: str):
        """
        Initializes the ProductImageProcessingAgent.

        Args:
            api_key (str): API key for the Gemini language model.
        """
        super().__init__(
            name="Product Image Processing",
            description="Identify the product in an image and generate a text query.",
            model=getModel("Gemini", api_key),
            instructions=Instructions.IMAGE_AGENT_INSTRUCTIONS,
            add_datetime_to_instructions=False,
        )

    def process_image(self, image_data) -> RunResponse:
        """
        Processes an image to identify the product and generate a text query.

        Args:
            image_data: The image data in bytes.

        Returns:
            RunResponse: The response from the language model, containing the generated text query.
        """
        logger.info("Processing image...")
        query = "Process the image to identify the product."

        response: RunResponse = self.run(query, images=[Image(content=image_data)])
        logger.info(f"Image processing response: {response.content}")
        return response
