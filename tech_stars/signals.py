# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry


@receiver(post_save)
def update_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'tech_stars':
        if model_name == 'TechStar':
            instances = instance.techstars.all()
            for _instance in instances:
                registry.update(_instance)


@receiver(post_delete)
def delete_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'tech_stars':
        if model_name == 'TechStar':
            instances = instance.techstars.all()
            print(instances)
            for _instance in instances:
                registry.update(_instance)
        # elif model_name == 'BlogArticle':
        #     instances = instance.blogs.all()
        #     print(instances)
        #     for _instance in instances:
        #         registry.update(_instance)


# @receiver(post_save)
# def update_document(sender, **kwargs):
#     app_label = sender._meta.app_label
#     model_name = sender._meta.model_name
#     instance = kwargs['instance']

#     if app_label == 'Blogs':
#         if model_name == 'BlogArticle':
#             instances = instance.blogs.all()
#             print(instances)
#             for _instance in instances:
#                 registry.update(_instance)


# @receiver(post_delete)
# def delete_document(sender, **kwargs):
#     app_label = sender._meta.app_label
#     model_name = sender._meta.model_name
#     instance = kwargs['instance']

#     if app_label == 'Blogs':
