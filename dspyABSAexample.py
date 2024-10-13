import openai
import dspy
from dspy import OpenAI
# openai.api_base = "https://api.gpts.vin/v1"
# openai.api_key = "sk-Pee7ZqyWixn655GY99Ff3eB6De9a4269Bf68E89505B90d48"
# openai.api_base = "https://api.gpts.vin/v1"  # use the IP or hostname of your instance
# openai.api_key = "sk-FhKeNgB7ZgqvpZqsF357D67eAa8c42339b02Cf57C56a7d19"
openai.api_base = "https://api.gpts.vin/v1/chat/completions"  # https://api.gpts.vin/v1  # https://api.gpts.vin/v1/chat/completions  # https://api.gpts.vin
openai.api_key = "sk-4HmIu1msph13JUMZ1fCf8082B9084927B88e6bEf3e9467Ac"
lm = OpenAI(api_base=openai.api_base,
             api_key=openai.api_key,
             model='gpt-3.5-turbo')  # model='gpt-3.5-turbo'  gpt-4o
dspy.settings.configure(lm=lm)

# Define the DSPy implementation of sentiment polarity analysis
class SentimentPolarityAnalysis(dspy.Signature):
    """Analyze the sentiment polarity of a given sentence."""
    sentence = dspy.InputField(desc="The sentence to analyze.")
    sentiment = dspy.OutputField(desc="The predicted sentiment polarity (positive, neutral, or negative).")

class SentimentAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.analyze_sentiment = dspy.ChainOfThought(SentimentPolarityAnalysis)
    
    def forward(self, sentence):
        prediction = self.analyze_sentiment(sentence=sentence)
        return dspy.Prediction(sentiment=prediction.sentiment)

    def analyze_sentiment(self, sentence):
        prompt = f"请分析以下句子的情感极性（积极，中立，消极）：\n句子: {sentence}\n情感极性: "
        response = lm.complete(prompt=prompt)
        return response.choices[0].message.content
    
analyzer = SentimentAnalyzer()
sentence = "这是一个美好的一天。"
result = analyzer(sentence)
print(f"句子: {sentence}\n情感极性: {result.sentiment}")