import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'literature_breakdown.settings')

import django
django.setup()
from lit.models import *


def populate():

    # creates new categories

    categories = [
        {"category": "Short Story",
         "slug": "short-story",
         },
        {"category": "Fiction",
         "slug": "fiction",
         },
        {"category": "Scripture",
         "slug": "scripture",
         },
        {"category": "Philosophy",
         "slug": "philosophy",
         },
    ]

   # creates new users

    users = [
        {"username": "lit_break",
         "password": "lit_break",
         "email": "ruairidh1998@icloud.com",
         "name": "Ronald McDonald",
         "slug": "lit_break",
         "age": 32,
         "location": "UK",
         },
        {"username": "conwayjw97",
         "password": "hello",
         "email": "jc@gmail.com",
         "name": "James",
         "slug": "lit_break",
         "age": 16,
         "gender": "Male",
         "location": "Scotland",
         },
        {"username": "guyfieri",
         "password": "TopLad",
         "email": "fieri@outlook.com",
         "name": "Guy Fieri",
         "slug": "guy-fieri",
         "age": 50,
         "gender": "Male",
         "location": "USA",
         },
        {"username": "2250079m",
         "password": "book_reviews",
         "email": "2250079m@student.gla.ac.uk",
         "name": "Book",
         "slug": "2250079",
         "age": 19,
         "gender": "Male",
         "location": "Scotland",
         },
        {"username": "2247492c",
         "password": "hellokitty",
         "email": "224749c@student.gla.ac.uk",
         "name": "James",
         "slug": "2247492",
         "age": 20,
         "gender": "Male",
         "location": "England",
         },
    ]

    # creates sample articles
    articles = [
        {"date_published": "02/01/18",
         "book": "Beyond Good and Evil",
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
         "img": "/profile_images/good_evil.jpg",
         "rating": 4.0,
         "book_author": "Friedrich Nietzsche",
         "book_published": "1886"
         },
        {"date_published": "19/02/18",
         "book": "The Gift of the Magi",
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
         "img": "/profile_images/gift_magi.jpg",
         "rating": 0.0,
         "book_author": "O. Henry",
         "book_published": "1906"
         },
        {"date_published": "03/03/18",
         "book": "Plato's Republic",
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
         "img": "/profile_images/plato.jpg",
         "rating": 0.0,
         "book_author": "Plato",
         "book_published": "380 BC"
         },
        {"date_published": "09/03/18",
         "book": "The Bible",
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
         "img": "/profile_images/Bible_Cover.jpg",
         "rating": 0.0,
         "book_author": "Matthew",
         "book_published": "Unknown",
         },
        {"date_published": "04/01/18",
         "book": "Kidnapped",
         "title": "Places in Kidnapped by Robert Louis Stevenson",
         "analysis": "*Scottish Highlands. Mountainous region of northern Scotland that is the scene of many adventures"
                     " of young David Balfour, who finds the Highlands a wild, frightening, demanding, and alien "
                     "environment. However, with the help of Highlander Alan Breck Stewart, he learns to survive"
                     " there and to understand himself in doing so. There, he learns what it means to be Scottish."
                     " His own upbringing in the Scottish Lowlands has made him ambitious, thrifty, careful, and a "
                     "little selfish. In the Highlands, he encounters heroism, romance, honor, tragedy, and loyalty. "
                     "The Highlands thus represent aspects of Scotland and of David himself which, after David’s "
                     "adventures with Alan Breck Stewart, he cannot ignore or forget.  House of Shaws  House of Shaws. "
                     "Balfour family estate that is David’s birthright but which at the beginning of the novel is in the"
                     " possession of David’s wicked uncle, Ebenezer Balfour. The House of Shaws is a dark, forbidding, "
                     "dangerous, and mysterious place. Its decayed and incomplete state reflects the grim family history"
                     " and blighted lives of the Balfours. Its darkness and dangers mirror the evils of Ebenezer Balfour."
                     " David’s retaking possession of Shaws at the end of the novel signals his achievement of maturity "
                     "and the beginning of a much brighter future for both the Shaws and the Balfour family. Covenant  "
                     "Covenant. Ship captained by Elias Hoseason on which David Balfour is carried away after being"
                     " kidnapped on his uncle’s orders. The ship’s name evokes Scottish religious tradition, but for"
                     " David the Covenant is merely a small and dangerous place in which he learns quickly about the "
                     "concentrated wickedness, violence, treachery, and brutality of men and the ruthlessness of wind "
                     "and sea. In the miniature world of the Covenant he also finds occasional kindness and the heroic"
                     " fighting abilities of the Jacobite adventurer Alan Breck Stewart.",
         "category": "Fiction",
         "slug": "kidnapped",
         "img": "/profile_images/kidnapped.jpg",
         "rating": 0.0,
         "book_author": "Robert Louis Stevenson",
         "book_published": "1886",
         },
        {"date_published": "06/02/18",
         "book": "Lord of the Flies",
         "title": "Analysis of Ralph from Lord of the Flies",
         "analysis": "Ralph is the athletic, charismatic protagonist of Lord of the Flies. Elected the leader of the "
                     "boys at the beginning of the novel, Ralph is the primary representative of order, civilization, "
                     "and productive leadership in the novel. While most of the other boys initially are concerned with"
                     " playing, having fun, and avoiding work, Ralph sets about building huts and thinking of ways to "
                     "maximize their chances of being rescued. For this reason, Ralph’s power and influence over the"
                     " other boys are secure at the beginning of the novel. However, as the group gradually succumbs to"
                     " savage instincts over the course of the novel, Ralph’s position declines precipitously while "
                     "Jack’s rises. Eventually, most of the boys except Piggy leave Ralph’s group for Jack’s, and Ralph"
                     " is left alone to be hunted by Jack’s tribe. Ralph’s commitment to civilization and morality is "
                     "strong, and his main wish is to be rescued and returned to the society of adults. In a sense,"
                     " this strength gives Ralph a moral victory at the end of the novel, when he casts the Lord of the"
                     " Flies to the ground and takes up the stake it is impaled on to defend himself against Jack’s "
                     "hunters. In the earlier parts of the novel, Ralph is unable to understand why the other boys would"
                     " give in to base instincts of bloodlust and barbarism. The sight of the hunters chanting and "
                     "dancing is baffling and distasteful to him. As the novel progresses, however, Ralph, like Simon, "
                     "comes to understand that savagery exists within all the boys. Ralph remains determined not to let"
                     " this savagery -overwhelm him, and only briefly does he consider joining Jack’s tribe in order to"
                     " save himself. When Ralph hunts a boar for the first time, however, he experiences the exhilaration"
                     " and thrill of bloodlust and violence. When he attends Jack’s feast, he is swept away by the frenzy,"
                     " dances on the edge of the group, and participates in the killing of Simon. This firsthand "
                     "knowledge of the evil that exists within him, as within all human beings, is tragic for Ralph, "
                     "and it plunges him into listless despair for a time. But this knowledge also enables him to cast "
                     "down the Lord of the Flies at the end of the novel. Ralph’s story ends semi-tragically: although"
                     " he is rescued and returned to civilization, when he sees the naval officer, he weeps with the "
                     "burden of his new knowledge about the human capacity for evil.",
         "category": "Fiction",
         "slug": "lord-of-the-flies",
         "img": "/profile_images/lotf.jpg",
         "rating": 2.0,
         "book_author": "William Golding",
         "book_published": "1954",
         },
        {"date_published": "01/02/18",
         "book": "It",
         "title": "Stephen King's 'It'",
         "analysis": "It, by Stephen King, was a book that impacted heavily upon my teenage years. It was at that time "
                     "both the biggest - and the scariest - book I’d ever read and it is a book I remember most fondly. "
                     "It is always a risk to revisit beloved books decades later - you’ve (hopefully) matured, which has"
                     " both negatives and positives when it comes to re-reading, and like as not the revisited book is "
                     "unable to pack the same punch it once did. And this was true of It, and also King’s other doorstopper,"
                     " The Stand. They were both good reads but this time around I found issues and weaknesses that I"
                     " gleefully missed and ignored when I was a teenager. Oh, how I miss being young...  It’s a book "
                     "about childhood, in particular the special elements like friendships that seem they will last "
                     "forever, days and lives that will last forever. I cannot think of many authors who can capture "
                     "what it was like to be a kid better than King. He remembers things vividly and through his words"
                     " allows us to remember the excitement, the awkwardness, the ability to laugh genuinely and hard "
                     "at the dumbest of things. But it is not all fun, there are the bullies, there is the feeling of "
                     "inadequacy and isolation. This is not just a horror story, indeed it is less about horror and more"
                     " about coming of age.  As always with any book, you should focus on the positives first and foremost."
                     " As already mentioned, this is not  simply a horror book, the scary moments are few and far between"
                     " and all the more powerful for it. This is a book that allows us to relive the most potent time "
                     "of our lives - our childhood. King’s narrative details the young and adult lives of Bill, Richie, "
                     "Stan, Bev, Eddie and Mike (The Loser’s Club) and at the same time bring to life the cursed town of"
                     " Derry. And to be honest the book’s colossal length of just shy of 1,200 pages does not feel that"
                     " long, especially when you are within the chapters that capture your imagination and fears most. "
                     "There is much of worth and value within the pages and nostalgia plays a large part in the reading"
                     " enjoyment. You’ll like these kids, they will remind you of yourself and your childhood friends, "
                     "and the fact that adult life rarely pans out the way you’d thought and hoped it might will resonate"
                     " with the large majority of adult readers.  However, if you speak to readers who did not enjoy It "
                     "their reservations often focus on the same two areas. Many say it’s too long and too detailed, "
                     "often pointlessly so. But the main recurring objection to the book is",
         "category": "Fiction",
         "slug": "stephen-kings-it",
         "img": "/profile_images/it.jpg",
         "rating": 0.0,
         "book_author": "Stephen King",
         "book_published": "1986",
         },
        {"date_published": "04/01/18",
         "book": "The Great Gatsby",
         "title": "The Great Gatsby Review",
         "analysis": "In The Great Gatsby Fitzgerald offers up commentary on a variety of themes — justice, power, greed,"
                     " betrayal, the American dream, and so on. Of all the themes, perhaps none is more well developed "
                     "than that of social stratification. The Great Gatsby is regarded as a brilliant piece of social "
                     "commentary, offering a vivid peek into American life in the 1920s. Fitzgerald carefully sets up "
                     "his novel into distinct groups but, in the end, each group has its own problems to contend with, "
                     "leaving a powerful reminder of what a precarious place the world really is. By creating distinct "
                     "social classes — old money, new money, and no money — Fitzgerald sends strong messages about the "
                     "elitism running throughout every strata of society.  The first and most obvious group Fitzgerald "
                     "attacks is, of course, the rich. However, for Fitzgerald (and certainly his characters), placing "
                     "the rich all in one group together would be a great mistake. For many of those of modest means, "
                     "the rich seem to be unified by their money. However, Fitzgerald reveals this is not the case. In "
                     "The Great Gatsby, Fitzgerald presents two distinct types of wealthy people. First, there are "
                     "people like the Buchanans and Jordan Baker who were born into wealth. Their families have had"
                     " money for many generations, hence they are 'old money.' As portrayed in the novel, the 'old money' "
                     "people don't have to work (they rarely, if ever, even speak about business arrangements) and "
                     "they spend their time amusing themselves with whatever takes their fancy. Daisy, Tom, Jordan, and"
                     " the distinct social class they represent are perhaps the story's most elitist group, imposing "
                     "distinctions on the other people of wealth (like Gatsby) based not so much on how much money one"
                     " has, but where that money came from and when it was acquired. For the 'old money' people, the fact"
                     " that Gatsby (and countless other people like him in the 1920s) has only just recently acquired"
                     " his money is reason enough to dislike him. In their way of thinking, he can't possibly have the"
                     " same refinement, sensibility, and taste they have. Not only does he work for a living, but he "
                     "comes from a low-class background which, in their opinion, means he cannot possibly be like them. "
                     " In many ways, the social elite are right. The 'new money' people cannot be like them, and in many"
                     " ways that works in their favor — those in society's highest echelon are not nice people at all. "
                     "They are judgmental and superficial, failing to look at the essence of the people around",
         "category": "Fiction",
         "slug": "the-great-gatsby-review",
         "img": "/profile_images/the_great_gatsby.jpg",
         "rating": 4.0,
         "book_author": "F. Scott Fitzgerald",
         "book_published": "1925",
         },
        {"date_published": "01/02/18",
         "book": "Moby Dick",
         "title": "Major Symbols of Moby Dick",
         "analysis": "Introduction Symbols in literature are usually objects used to represent or suggest important "
                     "concepts that inform and expand our appreciation of the work. Moby-Dick offers some of the most "
                     "widely known symbols in American literature. Being widely known, however, does not imply that the "
                     "symbols are simple or easy to understand. Like the themes in the novel, the symbols are ambiguous "
                     "in enriching ways. Father Mapple's Pulpit Father Mapple's pulpit in the Whaleman's Chapel"
                     " effectively represents this former harpooner's approach to his ministry. Everything about the "
                     "chapel reminds a visitor of life and death at sea. Father Mapple is the captain of the ship, the "
                     "congregation his crew. The pulpit itself is shaped like the prow of a ship and features a painting"
                     " of a vessel battling a storm near a rocky coast, an angel of hope watching over it. Without much"
                     " effort, we can see that the pulpit represents the leadership of the pastor and implies that God "
                     "himself is the pilot of this ship. Mapple's 'shipmates,' as he refers to the congregation, often"
                     " find themselves battling storms on rocky coasts — either literally, in ships, or figuratively in"
                     " the rest of their lives. They need the hope and consolation of God's grace, as represented by the "
                     "angel. Mapple ascends to the pulpit by climbing a rope ladder like one used to mount a ship from a"
                     " boat at sea. He then pulls the rope up after him, effectively cutting off contact with worldly"
                     " matters. In similar ways, the captain of a whaling ship assumes the pilot's role as he cuts off "
                     "contact with land; the ship becomes a floating microcosm at sea. Melville makes effective use of"
                     " contrast throughout the novel; here, it is between Mapple and Ahab. Mapple is an elderly but "
                     "vigorous man of God who sees his role as leading his ship through rocky waters by gladly submitting"
                     " to the will of a higher authority. Ahab is an ungodly man who doesn't mind wielding authority "
                     "but resents submitting to it. He wears his defiance proudly. In this sense, the pulpit represents"
                     " the proper position for a ship's captain, performing his duty in leading his congregation toward "
                     "an understanding of performing God's will. Queequeg's Coffin The symbolism of Queequeg's coffin "
                     "changes as the novel progresses. Initially, the coffin represents Queequeg's apparently impending "
                     "death and his nostalgic link to his home island. The coffin is shaped like a canoe because of the"
                     " custom on Kokovoko of setting the corpse adrift in such a craft. The belief was that eve",
         "category": "Fiction",
         "slug": "Major Symbols of Moby Dick",
         "img": "/profile_images/moby_dick.jpg",
         "rating": 5.0,
         "book_author": "Herman Melville",
         "book_published": "1851",
         },

    ]

    users_lst = []

    # adds categories to database
    for category in categories:
        add_category(category["category"], category["slug"])

    # adds users to database and stores each within a variable to help with setting up authors to each articles
    for user in users:
        # adds new user profile
        new_user = add_userprofile(add_user(user["username"], user["password"], user["email"]), user["name"],
                                   user["slug"], user["age"], user["location"])
        # stores each user object in a list to help with next part
        users_lst.append(new_user)

    articles_lst = []

    # adds lit_breaks articles
    for article in articles[:2]:
        art = add_article(users_lst[0], article["date_published"], article["book"], article["title"],
                          article["analysis"], article["category"], article["slug"], article["img"],
                          article["rating"], article["book_author"], article["book_published"])
        articles_lst.append(art)

    # adds guy fieris articles
    for article in articles[2: 4]:
        art = add_article(users_lst[2], article["date_published"], article["book"], article["title"],
                          article["analysis"], article["category"], article["slug"], article["img"],
                          article["rating"], article["book_author"], article["book_published"])
        articles_lst.append(art)

    # adds 2250079m articles
    for article in articles[4: 6]:
        art = add_article(users_lst[3], article["date_published"], article["book"], article["title"],
                          article["analysis"], article["category"], article["slug"], article["img"],
                          article["rating"], article["book_author"], article["book_published"])
        articles_lst.append(art)

    # adds 2247492c articles
    for article in articles[6: 9]:
        art = add_article(users_lst[4], article["date_published"], article["book"], article["title"],
                          article["analysis"], article["category"], article["slug"], article["img"],
                          article["rating"], article["book_author"], article["book_published"])
        articles_lst.append(art)

    # adds user comments for the great gatsby
    comments_gatsby = [
        {"user_comment": "Great!",
         "rating": 5.0,
         "user": users_lst[1],
         },
        {"user_comment": "OK!",
         "rating": 3.5,
         "user": users_lst[3],
         },
    ]

    for comment in comments_gatsby:
        add_comment(comment["user_comment"], comment["user"], comment["rating"], articles_lst[7])

    # adds user comments for moby dick
    comments_moby = [
        {"user_comment": "Top notch",
         "rating": 5.0,
         "user": users_lst[2],
         },
        {"user_comment": "Best analysis written!!",
         "rating": 5.0,
         "user": users_lst[4],
         },
    ]

    for comment in comments_moby:
        add_comment(comment["user_comment"], comment["user"], comment["rating"], articles_lst[8])

    # adds user comments for good and evil
    comments_good = [
        {"user_comment": "Great!",
         "rating": 4.0,
         "user": users_lst[4],
         },
        {"user_comment": "Really good!",
         "rating": 4.5,
         "user": users_lst[0],
         },
        {"user_comment": "Not the best but not bad!",
         "rating": 3.5,
         "user": users_lst[1],
         },
    ]

    for comment in comments_good:
        add_comment(comment["user_comment"], comment["user"], comment["rating"], articles_lst[0])

    # adds comments for lord of the flies
    comments_flies = [
        {"user_comment": "Not very good at all",
         "rating": 2.0,
         "user": users_lst[3],
         },
        {"user_comment": "Poor!",
         "rating": 2.0,
         "user": users_lst[2],
         },
    ]

    for comment in comments_flies:
        add_comment(comment["user_comment"], comment["user"], comment["rating"], articles_lst[5])

    # creates snippets to add to articles
    snippets = [
        {"snippet_title": "Overview of a Page in Chapter 7",
         "page": 140,
         "passage": "In front of them, only three or four yards away, was a rock-like hump where no rock should be. "
                    "Ralph could hear a tiny chattering noise coming from somewhere—perhaps his own mouth. He bound "
                    "himself together with his will, fused his fear and loathing into a hatred, and stood up. He took"
                    " two leaden steps forward.",
         "analysis": "On the one hand, this is real courage: when you're afraid of something but do it anyway. On the "
                     "other hand, notice how Ralph changing his 'fear' and 'loathing' into 'hatred.' Talk about dangerous"
                     " emotions—hatred makes people do horrible things.",
         },
        {"snippet_title": "Brief Look at the Uncle",
         "page": 40,
         "passage": "There was now no doubt about my uncle's enmity; there was no doubt I carried my life in my hand, "
                    "and he would leave no stone unturned that he might compass my destruction. But I was young and"
                    " spirited, and like most lads that have been country-bred, I had a great opinion of my shrewdness."
                    " I had come to his door no better than a beggar and little more than a child; he had met me with "
                    "treachery and violence; it would be a fine consummation to take the upper hand, and drive him like"
                    " a herd of sheep.",
         "analysis": "This quote, from Chapter 5, highlights both David's growing perceptiveness and his naïveté. He "
                     "has swiftly recognized his uncle Ebenezer's dislike or even hatred of him, and also his uncle's"
                     " intentions toward him. But rather than using his common sense and simply leaving the House of "
                     "Shaws, David decides to try and 'take the upper hand' and get back at his uncle, even come to "
                     "control him. David's pride leads to his downfall; he underestimates his uncle's cleverness and is"
                     " kidnapped at Queensferry.",
         },
        {"snippet_title": "Chapter 10 of Moby Dick (A passage)",
         "page": 200,
         "passage": "If there yet lurked any ice of indifference towards me in the Pagan’s breast, this pleasant, "
                    "genial smoke we had, soon thawed it out, and left us cronies. He seemed to take to me quite as"
                    " naturally and unbiddenly as I to him; and when our smoke was over, he pressed his forehead "
                    "against mine, clasped me round the waist, and said that henceforth we were married; meaning, in"
                    " his country’s phrase, that we were bosom friends; he would gladly die for me, if need should be.",
         "analysis": "This is a cute little 'lost' in 'translation' moment. If someone clasps you to them and "
                     "declares that you’re married, you usually don’t interpret that as meaning 'best pals.' So we’re "
                     "forced to wonder whether Ishmael is correct, or telling the truth, when he says that 'bosom friends'"
                     " are all they are. It’s possible, of course, that that’s the real version of the story. It’s "
                     "possible that Ishmael thinks that and Queequeg intends something else. And it’s possible that, "
                     "well, they really are married—at least according to Queequeg’s customs."
         },
        {"snippet_title": "Chpater 9 Page 1",
         "page": 156,
         "passage": "'Nevertheless you did throw me over,' said Jordan suddenly. 'You threw me over on the telephone."
                    " I don't give a damn about you now, but it was a new experience for me, and I felt a little dizzy "
                    "for a while.",
         "analysis": "You know how text messaging and online dating have supposedly changed dating? Well, new "
                     "technologies like cars and telephones were doing the same thing at the beginning of the twentieth"
                     " century. Can you imagine if Daisy had had Snapchat?",
         },
    ]

    # adds snippets to the database
    add_snippet(articles_lst[5], snippets[0]["snippet_title"], snippets[0]["page"], snippets[0]["passage"],
                snippets[0]["analysis"])
    add_snippet(articles_lst[4], snippets[1]["snippet_title"], snippets[1]["page"], snippets[1]["passage"],
                snippets[1]["analysis"])
    add_snippet(articles_lst[8], snippets[2]["snippet_title"], snippets[2]["page"], snippets[2]["passage"],
                snippets[2]["analysis"])
    add_snippet(articles_lst[7], snippets[3]["snippet_title"], snippets[3]["page"], snippets[3]["passage"],
                snippets[3]["analysis"])


