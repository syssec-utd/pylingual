import pandas as pd
import re
import string

def create_corpus(df):
    """
    V df projektů přejmenuje sloupce a vytvoří nový sloupec corpus (např. název + cíl)

    Je potřeba mít připravený df, kde 1. sloupec je kód, 2. název, 3. cíl a 4. stav (bez ohledu, jak jsou pojmenované).

    """
    df = df.rename(columns={df.columns[0]: 'kod', df.columns[1]: 'nazev', df.columns[2]: 'cil', df.columns[3]: 'stav'})
    df['corpus'] = df['nazev'] + '; ' + df['cil']
    df_corpus = df[['kod', 'stav', 'nazev', 'cil', 'corpus']]
    return df_corpus

def cz_lemma(text):
    """
    Lemmatizuje text na základní tvar. Např. lepší -> dobrý, projektový -> projekt.

    Parameters
    ----------
    text (str): corpus (text) jednoho projektu, dotazu atd. => 1 buňka

    Returns
    -------
    lemma (str): lemmatizovaný text => 1 buňka

    """
    sentence = []
    for s in m.process(text):
        for w in s.words:
            if '<root>' not in w.lemma:
                sentence.append(w.lemma)
    lemma = ' '.join(sentence)
    return lemma

def lemma_pickle(df, df_lemma, id_col, name):
    """
    Aktualizuje soubor (pickle) s lemmatizovanými texty (např. projekty, dotazy).

    Nejdříve zkontroluje, jestli existují texty, které nebyly lemmatizované.
    Pro texty, které nebyly lemmatizované provede lemmatizaci.
    Aktualizuje původní soubor s lemmatizovanými texty o nově lemmatizované texty.

    Parameters
    ----------
    df (DataFrame): dataframe se všemi texty (lemmatizované i nelemmatizované)
    df_lemma (DataFrame): dataframe s lemmatizovanými texty (původní soubor pickle)
    id_col (str): název sloupce s ID, pro oba df musí být stejné
    name (str): entita, které se lemmatizace týká (např. projekty), slouží pro pojmenování souboru

    Returns
    -------
    df_lemma (DataFrame): aktualizovaný dataframe lemmatizovaných textů

    """
    id_set = set(df[id_col]) - set(df_lemma[id_col])
    df = df[df[id_col].isin(id_set)]
    df['lemma'] = df['corpus'].apply(lambda x: cz_lemma(x))
    df = df[['kod', 'lemma']]
    df_lemma = pd.concat([df_lemma, df], ignore_index=True)
    df_lemma.to_pickle(name + '_lemma.pkl')
    return df_lemma

def text_cleaning(text):
    """ Preprocessing textu, odstranění netextových znaků."""
    text = text.lower()
    text = re.sub(';', ' ; ', text)
    text = re.sub(',', ' , ', text)
    text = re.sub('-', ' - ', text)
    text = re.sub('\\d', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    return text