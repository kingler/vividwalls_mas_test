from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class VwMasCrew(CrewBase):
    """VwMas crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def marketing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['marketing_agent'],
            tools=[],
            verbose=True,
            allow_delegation=True
        )

    @agent
    def notion_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['notion_agent'],
            tools=[],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def campaign_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['campaign_agent'],
            tools=[],
            verbose=True,
            allow_delegation=True
        )

    @agent
    def content_strategy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['content_strategy_agent'],
            tools=[],
            verbose=True,
            allow_delegation=True
        )
        
    @agent
    def market_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['market_research_agent'],
            tools=[],
            verbose=True,
            allow_delegation=False
        )
        
    @agent
    def social_media_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_agent'],
            tools=[],
            verbose=True,
            allow_delegation=True
        )
    
    @agent
    def facebook_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['facebook_agent'],
            tools=[],
            verbose=True,
            allow_delegation=False
        )
        
    @agent
    def instagram_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['instagram_agent'],
            tools=[],
            verbose=True
        )
        
    @agent
    def linkedin_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_agent'],
            tools=[],
            verbose=True,
            allow_delegation=False
        )
        
    @agent
    def pinterest_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['pinterest_agent'],
            tools=[],
            verbose=True
            allow_delegation=False
        )
        
    @agent
    def content_writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['content_writer_agent'],
            tools=[],
            verbose=True
            allow_delegation=False
        )
    
    @task
    def campaign_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['campaign_agent_task'],
        )

    @task
    def content_strategy_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_strategy_agent_task'],
        )    

    @task
    def marketing_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['marketing_agent_task'],
        )

    @task
    def market_research_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_research_agent_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the VwMas crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )