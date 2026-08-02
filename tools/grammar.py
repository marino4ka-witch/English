#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Генерирует фразы-паттерны: один глагол во всех лицах и временах
# (утверждение / отрицание / вопрос). Русскую грамматику задаём вручную —
# английские паттерны и транскрипцию собирает скрипт. => корректно и много.
import io

OUT="/home/user/English/словарь/грамматика.csv"

# местоимения: (En, en_lower, ipa, ru, tag)
PR=[("I","I","aɪ","я","1s"),("You","you","juː","ты","2s"),
    ("He","he","hiː","он","3m"),("She","she","ʃiː","она","3f"),
    ("We","we","wiː","мы","1p"),("They","they","ðeɪ","они","3p")]

def be_form(tag):
    if tag=="1s":return ("am","æm")
    if tag in("3m","3f"):return ("is","ɪz")
    return ("are","ɑː")

def budu(inf):  # будущее несов. вида: "буду + инф"
    return "|".join(x+" "+inf for x in ["буду","будешь","будет","будет","будем","будут"])

rows=[]  # (En, ipa, Ru)
def add(en,ipa,ru): rows.append((en,"/"+ipa+"/",ru))

# ── описание глагола ──
# en=(base,s,ing,past) ipa=(base,s,ing,past)
# hab/now/fut = 6 форм через | (я,ты,он,она,мы,они); past = masc|fem|pl
# stative=True → без Present Continuous
def verb(en,ipa,hab,fut,past,now=None,stative=False,head=None):
    base,s,ing,pst=en; ib,isg,iing,ipst=ipa
    H=hab.split("|"); N=(now or hab).split("|"); F=fut.split("|")
    pm,pf,ppl=past.split("|")
    PB={"1s":pm+"(а)","2s":pm+"(а)","3m":pm,"3f":pf,"1p":ppl,"3p":ppl}
    if head: rows.append(("# "+head,"",""))
    for i,(En,el,pi,ru,tag) in enumerate(PR):
        is3=tag in("3m","3f")
        vf=s if is3 else base; vfi=isg if is3 else ib
        neg="doesn't" if is3 else "don't"; negi="ˈdʌzənt" if is3 else "dəʊnt"
        qd="Does" if is3 else "Do"; qdi="dʌz" if is3 else "duː"
        # Present Simple
        add(f"{En} {vf}",f"{pi} {vfi}",f"{ru} {H[i]}")
        add(f"{En} {neg} {base}",f"{pi} {negi} {ib}",f"{ru} не {H[i]}")
        add(f"{qd} {el} {base}?",f"{qdi} {pi} {ib}",f"{ru} {H[i]}?")
        # Present Continuous
        if not stative:
            bf,bi=be_form(tag)
            add(f"{En} {bf} {ing}",f"{pi} {bi} {iing}",f"{ru} {N[i]}")
            add(f"{En} {bf} not {ing}",f"{pi} {bi} nɒt {iing}",f"{ru} не {N[i]}")
            add(f"{bf.capitalize()} {el} {ing}?",f"{bi} {pi} {iing}",f"{ru} {N[i]}?")
        # Future
        add(f"{En} will {base}",f"{pi} wɪl {ib}",f"{ru} {F[i]}")
        add(f"{En} won't {base}",f"{pi} wəʊnt {ib}",f"{ru} не {F[i]}")
        add(f"Will {el} {base}?",f"wɪl {pi} {ib}",f"{ru} {F[i]}?")
        # Past Simple
        add(f"{En} {pst}",f"{pi} {ipst}",f"{ru} {PB[tag]}")
        add(f"{En} didn't {base}",f"{pi} ˈdɪdənt {ib}",f"{ru} не {PB[tag]}")
        add(f"Did {el} {base}?",f"dɪd {pi} {ib}",f"{ru} {PB[tag]}?")

# ═══════════ BE: «я есть / она есть / я учитель / она врач / я дома» ═══════════
rows.append(("# ГРАММАТИКА · ГЛАГОЛ BE (быть)","",""))
BE_RU={"1s":"я есть","2s":"ты есть","3m":"он есть","3f":"она есть","1p":"мы есть","3p":"они есть"}
for En,el,pi,ru,tag in PR:
    bf,bi=be_form(tag)
    add(f"{En} {bf}",f"{pi} {bi}",BE_RU[tag])
    add(f"{En} {bf} not",f"{pi} {bi} nɒt",f"{ru} не...")
    add(f"{bf.capitalize()} {el}?",f"{bi} {pi}",f"это {ru}?")
