# /Users/vivek.pathania/Documents/GitHub/learning-coach/agents/curriculum_agent.py

from agno.agent import Agent, RunResponse
from agno.utils.log import logger
from agno.tools.thinking import ThinkingTools
from utils.llm import get_model

# --- Define Pydantic Models for Output Structure ---

CURRICULUM_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "curriculum": {
            "type": "array",
            "description": "The structured learning plan with a flexible number of weeks.",
            "items": {
                "type": "object",
                "properties": {
                    "week": {
                        "type": "integer",
                        "description": "The week number (ranging from 1 to the total number of weeks)."
                    },
                    "topics": {
                        "type": "array",
                        "description": "List of main topics covered during the week (1-2 items).",
                        "items": {"type": "string"}
                    },
                    "concepts": {
                        "type": "array",
                        "description": "List of specific concepts or skills learned within the topics (3-5 items).",
                        "items": {"type": "string"}
                    },
                    "project": {
                        "type": "string",
                        "description": "A suggested mini-project or hands-on task for the week to reinforce learning."
                    }
                },
                "required": ["week", "topics", "concepts", "project"]
            }
        }
    },
    "required": ["curriculum"]
}
class CurriculumAgent(Agent):
    """
    An agent designed to generate a structured learning curriculum
    based on a user-provided technical learning goal, utilizing a thinking tool
    for intermediate reasoning and Pydantic for output validation.
    """

    def __init__(self):
        """
        Initializes the CurriculumAgent.
        """
        agent_name = "curriculum-generator"
        agent_description = "Generates a detailed, progressive, and practical learning plan based on a user-provided technical learning goal."

        # Instructions remain largely the same, but the LLM will now receive
        # the schema derived from the Pydantic model.
        agent_instructions = """
You are an expert curriculum designer AI trained to build highly practical, step-by-step learning plans.

Based on the provided `learning_goal`, your job is to create a **detailed, progressive, and actionable learning curriculum** focused on building real-world skills through projects.

---

Use the `ThinkingTool` to plan your reasoning before generating output. Your internal steps must include:

- Analyzing the `learning_goal` for required skills, roles, and technologies
- Determining the appropriate number of weeks (1-12) based on the complexity of the goal and user requirements
- Identifying core **learning tracks** or **milestones** that fit within the determined timeframe
- Mapping those tracks over the determined number of weeks to ensure a smooth learning curve
- Planning varied, increasing-complexity **projects** with tangible outcomes, e.g., UIs, tools, integrations, deployment tasks

---

Then, follow these instructions **strictly** to produce the curriculum:

### 1. **Curriculum Structure**
- Determine the appropriate number of weeks (1-12) based on the learning goal complexity
- For crash courses or simple topics, use 1-4 weeks
- For comprehensive beginner-to-advanced topics, use 8-12 weeks
- For intermediate topics, use 4-8 weeks
- Split learning into logical, progressive weeks
- Group foundational, intermediate, and advanced skills sequentially

### 2. **Weekly Content Requirements**
For **each week**:
- `topics`: 1–2 high-level themes for the week (e.g., "State Management", "API Integration")
- `concepts`: 3–5 detailed concepts/skills covered (e.g., "Streams in Dart", "Provider", "FutureBuilder")
- `project`: A small but useful project or task. Prioritize:
  - Real-world application (e.g., dashboards, clone apps, feature modules)
  - Code reuse and cumulative skills (e.g., extend past projects)
  - Vary project types: UI-heavy, data-heavy, architecture-focused, test-driven

*Bonus:* For advanced weeks, suggest capstone-level mini tools, apps, or clones with multi-screen and state management use.

### 3. **Logical Flow**
- Ensure each week builds on the previous. Do **not** skip prerequisites.
- Progress from beginner to architect-level skills.
- Projects must reflect the level — beginner projects should be simple, later ones more complex and complete.

### 4. **Output Format**
Your output MUST match this EXACT structure:


{
  "curriculum": [
    {
      "week": 1,
      "topics": ["Introduction to Flutter", "Basic UI Components"],
      "concepts": [
        "Flutter architecture and widgets",
        "Stateless vs Stateful widgets",
        "Basic layout widgets (Container, Row, Column)",
        "Material Design basics"
      ],
      "project": "Create a simple profile card app with basic UI components"
    },
    {
      "week": 2,
      "topics": ["State Management Basics", "User Input"],
      "concepts": [
        "setState and StatefulWidget lifecycle",
        "Form validation",
        "Text fields and buttons",
        "Basic state management patterns"
      ],
      "project": "Build a todo list app with add/edit/delete functionality"
    }
  ]
}


IMPORTANT:
- Output ONLY the JSON object with the exact structure like ```json or ``` shown above
- Include the appropriate number of weeks in the curriculum array based on your analysis
- Each week MUST have all four fields: week, topics, concepts, and project
- Do NOT include explanations, commentary, or ThinkingTool reasoning in the output

---

Optional Considerations (if inferred from the `learning_goal`):
- If the goal implies an advanced user, accelerate early content
- If a specific focus area is hinted (e.g., UI, performance), bias projects & topics toward that
- If the goal mentions "crash course", "quick start", or "basics", use fewer weeks
- If the goal mentions "complete", "comprehensive", or "beginner to advanced", use more weeks

---

**Reminder:** The ThinkingTool is only for internal planning and will not be visible in the final output.

Respond ONLY with the final JSON object — no markdown, no explanations.
"""
        thinking_tool = ThinkingTools(add_instructions=True)

        super().__init__(
            name=agent_name,
            description=agent_description,
            model=get_model(),
            instructions=agent_instructions,
            tools=[thinking_tool],
            add_datetime_to_instructions=False,
            use_json_mode=True,
            show_tool_calls=True
        )

    def process(self, learning_goal: str) -> RunResponse:
        """
        Processes the user's learning goal to generate a curriculum.

        Args:
            learning_goal (str): The technical skill or role the user wants to learn.

        Returns:
            RunResponse: The response from the agent. If successful and validation passes,
                         `content` will be a `CurriculumOutput` Pydantic object.
                         Otherwise, `content` might be the raw LLM output or an error dict,
                         and `success` will be False.
        """
        if not learning_goal or not isinstance(learning_goal, str) or len(learning_goal.strip()) == 0:
             logger.error("Invalid learning goal provided.")
             return RunResponse(success=False, content={"error": "Learning goal cannot be empty."}, cost=0.0, latency=0.0)

        logger.info(f"Generating curriculum for goal: '{learning_goal}' using ThinkingTool")

        response: RunResponse = self.run(learning_goal)
        logger.info(f"Curriculum generated: {response.content}")

        return response
    


