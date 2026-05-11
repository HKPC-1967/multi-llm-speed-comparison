"""User-editable benchmark configuration.

Change the values in this file when you want to add models, add prompt sizes,
or run each model more than once before averaging the results.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkTask:
    name: str
    prompt: str


@dataclass(frozen=True)
class ModelConfig:
    display_name: str
    provider: str
    endpoint_env: str
    api_key_env: str
    model_env: str
    api_version_env: str | None = None


# Add more tasks here
BENCHMARK_TASKS = [
    BenchmarkTask(
        name="Summarize 1.7K words to 200 words",
        prompt="""
Please read the provided article regarding the evolution of human communication from the Stone Age to the Silicon Age. Your task is to summarize this text into exactly 200 words. The summary must capture the central thesis of each section, maintain the chronological flow, and accurately reflect the author's concluding thoughts on the future of neural interfaces. Do not include personal opinions or outside information. Focus strictly on the provided text.
Below is the source text intended for this evaluation.
The Evolution of Human Communication: From Stone Tablets to Neural Interfaces
The history of human civilization is, inextricably, the history of communication. It is the fundamental technology that separates us from every other species on the planet. While other animals possess methods of signaling—be it the waggle dance of the honeybee or the complex vocalizations of cetaceans—humans have developed the unique capacity to transmit abstract concepts, historical data, and future aspirations across time and space. This essay explores the transformative journey of human communication, tracing the arc from the earliest physical markings on stone to the emerging frontier of direct neural interfaces, arguing that each shift in medium has fundamentally altered not just how we speak, but how we think.
The Era of Physicality and the Invention of Writing
For the vast majority of human existence, communication was ephemeral. It existed only in the moment of utterance. If a hunter-gatherer discovered a rich source of food but died before returning to the tribe, that information perished with him. The first great leap in our species' cognitive evolution was the externalization of memory. This began with oral traditions, where rhythm and rhyme served as mnemonic devices to preserve history, but the true revolution occurred with the invention of writing around 3,400 BCE in Mesopotamia.
The Sumerians developed cuneiform, not for poetry or history, but for accounting. It was a tool of commerce, used to track grain and livestock. This shift from the spoken word to the physical mark allowed for the creation of complex bureaucracies and empires. It enabled a ruler in Babylon to send a command to a governor in Nineveh that would be understood weeks later, exactly as intended. The medium of clay tablets imposed a structure on thought; it required deliberation and permanence. Unlike speech, which can be slurred or retracted, a mark on clay is distinct and enduring.
This era of physicality continued through the Egyptians with hieroglyphs and the Chinese with oracle bones. However, the limitation remained the medium itself. Clay was heavy; papyrus was fragile. Information was tethered to physical objects that were difficult to transport and easy to destroy. The Library of Alexandria represented the pinnacle of this era, an attempt to centralize the world's knowledge in one physical location, yet its destruction highlighted the vulnerability of centralized, physical data storage.
The Gutenberg Revolution and the Democratization of Knowledge
The next seismic shift occurred in the 15th century with Johannes Gutenberg’s introduction of the movable type printing press to Europe. While woodblock printing had existed in East Asia for centuries, Gutenberg’s adaptation mechanized the reproduction of text. Before this, books were handwritten by scribes, often monks, a process that took months or years for a single volume. Books were rare, expensive, and prone to transcription errors.
The printing press changed the economics of information. Suddenly, texts could be mass-produced. The cost of books plummeted, and literacy rates began to climb. This was not merely a technological upgrade; it was a sociological upheaval. The monopoly on knowledge held by the clergy and the aristocracy was broken. Martin Luther’s 95 Theses, for instance, were printed and distributed across Germany in weeks, sparking the Protestant Reformation. This demonstrated the power of the printed word to mobilize populations and challenge established hierarchies.
Standardization also emerged during this period. As printed books spread, dialects began to merge into standardized national languages with fixed spelling and grammar. The way humans processed information changed as well. The shift from oral/aural culture to print culture fostered linear, sequential thinking. Readers learned to follow complex arguments from a starting point to a conclusion, a cognitive habit that would define the scientific and philosophical enlightenment of the following centuries.
The Telegraph and the Separation of Communication from Transportation
For millennia, the speed of communication was limited by the speed of a horse or a ship. If a message needed to travel from London to New York, it physically had to cross the Atlantic Ocean. The invention of the telegraph in the 19th century shattered this constraint. For the first time in history, information could travel faster than a human being.
Samuel Morse’s development of Morse code allowed for the transmission of complex messages via electrical pulses over wires. This led to the laying of the Transatlantic Telegraph Cable in 1858, connecting the Old World and the New World in near real-time. The implications were profound. News, stock prices, and military orders could be transmitted instantly. The world began to shrink.
This era marked the separation of communication from transportation. Previously, to send a message, you had to send a physical object (a letter, a tablet). With the telegraph, the message became energy. It was encoded, transmitted, and decoded. This abstraction of information paved the way for the digital age. It introduced the concept of the "network"—a web of connections where the physical location of the sender and receiver was irrelevant to the transmission of the signal.
The Electronic Age: Radio, Television, and the Global Village
The late 19th and early 20th centuries saw the evolution of the telegraph into the telephone, radio, and television. These technologies added layers of fidelity and immediacy to communication. The telephone reintroduced the human voice, adding tone and emotion back into long-distance communication. Radio and television, however, created a one-to-many broadcast model that unified cultures.
Marshall McLuhan, the Canadian philosopher, famously described this phenomenon as the creation of a "Global Village." Electronic media collapsed space and time, creating a situation where everyone was experiencing the same events simultaneously. The moon landing in 1969 is a prime example; an estimated 650 million people watched the same footage at the same time. This shared reality created a powerful sense of collective consciousness, but it also centralized the power of narrative in the hands of a few major networks and media conglomerates.
Unlike the printed word, which requires active engagement and imagination to visualize the described scenes, television is a passive medium. It presents a complete sensory package, requiring less cognitive effort to process but often delivering information in fragmented, bite-sized segments. This shift influenced political discourse, where image and charisma began to outweigh policy and detailed argumentation.
The Digital Revolution and the Internet
The late 20th century brought the most rapid and disruptive change in communication history: the Internet. Originally developed as a military project (ARPANET) to ensure communication resilience during a nuclear war, it evolved into a decentralized global network of computers. The introduction of the World Wide Web by Tim Berners-Lee in 1989 added a user-friendly interface to this network, allowing for the linking of documents across the globe.
The Internet combined the immediacy of the telegraph with the depth of print and the multimedia capabilities of television. It shifted communication from a one-to-many model (broadcast) to a many-to-many model. This democratization of content creation was unprecedented. Anyone with an internet connection could publish their thoughts, share their art, or organize a movement.
This era also introduced the concept of "hypertext," which mirrored the associative nature of human thought. Unlike a book, which must be read linearly, the web allows users to jump from one concept to another via links, creating a non-linear exploration of knowledge. However, this abundance of information brought new challenges: information overload, the spread of misinformation, and the creation of "echo chambers" where algorithms feed users only information that reinforces their existing biases.
The Mobile Era and the Always-On Culture
The proliferation of the smartphone in the 21st century untethered the internet from the desktop computer. Communication became constant and ubiquitous. Social media platforms like Facebook, Twitter (now X), and Instagram transformed communication into a continuous stream of status updates, photos, and short messages.
This "always-on" culture has fundamentally altered social dynamics. We are now accessible at all times, blurring the boundaries between work and leisure, public and private life. The brevity of these platforms—such as the original 140-character limit of Twitter—has influenced language, encouraging brevity and wit over nuance and depth. Emojis and GIFs have emerged as a new form of hieroglyphics, adding emotional context to text-based digital communication.
While this connectivity allows for rapid mobilization during social movements (such as the Arab Spring), it also contributes to a fragmented attention span. The constant barrage of notifications creates a state of continuous partial attention, making deep, sustained focus increasingly difficult.
The Future: Artificial Intelligence and Neural Interfaces
As we look toward the future, the boundaries between human cognition and digital communication are beginning to dissolve. We are currently witnessing the rise of Artificial Intelligence (AI) as a mediator in communication. Large Language Models (LLMs) can now draft emails, summarize complex texts, and translate languages in real-time, acting as a cognitive prosthesis for human expression.
The next frontier, however, is the Brain-Computer Interface (BCI). Companies like Neuralink are working on high-bandwidth connections between the human brain and computers. The goal is "telepathic" communication—transmitting thoughts directly from one mind to another without the bottleneck of language.
Language is, effectively, a compression algorithm. We take complex thoughts and compress them into words, transmit them via sound or text, and the receiver decompresses them back into thoughts. This process is lossy; much meaning is lost in translation. A direct neural link could theoretically allow for the transmission of raw concepts, emotions, and sensory experiences with 100% fidelity.
This potential future raises profound ethical and philosophical questions. If our thoughts can be transmitted or accessed digitally, what happens to the concept of privacy? If we can offload our memory to the cloud, how does that change our sense of self? We are standing on the precipice of a new evolutionary step, one where the tool of communication may no longer be something we hold in our hands, but something we become.
        """,
    ),
    BenchmarkTask(
        name="Simple Question",
        prompt="what model are you?",
    ),
]

# Number of calls per model/task pair. The final Excel value is the average.
RUNS_PER_MODEL = 1

# Sampling temperature used for all model calls.
TEMPERATURE = 0


MODEL_CONFIGS = [
    # ModelConfig(
    #     display_name="GPT-4.1 - Azure OpenAI - westus3 Global Standard",
    #     provider="azure_openai",
    #     endpoint_env="AZURE_OPENAI_ENDPOINT",
    #     api_key_env="AZURE_OPENAI_API_KEY",
    #     model_env="AZURE_OPENAI_GPT41_DEPLOYMENT",
    #     api_version_env="AZURE_OPENAI_API_VERSION",
    # ),
    # ModelConfig(
    #     display_name="GPT-5.4 Mini - Azure AI Foundry OpenAI - westus3 Global Standard",
    #     provider="azure_foundry_openai",
    #     endpoint_env="AZURE_FOUNDRY_ENDPOINT_OPENAI",
    #     api_key_env="AZURE_FOUNDRY_API_KEY",
    #     model_env="AZURE_FOUNDRY_GPT54_MINI_MODEL_OPENAI",
    #     api_version_env="AZURE_FOUNDRY_API_VERSION_OPENAI",
    # ),
    # ModelConfig(
    #     display_name="GPT-5.4 Mini - Azure AI Foundry OpenAI - westus3 Global Standard - Priority",
    #     provider="azure_foundry_openai",
    #     endpoint_env="AZURE_FOUNDRY_ENDPOINT_OPENAI",
    #     api_key_env="AZURE_FOUNDRY_API_KEY",
    #     model_env="AZURE_FOUNDRY_GPT54_MINI_MODEL_OPENAI_priority",
    #     api_version_env="AZURE_FOUNDRY_API_VERSION_OPENAI",
    # ),
    # ModelConfig(
    #     display_name="DeepSeek-V4-Flash - Azure AI Foundry - westus3 Global Standard",
    #     provider="azure_foundry",
    #     endpoint_env="AZURE_FOUNDRY_ENDPOINT",
    #     api_key_env="AZURE_FOUNDRY_API_KEY",
    #     model_env="AZURE_FOUNDRY_DEEPSEEK_V4_FLASH_MODEL",
    #     api_version_env="AZURE_FOUNDRY_API_VERSION",
    # ),
    # ModelConfig(
    #     display_name="DeepSeek-V4-Flash - Azure AI Foundry - koreacentral Global Standard",
    #     provider="azure_foundry",
    #     endpoint_env="AZURE_FOUNDRY_ENDPOINT_KOREA_CENTRAL",
    #     api_key_env="AZURE_FOUNDRY_API_KEY_KOREA_CENTRAL",
    #     model_env="AZURE_FOUNDRY_DEEPSEEK_V4_FLASH_MODEL_KOREA_CENTRAL",
    #     api_version_env="AZURE_FOUNDRY_API_VERSION_KOREA_CENTRAL",
    # ),
    # ModelConfig(
    #     display_name="DeepSeek-V4-Flash - Alibaba Cloud - Germany",
    #     provider="openai_compatible",
    #     endpoint_env="ALIBABA_CLOUD_COMPATIBLE_BASE_URL",
    #     api_key_env="ALIBABA_CLOUD_API_KEY",
    #     model_env="ALIBABA_DEEPSEEK_V4_FLASH_MODEL",
    # ),
    ModelConfig(
        display_name="DeepSeek-V4-Flash - Aliyun - China",
        provider="openai_compatible",
        endpoint_env="ALIYUN_COMPATIBLE_BASE_URL",
        api_key_env="ALIYUN_API_KEY",
        model_env="ALIYUN_DEEPSEEK_V4_FLASH_MODEL",
    ),
]
