# Financial AI Chatbot Guide

## Overview

The Financial AI Chatbot is a conversational AI agent that can answer **any financial-related questions** about your uploaded financial data. Simply type your question in natural language, and the AI will provide intelligent analysis and insights.

## Features

✅ **Natural Language Queries** - Ask questions in plain English  
✅ **Context-Aware** - Uses your uploaded financial data automatically  
✅ **Conversational** - Maintains conversation history for better context  
✅ **Multiple Analysis Types** - Handles variance, KPIs, ratios, trends, and more  
✅ **Smart Fallback** - Works even without OpenAI API key (with limited features)

## How to Use

### 1. Upload Your Financial Data

First, upload your CSV file to generate financial statements. The chatbot will automatically have access to:
- Balance Sheet data
- Profit & Loss data
- Cash Flow data

### 2. Open the Chatbox

After uploading data, scroll down to find the **"🤖 Financial AI Assistant"** section.

### 3. Ask Your Questions

Type any financial question in the chatbox. Examples:

#### Variance Analysis
- "Compare this period's revenue with last period"
- "What's the variance in operating expenses?"
- "Show me the biggest changes in the balance sheet"

#### KPI Analysis
- "What's our current profit margin?"
- "Calculate the return on assets"
- "How are we performing against our targets?"

#### Financial Insights
- "What are the main risks in our financial position?"
- "Suggest ways to improve cash flow"
- "Analyze our liquidity ratios"
- "What trends do you see in our expenses?"

#### General Questions
- "Explain what the cash flow statement shows"
- "What does a high debt-to-equity ratio mean?"
- "How can we reduce operating expenses?"

### 4. Get AI-Powered Answers

The chatbot will:
- Analyze your specific financial data
- Provide detailed explanations
- Give actionable recommendations
- Answer follow-up questions with context

## Example Conversations

### Example 1: Variance Analysis
```
You: "What's the variance in revenue compared to last period?"

AI: "Based on your financial data, I can see that revenue has increased by 15% 
compared to the previous period. The main drivers are:
• Sales revenue increased by $50,000
• Interest income contributed an additional $2,000
• This represents a positive trend indicating business growth..."
```

### Example 2: KPI Analysis
```
You: "Calculate our profit margin and compare it to industry standards"

AI: "Your current profit margin is 18.5%, calculated as:
Net Income: $155,000
Total Revenue: $155,000
Profit Margin: 18.5%

This is above the industry average of 10-15% for similar businesses, 
indicating strong profitability. However, I notice operating expenses 
have increased by 12%, which could impact margins if not controlled..."
```

### Example 3: Financial Insights
```
You: "What are the main risks in our financial position?"

AI: "Based on your financial statements, I've identified several risk factors:
1. High debt-to-equity ratio (0.33) - while manageable, monitor debt levels
2. Accounts receivable increased significantly - potential cash flow risk
3. Operating expenses growing faster than revenue - margin compression risk

Recommendations:
• Implement stricter credit policies to reduce receivables
• Review operating expense categories for cost optimization
• Consider building cash reserves for unexpected expenses..."
```

## Tips for Best Results

1. **Be Specific** - More specific questions get better answers
   - ✅ "What's the variance in operating expenses between Q1 and Q2?"
   - ❌ "Tell me about expenses"

2. **Use Financial Terms** - The AI understands accounting terminology
   - "Calculate current ratio"
   - "Analyze working capital"
   - "What's our debt-to-equity ratio?"

3. **Ask Follow-ups** - The chatbot remembers conversation context
   - "Can you explain that in more detail?"
   - "What are the implications?"
   - "What should we do about it?"

4. **Request Analysis** - Ask for specific types of analysis
   - "Perform a trend analysis"
   - "Compare with industry benchmarks"
   - "Identify key risks and opportunities"

## Setup for Full AI Features

For the best experience with advanced AI capabilities:

1. Get an OpenAI API key from https://platform.openai.com/
2. Add it to `backend/.env`:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Restart the backend server

**Note**: The chatbot works without an API key but with limited capabilities (keyword-based responses).

## Troubleshooting

### Chatbot not responding?
- Check that backend server is running on port 8000
- Verify API endpoint: `http://localhost:8000/api/ai/chat`
- Check browser console for errors (F12)

### Responses seem generic?
- Make sure you've uploaded financial data first
- Try more specific questions
- Set up OpenAI API key for full AI capabilities

### Want to start a new conversation?
- Refresh the page to reset conversation history
- Or ask "Let's start over" and the AI will reset context

## Supported Question Types

✅ Variance analysis  
✅ KPI calculations and analysis  
✅ Financial ratio analysis  
✅ Trend identification  
✅ Risk assessment  
✅ Performance benchmarking  
✅ Cash flow analysis  
✅ Profitability analysis  
✅ Liquidity analysis  
✅ Accounting questions  
✅ Financial recommendations  
✅ Industry comparisons  

## Next Steps

- Try asking about specific metrics from your financial statements
- Request detailed analysis of any financial aspect
- Get recommendations for improvement
- Learn about financial concepts and ratios

The chatbot is designed to be your intelligent financial analyst - ask it anything!

