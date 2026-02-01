#!/usr/bin/env python
from crewai.flow.flow import Flow, listen, start
from flow_exp_orches.crews.poem_crew.poem_crew import TeachingCrew
from litellm import completion
from dotenv import load_dotenv, find_dotenv



class Panaflow(Flow):

    @start()
    def generate_topic(self):
        response = completion(
            model = "gemini/gemini-2.0-flash-exp",
            messages = [
                {"role": "user",
                 "content": "Generate a single topic for a blog post about the current politics of USA."}
            ]
        )
        self.state["topic"] = response["choices"][0]["message"]["content"]
        print(f"Generated topic: {self.state['topic']}")


    @listen(generate_topic)
    def teach_topic(self):
        print("Starting teaching")
        result = (
            TeachingCrew()
            .crew()
            .kickoff(inputs={"topic": self.state["topic"]})
        )

        print("Tutorial generated", result.raw)
        self.state["topic"] = result.raw

    @listen(teach_topic)
    def save_poem(self):
        print("Saving Tutorial")
        with open("Teaching.txt", "w") as f:
            f.write(self.state["topic"])


def kickoff():
    teach = Panaflow()
    teach.kickoff()


# def plot():
#     poem_flow = PoemFlow()
#     poem_flow.plot()


# if __name__ == "__main__":
#     kickoff()
