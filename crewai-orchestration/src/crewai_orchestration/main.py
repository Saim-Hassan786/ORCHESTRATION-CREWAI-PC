from crewai.flow.flow import Flow, start, listen
from litellm import completion
from dotenv import load_dotenv, find_dotenv
from crewai_orchestration.crews.teaching_crew import TeachingCrew

_:bool = load_dotenv(find_dotenv())

class Panaflow(Flow):

    @start()
    def generate_topic(self):
        response = completion(
            model = "gemini/gemini-2.0-flash-exp",
            messages = [
                {"role": "user",
                 "content": "Generate a  single topic for a blog post about the latest trends in technology."}
            ]
        )
        self.state["topic"] = response["choices"][0]["message"]["content"]
        print(f"Generated topic: {self.state['topic']}")

    @listen(generate_topic)
    def teach_topic(self):
        result = TeachingCrew().crew().kickoff(
            inputs = {"topic": self.state.topic}
        )
        print(result) 
        
def flow_init():
    flow = Panaflow()
    flow.kickoff()

    

