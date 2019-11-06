import jinja2
import json

from dataclasses import dataclass, field
from typing import List

from gherkin.parser import Parser
from gherkin.pickles.compiler import compile

template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
TEMPLATE_FILE = "template.cpp"
template = template_env.get_template(TEMPLATE_FILE)


@dataclass
class Test:
    given: str
    whens: [str]
    thens: [str]


@dataclass
class Scenario:
    name: str
    tests: [Test]
    tag: str = ""


def parse_file(filename):
    with open(filename, "r") as f:
        content = f.read()
        parser = Parser()
        doc = parser.parse(content)
        print(json.dumps(doc, indent=2))

        if "feature" not in doc:
            return []

        feature = doc["feature"]
        scenarios = []
        for child in feature["children"]:
            tests = []
            given = ""
            whens = []
            thens = []
            for step in child["steps"]:
                step_text = step["text"].replace('"', '\\"')
                if "Given" in step["keyword"]:
                    given = step_text

                if "When" in step["keyword"]:
                    whens.append(step_text)

                if "Then" in step["keyword"]:
                    thens.append(step_text)

            tests.append(Test(given, whens, thens))
            scenarios.append(Scenario(name=child["name"], tests=tests))
        return scenarios


scenarios = parse_file("example.feature")
generated = template.render(scenarios=scenarios)
print(generated)
