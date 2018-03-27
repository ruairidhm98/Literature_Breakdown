# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-27 17:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_published', models.CharField(max_length=8)),
                ('book', models.CharField(max_length=128)),
                ('views', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=128, unique=True)),
                ('analysis', models.CharField(max_length=2500)),
                ('category', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('img', models.ImageField(blank=True, upload_to='profile_images')),
                ('rating', models.FloatField(default=0.0, max_length=5.0)),
                ('book_author', models.CharField(default='', max_length=128)),
                ('book_published', models.CharField(default='', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('user_comment', models.CharField(max_length=128)),
                ('rating', models.FloatField(max_length=5.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lit.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_list', models.ManyToManyField(to='lit.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snippet_title', models.CharField(default='', max_length=128)),
                ('page', models.IntegerField()),
                ('passage', models.CharField(max_length=500)),
                ('analysis', models.CharField(max_length=1000)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lit.Article')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.URLField(blank=True, default='')),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('name', models.CharField(blank=True, default='', max_length=128)),
                ('num_articles', models.IntegerField(default=0)),
                ('slug', models.SlugField()),
                ('age', models.IntegerField(default=18)),
                ('gender', models.CharField(blank=True, default='', max_length=4)),
                ('location', models.CharField(blank=True, default='', max_length=128)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='favourites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lit.UserProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lit.UserProfile'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lit.UserProfile'),
        ),
    ]
