from django.db import models


class Riddle(models.Model):
    number = models.IntegerField(null=False, unique=True)
    question = models.TextField(null=False)
    answer = models.CharField(null=False, max_length=255)
    level = models.ForeignKey("Level", on_delete=models.CASCADE)
    is_trap = models.BooleanField(default=False)
    code = models.TextField(null=True)
    image = models.TextField(null=True)
    hint = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    from django.db import models


class Riddle(models.Model):
    riddle_id = models.CharField(null=False, unique=True, max_length=10)
    question = models.TextField(null=False)
    answer = models.CharField(null=False, max_length=255)
    level = models.ForeignKey("Level", on_delete=models.CASCADE)
    is_trap = models.BooleanField(default=False)
    code = models.TextField(null=True)
    image = models.TextField(null=True)
    hint = models.TextField(null=True)
    link = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate the unique number
        # Extract the current level number
        level_num = self.level.number  # Assuming your Level model has an 'id' field
        # Grab number from request body
        number = int(self.riddle_id)
        # Generate the new riddle number
        self.riddle_id = f"L{level_num:02d}R{number:02d}"  # Format: L01R01
        super(Riddle, self).save(*args, **kwargs)

    def __str__(self):
        return f"Riddle {self.number}: {self.question}"
