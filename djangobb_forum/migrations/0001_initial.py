# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm.db.fields.fsmfield
import djangobb_forum.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.IntegerField(verbose_name='Size')),
                ('content_type', models.CharField(max_length=255, verbose_name='Content type')),
                ('path', models.CharField(max_length=255, verbose_name='Path')),
                ('name', models.TextField(verbose_name='Name')),
                ('hash', models.CharField(default=b'', max_length=40, verbose_name='Hash', db_index=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ban_start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Ban start')),
                ('ban_end', models.DateTimeField(null=True, verbose_name='Ban end', blank=True)),
                ('reason', models.TextField(verbose_name='Reason')),
                ('user', models.OneToOneField(related_name=b'ban_users', verbose_name='Banned user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ban',
                'verbose_name_plural': 'Bans',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('position', models.IntegerField(default=0, verbose_name='Position', blank=True)),
                ('groups', models.ManyToManyField(help_text='Only users from these groups can see this category', to='auth.Group', null=True, verbose_name='Groups', blank=True)),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('moderator_only', models.BooleanField(default=False, verbose_name='New topics by moderators only')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('position', models.IntegerField(default=0, verbose_name='Position', blank=True)),
                ('description', models.TextField(default=b'', verbose_name='Description', blank=True)),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('post_count', models.IntegerField(default=0, verbose_name='Post count', blank=True)),
                ('topic_count', models.IntegerField(default=0, verbose_name='Topic count', blank=True)),
                ('category', models.ForeignKey(related_name=b'forums', verbose_name='Category', to='djangobb_forum.Category')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Forums',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200)),
                ('choice_count', models.PositiveSmallIntegerField(default=1, help_text='How many choices are allowed simultaneously.')),
                ('active', models.BooleanField(default=True, help_text='Can users vote to this poll or just see the result?')),
                ('deactivate_date', models.DateTimeField(help_text='Point of time after this poll would be automatic deactivated', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PollChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0, editable=False)),
                ('poll', models.ForeignKey(related_name=b'choices', to='djangobb_forum.Poll')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(null=True, verbose_name='Updated', blank=True)),
                ('markup', models.CharField(default=b'bbcode', max_length=15, verbose_name='Markup', choices=[(b'bbcode', b'bbcode')])),
                ('body', models.TextField(verbose_name='Message')),
                ('body_html', models.TextField(verbose_name='HTML version')),
                ('user_ip', models.IPAddressField(null=True, verbose_name='User IP', blank=True)),
            ],
            options={
                'ordering': ['created'],
                'get_latest_by': 'created',
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'permissions': (('fast_post', 'Can add posts without a time limit'), ('med_post', 'Can add posts at medium speed'), ('post_external_links', 'Can post external links'), ('delayed_delete', 'Can delete posts after a delay')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', django_fsm.db.fields.fsmfield.FSMField(default=b'unreviewed', max_length=50, db_index=True)),
                ('user_agent', models.CharField(max_length=200, null=True, blank=True)),
                ('referrer', models.CharField(max_length=200, null=True, blank=True)),
                ('permalink', models.CharField(max_length=200, null=True, blank=True)),
                ('forum', models.ForeignKey(to='djangobb_forum.Forum')),
                ('post', models.OneToOneField(to='djangobb_forum.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topics', djangobb_forum.fields.JSONField(null=True, blank=True)),
                ('last_read', models.DateTimeField(null=True, blank=True)),
                ('user', djangobb_forum.fields.AutoOneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post tracking',
                'verbose_name_plural': 'Post tracking',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=30, verbose_name='Status', blank=True)),
                ('site', models.URLField(verbose_name='Site', blank=True)),
                ('jabber', models.CharField(max_length=80, verbose_name='Jabber', blank=True)),
                ('icq', models.CharField(max_length=12, verbose_name='ICQ', blank=True)),
                ('msn', models.CharField(max_length=80, verbose_name='MSN', blank=True)),
                ('aim', models.CharField(max_length=80, verbose_name='AIM', blank=True)),
                ('yahoo', models.CharField(max_length=80, verbose_name='Yahoo', blank=True)),
                ('location', models.CharField(max_length=30, verbose_name='Location', blank=True)),
                ('signature', models.TextField(default=b'', max_length=2000, verbose_name='Signature', blank=True)),
                ('signature_html', models.TextField(default=b'', max_length=2000, verbose_name='Signature', blank=True)),
                ('time_zone', models.FloatField(default=0.0, verbose_name='Time zone', choices=[(-12.0, b'-12'), (-11.0, b'-11'), (-10.0, b'-10'), (-9.5, b'-09.5'), (-9.0, b'-09'), (-8.5, b'-08.5'), (-8.0, b'-08 PST'), (-7.0, b'-07 MST'), (-6.0, b'-06 CST'), (-5.0, b'-05 EST'), (-4.0, b'-04 AST'), (-3.5, b'-03.5'), (-3.0, b'-03 ADT'), (-2.0, b'-02'), (-1.0, b'-01'), (0.0, b'00 GMT'), (1.0, b'+01 CET'), (2.0, b'+02'), (3.0, b'+03'), (3.5, b'+03.5'), (4.0, b'+04'), (4.5, b'+04.5'), (5.0, b'+05'), (5.5, b'+05.5'), (6.0, b'+06'), (6.5, b'+06.5'), (7.0, b'+07'), (8.0, b'+08'), (9.0, b'+09'), (9.5, b'+09.5'), (10.0, b'+10'), (10.5, b'+10.5'), (11.0, b'+11'), (11.5, b'+11.5'), (12.0, b'+12'), (13.0, b'+13'), (14.0, b'+14')])),
                ('language', models.CharField(default=b'', max_length=5, verbose_name='Language', choices=[(b'en', b'English'), (b'an', b'Aragon\xc3\xa9s'), (b'ast', b'Asturianu'), (b'id', b'Bahasa Indonesia'), (b'ms', b'Bahasa Melayu'), (b'ca', b'Catal\xc3\xa0'), (b'cs', b'\xc4\x8cesky'), (b'cy', b'Cymraeg'), (b'da', b'Dansk'), (b'fa-af', b'Dari'), (b'de', b'Deutsch'), (b'et', b'Eesti'), (b'eo', b'Esperanto'), (b'es', b'Espa\xc3\xb1ol'), (b'eu', b'Euskara'), (b'fr', b'Fran\xc3\xa7ais'), (b'fr-ca', b'Fran\xc3\xa7ais (Canada)'), (b'ga', b'Gaeilge'), (b'gl', b'Galego'), (b'hr', b'Hrvatski'), (b'is', b'\xc3\x8dslenska'), (b'it', b'Italiano'), (b'rw', b'Kinyarwanda'), (b'ku', b'Kurd\xc3\xae'), (b'la', b'Latina'), (b'lv', b'Latvie\xc5\xa1u'), (b'lt', b'Lietuvi\xc5\xb3'), (b'hu', b'Magyar'), (b'mt', b'Malti'), (b'cat', b'Meow'), (b'nl', b'Nederlands'), (b'nb', b'Norsk Bokm\xc3\xa5l'), (b'pl', b'Polski'), (b'pt', b'Portugu\xc3\xaas'), (b'pt-br', b'Portugu\xc3\xaas Brasileiro'), (b'ro', b'Rom\xc3\xa2n\xc4\x83'), (b'sc', b'Sardu'), (b'sk', b'Sloven\xc4\x8dina'), (b'sl', b'Sloven\xc5\xa1\xc4\x8dina'), (b'fi', b'suomi'), (b'sv', b'Svenska'), (b'nai', b'Tepehuan'), (b'vi', b'Ti\xe1\xba\xbfng Vi\xe1\xbb\x87t'), (b'tr', b'T\xc3\xbcrk\xc3\xa7e'), (b'ab', b'\xd0\x90\xd2\xa7\xd1\x81\xd1\x88\xd3\x99\xd0\xb0'), (b'ar', b'\xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd8\xa9'), (b'bg', b'\xd0\x91\xd1\x8a\xd0\xbb\xd0\xb3\xd0\xb0\xd1\x80\xd1\x81\xd0\xba\xd0\xb8'), (b'el', b'\xce\x95\xce\xbb\xce\xbb\xce\xb7\xce\xbd\xce\xb9\xce\xba\xce\xac'), (b'fa', b'\xd9\x81\xd8\xa7\xd8\xb1\xd8\xb3\xdb\x8c'), (b'he', b'\xd7\xa2\xd6\xb4\xd7\x91\xd6\xb0\xd7\xa8\xd6\xb4\xd7\x99\xd7\xaa'), (b'hi', b'\xe0\xa4\xb9\xe0\xa4\xbf\xe0\xa4\xa8\xe0\xa5\x8d\xe0\xa4\xa6\xe0\xa5\x80'), (b'hy', b'\xd5\x80\xd5\xa1\xd5\xb5\xd5\xa5\xd6\x80\xd5\xa5\xd5\xb6'), (b'ja', b'\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'), (b'ja-hr', b'\xe3\x81\xab\xe3\x81\xbb\xe3\x82\x93\xe3\x81\x94'), (b'km', b'\xe1\x9e\x9f\xe1\x9f\x86\xe1\x9e\x9b\xe1\x9f\x80\xe1\x9e\x80\xe1\x9e\x94\xe1\x9f\x86\xe1\x9e\x96\xe1\x9e\xb6\xe1\x9e\x80'), (b'kn', b'\xe0\xb2\xad\xe0\xb2\xbe\xe0\xb2\xb7\xe0\xb3\x86-\xe0\xb2\xb9\xe0\xb3\x86\xe0\xb2\xb8\xe0\xb2\xb0\xe0\xb3\x81'), (b'ko', b'\xed\x95\x9c\xea\xb5\xad\xec\x96\xb4'), (b'mk', b'\xd0\x9c\xd0\xb0\xd0\xba\xd0\xb5\xd0\xb4\xd0\xbe\xd0\xbd\xd1\x81\xd0\xba\xd0\xb8'), (b'ml', b'\xe0\xb4\xae\xe0\xb4\xb2\xe0\xb4\xaf\xe0\xb4\xbe\xe0\xb4\xb3\xe0\xb4\x82'), (b'mn', b'\xd0\x9c\xd0\xbe\xd0\xbd\xd0\xb3\xd0\xbe\xd0\xbb \xd1\x85\xd1\x8d\xd0\xbb'), (b'mr', b'\xe0\xa4\xae\xe0\xa4\xb0\xe0\xa4\xbe\xe0\xa4\xa0\xe0\xa5\x80'), (b'my', b'\xe1\x80\x99\xe1\x80\xbc\xe1\x80\x94\xe1\x80\xba\xe1\x80\x99\xe1\x80\xac\xe1\x80\x98\xe1\x80\xac\xe1\x80\x9e\xe1\x80\xac'), (b'ru', b'\xd0\xa0\xd1\x83\xd1\x81\xd1\x81\xd0\xba\xd0\xb8\xd0\xb9'), (b'sr', b'\xd0\xa1\xd1\x80\xd0\xbf\xd1\x81\xd0\xba\xd0\xb8'), (b'th', b'\xe0\xb9\x84\xe0\xb8\x97\xe0\xb8\xa2'), (b'uk', b'\xd0\xa3\xd0\xba\xd1\x80\xd0\xb0\xd1\x97\xd0\xbd\xd1\x81\xd1\x8c\xd0\xba\xd0\xb0'), (b'zh-cn', b'\xe7\xae\x80\xe4\xbd\x93\xe4\xb8\xad\xe6\x96\x87'), (b'zh-tw', b'\xe6\xad\xa3\xe9\xab\x94\xe4\xb8\xad\xe6\x96\x87')])),
                ('avatar', djangobb_forum.fields.ExtendedImageField(default=b'', upload_to=b'djangobb_forum/avatars', verbose_name='Avatar', blank=True)),
                ('theme', models.CharField(default=b'default', max_length=80, verbose_name='Theme')),
                ('show_avatar', models.BooleanField(default=True, verbose_name='Show avatar')),
                ('show_signatures', models.BooleanField(default=True, verbose_name='Show signatures')),
                ('show_smilies', models.BooleanField(default=True, verbose_name='Show smilies')),
                ('privacy_permission', models.IntegerField(default=1, verbose_name='Privacy permission', choices=[(0, 'Display your e-mail address.'), (1, 'Hide your e-mail address but allow form e-mail.'), (2, 'Hide your e-mail address and disallow form e-mail.')])),
                ('auto_subscribe', models.BooleanField(default=False, help_text='Auto subscribe all topics you have created or reply.', verbose_name='Auto subscribe')),
                ('markup', models.CharField(default=b'bbcode', max_length=15, verbose_name='Default markup', choices=[(b'bbcode', b'bbcode')])),
                ('post_count', models.IntegerField(default=0, verbose_name='Post count', blank=True)),
                ('user', djangobb_forum.fields.AutoOneToOneField(related_name=b'forum_profile', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zapped', models.BooleanField(default=False, verbose_name='Zapped')),
                ('created', models.DateTimeField(verbose_name='Created', blank=True)),
                ('reason', models.TextField(default=b'', max_length=b'1000', verbose_name='Reason', blank=True)),
                ('post', models.ForeignKey(verbose_name='Post', to='djangobb_forum.Post')),
                ('reported_by', models.ForeignKey(related_name=b'reported_by', verbose_name='Reported by', to=settings.AUTH_USER_MODEL)),
                ('zapped_by', models.ForeignKey(related_name=b'zapped_by', verbose_name='Zapped by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reputation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='Time')),
                ('sign', models.IntegerField(default=0, verbose_name='Sign', choices=[(1, b'PLUS'), (-1, b'MINUS')])),
                ('reason', models.TextField(max_length=1000, verbose_name='Reason')),
                ('from_user', models.ForeignKey(related_name=b'reputations_from', verbose_name='From', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(related_name=b'post', verbose_name='Post', to='djangobb_forum.Post')),
                ('to_user', models.ForeignKey(related_name=b'reputations_to', verbose_name='To', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reputation',
                'verbose_name_plural': 'Reputations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Subject')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(null=True, verbose_name='Updated')),
                ('views', models.IntegerField(default=0, verbose_name='Views count', blank=True)),
                ('sticky', models.BooleanField(default=False, verbose_name='Sticky')),
                ('closed', models.BooleanField(default=False, verbose_name='Closed')),
                ('post_count', models.IntegerField(default=0, verbose_name='Post count', blank=True)),
                ('forum', models.ForeignKey(related_name=b'topics', verbose_name='Forum', to='djangobb_forum.Forum')),
                ('last_post', models.ForeignKey(related_name=b'last_topic_post', blank=True, to='djangobb_forum.Post', null=True)),
                ('subscribers', models.ManyToManyField(related_name=b'subscriptions', verbose_name='Subscribers', to=settings.AUTH_USER_MODEL, blank=True)),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated'],
                'get_latest_by': 'updated',
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'permissions': (('delayed_close', 'Can close topics after a delay'),),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='reputation',
            unique_together=set([('from_user', 'post')]),
        ),
        migrations.AddField(
            model_name='poststatus',
            name='topic',
            field=models.ForeignKey(to='djangobb_forum.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(related_name=b'posts', verbose_name='Topic', to='djangobb_forum.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(verbose_name='Updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(related_name=b'posts', verbose_name='User', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poll',
            name='topic',
            field=models.ForeignKey(to='djangobb_forum.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poll',
            name='users',
            field=models.ManyToManyField(help_text='Users who has voted this poll.', to=settings.AUTH_USER_MODEL, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='last_post',
            field=models.ForeignKey(related_name=b'last_forum_post', blank=True, to='djangobb_forum.Post', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='moderators',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, verbose_name='Moderators', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(related_name=b'attachments', verbose_name='Post', to='djangobb_forum.Post'),
            preserve_default=True,
        ),
    ]
