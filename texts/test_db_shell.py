from texts.models import Text, Author
author = Author.objects.create(name_chinese="shitao", name_pinyin="shitao")
text1 = Text.objects.create(title_french="the shitao poem", title_chinese="the shitao poem", content_french="Un poeme de Shitao", auteur = author)
text2 = Text.objects.create(title_french="the other shitao poem", title_chinese="the other shitao poem", content_french="Un autre poeme de Shitao", auteur = author)
Text.objects.all()