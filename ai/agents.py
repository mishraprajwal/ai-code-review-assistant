from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv
import time
import threading

load_dotenv()

# Initialize OpenAI client
openai_api_key = os.getenv('OPENAI_API_KEY')

def create_agents():
    """Create specialized agents with proper LLM configuration"""
    if not openai_api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")

    code_analyzer = Agent(
        role='Code Structure Analyzer',
        goal='Analyze code structure, complexity, and readability',
        backstory='You are an expert code reviewer specializing in structural analysis.',
        allow_delegation=False,
        verbose=False,
        llm_config={'model': 'gpt-3.5-turbo', 'api_key': openai_api_key}
    )

    bug_detector = Agent(
        role='Bug Detection Specialist',
        goal='Identify potential bugs, logical errors, and edge cases',
        backstory='You are a meticulous debugger with years of experience finding hidden bugs.',
        allow_delegation=False,
        verbose=False,
        llm_config={'model': 'gpt-3.5-turbo', 'api_key': openai_api_key}
    )

    security_reviewer = Agent(
        role='Security Code Reviewer',
        goal='Check for security vulnerabilities and best practices',
        backstory='You are a cybersecurity expert focused on secure coding practices.',
        allow_delegation=False,
        verbose=False,
        llm_config={'model': 'gpt-3.5-turbo', 'api_key': openai_api_key}
    )

    performance_optimizer = Agent(
        role='Performance Optimization Expert',
        goal='Suggest performance improvements and optimizations',
        backstory='You are a performance engineering specialist optimizing code efficiency.',
        allow_delegation=False,
        verbose=False,
        llm_config={'model': 'gpt-3.5-turbo', 'api_key': openai_api_key}
    )

    orchestrator = Agent(
        role='Code Review Orchestrator',
        goal='Coordinate and synthesize feedback from all specialized agents',
        backstory='You are the lead reviewer who brings together insights from all specialists.',
        allow_delegation=True,
        verbose=False,
        llm_config={'model': 'gpt-3.5-turbo', 'api_key': openai_api_key}
    )

    return code_analyzer, bug_detector, security_reviewer, performance_optimizer, orchestrator

def create_code_review_crew(code_snippet):
    """Create a crew of agents to review the code collaboratively"""
    code_analyzer, bug_detector, security_reviewer, performance_optimizer, orchestrator = create_agents()

    # Define tasks for each agent
    analyze_task = Task(
        description=f"Analyze the structure and complexity of this code: {code_snippet}",
        agent=code_analyzer,
        expected_output="Detailed analysis of code structure, time/space complexity, and readability suggestions."
    )

    bug_task = Task(
        description=f"Detect potential bugs and logical errors in this code: {code_snippet}",
        agent=bug_detector,
        expected_output="List of potential bugs, edge cases, and logical issues with explanations."
    )

    security_task = Task(
        description=f"Review security aspects of this code: {code_snippet}",
        agent=security_reviewer,
        expected_output="Security vulnerabilities, risks, and recommendations for secure coding."
    )

    performance_task = Task(
        description=f"Optimize performance of this code: {code_snippet}",
        agent=performance_optimizer,
        expected_output="Performance bottlenecks, optimization suggestions, and efficiency improvements."
    )

    # Orchestrator task to synthesize all feedback
    orchestrate_task = Task(
        description="Synthesize all agent feedback into a comprehensive code review report",
        agent=orchestrator,
        expected_output="A complete, well-structured code review with all findings and recommendations.",
        context=[analyze_task, bug_task, security_task, performance_task]
    )

    # Create and return the crew
    crew = Crew(
        agents=[code_analyzer, bug_detector, security_reviewer, performance_optimizer, orchestrator],
        tasks=[analyze_task, bug_task, security_task, performance_task, orchestrate_task],
        verbose=True
    )

    return crew

def get_agentic_review(code_snippet):
    """Get comprehensive code review from multi-agent system"""
    try:
        # Check if API key is available
        if not openai_api_key:
            return "Error: OpenAI API key not found. Please set OPENAI_API_KEY environment variable."

        # Try multi-agent review with shorter timeout
        try:
            crew = create_code_review_crew(code_snippet)
            
            # Set a shorter timeout for the crew execution (15 seconds)
            import threading
            result = [None]
            error = [None]
            
            def run_crew():
                try:
                    result[0] = crew.kickoff()
                except Exception as e:
                    error[0] = str(e)
            
            thread = threading.Thread(target=run_crew)
            thread.start()
            thread.join(timeout=15)  # 15 second timeout
            
            if thread.is_alive():
                raise TimeoutError("Multi-agent review timed out")
            elif error[0]:
                raise Exception(f"Multi-agent error: {error[0]}")
            else:
                return str(result[0])
                
        except Exception as e:
            # Fallback to single-agent mode
            print(f"Multi-agent review failed ({str(e)}), falling back to single-agent mode")
            
            # Import here to avoid circular imports
            import openai
            
            client = openai.OpenAI(api_key=openai_api_key)
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a code review assistant. Analyze the provided code and provide detailed feedback including time complexity, space complexity, potential bugs, and suggestions for improvement."},
                        {"role": "user", "content": f"Review this code:\n\n{code_snippet}"}
                    ],
                    max_tokens=500,
                    temperature=0.5
                )
                return response.choices[0].message.content.strip()
            except openai.RateLimitError:
                return "AI Review (Demo Mode - Quota Exceeded):\n\nTime Complexity: O(n)\nSpace Complexity: O(1)\nSuggestions:\n- Consider optimizing loops.\n- Add error handling.\n- Improve code readability with comments.\n\nPlease check your OpenAI billing or use a valid API key for full AI reviews."
            except Exception as e:
                return f"Error in single-agent review: {str(e)}"
            
    except Exception as e:
        return f"Error in agentic review: {str(e)}"