from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings

# College choices
COLLEGE_CHOICES = [
    ('PCE', 'PCE'),
    ('PIET', 'PIET'),
    ('PU', 'PU'),
]

DEPARTMENT_CHOICES = [
    ('CORE', 'CORE'),
    ('ECE', 'ECE'),
    ('Cyber Security', 'Cyber Security'),
    ('IT', 'IT'),
    ('Civil', 'Civil'),
    ('Mechanical', 'Mechanical'),
    ('Electrical', 'Electrical'),
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class User(AbstractUser):
    objects = UserManager()

    full_name = models.CharField(max_length=255, default="No Name Provided")
    college_email = models.EmailField(unique=True, default="noemail@poornima.org")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    college = models.CharField(max_length=50, choices=COLLEGE_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField(default='2000-01-01')
    otp_verified = models.BooleanField(default=False)
    has_answered_questionnaire = models.BooleanField(default=False)
    is_profile_locked = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['college_email', 'full_name', 'dob', 'college', 'department', 'gender']

    def __str__(self):
        return self.username

    # Check if mutual heart exists with another user
    def has_mutual_heart(self, other_user):
        return Crush.objects.filter(
            sender=self, receiver=other_user, is_mutual=True
        ).exists()

# 💘 Crush Model
class Crush(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crushes_sent')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crushes_received')
    is_mutual = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        status = "Mutual ❤️" if self.is_mutual else "Sent 💘"
        return f"{self.sender.username} → {self.receiver.username} [{status}]"

    def check_mutual_and_create_friendship(self):
        reverse = Crush.objects.filter(sender=self.receiver, receiver=self.sender).first()
        if reverse:
            self.is_mutual = True
            reverse.is_mutual = True
            self.save()
            reverse.save()

            # Ensure the friendship is created only if it doesn't exist
            if not Friendship.are_friends(self.sender, self.receiver):
                Friendship.objects.get_or_create(user1=self.sender, user2=self.receiver)


# 🤝 Friendship Model
class Friendship(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendships_from')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendships_to')
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)  # Track when friendship is confirmed

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1.username} 🤝 {self.user2.username}"

    @staticmethod
    def are_friends(user1, user2):
        return Friendship.objects.filter(
            models.Q(user1=user1, user2=user2) |
            models.Q(user1=user2, user2=user1)
        ).exists()

    @staticmethod
    def get_or_create_friendship(user1, user2):
        """Returns existing friendship or creates one if it doesn't exist."""
        return Friendship.objects.get_or_create(user1=user1, user2=user2)


# Questionnaire Model
class UserQuestionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='questionnaire')

    # Set 1: Multiple Choice Inputs (stored as comma-separated text)
    hobbies = models.TextField(blank=True)
    college_events = models.TextField(blank=True)
    weekend_plans = models.TextField(blank=True)
    friendship_values = models.TextField(blank=True)
    content_posting = models.TextField(blank=True)
    college_excitements = models.TextField(blank=True)
    learning_preferences = models.TextField(blank=True)
    relaxation_methods = models.TextField(blank=True)

    # Set 2: Single Choice
    introvert_extrovert = models.CharField(max_length=100, choices=[('Introvert', 'Introvert'), ('Extrovert', 'Extrovert'), ('Ambivert', 'Ambivert'), ('Shy', 'Shy')])
    first_meet = models.CharField(max_length=100, choices=[('Canteen chai', 'Canteen chai'), ('Library talk', 'Library talk'), ('Random walk', 'Random walk'), ('Event hangout', 'Event hangout'), ('Virtual hangout (online)', 'Virtual hangout (online)')])
    sleep_type = models.CharField(max_length=100, choices=[('Night owl', 'Night owl'), ('Early bird', 'Early bird'), ('Neither, depends on my mood', 'Neither, depends on my mood')])
    important_trait = models.CharField(max_length=100, choices=[('Looks', 'Looks'), ('Vibe', 'Vibe'), ('Communication', 'Communication'), ('Ambition', 'Ambition'), ('Humor', 'Humor')])
    year = models.CharField(max_length=100, choices=[('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'), ('Final Year', 'Final Year'), ('Postgraduate', 'Postgraduate')])
    comm_style = models.CharField(max_length=100, choices=[('Dry Texter', 'Dry Texter'), ('Emojis & Memes', 'Emojis & Memes'), ('Deep Conversations', 'Deep Conversations'), ('Voice Notes Lover', 'Voice Notes Lover'), ('Frequent Calls', 'Frequent Calls')])
    posting_frequency = models.CharField(max_length=100, choices=[('Rarely', 'Rarely'), ('Occasionally', 'Occasionally'), ('Frequently', 'Frequently'), ('Almost daily', 'Almost daily'), ('Only when I have something important to share', 'Only when I have something important to share')])
    decision_style = models.CharField(max_length=100, choices=[('Logically', 'Logically'), ('Emotionally', 'Emotionally'), ('Mix of both', 'Mix of both'), ('Impulsive', 'Impulsive')])
    free_time = models.CharField(max_length=100, choices=[('Alone, doing my own thing', 'Alone, doing my own thing'), ('Hanging with friends', 'Hanging with friends'), ('Exploring new activities', 'Exploring new activities'), ('Doing something creative (art, writing, etc.)', 'Doing something creative (art, writing, etc.)')])

    # Set 3: Relationship Intent
    relationship_status = models.CharField(max_length=100, choices=[('Single', 'Single'), ('Taken', 'Taken'), ('It’s complicated', 'It’s complicated'), ('Not telling', 'Not telling'), ('In an open relationship', 'In an open relationship')])
    dating_approach = models.CharField(max_length=100, choices=[('I like to take things slow', 'I like to take things slow'), ('I dive in quickly and see where it goes', 'I dive in quickly and see where it goes'), ('I prefer long-term commitment', 'I prefer long-term commitment'), ('I’m just here for fun', 'I’m just here for fun')])
    compatibility = models.CharField(max_length=100, choices=[('Very important', 'Very important'), ('Somewhat important', 'Somewhat important'), ('I’m open to exploring any kind of relationship', 'I’m open to exploring any kind of relationship'), ('Not important at all', 'Not important at all')])
    similar_interests = models.CharField(max_length=100, choices=[('Yes, definitely', 'Yes, definitely'), ('I’m open to different interests', 'I’m open to different interests'), ('I prefer finding someone with unique interests', 'I prefer finding someone with unique interests')])
    relationship_view = models.CharField(max_length=100, choices=[('Serious commitment', 'Serious commitment'), ('Fun and casual', 'Fun and casual'), ('I’m unsure', 'I’m unsure'), ('Just enjoying the journey', 'Just enjoying the journey')])

    def __str__(self):
        return f"Questionnaire - {self.user.username}"