def add_category(name, slug):
    c = Category.objects.get_or_create(name=name)[0]
    c.slug = slug
    c.save()
    return c


def add_user(username, password, email):
    u = User.objects.get_or_create(username=username)[0]
    u.password = password
    u.email = email
    u.save()
    return u


def add_userprofile(user, name, slug, age, location):
    up = UserProfile.objects.get_or_create(user=user)[0]
    up.name = name
    up.slug = slug
    up.age = age
    up.location = location
    up.save()
    return up


def add_article(author, date_published, book, title, analysis, category, slug, img, rating, book_author, book_published):
    a = Article.objects.get_or_create(author=author, title=title)[0]
    a.author = author
    a.date_published = date_published
    a.book = book
    a.analysis = analysis
    a.category = category
    a.slug = slug
    a.img = img
    a.rating = rating
    a.book_author = book_author
    a.book_published = book_published
    a.save()
    return a


def add_snippet(title, snippet_title, page, passage, analysis):
    s = Snippet.objects.create(snippet_title=snippet_title, title=title, page=page)
    s.passage = passage
    s.analysis = analysis
    s.save()
    return s


def add_comment(user_comment, user, rating, article):
    c = Comment.objects.create(user=user, rating=rating, article=article)
    c.user_comment = user_comment
    c.save()
    return c


if __name__ == '__main__':
    print("Starting population script...")
    populate()
    print("Success! Population script complete")