# be + профессия (ед./мн.)
JOBS=[("a teacher","ə ˈtiːtʃər","учитель","учителя"),
      ("a doctor","ə ˈdɒktər","врач","врачи"),
      ("a driver","ə ˈdraɪvər","водитель","водители"),
      ("a student","ə ˈstjuːdənt","студент","студенты")]
for en,ip,sg,pl in JOBS:
    for En,el,pi,ru,tag in PR:
        bf,bi=be_form(tag); plural=tag in("1p","3p")
        noun_en = en.replace("a ","").replace("an ","")+"s" if plural else en
        noun_ip = ip+"z" if plural else ip
        noun_ru = pl if plural else sg
        add(f"{En} {bf} {noun_en}",f"{pi} {bi} {noun_ip}",f"{ru} {noun_ru}")
        add(f"{En} {bf} not {noun_en}",f"{pi} {bi} nɒt {noun_ip}",f"{ru} не {noun_ru}")
        add(f"{bf.capitalize()} {el} {noun_en}?",f"{bi} {pi} {noun_ip}",f"{ru} {noun_ru}?")
# be + место
LOC=[("at home","ət həʊm","дома"),("here","hɪər","здесь"),
     ("there","ðeər","там"),("at work","ət wɜːk","на работе")]
for en,ip,rul in LOC:
    for En,el,pi,ru,tag in PR:
        bf,bi=be_form(tag)
        add(f"{En} {bf} {en}",f"{pi} {bi} {ip}",f"{ru} {rul}")
        add(f"{En} {bf} not {en}",f"{pi} {bi} nɒt {ip}",f"{ru} не {rul}")
        add(f"{bf.capitalize()} {el} {en}?",f"{bi} {pi} {ip}",f"{ru} {rul}?")

# ═══════════ ГЛАГОЛЫ ВО ВСЕХ ВРЕМЕНАХ ═══════════
verb(("go","goes","going","went"),("ɡəʊ","ɡəʊz","ˈɡəʊɪŋ","went"),
     "хожу|ходишь|ходит|ходит|ходим|ходят",
     "пойду|пойдёшь|пойдёт|пойдёт|пойдём|пойдут","ходил|ходила|ходили",
     now="иду|идёшь|идёт|идёт|идём|идут",head="ГРАММАТИКА · GO (идти/ходить)")
verb(("come","comes","coming","came"),("kʌm","kʌmz","ˈkʌmɪŋ","keɪm"),
     "прихожу|приходишь|приходит|приходит|приходим|приходят",
     "приду|придёшь|придёт|придёт|придём|придут","приходил|приходила|приходили",
     head="ГРАММАТИКА · COME (приходить)")
verb(("do","does","doing","did"),("duː","dʌz","ˈduːɪŋ","dɪd"),
     "делаю|делаешь|делает|делает|делаем|делают",
     "сделаю|сделаешь|сделает|сделает|сделаем|сделают","делал|делала|делали",
     head="ГРАММАТИКА · DO (делать)")
verb(("want","wants","wanting","wanted"),("wɒnt","wɒnts","ˈwɒntɪŋ","ˈwɒntɪd"),
     "хочу|хочешь|хочет|хочет|хотим|хотят",
     "захочу|захочешь|захочет|захочет|захотим|захотят","хотел|хотела|хотели",
     head="ГРАММАТИКА · WANT (хотеть)")
verb(("eat","eats","eating","ate"),("iːt","iːts","ˈiːtɪŋ","eɪt"),
     "ем|ешь|ест|ест|едим|едят",
     "поем|поешь|поест|поест|поедим|поедят","ел|ела|ели",
     head="ГРАММАТИКА · EAT (есть/кушать)")
verb(("drink","drinks","drinking","drank"),("drɪŋk","drɪŋks","ˈdrɪŋkɪŋ","dræŋk"),
     "пью|пьёшь|пьёт|пьёт|пьём|пьют",
     "выпью|выпьешь|выпьет|выпьет|выпьем|выпьют","пил|пила|пили",
     head="ГРАММАТИКА · DRINK (пить)")
