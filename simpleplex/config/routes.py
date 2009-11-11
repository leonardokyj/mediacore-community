# Use absolute imports, otherwise importing routes tries to import from
# THIS file instead of the *package* routes. This works in python >= 2.5
from __future__ import absolute_import
from routes import Mapper
from tg.configuration import config

def make_map():
    """Setup our custom named routes"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])

    # Concept sunday school action
    map.connect('/concept',
        controller='media', action='concept_preview')
    map.connect('/concept/{slug}/comment',
        controller='media', action='concept_comment')
    map.connect('/concept/{slug}',
        controller='media', action='concept_view')
    map.connect('/lessons',
        controller='media', action='lessons')
    map.connect('/lessons/{slug}',
        controller='media', action='lesson_view')
    map.connect('/lessons/{slug}/comment',
        controller='media', action='lesson_comment')
    map.connect('/latest',
        controller='media', action='latest')
    map.connect('/most_popular',
        controller='media', action='most_popular')

    #################
    # Public Routes #
    #################

    # Media actions
    # These are all mapped without any prefix to indicate the controller
    map.connect('/',
        controller='media',
        action='index')
    map.connect('/{action}',
        controller='media',
        requirements={'action': 'flow|upload|upload_submit|upload_submit_async|upload_success|upload_failure'})

    map.connect('/tags/{slug}',
        controller='media',
        action='tags',
        slug=None)
    map.connect('/topics/{slug}',
        controller='media',
        action='topics',
        slug=None)

    # Individual media and actions their related actions
    map.connect('/view/{slug}/{action}',
        controller='media',
        action='view')
    map.connect('/files/{id}-{slug}.{type}',
        controller='media',
        action='serve',
        requirements={'id': '\d+'})

    # Individual podcast media actions
    map.connect('/podcasts/{podcast_slug}/{slug}/{action}',
        controller='media',
        action='view')

    # Podcast list actions
    map.connect('/podcasts/{slug}',
        controller='podcasts',
        action='view')
    map.connect('/podcasts/feed/{slug}.xml',
        controller='podcasts',
        action='feed')


    ################
    # Admin routes #
    ################

    map.connect('/admin/media_table/{table}/{page}',
        controller='admin',
        action='media_table')

    map.connect('/admin/media',
        controller='mediaadmin',
        action='index')
    map.connect('/admin/media/{id}/{action}',
        controller='mediaadmin',
        action='edit')

    map.connect('/admin/podcasts',
        controller='podcastadmin',
        action='index')
    map.connect('/admin/podcasts/{id}/{action}',
        controller='podcastadmin',
        action='edit')

    map.connect('/admin/comments',
        controller='commentadmin',
        action='index')
    map.connect('/admin/comments/{id}/{status}',
        controller='commentadmin',
        action='save_status',
        requirements={'status': 'approve|trash'})

    map.connect('/admin/settings',
        controller='settingadmin',
        action='index')

    map.connect('/admin/settings/config/{action}',
        controller='settingadmin',
        action='edit')

    map.connect('/admin/settings/users',
        controller='useradmin',
        action='index')
    map.connect('/admin/settings/users/{id}/{action}',
        controller='useradmin',
        action='edit')

    map.connect('/admin/settings/{category}',
        controller='categoryadmin',
        action='index',
        requirements={'category': 'topics|tags'})
    map.connect('/admin/settings/{category}/{id}/{action}',
        controller='categoryadmin',
        requirements={'category': 'topics|tags'})

    # Set up the default route
    map.connect('/{controller}/{action}',
        action='index')

    # Set up a fallback route for object dispatch
    # FIXME: Look into this further...
    # Looks like routes.url_for doesn't work when using this route, so you
    # can't even switch back to routing. Argh.
    map.connect('*url',
        controller='root',
        action='routes_placeholder')

    return map
