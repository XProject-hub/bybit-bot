import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_decide(symbol: str, rsi: float, ema: float, macd: float, bb_width: float, ai_suggestion: str) -> str:
    prompt = f"""
    You are a crypto trading assistant. An AI model suggested '{ai_suggestion.upper()}' for {symbol}.
    Indicators:
    - RSI: {rsi}
    - EMA: {ema}
    - MACD: {macd}
    - Bollinger Band Width: {bb_width}

    Based on this data, do you agree with the AI decision?
    Reply ONLY with one of: BUY, SELL, or HOLD.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )
        return response.choices[0].message["content"].strip().upper()
    except Exception as e:
        print(f"[GPT Error] {e}")
        return "HOLD"

def gpt_reason(symbol: str, rsi: float, ema: float, macd: float, bb_width: float, ai_suggestion: str) -> str:
    prompt = f"""
    You're a smart crypto bot logging trade reasoning.
    - Symbol: {symbol}
    - RSI: {rsi}
    - EMA: {ema}
    - MACD: {macd}
    - BB Width: {bb_width}
    - AI Suggestion: {ai_suggestion.upper()}

    Write a short reason (1-2 lines) why this trade was entered.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"[GPT Reason Error] {e}")
        return "No GPT reason available."
