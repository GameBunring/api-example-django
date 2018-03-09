from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import bcrypt


class Configure(models.Model):
    user = models.ForeignKey(User)
    id = models.IntegerField(primary_key=True)
    dr_name = models.CharField(max_length=100)

    @classmethod
    def get_name_for_user(cls, user):
        configs = cls.objects.filter(user=user)
        if configs.count() < 1:
            return None
        return configs.first().user

    @classmethod
    def delete_configure(cls, user):
        cls.objects.filter(user=user).delete()


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(Configure, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    salt_ssn = models.CharField(max_length=100)
    photo = models.CharField(max_length=500)
    # appointment_today = models.BooleanField(default=False)

    # @classmethod
    # def archive_patient(cls, user):
    #     cls.objects.update(appointment_today=False, )

    @classmethod
    def match_patients(cls, last_name, first_name, ssn_tail, user):
        res = cls.objects.filter(last_name=last_name, first_name=first_name)
        if ssn_tail:
            return [r for r in res if bcrypt.hashpw(r.salted_ssn, ssn_tail)]
        return [r for r in res]


class Appointment(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(Configure, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient)
    scheduled_time = models.DateTimeField(null=True)
    reason = models.CharField(null=True, max_length=100)
    checked = models.BooleanField(default=False)

    class Meta:
        ordering = ['scheduled_time']


class CheckIns(models.Model):
    STATUS_CHOICES = (
        ("checked_in", "Checked In"),
        ("arrived", "Arrived"),
        ("completed", "Complete")
    )

    appointment_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(Configure, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)
    meet_time = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=0)

    class Meta:
        ordering = ['-meet_time']

    @property
    def waiting_time(self):
        if self.meet_time:
            return (self.meet_time - self.check_in_time).seconds
        else:
            return (timezone.now() - self.check_in_time).seconds

    @classmethod
    def avg_waiting_time(cls, user):
        check_ins = cls.objects.filter(user=user)
        total_num = check_ins.count()
        if not total_num:
            return 0
        return sum([c.waiting_time for c in check_ins]) / total_num

    @classmethod
    def get_in_sessions(cls, user):
        return cls.objects.filter(user=user, status='arrived')

    @classmethod
    def get_waitings(cls, user):
        return cls.objects.filter(user=user, status='checked_in')

