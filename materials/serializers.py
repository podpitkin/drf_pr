from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from materials.models import Course, Lesson
from materials.validators import validate_video_link


class LessonSerializer(ModelSerializer):
    link = CharField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ["owner"]


class CourseSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "owner", "name", "preview", "discription", "lessons_count", "lessons"]
        read_only_fields = ["owner"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.subscriptions.filter(user=user).exists()
        return False