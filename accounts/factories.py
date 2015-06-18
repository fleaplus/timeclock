import factory

from . import models


class TimeclockUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TimeclockUser
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda n: 'user%d@example.com' % n)
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_superuser = False
    is_active = True


class EmployeeFactory(TimeclockUserFactory):
    is_superuser = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)
