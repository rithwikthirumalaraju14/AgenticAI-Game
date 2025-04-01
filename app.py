import json
from pathlib import Path
from typing import Iterator

from agno.agent import Agent, RunResponse
from agno.models.groq import Groq
from agno.run.response import RunEvent
from agno.storage.workflow.sqlite import SqliteWorkflowStorage
from agno.utils.log import logger
from agno.utils.pprint import pprint_run_response
from agno.utils.string import hash_string_sha256
from agno.utils.web import open_html_file
from agno.workflow import Workflow
from pydantic import BaseModel, Field

games_dir = Path(__file__).parent.joinpath("games")
games_dir.mkdir(parents=True, exist_ok=True)
game_output_path = games_dir / "unicorn.html"
game_output_path.unlink(missing_ok=True)


class GameOutput(BaseModel):
    reasoning: str = Field(..., description="Explain your reasoning")
    code: str = Field(..., description="The html5 code for the game")
    instructions: str = Field(..., description="Instructions how to play the game")


class QAOutput(BaseModel):
    reasoning: str = Field(..., description="Explain your reasoning")
    correct: bool = Field(False, description="Does the game pass your criteria?")


class GameGenerator(Workflow):
    # This description is only used in the workflow UI
    description: str = "Generator for single-page HTML5 games"

    game_developer: Agent = Agent(
        name="Game Developer Agent",
        description="You are a game developer that produces working HTML5 code.",
        model=Groq(id="llama-3.3-70b-versatile"),
        instructions=[
            "Create a game based on the user's prompt. "
            "The game should be HTML5, completely self-contained and must be runnable simply by opening on a browser",
            "Ensure the game has a alert that pops up if the user dies and then allows the user to restart or exit the game.",
            "Ensure instructions for the game are displayed on the HTML page."
            "Use user-friendly colours and make the game canvas large enough for the game to be playable on a larger screen.",
        ],
        response_model=GameOutput,
    )

    qa_agent: Agent = Agent(
        name="QA Agent",
        model=Groq(id="llama-3.3-70b-versatile"),
        description="You are a game QA and you evaluate html5 code for correctness.",
        instructions=[
            "You will be given some HTML5 code."
            "Your task is to read the code and evaluate it for correctness, but also that it matches the original task description.",
        ],
        response_model=QAOutput,
    )

    def run(self, game_description: str) -> Iterator[RunResponse]:
        logger.info(f"Game description: {game_description}")

        game_output = self.game_developer.run(game_description)

        if (
            game_output
            and game_output.content
            and isinstance(game_output.content, GameOutput)
        ):
            game_code = game_output.content.code
            logger.info(f"Game code: {game_code}")
        else:
            yield RunResponse(
                run_id=self.run_id,
                event=RunEvent.workflow_completed,
                content="Sorry, could not generate a game.",
            )
            return

        logger.info("QA'ing the game code")
        qa_input = {
            "game_description": game_description,
            "game_code": game_code,
        }
        qa_output = self.qa_agent.run(json.dumps(qa_input, indent=2))

        if qa_output and qa_output.content and isinstance(qa_output.content, QAOutput):
            logger.info(qa_output.content)
            if not qa_output.content.correct:
                raise Exception(f"QA failed for code: {game_code}")

            # Store the resulting code
            game_output_path.write_text(game_code)

            yield RunResponse(
                run_id=self.run_id,
                event=RunEvent.workflow_completed,
                content=game_output.content.instructions,
            )
        else:
            yield RunResponse(
                run_id=self.run_id,
                event=RunEvent.workflow_completed,
                content="Sorry, could not QA the game.",
            )
            return


# Run the workflow if the script is executed directly
if __name__ == "__main__":
    from rich.prompt import Prompt

    game_description = Prompt.ask(
        "[bold]Describe the game you want to make (keep it simple)[/bold]\n",
        # default="An asteroids game."
        default="The player must connect a power source to different lights by rotating and rearranging electrical circuit pieces on a grid. The goal is to complete the circuit before time runs out. Some tiles are locked in place, while others can be rotated or swapped. As the game progresses, new mechanics like splitters, switches, and faulty wires are introduced, making puzzles more challenging",
    )

    hash_of_description = hash_string_sha256(game_description)

    # Initialize the investment analyst workflow
    game_generator = GameGenerator(
        session_id=f"game-gen-{hash_of_description}",
        storage=SqliteWorkflowStorage(
            table_name="game_generator_workflows",
            db_file="tmp/workflows.db",
        ),
    )

    # Execute the workflow
    result: Iterator[RunResponse] = game_generator.run(
        game_description=game_description
    )

    # Print the report
    pprint_run_response(result)

    if game_output_path.exists(): 
        open_html_file(game_output_path)
