from texts.models import Text, Author
author_1 = Author.objects.create(name_chinese="李商隱",
                                 name_pinyin="Li Shangyin")
title_french_1 = "Cithare ornée de brocart"
title_chinese_1 = "錦瑟"
content_chinese_1 = """
錦瑟無端五十弦
一弦一柱思華年
莊生曉夢迷蝴蝶
望帝春心託杜鵑
滄海月明珠有淚
藍田日暖玉生煙
此情可待成追憶
只是當時已惘然
"""
content_pinyin_1 = """
Jǐn sè wúduān wǔshí xián
yī xián yī zhù sī huá nián
zhuāngshēngxiǎo mèng mí húdié
wàng dì chūnxīn tuō dùjuān
cānghǎi yuè míngzhū yǒu lèi
lántián rì nuǎn yùshēng yān
cǐ qíng kě dài chéng zhuīyì
zhǐshì dāngshí yǐ wǎngrán
"""
content_french_1 = """
cithare ornée pur hasard / avec cinquante cordes
chaque corde chaque chevalet / penser années fleuries
Lettré Zhuang rêve matinal / s’égarer papilloon
empereur Wang coeur printanier / se confier tourterelle
mer vaste lune claire / perle avoir larme
champ bleu soleil chaud / jade naître fumée
cette passion pouvoir durer / devenir poursuite mémoire
seulement instant même / déjà dé-possédé
"""

author_2 = Author.objects.create(name_chinese="陶淵明",
                                 name_pinyin="Tao Yuanming")
title_french_2 = "Buvant le vin"
title_chinese_2 = "饮酒"
content_chinese_2 = """
结庐在人境
而无车马喧
问君何能尔
心远地自偏
采菊东篱下
悠悠见南山
山气日夕佳
飞鸟相与还
此中有真意
欲辩已忘言
"""
content_pinyin_2 = """
Jié lú zài rén jìng
Ér wú chē mǎ xuān
Wèn jūn hé néng ěr
Xīn yuǎn dì zì piān
Cǎi jú dōng lí xià
Yōuyōu jiàn nánshān
Shān qì rì xījiā
Fēiniǎo xiāng yǔ hái
Cǐ zhōng yǒu zhēnyì
Yù biàn yǐ wàng yán
"""
content_french_2 = """
construire une cabane dans le monde des hommes...
mais sans bruit de voitures et de chevaux
vous demandez, Monsieur, comment en être capable ?
retiré au lieu d’origine, le cœur est loin...
cueillant des chrysanthèmes sous la haie de l’Est
étant ainsi pensif, contemplant les monts du Sud
souffle des montagnes, charme du jour et de la nuit
les oiseaux volent, ensemble ils s’en retournent
dans tout ceci est le sens réel
sur le point de le dire, ah ! oublier les mots...
"""
text_1 = Text.objects.create(title_french=title_french_1,
                             title_chinese=title_chinese_1,
                             content_french=content_french_1,
                             content_chinese=content_chinese_1,
                             author=author_1)
text_2 = Text.objects.create(title_french=title_french_2,
                             title_chinese=title_chinese_2,
                             content_french=content_french_2,
                             content_chinese=content_chinese_2,
                             author=author_2)
Text.objects.all()
