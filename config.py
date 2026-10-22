from pathlib import Path
FPS = 30
DURATION = 295  # 4:55, including 5-second closing title
WIDTH, HEIGHT = 1920, 1080
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
CACHE = ROOT / "cache"
MUSIC_SOURCE = ROOT / "assets" / "openai_futuristic_background_music.wav"
SCENES = [
    (0,15,"INTRO","OPENAI & ARTIFICIAL INTELLIGENCE","FROM ZERO TO THE FUTURE"),
    (15,40,"AI BASICS","WHAT IS AI?","OPENAI  •  CHATGPT  •  AI MODELS"),
    (40,70,"LLMs","LANGUAGE BECOMES NUMBERS","TOKENS  •  PATTERNS  •  PREDICTION"),
    (70,95,"ATTENTION","CONTEXT CHANGES MEANING","TRANSFORMER SELF-ATTENTION"),
    (95,120,"TRAINING / INFERENCE","LEARN PARAMETERS  /  GENERATE OUTPUTS","TRAINING ≠ INFERENCE"),
    (120,180,"AI AGENTS","GOAL → PLAN → TOOL → OBSERVE → VERIFY","SIMULATED RESEARCH AGENT"),
    (180,205,"MULTIMODAL AI","TEXT  •  IMAGE  •  AUDIO  •  VIDEO","MODELS + APPS + APIs + TOOLS"),
    (205,245,"AGI / ASI","GENERAL INTELLIGENCE?","AGI: DEBATED CONCEPT  •  ASI: HYPOTHETICAL"),
    (245,270,"AI SAFETY","CAPABILITY NEEDS CONTROL","PERMISSIONS  •  VERIFICATION  •  HUMAN OVERSIGHT"),
    (270,295,"THE FUTURE","UNDERSTAND AI. BUILD RESPONSIBLY.","SHAPE THE FUTURE."),
]
NARRATION = [
"What is artificial intelligence? How does OpenAI create AI systems, and how can an AI agent move beyond answering questions to completing tasks? In the next five minutes, let's explore the technology changing our world.",
"Artificial intelligence is a field focused on building systems that can recognize patterns, work with language, generate content, and solve problems. OpenAI is an AI research and deployment organization. ChatGPT is an application people use to interact with AI models.",
"A large language model, or LLM, learns statistical patterns from large collections of data. Text is split into tokens and converted into numerical representations. A neural network transforms those representations through layers of learned parameters. The trained model generates responses step by step. But fluent language is not proof of truth: an answer can sound confident and still be wrong.",
"Transformers use a mechanism called self-attention to weigh relationships between tokens. In the sentence, context helps a model interpret how words relate to one another. This animation is a simplified picture: real attention operates on numerical representations, not glowing lines between words.",
"During training, optimization adjusts model parameters to reduce errors on a learning objective. After training, inference uses those parameters to process new inputs and generate outputs. Evaluation and post-training methods can improve usefulness and behavior, but no training process makes a model perfectly accurate.",
"A chatbot may answer a question in one turn. An AI agent is a broader system designed to pursue a goal by choosing actions, using tools, observing results, and deciding what to do next. A language model may provide reasoning or language, while surrounding software manages tools, task state, permissions, and execution. Here, our simulated agent has one goal: compare solar and wind energy and prepare a short report. It breaks the goal into tasks, selects a search tool, receives simulated results, compares evidence, notices missing information, revises its plan, drafts a report, and checks its findings. A permission checkpoint should appear before consequential external actions. Not every chatbot is an agent, and agents do not automatically have persistent memory or unrestricted autonomy.",
"Multimodal systems can work with more than one kind of input, such as text, images, audio, or video, depending on the model. Applications can connect models to external services through APIs. The model, the app, the API, and the agent are related components, but they are not the same thing.",
"Artificial general intelligence, or AGI, is a debated concept that broadly refers to AI with general capabilities across many domains. There is no universally accepted operational definition, and impressive performance alone does not settle whether a system qualifies. Artificial superintelligence, or ASI, is hypothetical: it describes intelligence that substantially exceeds human capabilities across many important domains. Such systems could bring scientific benefits, but uncertainty, alignment, safety, and control would be major challenges. Neither AGI nor ASI should be presented as definitively achieved.",
"AI systems can make mistakes, expose sensitive information, or misuse tools when they are poorly designed or deployed. The unchecked agent acts quickly but may create harm. A safer system uses restricted permissions, verification, logging, and human approval before consequential actions. These safeguards reduce risk, but they cannot guarantee perfection.",
"Artificial intelligence is more than a chatbot. Models learn patterns, applications make those models useful, and agents can combine decisions with tools to pursue goals. AGI remains a debated concept, while ASI is a hypothetical future. Understanding the technology, questioning its limitations, and building it responsibly are essential as AI advances."
]
