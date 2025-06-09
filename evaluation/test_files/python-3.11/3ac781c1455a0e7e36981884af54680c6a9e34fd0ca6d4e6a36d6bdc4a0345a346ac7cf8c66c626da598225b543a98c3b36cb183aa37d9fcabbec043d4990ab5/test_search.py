import os
from typing import Any, Dict
import pytest
from sentence_transformers import SentenceTransformer
from nucliadb_sdk import Entity, File, KnowledgeBox
from nucliadb_sdk.labels import Label
from nucliadb_sdk.search import ResultType, ScoreType
TESTING_IN_CI = os.environ.get('CI') == 'true'
DATA: Dict[str, Any] = {'text': ['Sunday afternoon walking through Venice in the sun with @user ️ ️ ️ @ Abbot Kinney, Venice', "Time for some BBQ and whiskey libations. Chomp, belch, chomp! (@ Lucille's Smokehouse Bar-B-Que)", 'Love love love all these people ️ ️ ️ #friends #bff #celebrate #blessed #sundayfunday @ San…', '️ ️ ️ ️ @ Toys"R"Us', 'Man these are the funniest kids ever!! That face! #HappyBirthdayBubb @ FLIPnOUT Xtreme', '#sandiego @ San Diego, California', 'My little ️ ️ ️ ️ ️ #ObsessedWithMyDog @ Cafe Solstice Capitol Hill', 'More #tinyepic things #tinyepicwestern, this one is crazy @user I may be one of your…', 'Last night ️ @ Omnia Night Club At Caesars Palace', 'friendship at its finest. ....#pixar #toystory #buzz #woody #friends #friendship #bff…', "I L VE working for a cause! Yesterday's balloon decor for SNN 11th Annual Back 2 School Health…", "Dem shoes tho! Lol! ...I'm getting some! Get ready copleypriceymca…", 'I love weekends with you, calebrancourt @ Cannery Row At Monterey Bay, CA', 'Yesss! August is full of love and birthdays ️ @ Los Angeles,…', 'I took a pic with Eminem! *still not over that performance vibe from #parrisproject!…', "I L VE working for a cause! Yesterday's balloon decor for SNN 11th Annual Back 2 School Health…", 'Sundays are all about the cute babies and dogs! #Ballard #sundaymarket #littelestmodel…', 'it was too hot .. trying to find shade behind @user at the roadraceengineering booth…', 'Sometimes you just have to be a kid Skyspace, Los Angeles. #CRStylesTravel #FunDay #LALife…', 'had an amazing night, with some pretty amazing people @ Pandora Summer', 'Thank you @user for an incredible night last night @ Shrine Auditorium &amp; Expo Hall', 'thanks for the amazing night @ Pandora Summer', '@user draw the line ~', 'This is why I hate when Taylor visits #Bunny #NotCaturday @ Our House', 'thank you to my boys for performing so well last night, I love you all very much @ Pandora…', '2nd theater and 3rd movie of the day a new record #badmoms #suicidesquad #sausageparty (at @user', 'In honor of #happygayunclesday ️ #happygunclesday #guncle #guncles @ Chula Vista, California', "I think it's nap time for us @ Los Angeles, California", "I L VE working for a cause! Yesterday's balloon decor for SNN 11th Annual Back 2 School Health…", 'Chasing #mclarenp1 in Malibu today.________________________________________ : credit: @user', 'Sunday afternoon at home! Drinking good wine and enjoying this incredible view to the sound of…', '#Lunch @user best #Ribs in #SanDiego (at @user in San Diego, CA)', "Here's to the start of a great adventure. Niners today, Alaska tomorrow. #grams @ Levi's Stadium", 'Really horrible seats for a really awful Sunday afternoon! Life is really bad #soundersfc.…', 'Enjoy your last days of summer! Clearly, mauricethewhale is enjoying his! #ladykiller…', 'Surprised everyone by actually surviving a weekend in the wild (however still came close to…', 'In the zone | : @user #colorsworldwide #RnBOnly @ The Regent', '“Me &amp; Catherine Sutherland!!!” #PowerMorphicon2016 #PowerRangersZeo #PowerRangersTurbo…', "Taped up and dripped out. Know what I'm talking bout #paint #painting #diy #homeimprovement…", 'princesscruises @ Port of Seattle, Pier 91', 'Stay classy #SanDiego (@ San Diego International Airport - @user in San Diego, CA)', 'I ️ the people I work with. Enjoying our Sunday watching the first…', "Another big happy 18th birthday to my partner in crime ️ I love u and all the crazy times we've…", 'Day is DONE! Thank u INSTA-LIKERS! Rollicking day at FRINGE! C U THURSDAY~~~and then some .…', 'SnakeShred recording guitars for the new SnakeSkin record #guitar #recording #api #apipegged…', 'My sisters, my best friends #hamessisters #andlewisandclark…', 'my absolute favorite place. @ La Jolla Cove Seal Beach', 'To live is an awfully big adventure #Seattle #spaceneedle @ Space Needle', 'Finally met Snow White ! She was my favorite when i was little :) #SnowWhite #Disneyland @user', '@user loved your coverage at TI as always, now need to get you on some of those Sounders matches...', "Saturdayzzz w/ Lionel Richie @ Harvey's Outdoor Ampitheater", 'All the beautiful ladies that helped make last night #APositiveExperience @ Upscale Salon', 'Sunday funday indeed #sundayfunday #igers #igdaily #instalike #enjoylife #asian #LA…', 'Lights, Camera, Action @ Hollywood Walk of Fame', "Found your Unicorn @user it's a pillow/stuffed toy and every pride weekend it…", 'Harry Potter ️ @ TCL Chinese Theatres', 'My key was still here...thank the Lawd #littlehoneyvee #doodles #doodleoftheday #illustration…', '️ ️ ️ @ Los Angeles, California', 'Absolutely in love with this ethereal glow on holytolidoitseric. Who would rock this look?…', 'Getting up that ice wall one ax at a time : pechoi11 @ Mount Shasta, California', 'Sephora is my favorite place @ SEPHORA', 'Tutorial time w/ @user @user @ Stern Grove Festival', 'I love my people! @ Paso Robles, California', 'Rad Fashion at the midway SF on a Sunday ️ ️ ️ @ The Midway SF', 'Just like the movie... Radiator Springs ️ #cars #inlove…', 'Cheers to Bruce on his birthday. ️#westhollywood…', 'My bears! #cityfest ️ ️ ️ @ Babycakes San Diego', 'gonna miss you guys so much. thank you for an amazing experience ️#ballyhoocarrie…', 'MATTRESS HELPER - new again SAGGING #BED #FIRMER #fix #guaranteed #sleepless #needsleep…', 'Just that sound alone makes the world stop ️ @ Sausalito, California', '#ExclusiveBaseballPicks are KILLING the #Bookie like always. #WeeklyRecap 8/8-8/14. 96-3…', 'My lady love beautiful friend #doubleLtrouble #leilavie #beachour @ Stinson Beach, California', 'My date for tonight @ Hotel Las Rocas', 'This weekend love was truly in the air but out of all the celeb weddings I have to say…', '@user hi from Tijuana B.C. See you soon', '️ #gramma @ Living Way Christian Fellowship', 'Acquired this stunner today at my new favorite spot Sharks Tooth #crassula.…', 'Birthday cheers with my favorite people!!#26again #justafewofmygirls #justafewofmygirls…', 'today was my first day of work at Victoria Secret SO happy and SO…', 'Taking bae to all my favorite #LA spots. #gettycenter @ Getty Center', 'So much fun this weekend celebrating the bride to be. #MalliesLastRally @ Las Vegas, Nevada', 'Love this picture of me and baby Eve at Disneyland earlier today …', "The one photo I've taken with my Mother that I like for once. -08/13/16, Sat. @ El Dorado…", 'Love my bed @ Downey, California', "So cute!! #KnottsBerryFarm #Charlie #Snoopy #Woodstock @ Knott's Berry Farm", 'I ️ Faure Requiem @user oboyddd @ Walt Disney Concert Hall', '️ @ Columbia River', "No I don't have any carrots!! #seattlepoloclub #horse #horses @ Seattle Polo &amp; Equestrian Club", 'My favourite place in California #YosemiteNationalPark #California @ Yosemite Wilderness', '#sundayfunday #live at allure... @user @user @user', 'My babies ️ ️ ️ #cat #dog #catsofinstagram #dogsofinstagram #lovemyfurbabies @ Port Hueneme,…', 'Photo taken Thursday at SDCC2016 by MannyLLanura Photography. #widowmaker #overwatch…', 'Hello there, my king Jareth #bowie #goblinking #labyrinth @ Los Angeles, California', 'These Teens @ ARIA Resort &amp; Casino', 'Sunday views #hike #waterfall #waterfallhike #latourellfalls #hikeoregon #hikepnw #whyihike…', '"Beauty begins the moment you decide to be yourself" -Coco Chanel love this!Skin is the largest…', 'Caught by the lens of Yc Wong. photo by 8888tiger8888 suit by virginblak #ljifff…', 'Weldone champ #babrain #alikhamis #rio #rio2016 #olympics @ Los…', 'Took a lil trip to Tahoe #iputhehoeintahoe @ Incline Village At…', 'About to hang out with a bunch of #Armenians and #Russians...trying to fit in Sporting my…'], 'label': [12, 19, 0, 0, 2, 11, 0, 19, 0, 7, 1, 2, 9, 0, 1, 1, 1, 4, 19, 8, 7, 8, 5, 2, 8, 2, 0, 1, 1, 10, 8, 14, 1, 16, 2, 14, 18, 6, 6, 8, 14, 0, 0, 9, 19, 13, 3, 8, 0, 16, 7, 7, 6, 6, 2, 0, 0, 0, 1, 18, 7, 2, 8, 0, 0, 0, 0, 0, 7, 0, 19, 1, 1, 0, 14, 0, 1, 14, 1, 8, 3, 1, 5, 1, 1, 0, 12, 2, 1, 6, 0, 10, 0, 14, 12, 13, 18, 7, 8, 19]}

