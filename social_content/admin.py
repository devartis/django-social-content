from django.contrib import admin
from social_content.models import YoutubeContent, TwitterContent, FacebookContent


class YoutubeContentAdmin(admin.ModelAdmin):

    list_display = ('title', 'original_url', 'position', 'published', )
    list_editable = ('position', 'published', )
    search_fields = ('title', 'text', 'original_url', )


class TwitterContentAdmin(admin.ModelAdmin):

    list_display = ('original_url', 'position', 'published', )
    list_editable = ('position', 'published', )
    search_fields = ('text', 'original_url', )


class FacebookContentAdmin(admin.ModelAdmin):

    list_display = ('original_url', 'position', 'published', )
    list_editable = ('position', 'published', )
    search_fields = ('text', 'original_url', )

admin.site.register(TwitterContent, TwitterContentAdmin)
admin.site.register(YoutubeContent, YoutubeContentAdmin)
admin.site.register(FacebookContent, FacebookContentAdmin)
