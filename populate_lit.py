import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'literature_breakdown.settings')

import django
django.setup()
from lit.models import UserProfile, Article


def populate():

    # gets two users already saved within the database, which
    # will be authors to the articles below
    user_1 = UserProfile.objects.first()
    user_2 = UserProfile.objects.last()

    articles = [
        {"author": user_1,
         "date_published": "02/01/18",
         "book": "Beyond Good and Evil",
         "views": 0,
         "title": "An Analysis of Beyond Good and Evil",
         "analysis": "An understanding of Nietzsche's work as a whole relies on a solid grasp of his views on truth and "
                     "language, and his metaphysics and conception of the will to power. At the very bottom of Nietzsche"
                     "'s philosophy lies the conviction that the universe is in a constant state of change, and his hatred "
                     "and disparagement of almost any position can be traced back to that position's temptation to look "
                     "at the universe as fixed in one place. Nietzsche is skeptical of both language and 'truth' because"
                     " they are liable to adopt a fixed perspective toward things. Words, unlike thoughts, are fixed."
                     " Our thoughts can flow and change just as things in the universe flow and change, but a word,"
                     " once uttered, cannot be changed. Because language has this tendency toward fixity, it expresses"
                     " the world in terms of facts and things, which has led philosophers to think of the world as fixed"
                     " rather than fluid. A world of rigid facts can be spoken about definitively, which is the source "
                     " of our conception of truth and other absolutes, such as God and morality.",
         "category": "Philosophy",
         "slug": "beyond-good-and-evil",
         "rating": 0.0,
         "book_author": "Friedrich Nietzsche",
         "book_published": "1886"
         },
        {"author": user_2,
         "date_published": "19/02/18",
         "book": "The Gift of the Magi",
         "views": 0,
         "title": "Review of 'The Gift of the Magi'",
         "analysis": "If you are looking for a Christmas story that doesn’t feature either a nativity or Santa, The "
                     "Gift of the Magi is a story that reinforces the value of selfless giving. This classic story by "
                     "O. Henry (William Sydney Porter) shares the story of Jim and Della as they seek to show their "
                     "love for each other in a special Christmas gift despite their poverty. Hard times have hit the "
                     "Dillingham Young family. Earning only $20 per week, Jim and his wife Della can barely make ends "
                     "meet and certainly can’t afford to buy each other expensive gifts for Christmas. Despite this,"
                     " they each want to find the perfect gift to show their love. In a beautiful tragedy, each "
                     "sacrifices something the other treasures in order to earn the money to purchase a gift. The author"
                     " refers to them as ‘two foolish children’ for doing so, but also describes them as wise, for they "
                     "understood the value of love and showing their love to each other. The language of this story is"
                     " formal, but the message is one that can be understood by children as well as adults. The "
                     "illustrations in this edition are beautifully suited to the story, capturing the feeling of the "
                     "relationship between Della and Jim in this classic story first published over 100 years ago.",
         "category": "Short Story",
         "slug": "gift-of-magi",
         "rating": 0.0,
         "book_author": "O. Henry",
         "book_published": "1906"
         },
        {"author": user_1,
         "date_published": "03/03/18",
         "book": "Plato's Republic",
         "views": 0,
         "title": "An Overview of 'Plato's Republic'",
         "analysis": "The Republic is arguably the most popular and most widely taught of Plato's writings. Although it"
                     " contains its dramatic moments and it employs certain literary devices, it is not a play, a novel,"
                     " a story; it is not, in a strict sense, an essay. It is a kind of extended conversation that "
                     "embraces a central argument, an argument that is advanced by the proponent of the argument, "
                     "Socrates. The Republic may be seen as a kind of debate, a fitting description for most of the Dialogues."
                     "It is Plato's intent in this dialogue to establish, philosophically, the ideal state, a state "
                     "that would stand as a model for all emerging or existing societies currently functioning during "
                     "Plato's time and extending into our own times. And we are to infer that any proposed changes in "
                     "the policy of effecting justice in any state would have to meet the criteria of the ideal state: "
                     "the Republic. Since its first appearance, the Republic has traditionally been published in ten "
                     "books, probably from its having been so divided into ten 'books' in its manuscript form. In order "
                     "to clarify its argument, this Note further subdivides those ten books in its discussion.",
         "category": "Philosophy",
         "slug": "platos-republic",
         "rating": 0.0,
         "book_author": "Plato",
         "book_published": "380 BC"
         },
        {"author": user_2,
         "date_published": "09/03/18",
         "book": "The Bible",
         "views": 0,
         "title": "Critical Study of Matthew 6:9-13",
         "analysis": "Matthew 6:9-13 “Pray then like this: ‘Our Father in heaven, hallowed be your name. Your kingdom "
                     "come, your will be done, on earth as it is in heaven. Give us this day our daily bread, and forgive "
                     "us our debts, as we also have forgiven our debtors.  And lead us not into temptation, but deliver "
                     "us from evil.’” This passage in Matthew is often referred to as “The Lord’s Prayer,” when Jesus "
                     "is teaching his disciples how they should pray. It is among the most famous Scriptures, because "
                     "almost every Bible-believing church and denomination around the world recites this passage during"
                     " their services on Sunday. It is also quoted in weddings and funerals, mealtimes and bedtimes, "
                     "convocations and prayer assemblies. For some, this prayer is a liturgical part of their worship "
                     "service, and for others it represents a powerful communion with God that changes them as well as "
                     "their circumstances.",
         "category": "Scripture",
         "slug": "matthew",
         "rating": 0.0,
         "book_author": "Matthew",
         "book_published": "Unknown",
         }
    ]

    # adds our articles to our database
    for article in articles:
        add_article(article["author"], article["date_published"], article["book"], article["views"], article["title"],
                    article["analysis"], article["category"], article["slug"], article["rating"],
                    article["book_author"], article["book_published"])


def add_article(author, date_published, book, views, title, analysis, category,
                slug, rating, book_author, book_published):
    a = Article.objects.get_or_create(author=author, title=title)[0]
    a.author = author
    a.date_published = date_published
    a.book = book
    a.views = views
    a.analysis = analysis
    a.category = category
    a.slug = slug
    a.rating = rating
    a.book_author = book_author
    a.book_published = book_published
    a.save()
    return a


if __name__ == '__main__':
    print("Starting population script...")
    populate()
