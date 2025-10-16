import main
import asyncio

## map backend functions in main.py
agg_functions = ['overview', 'recent_news_trends', 'financial_info', 'management_info', 'oppotunities_competition_info', 'geographic', 'M_n_A_profile']


async def run_all_backend_functions(agg_functions, module, company):
    """
    Run all functions concurrently and store their results in a dictionary
    """

    results = await asyncio.gather(*[getattr(module, func_name)(company) for func_name in agg_functions])
    return {func_name: result.messages[-1].content for func_name, result in zip(agg_functions, results)}

asyncio.run(run_all_backend_functions(agg_functions, main, 'GOOGL'))