def test_search_resource(knowledgebox: KnowledgeBox):
    text: str
    for index, text in enumerate(DATA['text']):
        if index == 50:
            break
        label = DATA['label'][index]
        knowledgebox.create_resource(text=text, labels=[f'emoji/{label}'], vectors={'all-MiniLM-L6-v2': [1.0, 2.0, 3.0, 2.0]})
    assert len(knowledgebox) == 50
    labels = knowledgebox.get_uploaded_labels()
    assert labels['emoji'].count == 50 * 2
    assert labels['emoji'].labels['0'] == 9 * 2
    resources = knowledgebox.search(text='love')
    assert resources.fulltext.total == 5
    assert len(resources.resources) == 5
    resources = knowledgebox.search(filter=[Label(labelset='emoji', label='0')])
    assert resources.fulltext.total == 9 * 2
    resources = knowledgebox.search(filter=['emoji/0'])
    assert resources.fulltext.total == 9 * 2
    vector_q = [1.0, 2.0, 3.0, 2.0]
    results = knowledgebox.search(vector=vector_q, vectorset='all-MiniLM-L6-v2', min_score=0.7, page_number=0, page_size=20)
    assert len(results.sentences.results) == 20

@pytest.mark.skipif(TESTING_IN_CI, reason='It is accessing the HuggingFace API')
def test_standard_examples(knowledgebox: KnowledgeBox):
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    knowledgebox.create_resource(title='Happy dog', binary=File(data=b'Happy dog file data', filename='data.txt'), text="I'm Sierra, a very happy dog", labels=['emotion/positive'], entities=[Entity(type='NAME', value='Sierra', positions=[(4, 9)])], vectors={'all-MiniLM-L6-v2': encoder.encode(["I'm Sierra, a very happy dog"])[0]})
    sentences = [('Day 1', "She's having a terrible day", 'emotion/negative'), ('Day 2', 'what a delighful day', 'emotion/positive'), ('Day 3', 'Dog in catalan is gos', 'emotion/neutral'), ('Day 4', 'he is heartbroken', 'emotion/negative'), ('Day 5', 'He said that the race is quite tough', 'emotion/neutral'), ('Day 6', 'love is tough', 'emotion/negative')]
    for title, sentence, label in sentences:
        knowledgebox.create_resource(title=title, text=sentence, labels=[label], vectors={'all-MiniLM-L6-v2': encoder.encode([sentence])[0]})
    results = list(knowledgebox.search(vector=encoder.encode(['To be in love'])[0], vectorset='all-MiniLM-L6-v2', min_score=0.25))
    assert len(results) == 2
    assert results[0].text == 'love is tough'
    assert results[0].labels == ['negative']
    assert results[0].score_type == ScoreType.COSINE
    assert results[1].text == 'he is heartbroken'
    assert results[1].labels == ['negative']
    assert results[0].score_type == ScoreType.COSINE
    results = list(knowledgebox.search(text='dog'))
    assert len(results) == 4
    assert results[0].text == 'Happy dog'
    assert results[0].labels == ['positive']
    assert results[0].score_type == ScoreType.BM25
    assert results[0].result_type == ResultType.FULLTEXT
    assert results[1].text == 'Dog in catalan is gos'
    assert results[1].labels == ['neutral']
    assert results[1].score_type == ScoreType.BM25
    assert results[1].result_type == ResultType.FULLTEXT
    assert results[2].text == "I'm Sierra, a very happy dog"
    assert results[2].labels == ['positive']
    assert results[2].score_type == ScoreType.BM25
    assert results[2].result_type == ResultType.FULLTEXT
    assert results[3].text == 'Happy dog'
    assert results[3].labels == ['positive']
    assert results[3].result_type == ResultType.PARAGRAPH
    results = list(knowledgebox.search(filter=['emotion/positive']))
    assert len(results) == 6
    assert set([r.text for r in results]) == set(['what a delighful day', 'Happy dog', "I'm Sierra, a very happy dog", 'Day 2'])

def test_search_resource_simple_label(knowledgebox: KnowledgeBox):
    text: str
    for index, text in enumerate(DATA['text']):
        if index == 50:
            break
        label = DATA['label'][index]
        knowledgebox.create_resource(text=text, labels=[str(label)], vectors={'all-MiniLM-L6-v2': [1.0, 2.0, 3.0, 2.0]})
    assert len(knowledgebox) == 50
    labels = knowledgebox.get_uploaded_labels()
    assert labels['default'].count == 100
    assert labels['default'].labels['0'] == 18
    resources = knowledgebox.search(text='love')
    assert resources.fulltext.total == 5
    assert len(resources.resources) == 5
    resources = knowledgebox.search(filter=['12'])
    vector_q = [1.0, 2.0, 3.0, 2.0]
    resources = knowledgebox.search(vector=vector_q, vectorset='all-MiniLM-L6-v2')