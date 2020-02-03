from django.contrib.auth import get_user_model

from faker import Faker

from app.models import Article

fake = Faker('en_US')


def populate_articles(count):
    user, _ = get_user_model().objects.get_or_create(
        username='seba',
        defaults={
            'email': 'sebastian.wierzchowski@netguru.com',
            'password': '1234asdf'
        }
    )
    for x in range(count):
        Article.objects.create(
            user=user,
            title=fake.sentence(),
            text=fake.paragraph(nb_sentences=10, variable_nb_sentences=True)
        )
        if not x % 50:
            print(f'Progress creating articles: {x} / {count}')
