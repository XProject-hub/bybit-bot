import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_decide(symbol: str, rsi: float, ema: float, ai_suggestion: str) -> str:
    prompt = f"""
    You are a crypto trading assistant. An AI model suggested '{ai_suggestion.upper()}' for {symbol}.
    RSI is {rsi}, EMA is {ema}.
    
    Based on this data, do you agree with the AI decision?
    Reply ONLY with one of: BUY, SELL, or HOLD.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )
        decision = response.choices[0].message["content"].strip().upper()
        return decision
    except Exception as e:
        print(f"[GPT Error] {e}")
        return "HOLD"
