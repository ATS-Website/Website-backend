# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import inspect

from django_elasticsearch_dsl.registries import registry
from .models import BlogArticle


@receiver(post_save, sender=BlogArticle)
def update_document(sender, **kwargs):
    app_label = sender._meta.app_label
    print(app_label, "1")
    model_name = sender._meta.model_name
    print(model_name, "1")
    instance = kwargs['instance']
    # print(dir(instance), "3")
    # for i in inspect.getmembers(instance):
    #     print(i, "a")

    if app_label == 'Blogs':
        if model_name == 'author':
            instances = instance.newarticle_set.all()
            print(instances, "here")
            for _instance in instances:
                registry.update(_instance)
        elif model_name == 'category':
            instances = instance.blogarticle_set.all()
            print(instances)
            for _instance in instances:
                print(_instance)
                registry.update(_instance)
        elif model_name == 'tag':
            instances = instance.blogarticle_set.all()
            print(instances)
            for _instance in instances:
                print(_instance)
                registry.update(_instance)


@receiver(post_delete)
def delete_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']
    print(instance)

    if app_label == 'Blogs':
        if model_name == 'author':
            instances = instance.newarticle_set.all()
            print(instances, "here")
            for _instance in instances:
                registry.update(_instance)
        elif model_name == 'category':
            instances = instance.blogarticle_set.all()
            print(instances)
            for _instance in instances:
                print(_instance)
                registry.update(_instance)
        elif model_name == 'tag':
            instances = instance.blogarticle_set.all()
            print(instances)
            for _instance in instances:
                print(_instance)
                registry.update(_instance)
