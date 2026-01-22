# tanglish_sentiment_mega.py

import re

# ------------------------------
# 250 Positive Words
# ------------------------------
positive_words = set([

    # English Positive (125)
    "good","great","awesome","excellent","super","happy","love","nice","beautiful","wonderful",
    "best","amazing","fantastic","brilliant","cool","positive","success","enjoy","lucky","strong",
    "fun","smile","progress","bright","celebrate","respect","peace","kind","support","care",
    "friendly","perfect","sweet","joy","dream","hope","strength","cheer","amused","calm",
    "grateful","charming","winning","motivated","confidence","famous","top","glad","clever",
    "victory","pleasure","sunshine","energetic","helpful","fresh","healthy","awesome","epic",
    "legend","safe","prosper","delight","loyal","trust","wonder","heaven","spark","unique",
    "greatful","lovely","positivevibe","growth","classy","humble","blessing","cute","handsome",
    "pretty","smiling","joyful","peaceful","leader","strongest","amazingness","creative",
    "talented","intelligent","motivating","powerful","bold","fearless","brightest","smart",
    "wonderous","kindhearted","selfless","caring","bliss","angel","hero","bestie","rockstar",
    "shining","topper","courage","respectful","sweetheart","adorable","innocent","energetic",
    "valued","inspiring","gifted","gem","star","happyheart","victorious","wonderkid","mentor",
    "helping","supportive","trustworthy","optimistic","chilled","positiveenergy",

    # Tamil/Tanglish Positive (125)
    "nandri","santosham","magizhchi","inbam","anbu","arumaai","sandhosham","romba nalla","superu","semma",
    "azhagu","sirappu","intha maari nalla","mikka nandri","thalaiva","mass","vera level","semma kalakku","kalakkal","awesomeu",
    "sirappana","periya vetri","arputham","nandri romba","thangam","ponnu azhagu","valkai nalla","miga nalla","semma content","sirikkuthu",
    "sandhoshama irukku","sirappu performance","azhagana","nanmaiyana","vallamai","selvam","sirappu thunai","vetrikuri","azhagumai","pugazh",
    "siranda","semma scene","paasa kaara","vetri","gumbaloda super","semma thalaiva","massu","semma love","nallathu","sirappu kalai",
    "nandri solluren","azhagulla","miga sirappu","velicham","arivoli","nalla payan","sirandha thunai","vazhkai super","saga vetri","sirandha kaalam",
    "periya thunai","arasan","thala mass","semma vaazhkai","azhagana ulagam","nandri than","semma vetri","vetri nadai","azhagana mugam","siranda payan",
    "semma gumbal","sandhosham pola","azhagaana life","periya anbu","thunai","semma feeling","semma team","kalai arasan","siranda pathi","semma kaalam",
    "sirappu valkai","nandri kuduthadhu","vetri nadai podu","azhagaana sirippu","semma anbu","azhagaana kaadhal","sirandhadhu","miga nandri","azhagaana paadal","sirappu sambavam",
    "semma nattamai","nandri kadan","azhagaana kaatchi","siranda thalaivar","vetri kodi","siranda ulagam","nandri ungaluku","magizhchi pola","sirappu thunaiyaga","azhagana vetrigal",
    "semma idea","nandri peruga","azhagaana suvai","siranda pathi thunai","nandri romba perisu"
])