verb(("work","works","working","worked"),("wɜːk","wɜːks","ˈwɜːkɪŋ","wɜːkt"),
     "работаю|работаешь|работает|работает|работаем|работают",
     budu("работать"),"работал|работала|работали",
     head="ГРАММАТИКА · WORK (работать)")
verb(("live","lives","living","lived"),("lɪv","lɪvz","ˈlɪvɪŋ","lɪvd"),
     "живу|живёшь|живёт|живёт|живём|живут",
     budu("жить"),"жил|жила|жили",head="ГРАММАТИКА · LIVE (жить)")
verb(("speak","speaks","speaking","spoke"),("spiːk","spiːks","ˈspiːkɪŋ","spəʊk"),
     "говорю|говоришь|говорит|говорит|говорим|говорят",
     budu("говорить"),"говорил|говорила|говорили",
     head="ГРАММАТИКА · SPEAK (говорить)")
verb(("read","reads","reading","read"),("riːd","riːdz","ˈriːdɪŋ","red"),
     "читаю|читаешь|читает|читает|читаем|читают",
     budu("читать"),"читал|читала|читали",head="ГРАММАТИКА · READ (читать)")
verb(("play","plays","playing","played"),("pleɪ","pleɪz","ˈpleɪɪŋ","pleɪd"),
     "играю|играешь|играет|играет|играем|играют",
     budu("играть"),"играл|играла|играли",head="ГРАММАТИКА · PLAY (играть)")
verb(("watch","watches","watching","watched"),("wɒtʃ","ˈwɒtʃɪz","ˈwɒtʃɪŋ","wɒtʃt"),
     "смотрю|смотришь|смотрит|смотрит|смотрим|смотрят",
     "посмотрю|посмотришь|посмотрит|посмотрит|посмотрим|посмотрят","смотрел|смотрела|смотрели",
     head="ГРАММАТИКА · WATCH (смотреть)")
verb(("help","helps","helping","helped"),("help","helps","ˈhelpɪŋ","helpt"),
     "помогаю|помогаешь|помогает|помогает|помогаем|помогают",
     "помогу|поможешь|поможет|поможет|поможем|помогут","помогал|помогала|помогали",
     head="ГРАММАТИКА · HELP (помогать)")
verb(("wait","waits","waiting","waited"),("weɪt","weɪts","ˈweɪtɪŋ","ˈweɪtɪd"),
     "жду|ждёшь|ждёт|ждёт|ждём|ждут",
     "подожду|подождёшь|подождёт|подождёт|подождём|подождут","ждал|ждала|ждали",
     head="ГРАММАТИКА · WAIT (ждать)")
verb(("sleep","sleeps","sleeping","slept"),("sliːp","sliːps","ˈsliːpɪŋ","slept"),
     "сплю|спишь|спит|спит|спим|спят",
     budu("спать"),"спал|спала|спали",head="ГРАММАТИКА · SLEEP (спать)")
verb(("cook","cooks","cooking","cooked"),("kʊk","kʊks","ˈkʊkɪŋ","kʊkt"),
     "готовлю|готовишь|готовит|готовит|готовим|готовят",
     "приготовлю|приготовишь|приготовит|приготовит|приготовим|приготовят","готовил|готовила|готовили",
     head="ГРАММАТИКА · COOK (готовить)")
verb(("take","takes","taking","took"),("teɪk","teɪks","ˈteɪkɪŋ","tʊk"),
     "беру|берёшь|берёт|берёт|берём|берут",
     "возьму|возьмёшь|возьмёт|возьмёт|возьмём|возьмут","брал|брала|брали",
     head="ГРАММАТИКА · TAKE (брать)")
verb(("give","gives","giving","gave"),("ɡɪv","ɡɪvz","ˈɡɪvɪŋ","ɡeɪv"),
     "даю|даёшь|даёт|даёт|даём|дают",
     "дам|дашь|даст|даст|дадим|дадут","давал|давала|давали",
     head="ГРАММАТИКА · GIVE (давать)")
verb(("buy","buys","buying","bought"),("baɪ","baɪz","ˈbaɪɪŋ","bɔːt"),
     "покупаю|покупаешь|покупает|покупает|покупаем|покупают",
     "куплю|купишь|купит|купит|купим|купят","покупал|покупала|покупали",
     head="ГРАММАТИКА · BUY (покупать)")
