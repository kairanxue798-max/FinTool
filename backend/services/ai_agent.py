import os
from typing import Dict, Optional, List
from openai import OpenAI
import json


class AIAgent:
    """
    AI Agent for financial analysis including variance analysis and KPI achievement
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            print("Warning: OPENAI_API_KEY not set. AI features will use fallback analysis.")
    
    async def analyze_variance(
        self,
        current_period: Dict,
        previous_period: Dict,
        period_name: str
    ) -> Dict:
        """
        Analyze variance between current and previous period using AI
        """
        if not self.client:
            return self._fallback_variance_analysis(current_period, previous_period, period_name)
        
        try:
            prompt = f"""
            Analyze the financial variance between the current period and previous period.
            
            Current Period ({period_name}):
            {json.dumps(current_period, indent=2)}
            
            Previous Period:
            {json.dumps(previous_period, indent=2)}
            
            Provide a detailed analysis including:
            1. Key variances (positive and negative)
            2. Percentage changes for major line items
            3. Potential reasons for significant changes
            4. Recommendations for improvement
            5. Risk factors identified
            
            Format the response as JSON with the following structure:
            {{
                "summary": "Overall summary of variance",
                "key_variances": [
                    {{
                        "item": "Item name",
                        "current": 0,
                        "previous": 0,
                        "variance": 0,
                        "percentage_change": 0,
                        "analysis": "Explanation"
                    }}
                ],
                "recommendations": ["Recommendation 1", "Recommendation 2"],
                "risk_factors": ["Risk 1", "Risk 2"]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a financial analyst expert. Provide detailed variance analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            # Try to extract JSON from the response
            try:
                analysis = json.loads(analysis_text)
            except:
                # If response is not pure JSON, try to extract it
                start = analysis_text.find('{')
                end = analysis_text.rfind('}') + 1
                if start >= 0 and end > start:
                    analysis = json.loads(analysis_text[start:end])
                else:
                    analysis = {"summary": analysis_text, "key_variances": [], "recommendations": [], "risk_factors": []}
            
            return analysis
        
        except Exception as e:
            print(f"Error in AI variance analysis: {e}")
            return self._fallback_variance_analysis(current_period, previous_period, period_name)
    
    async def analyze_kpi_achievement(
        self,
        financial_data: Dict,
        kpi_targets: Dict
    ) -> Dict:
        """
        Analyze KPI achievement using AI
        """
        if not self.client:
            return self._fallback_kpi_analysis(financial_data, kpi_targets)
        
        try:
            prompt = f"""
            Analyze KPI achievement based on financial data and targets.
            
            Financial Data:
            {json.dumps(financial_data, indent=2)}
            
            KPI Targets:
            {json.dumps(kpi_targets, indent=2)}
            
            Provide a detailed analysis including:
            1. KPI achievement status (achieved/not achieved)
            2. Percentage of target achieved
            3. Gap analysis
            4. Performance trends
            5. Action items to improve KPIs
            
            Format the response as JSON with the following structure:
            {{
                "overall_performance": "Summary of overall KPI performance",
                "kpi_results": [
                    {{
                        "kpi_name": "KPI name",
                        "target": 0,
                        "actual": 0,
                        "achievement_percentage": 0,
                        "status": "achieved/not_achieved",
                        "gap": 0,
                        "analysis": "Explanation"
                    }}
                ],
                "action_items": ["Action 1", "Action 2"],
                "trends": "Performance trends analysis"
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a financial analyst expert. Provide detailed KPI analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            try:
                analysis = json.loads(analysis_text)
            except:
                start = analysis_text.find('{')
                end = analysis_text.rfind('}') + 1
                if start >= 0 and end > start:
                    analysis = json.loads(analysis_text[start:end])
                else:
                    analysis = {"overall_performance": analysis_text, "kpi_results": [], "action_items": [], "trends": ""}
            
            return analysis
        
        except Exception as e:
            print(f"Error in AI KPI analysis: {e}")
            return self._fallback_kpi_analysis(financial_data, kpi_targets)
    
    def _fallback_variance_analysis(self, current: Dict, previous: Dict, period: str) -> Dict:
        """Fallback variance analysis without AI"""
        key_variances = []
        
        # Simple comparison logic
        if isinstance(current, dict) and isinstance(previous, dict):
            for key in set(list(current.keys()) + list(previous.keys())):
                curr_val = current.get(key, 0)
                prev_val = previous.get(key, 0)
                
                if isinstance(curr_val, (int, float)) and isinstance(prev_val, (int, float)):
                    variance = curr_val - prev_val
                    pct_change = (variance / prev_val * 100) if prev_val != 0 else 0
                    
                    key_variances.append({
                        "item": key,
                        "current": curr_val,
                        "previous": prev_val,
                        "variance": variance,
                        "percentage_change": round(pct_change, 2),
                        "analysis": f"{'Increase' if variance > 0 else 'Decrease'} of {abs(pct_change):.2f}%"
                    })
        
        return {
            "summary": f"Variance analysis for {period} - Calculated {len(key_variances)} variances",
            "key_variances": key_variances[:10],  # Limit to top 10
            "recommendations": [
                "Review significant variances with management",
                "Investigate items with >10% change"
            ],
            "risk_factors": ["Large variances may indicate data quality issues"]
        }
    
    def _fallback_kpi_analysis(self, financial_data: Dict, kpi_targets: Dict) -> Dict:
        """Fallback KPI analysis without AI"""
        kpi_results = []
        
        for kpi_name, target in kpi_targets.items():
            actual = financial_data.get(kpi_name, 0)
            if isinstance(target, (int, float)) and isinstance(actual, (int, float)):
                achievement_pct = (actual / target * 100) if target != 0 else 0
                gap = actual - target
                status = "achieved" if actual >= target else "not_achieved"
                
                kpi_results.append({
                    "kpi_name": kpi_name,
                    "target": target,
                    "actual": actual,
                    "achievement_percentage": round(achievement_pct, 2),
                    "status": status,
                    "gap": gap,
                    "analysis": f"{'Achieved' if status == 'achieved' else 'Not achieved'} - {achievement_pct:.2f}% of target"
                })
        
        return {
            "overall_performance": f"Analyzed {len(kpi_results)} KPIs",
            "kpi_results": kpi_results,
            "action_items": [
                "Focus on KPIs below target",
                "Review strategies for underperforming metrics"
            ],
            "trends": "Historical trend analysis requires multiple periods of data"
        }
    
    async def chat(
        self,
        message: str,
        financial_data: Optional[Dict] = None,
        transactions: Optional[List[Dict]] = None,
        conversation_history: Optional[List[Dict]] = None,
        entity: Optional[str] = None
    ) -> Dict:
        """
        General-purpose financial AI chat agent that can answer any financial-related questions
        """
        if not self.client:
            return self._fallback_chat(message, financial_data, transactions, entity)
        
        try:
            # Build system prompt with financial context
            system_prompt = """You are an expert financial analyst AI assistant. Your role is to help users understand and analyze their financial data.

CRITICAL INSTRUCTIONS:
1. When transaction data is provided with revenue by entity calculations, USE THAT DATA to answer questions directly
2. If the user asks "which subsidiary has the highest revenue", look at the "REVENUE BY ENTITY" section in the transaction data and identify the entity with the highest value
3. DO NOT ask the user to upload data if transaction data is already provided - analyze what you have
4. Provide specific numbers and entity names from the data provided

You can:
- Analyze financial statements (Balance Sheet, Profit & Loss, Cash Flow)
- Perform variance analysis
- Calculate and analyze KPIs (AR Aging, DSO, Revenue YTD, etc.)
- Multi-entity/subsidiary analysis - COMPARE revenue, expenses, and performance across different subsidiaries/entities
- Foreign exchange rate conversions
- Revenue analytics:
  * Revenue YTD (Year-to-Date)
  * Revenue variance compared to previous month
  * Trailing 3 months rolling revenue
  * TOP N revenue transactions
  * Unusual transactions (e.g., weekend postings)
- Provide financial insights and recommendations
- Answer questions about accounting principles
- Explain financial metrics and ratios
- Identify trends and patterns in financial data
- Suggest improvements for financial performance

IMPORTANT: When transaction data is provided:
- The data will include a "REVENUE BY ENTITY" section showing revenue for each subsidiary
- Use this data to directly answer questions like "which subsidiary has the highest revenue"
- Compare entities using the provided revenue and expense data
- Provide specific numbers, entity names, and percentages
- DO NOT say "please upload data" if transaction data is already provided

Always provide clear, actionable insights with specific numbers from the data. If transaction data is provided, analyze it directly to answer questions about subsidiaries, revenue, and entity performance. If financial data is provided, use it to give specific, data-driven answers. If no data is provided, give general financial advice."""

            # Build user message with financial context
            user_message = message
            
            # Add transaction data if available - this is crucial for subsidiary analysis
            if transactions:
                # Calculate revenue by entity for quick reference
                # Revenue transactions are identified by account name (Revenue, Sales, Income) and type='credit'
                entity_revenue = {}
                entity_expenses = {}
                entity_summary = {}
                
                for txn in transactions:
                    account = str(txn.get('account', '')).lower()
                    txn_type = str(txn.get('type', '')).lower()
                    amount = float(txn.get('amount', 0) or 0)
                    entity = txn.get('entity') or txn.get('subsidiary') or txn.get('company') or 'Unknown'
                    
                    # Identify revenue transactions (credit entries with revenue/sales/income accounts)
                    if txn_type == 'credit' and amount > 0:
                        if any(keyword in account for keyword in ['revenue', 'sales', 'income', 'revenue']):
                            entity_revenue[entity] = entity_revenue.get(entity, 0) + amount
                    
                    # Also track expenses for comparison
                    if txn_type == 'debit' and amount > 0:
                        if any(keyword in account for keyword in ['expense', 'cost', 'salary', 'rent', 'utilities']):
                            entity_expenses[entity] = entity_expenses.get(entity, 0) + amount
                    
                    # Track total transactions per entity
                    if entity not in entity_summary:
                        entity_summary[entity] = {'total_transactions': 0, 'total_amount': 0}
                    entity_summary[entity]['total_transactions'] += 1
                    entity_summary[entity]['total_amount'] += abs(amount)
                
                # Add comprehensive summary
                user_message += f"\n\n=== TRANSACTION DATA ANALYSIS ===\n"
                user_message += f"Total transactions: {len(transactions)}\n"
                user_message += f"Unique entities: {len(entity_summary)}\n\n"
                
                if entity_revenue:
                    user_message += f"REVENUE BY ENTITY:\n{json.dumps(entity_revenue, indent=2)}\n\n"
                    # Identify highest revenue entity
                    if entity_revenue:
                        highest_entity = max(entity_revenue.items(), key=lambda x: x[1])
                        user_message += f"HIGHEST REVENUE ENTITY: {highest_entity[0]} with ${highest_entity[1]:,.2f}\n\n"
                
                if entity_expenses:
                    user_message += f"EXPENSES BY ENTITY:\n{json.dumps(entity_expenses, indent=2)}\n\n"
                
                user_message += f"ENTITY SUMMARY:\n{json.dumps(entity_summary, indent=2, default=str)}\n\n"
                
                # Include sample transactions for context (first 30 to show entity diversity)
                user_message += f"SAMPLE TRANSACTIONS (first 30):\n{json.dumps(transactions[:30], indent=2, default=str)}\n"
            
            if financial_data:
                user_message += f"\n\nCurrent Financial Data:\n{json.dumps(financial_data, indent=2)}"
            
            # Build conversation history
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "response": ai_response,
                "success": True
            }
        
        except Exception as e:
            print(f"Error in AI chat: {e}")
            return self._fallback_chat(message, financial_data, transactions, entity)
    
    def _fallback_chat(self, message: str, financial_data: Optional[Dict] = None, transactions: Optional[List[Dict]] = None, entity: Optional[str] = None) -> Dict:
        """Fallback chat without AI - with transaction analysis"""
        message_lower = message.lower()
        
        # Handle subsidiary/revenue questions if transactions are available
        if transactions and len(transactions) > 0:
            # Calculate revenue by entity - identify revenue by account name and credit type
            entity_revenue = {}
            entity_expenses = {}
            entity_summary = {}
            
            for txn in transactions:
                account = str(txn.get('account', '')).lower()
                txn_type = str(txn.get('type', '')).lower()
                amount = float(txn.get('amount', 0) or 0)
                txn_entity = txn.get('entity') or txn.get('subsidiary') or txn.get('company') or 'Unknown'
                
                # Identify revenue transactions (credit entries with revenue/sales/income accounts)
                if txn_type == 'credit' and amount > 0:
                    if any(keyword in account for keyword in ['revenue', 'sales', 'income']):
                        entity_revenue[txn_entity] = entity_revenue.get(txn_entity, 0) + amount
                
                # Track expenses for comparison
                if txn_type == 'debit' and amount > 0:
                    if any(keyword in account for keyword in ['expense', 'cost', 'salary', 'rent', 'utilities']):
                        entity_expenses[txn_entity] = entity_expenses.get(txn_entity, 0) + amount
                
                # Track total transactions per entity
                if txn_entity not in entity_summary:
                    entity_summary[txn_entity] = {'total_transactions': 0, 'total_amount': 0}
                entity_summary[txn_entity]['total_transactions'] += 1
                entity_summary[txn_entity]['total_amount'] += abs(amount)
            
            # Answer subsidiary/revenue questions
            if ("subsidiary" in message_lower or "entity" in message_lower or "highest revenue" in message_lower or 
                ("compare" in message_lower and "revenue" in message_lower) or
                ("which" in message_lower and "highest" in message_lower)):
                
                if entity_revenue:
                    sorted_entities = sorted(entity_revenue.items(), key=lambda x: x[1], reverse=True)
                    highest = sorted_entities[0]
                    
                    response_text = f"📊 **Revenue Analysis by Entity**\n\n"
                    response_text += f"🏆 **Highest Revenue Entity:** {highest[0]}\n"
                    response_text += f"   Revenue: ${highest[1]:,.2f}\n\n"
                    
                    if len(sorted_entities) > 1:
                        response_text += "**All Entities Revenue Ranking:**\n"
                        for i, (ent, rev) in enumerate(sorted_entities, 1):
                            percentage = (rev / highest[1] * 100) if highest[1] > 0 else 0
                            response_text += f"{i}. {ent}: ${rev:,.2f} ({percentage:.1f}% of highest)\n"
                    
                    # Add expense comparison if available
                    if entity_expenses and highest[0] in entity_expenses:
                        net_income = highest[1] - entity_expenses.get(highest[0], 0)
                        response_text += f"\n💰 **Net Income for {highest[0]}:** ${net_income:,.2f}\n"
                        response_text += f"   (Revenue: ${highest[1]:,.2f} - Expenses: ${entity_expenses.get(highest[0], 0):,.2f})"
                    
                    return {
                        "response": response_text,
                        "success": True
                    }
                else:
                    return {
                        "response": "I analyzed your transaction data but couldn't find any revenue transactions. Please ensure your CSV includes transactions with:\n- Account names containing 'Revenue', 'Sales', or 'Income'\n- Type: 'Credit'\n- Entity/Subsidiary column",
                        "success": True
                    }
            
            # Answer general revenue questions
            if "revenue" in message_lower and ("total" in message_lower or "ytd" in message_lower or "year" in message_lower):
                total_revenue = sum(entity_revenue.values())
                response_text = f"📈 **Total Revenue Analysis**\n\n"
                response_text += f"**Total Revenue:** ${total_revenue:,.2f}\n\n"
                if entity_revenue:
                    response_text += "**Breakdown by Entity:**\n"
                    for ent, rev in sorted(entity_revenue.items(), key=lambda x: x[1], reverse=True):
                        percentage = (rev / total_revenue * 100) if total_revenue > 0 else 0
                        response_text += f"- {ent}: ${rev:,.2f} ({percentage:.1f}%)\n"
                return {
                    "response": response_text,
                    "success": True
                }
        
        # Simple keyword-based responses
        if "variance" in message_lower or "compare" in message_lower:
            return {
                "response": "I can help with variance analysis. Please provide current and previous period data, or upload your financial statements. For full AI-powered analysis, please set up an OpenAI API key.",
                "success": True
            }
        
        if "kpi" in message_lower or "key performance" in message_lower:
            return {
                "response": "I can analyze KPI achievement. Please provide your financial data and KPI targets. For detailed AI analysis, please configure an OpenAI API key in the backend/.env file.",
                "success": True
            }
        
        if "balance sheet" in message_lower or "assets" in message_lower or "liabilities" in message_lower:
            return {
                "response": "I can help analyze your Balance Sheet. Please upload your financial data first. The Balance Sheet shows assets, liabilities, and equity at a specific point in time.",
                "success": True
            }
        
        if "revenue" in message_lower or "expense" in message_lower:
            # This is handled above in the transaction analysis section
            # But if we get here and have transactions, analyze them
            if transactions and len(transactions) > 0:
                entity_revenue = {}
                total_revenue = 0
                total_expenses = 0
                
                for txn in transactions:
                    account = str(txn.get('account', '')).lower()
                    txn_type = str(txn.get('type', '')).lower()
                    amount = float(txn.get('amount', 0) or 0)
                    
                    if txn_type == 'credit' and any(k in account for k in ['revenue', 'sales', 'income']):
                        total_revenue += amount
                        entity = txn.get('entity') or txn.get('subsidiary') or 'Unknown'
                        entity_revenue[entity] = entity_revenue.get(entity, 0) + amount
                    elif txn_type == 'debit' and any(k in account for k in ['expense', 'cost', 'salary', 'rent']):
                        total_expenses += amount
                
                response_text = f"📊 **Revenue & Expense Analysis**\n\n"
                response_text += f"**Total Revenue:** ${total_revenue:,.2f}\n"
                response_text += f"**Total Expenses:** ${total_expenses:,.2f}\n"
                response_text += f"**Net Income:** ${total_revenue - total_expenses:,.2f}\n"
                
                if entity_revenue:
                    response_text += f"\n**Revenue by Entity:**\n"
                    for ent, rev in sorted(entity_revenue.items(), key=lambda x: x[1], reverse=True):
                        response_text += f"- {ent}: ${rev:,.2f}\n"
                
                return {
                    "response": response_text,
                    "success": True
                }
            
            return {
                "response": "I can help analyze revenue and expenses. Please upload your transaction data first. For detailed AI-powered analysis, please set up an OpenAI API key in backend/.env file.",
                "success": True
            }
        
        if "cash flow" in message_lower or "cashflow" in message_lower:
            return {
                "response": "I can help analyze your Cash Flow statement. Please upload your financial data. Cash Flow shows operating, investing, and financing activities.",
                "success": True
            }
        
        # Default response - if we have transactions, offer to analyze them
        if transactions and len(transactions) > 0:
            return {
                "response": f"I'm your financial AI assistant. I have access to {len(transactions)} transactions.\n\nI can help you with:\n- Which subsidiary has the highest revenue\n- Compare revenue across entities\n- Total revenue calculations\n- Profit & Loss analysis\n- Multi-entity/subsidiary analysis\n\nTry asking:\n- 'Which subsidiary has the highest revenue?'\n- 'Compare revenue across all entities'\n- 'What's the total revenue?'\n\nFor advanced AI-powered analysis, please set up an OpenAI API key in backend/.env file.",
                "success": True
            }
        
        # Default response
        return {
            "response": f"I'm your financial AI assistant. I can help with:\n- Variance analysis\n- KPI analysis\n- Financial statement analysis\n- Accounting questions\n- Financial insights\n- Multi-entity/subsidiary analysis\n\nPlease upload your financial data or ask a specific question. For full AI capabilities, please set up an OpenAI API key in backend/.env file.\n\nYour question: {message}",
            "success": True
        }

