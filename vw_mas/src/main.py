#!/usr/bin/env python
from vw_mas.crew import VwMasCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    VwMasCrew().crew().kickoff(inputs=inputs)