verb(("run","runs","running","ran"),("rʌn","rʌnz","ˈrʌnɪŋ","ræn"),
     "бегаю|бегаешь|бегает|бегает|бегаем|бегают",
     "побегу|побежишь|побежит|побежит|побежим|побегут","бегал|бегала|бегали",
     now="бегу|бежишь|бежит|бежит|бежим|бегут",head="ГРАММАТИКА · RUN (бегать/бежать)")
verb(("open","opens","opening","opened"),("ˈəʊpən","ˈəʊpənz","ˈəʊpənɪŋ","ˈəʊpənd"),
     "открываю|открываешь|открывает|открывает|открываем|открывают",
     "открою|откроешь|откроет|откроет|откроем|откроют","открывал|открывала|открывали",
     head="ГРАММАТИКА · OPEN (открывать)")
verb(("meet","meets","meeting","met"),("miːt","miːts","ˈmiːtɪŋ","met"),
     "встречаю|встречаешь|встречает|встречает|встречаем|встречают",
     "встречу|встретишь|встретит|встретит|встретим|встретят","встречал|встречала|встречали",
     head="ГРАММАТИКА · MEET (встречать)")
verb(("drive","drives","driving","drove"),("draɪv","draɪvz","ˈdraɪvɪŋ","drəʊv"),
     "вожу|водишь|водит|водит|водим|водят",
     "поеду|поедешь|поедет|поедет|поедем|поедут","водил|водила|водили",
     now="еду|едешь|едет|едет|едем|едут",head="ГРАММАТИКА · DRIVE (водить/ехать)")
verb(("write","writes","writing","wrote"),("raɪt","raɪts","ˈraɪtɪŋ","rəʊt"),
     "пишу|пишешь|пишет|пишет|пишем|пишут",
     "напишу|напишешь|напишет|напишет|напишем|напишут","писал|писала|писали",
     head="ГРАММАТИКА · WRITE (писать)")
verb(("sing","sings","singing","sang"),("sɪŋ","sɪŋz","ˈsɪŋɪŋ","sæŋ"),
     "пою|поёшь|поёт|поёт|поём|поют",
     "спою|споёшь|споёт|споёт|споём|споют","пел|пела|пели",
     head="ГРАММАТИКА · SING (петь)")
verb(("dance","dances","dancing","danced"),("dɑːns","ˈdɑːnsɪz","ˈdɑːnsɪŋ","dɑːnst"),
     "танцую|танцуешь|танцует|танцует|танцуем|танцуют",
     budu("танцевать"),"танцевал|танцевала|танцевали",
     head="ГРАММАТИКА · DANCE (танцевать)")
# стативные (без Present Continuous)
verb(("know","knows","knowing","knew"),("nəʊ","nəʊz","ˈnəʊɪŋ","njuː"),
     "знаю|знаешь|знает|знает|знаем|знают",
     "узнаю|узнаешь|узнает|узнает|узнаем|узнают","знал|знала|знали",
     stative=True,head="ГРАММАТИКА · KNOW (знать)")
verb(("see","sees","seeing","saw"),("siː","siːz","ˈsiːɪŋ","sɔː"),
     "вижу|видишь|видит|видит|видим|видят",
     "увижу|увидишь|увидит|увидит|увидим|увидят","видел|видела|видели",
     stative=True,head="ГРАММАТИКА · SEE (видеть)")
verb(("love","loves","loving","loved"),("lʌv","lʌvz","ˈlʌvɪŋ","lʌvd"),
     "люблю|любишь|любит|любит|любим|любят",
     budu("любить"),"любил|любила|любили",
     stative=True,head="ГРАММАТИКА · LOVE (любить)")

