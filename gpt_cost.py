"""
requirement: 
 - tiktoken
 - openai
"""

import tiktoken


# {'model_name': {prices...}}
price_rule = {
    # ref: https://openai.com/pricing#language-models
    'gpt-4': {'in':0.03, 'out':0.06},
    'gpt-4-32k': {'in':0.06, 'out': 0.12},
    'gpt-3.5-turbo-1106': {'in':0.001, 'out':0.002},
    'gpt-3.5-turbo-instruct': {'in':0.0015, 'out':0.002},
    'gpt-4-1106-preview': {'in':0.01, 'out':0.03},
    'gpt-4-1106-vision-preview': {'in':0.01, 'out':0.03}
}


def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def price_per_token(model_name='gpt-4') -> dict:
    return {'in':price_rule[model_name]['in']/1000, 'out': price_rule[model_name]['out']/1000}


def num_tokens(docs: list, model_name: str):
    tot = 0
    for doc in docs:
        tot += num_tokens_from_string(doc, model_name)
    return tot


def tot_cost_by_docs(docs: list, request_type: str, model_name: str):
    """
    compute the cost when you only have the documents.
    Args:
        docs: list of str.
        request_type: ['in', 'out']
        model_name: names must in price_rule.
    """
    token_num = num_tokens(docs, model_name)
    return price_per_token(model_name)[request_type] * token_num


def tot_cost_by_token_num(token_num: int, request_type: str, model_name: str):
    """
    compute the cost when you know the number of token.
    Args:
        token_num: number of token.
        request_type: ['in', 'out']
        model_name: names must in price_rule.
    """
    return price_per_token(model_name)[request_type] * token_num