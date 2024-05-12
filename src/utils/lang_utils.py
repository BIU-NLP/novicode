import nltk
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import SmoothingFunction
from nltk.corpus import stopwords
import string
import warnings

warnings.filterwarnings("ignore")
nltk.download("stopwords", quiet=True)

def tokenize(text, filter_stopwords=False):
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    tokens = remove_common_words(tokens) if filter_stopwords else tokens
    return tokens


def compute_bleu_score(a, b, weights=(1.0, 0.0, 0.0, 0.0), filter_stopwords=False):
    hypothesis = tokenize(a, filter_stopwords=filter_stopwords)
    reference = tokenize(b, filter_stopwords=filter_stopwords)
    chencherry = SmoothingFunction()
    bleu_score = nltk.translate.bleu_score.sentence_bleu(
        [reference], hypothesis, weights, smoothing_function=chencherry.method1
    )
    return bleu_score


def remove_common_words(tokens):
    """
    This method removes common words like determiners and prepositions from the text.

    Parameters
    ----------
    tokens : List[str]
        The tokens list to remove common words from

    Returns
    -------
    tokens : List[str]
        The tokens with common words removed
    """
    
    # Define a list of determiners and prepositions to remove
    # Note: This is a basic list; you might need to expand it based on your needs
    to_remove = [
        'a', 'an', 'the', 'in', 'on', 'at', 'of', 'for', 'with', 'about', 'above',
        'across', 'after', 'against', 'along', 'amid', 'among', 'around', 'as',
        'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'by',
        'concerning', 'considering', 'despite', 'down', 'during', 'except', 'from',
        'inside', 'into', 'like', 'near', 'off', 'onto', 'outside', 'over', 'past',
        'regarding', 'round', 'since', 'through', 'throughout', 'till', 'to',
        'toward', 'under', 'underneath', 'until', 'unto', 'up', 'upon', 'via',
        'within', 'without', 'this', 'that', 'these', 'those', 'my', 'your', 'his',
        'her', 'its', 'our', 'their', 'some', 'any', 'no', 'every', 'each', 'all'
    ]

    
    # Filter out the words that are in the list of words to remove
    stop_tokens = set(stopwords.words("english") + list(string.punctuation) + to_remove)
    filtered_tokens = (
        [w.lower() for w in tokens if not w.lower() in stop_tokens]
        if all(w in stop_tokens for w in tokens)
        else tokens
    )
    filtered_tokens = [word for word in tokens if word.lower() not in to_remove]
    
    return filtered_tokens