# ═══════════ МОДАЛЬНЫЕ ГЛАГОЛЫ ═══════════
MOD=[
 ("I can swim","aɪ kæn swɪm","я умею плавать"),
 ("I can help","aɪ kæn help","я могу помочь"),
 ("I can't sleep","aɪ kɑːnt sliːp","я не могу спать"),
 ("Can you help me?","kæn juː help miː","ты можешь мне помочь?"),
 ("She can drive","ʃiː kæn draɪv","она умеет водить"),
 ("You must go","juː mʌst ɡəʊ","ты должен(на) идти"),
 ("I must work","aɪ mʌst wɜːk","я должен(на) работать"),
 ("You mustn't lie","juː ˈmʌsənt laɪ","тебе нельзя лгать"),
 ("I should sleep","aɪ ʃʊd sliːp","мне следует поспать"),
 ("You should rest","juː ʃʊd rest","тебе стоит отдохнуть"),
 ("We should try","wiː ʃʊd traɪ","нам стоит попробовать"),
 ("I have to go","aɪ hæv tuː ɡəʊ","мне нужно идти"),
 ("She has to work","ʃiː hæz tuː wɜːk","ей нужно работать"),
 ("I don't have to go","aɪ dəʊnt hæv tuː ɡəʊ","мне не обязательно идти"),
 ("I would like to eat","aɪ wʊd laɪk tuː iːt","я хотел(а) бы поесть"),
 ("I'd like a coffee","aɪd laɪk ə ˈkɒfi","я хотел(а) бы кофе"),
 ("Would you like tea?","wʊd juː laɪk tiː","хочешь чаю?"),
 ("He might come","hiː maɪt kʌm","он, возможно, придёт"),
 ("It might rain","ɪt maɪt reɪn","возможно, будет дождь"),
 ("I will help you","aɪ wɪl help juː","я тебе помогу"),
 ("I won't give up","aɪ wəʊnt ɡɪv ʌp","я не сдамся"),
 ("Could you repeat?","kʊd juː rɪˈpiːt","не могли бы вы повторить?"),
 ("May I come in?","meɪ aɪ kʌm ɪn","можно войти?"),
 ("We can try again","wiː kæn traɪ əˈɡen","мы можем попробовать снова"),
 ("You may sit down","juː meɪ sɪt daʊn","можете сесть"),
]
rows.append(("# ГРАММАТИКА · МОДАЛЬНЫЕ (can/must/should/have to/would like)","",""))
for en,ip,ru in MOD: add(en,ip,ru)

# ═══════════ ФРАЗОВЫЕ ГЛАГОЛЫ В ПРЕДЛОЖЕНИЯХ ═══════════
PHR=[
 ("I get up early","aɪ ɡet ʌp ˈɜːli","я встаю рано"),
 ("I wake up at seven","aɪ weɪk ʌp ət ˈsevən","я просыпаюсь в семь"),
 ("Please sit down","pliːz sɪt daʊn","сядь(те), пожалуйста"),
 ("Stand up, please","stænd ʌp pliːz","встань(те), пожалуйста"),
 ("Turn on the light","tɜːn ɒn ðə laɪt","включи свет"),
 ("Turn off the TV","tɜːn ɒf ðə ˌtiːˈviː","выключи телевизор"),
 ("Don't give up","dəʊnt ɡɪv ʌp","не сдавайся"),
 ("I woke up late","aɪ wəʊk ʌp leɪt","я проснулся(ась) поздно"),
 ("Look out!","lʊk aʊt","берегись!"),
 ("Come in, please","kʌm ɪn pliːz","входи(те), пожалуйста"),
 ("Wait for me","weɪt fɔːr miː","подожди меня"),
 ("I'm looking for my keys","aɪm ˈlʊkɪŋ fɔːr maɪ kiːz","я ищу свои ключи"),
 ("Calm down","kɑːm daʊn","успокойся"),
 ("Hurry up!","ˈhʌri ʌp","поторопись!"),
 ("I look after my kids","aɪ lʊk ˈɑːftər maɪ kɪdz","я забочусь о детях"),
 ("Get on the bus","ɡet ɒn ðə bʌs","садись в автобус"),
 ("Get off here","ɡet ɒf hɪər","выходи здесь"),
 ("Put on your coat","pʊt ɒn jɔːr kəʊt","надень пальто"),
 ("Take off your shoes","teɪk ɒf jɔːr ʃuːz","сними обувь"),
 ("I found out the truth","aɪ faʊnd aʊt ðə truːθ","я узнал(а) правду"),
]
rows.append(("# ГРАММАТИКА · ФРАЗОВЫЕ ГЛАГОЛЫ","",""))
for en,ip,ru in PHR: add(en,ip,ru)

with io.open(OUT,"w",encoding="utf-8") as f:
    f.write("English,Transcription,Русский\n")
    for en,ip,ru in rows:
        if en.startswith("# "):
            f.write(en+"\n")
        else:
            f.write(f"{en},{ip},{ru}\n")

data=[r for r in rows if not r[0].startswith("# ")]
print(f"Сгенерировано паттернов: {len(data)}")