# ------------------------------
# 250 Negative Words
# ------------------------------
negative_words = set([

    # English Negative (125)
    "bad","sad","angry","worst","hate","poor","waste","ugly","terrible","boring",
    "pain","annoying","disgusting","useless","failure","weak","cry","lost","fear","depress",
    "tired","frustrated","negative","stress","broken","hateful","jealous","selfish","fool","dirty",
    "angst","unhappy","lazy","dull","careless","cheap","greedy","problem","rough","fake",
    "sorrow","ill","worried","hurt","blame","regret","loser","pathetic","toxic","dirtymind",
    "worstday","irritated","hatefull","coward","nonsense","crap","trash","stupid","idiot","mad",
    "nasty","bully","rude","hopeless","scared","fearful","crying","lame","awful","junk",
    "corrupt","bitter","unfair","shame","fail","corruption","worthless","meaningless","killing","danger",
    "scam","fraud","arrogant","brokenheart","weakness","fearful","stressful","nervous","messy","damaged",
    "brokenmind","heartless","foolish","painful","horrible","worstlife","unwanted","cheapwork","wastefellow","negativevibe",
    "toxicfriend","angryman","hatred","nohope","stressed","weakman","poorservice","shameless","disaster","problematic",
    "terrifying","dangerous","brainless","backstabber","enemy","sadness","drama","looser","fakefriend","crybaby",
    "uselesswork","dirtygame","lifeless","helpless","hopelessly",

    # Tamil/Tanglish Negative (125)
    "mosam","kevalam","thunbam","thevai illa","azhudhu","kobam","valikuthu","romba mosam","sokka","kandupidikka mudiyala",
    "kandravedi","sirippu varala","kandam","seththu pochu","aluthhu","loosu","waste fellow","ketta paiyan","romba kevalam","sirappu illa",
    "azhukku","thimiru","thagudi illa","pirivu","siripu varala","thala valikkuthu","romba varutham","vetti","kovam","azhudhu thavara",
    "alunga","poramai","sirandhadhu illa","pazhaya scene","seriya illa","pazhaiya mosam","sombu","romba mosamana","pudhu problem","azhudhu mood",
    "vetkamana","mosamaana feeling","sirappu illa romba","sirandhadhu kedu","siranda mosam","seriya kevalam","kevalamana","sirippu kedu","azhudhal","sokka life",
    "azhudhu poguthu","siranda illa","vetri kedu","azhudhu payan","sirappu thevai illa","romba kevalam","azhudhu than","kevalam pola","azhudhu moodu","sokka payan",
    "azhudhu poda","sirappu kadan","azhudhu scene","romba mosamana service","azhudhu thunbam","azhudhu aluthal","siranda mosam","azhudhu kadan","azhudhu sirippu","azhudhu paadu",
    "siranda illa romba","azhudhu sambavam","mosam pola","azhudhu sirandhadhu","azhudhu sirapu illa","azhudhu nalla illa","azhudhu kevalam","azhudhu kedaikkala","azhudhu sogam","azhudhu varutham",
    "azhudhu kovam","azhudhu siripu illa","azhudhu mosam pola","azhudhu paavam","azhudhu siranda kedu","azhudhu vetkam","azhudhu seththu pochu","azhudhu loosu","azhudhu sokka","azhudhu problem",
    "azhudhu kadan romba","azhudhu thimiru","azhudhu kevalamana","azhudhu sirappu illa","azhudhu vetri illa","azhudhu waste","azhudhu sokka payan","azhudhu sogam pola","azhudhu vetkamana","azhudhu aluthal",
    "azhudhu thunbam pola","azhudhu scene romba","azhudhu ketta paiyan","azhudhu mosam payan","azhudhu romba kevalam","azhudhu sirappu thevai illa","azhudhu sokka scene","azhudhu siripu varala","azhudhu valikuthu","azhudhu siranda illa"
])

# Negation words
negation_words = set(["not", "no", "illa", "illai", "kidayathu", "vendam"])

# Intensifiers
intensifiers = set(["very", "so", "too", "romba", "super", "semma", "extremely"])

# ------------------------------
# Preprocessing + Analyzer
# ------------------------------
def clean_text(text):
    """Lowercase + keep Tamil and English letters"""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\u0B80-\u0BFF\s]", "", text)
    return text

def analyze_sentiment(text):
    text = clean_text(text)
    words = text.split()

    pos_score, neg_score = 0, 0
    skip_next = False

    for i, word in enumerate(words):
        if skip_next:
            skip_next = False
            continue

        # Negation flips
        if word in negation_words and i + 1 < len(words):
            next_word = words[i + 1]
            if next_word in positive_words:
                neg_score += 1
                skip_next = True
            elif next_word in negative_words:
                pos_score += 1
                skip_next = True

        # Intensifiers boost
        elif word in intensifiers and i + 1 < len(words):
            next_word = words[i + 1]
            if next_word in positive_words:
                pos_score += 2
                skip_next = True
            elif next_word in negative_words:
                neg_score += 2
                skip_next = True

        # Normal matches
        elif word in positive_words:
            pos_score += 1
        elif word in negative_words:
            neg_score += 1

    if pos_score > neg_score:
        return f"Positive 😀 (score: {pos_score})"
    elif neg_score > pos_score:
        return f"Negative 😞 (score: {neg_score})"
    else:
        return "Neutral 😐"

# ------------------------------
# Test
# ------------------------------
examples = [
    "Semma awesomeu da! Vera level magizhchi.",  # Positive
    "Indha padam romba mosam and boring.",        # Negative
    "Illa idhu good illa, romba kevalam.",        # Negative
    "Movie was not bad, actually super.",         # Positive
    "Santosham da! Vetri than.",                  # Positive
    "Service romba waste, sokka paduthu.",        # Negative
]

for s in examples:
    print(f"{s} → {analyze_sentiment(s)}")
